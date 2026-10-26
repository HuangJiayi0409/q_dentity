"""One state machine for snapshot -> analysis -> attempts -> kernel acceptance."""
from dataclasses import asdict,dataclass
from pathlib import Path
import json
import os
import signal
import subprocess
import sys
import time
from .contracts import HERE,FAMILIES,BACKENDS,accept_proof,check_source,save,snapshot

@dataclass(frozen=True)
class Budget:
    seconds:float=900
    attempt_seconds:float=600
    analysis_seconds:float=120
    preprocessing_seconds:float=600
    selection_seconds:float=10
    symbolic_seconds:float=240
    max_order:int=4
    max_unknowns:int=10000
    max_degree:int=5
    laurent_floor:int=-1

    def validate(self):
        for name in ('seconds','attempt_seconds','analysis_seconds','symbolic_seconds','preprocessing_seconds','selection_seconds'):
            value=getattr(self,name)
            if not 0<value<=7200:raise ValueError('invalid budget: '+name)
        if not 1<=self.max_order<=16 or not 1<=self.max_unknowns<=100000:
            raise ValueError('invalid order/unknown limit')
        if not 0<=self.max_degree<=12 or not -8<=self.laurent_floor<=0:
            raise ValueError('invalid Laurent degree limit')


def call_worker(request,directory,timeout):
    """Bound all descendants, including Lean and nested symbolic workers."""
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    request_file=directory/'request.json';result_file=directory/'result.json'
    save(request_file,request)
    with (directory/'worker.log').open('w') as log:
        process=subprocess.Popen([sys.executable,str(HERE/'workflow/worker.py'),str(request_file),str(result_file)],
                                 stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        try:process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL);process.wait()
            return {'status':'timeout','error':'attempt wall-clock budget exhausted',
                    'remaining_obligations':['Complete this stage within resource budget']}
        except BaseException:
            os.killpg(process.pid,signal.SIGKILL);process.wait();raise
    if process.returncode or not result_file.exists():
        return {'status':'worker_failed','error':'isolated adapter exited without a valid result',
                'remaining_obligations':['Inspect worker.log']}
    try:return json.loads(result_file.read_text())
    except (ValueError,OSError):return {'status':'worker_failed','error':'invalid worker result'}


def failure_stage(result):
    if result.get('failure_stage'):return result['failure_stage']
    if result.get('verification'):return 'verification'
    if result.get('construction') or result.get('status') in ('timeout','search_exhausted','resource_exhausted','construction_failed'):
        return 'construction'
    return 'representation'


class PreprocessingFailure(ValueError):
    pass


class SelectionFailure(ValueError):
    pass


def prove(identity,output_root=None,method=None,budget=None,*,runner=call_worker,preprocess=False,preprocessing_view="structured",select_only=False,
          unknown_policy='mark',unknown_workers=4,preprocessing_descriptor=None):
    if preprocessing_view not in ("structured", "expanded"): raise ValueError("unknown_preprocessing_view")
    budget=budget or Budget();budget.validate()
    if method not in (*FAMILIES,'auto'):raise ValueError('inactive method')
    automatic=method=='auto'
    if unknown_policy not in ('mark','all'):raise ValueError('unknown unclassified-input policy')
    if unknown_policy=='all' and not automatic:raise ValueError('all-method unknown policy requires auto')
    if not 1<=unknown_workers<=4:raise ValueError('unknown workers must be 1..4')
    if preprocessing_descriptor is not None and not preprocess:raise ValueError('shared descriptor requires preprocessing')
    if select_only and not automatic:raise ValueError('select_only requires automatic selection')
    if automatic:preprocess=True
    # Never reuse outputs from an earlier attempt (including timed-out workers).
    import uuid
    work=(Path(output_root) if output_root else HERE/'generated'/method)/uuid.uuid4().hex
    work=work.resolve();work.mkdir(parents=True)
    start=time.monotonic();deadline=start+budget.seconds
    report={'schema_version':1,'status':'started','identity':identity,'method_request':method,
            'budget':asdict(budget),'work_directory':str(work),'source':None,
            'analysis':[],'plan':[],'attempts':[],'events':[],
            'automatic_train_proofs':0,'test_files_read':0,'remaining_obligations':[],
            'new_unique_train_proofs':'not_counted_by_individual_run',
            'unknown_policy':unknown_policy}
    def event(stage,status,**details):
        report['events'].append({'stage':stage,'status':status,'elapsed_seconds':round(time.monotonic()-start,3),**details})
        save(work/'report.json',report)
    def finish():
        report['elapsed_seconds']=round(time.monotonic()-start,3)
        event('finished',report['status'])
        return report
    try:
        report['source']=source=snapshot(identity,work,method,preprocess=preprocess);event('snapshot','passed')
        if preprocess:
            directory=work/'preprocessing'
            remaining=deadline-time.monotonic()
            limit=min(remaining,budget.preprocessing_seconds)
            if limit<=0:raise PreprocessingFailure('preprocessing budget exhausted')
            phase_start=time.monotonic()
            if preprocessing_descriptor is None:
                result=runner({'action':'preprocess','method':method,'source':source,
                    'work':str(directory),'timeout':max(.01,limit-1),'normalization_view':preprocessing_view},directory,limit)
            else:
                source['preprocessing']=preprocessing_descriptor
                check_source(source)
                result=dict(status=preprocessing_descriptor['status'],descriptor=preprocessing_descriptor,
                            reused_from_parent=True)
            save(directory/'result.json',result)
            report['preprocessing']={'status':result['status'],'result':str(directory/'result.json'),'normalization_view':preprocessing_view}
            report['preprocessing']['cache_hit']=result.get('cache_hit',False)
            report['preprocessing']['reused_from_parent']=result.get('reused_from_parent',False)
            report['preprocessing']['wall_seconds']=time.monotonic()-phase_start
            if result['status'] not in ('verified_normalized','verified_unchanged'):
                raise PreprocessingFailure(result.get('error','shared preprocessing failed'))
            source['preprocessing']=result['descriptor']
            check_source(source);event('preprocessing',result['status'])
        if automatic:
            remaining=deadline-time.monotonic()
            if remaining<=0:
                report.update(status='resource_exhausted',remaining_obligations=['Budget exhausted before selection'])
                return finish()
            directory=work/'selection';limit=min(remaining,budget.selection_seconds)
            phase_start=time.monotonic()
            result=runner({'action':'select','method':'auto','source':source,
                'work':str(directory),'timeout':max(.001,limit-.1)},directory,limit)
            save(directory/'result.json',result)
            report['selection']={'status':result.get('status'),'result':str(directory/'result.json')}
            report['selection']['wall_seconds']=time.monotonic()-phase_start
            check_source(source)
            if time.monotonic()>=deadline:
                report.update(status='resource_exhausted',remaining_obligations=['Budget exhausted during selection'])
                return finish()
            if result.get('status') not in ('selected','unsupported_input','unclassified'):
                raise SelectionFailure(result.get('error','method selection failed'))
            from .contracts import sha
            standard=Path(source['preprocessing']['directory'])/'standard.json'
            if result.get('source_sha256')!=source['sha256'] or result.get('standard_sha256')!=sha(standard):
                raise SelectionFailure('selection/input binding mismatch')
            if result['status']=='unsupported_input':
                report.update(status='unsupported_input',remaining_obligations=['Current selector found no supported route; not mathematical unprovability'])
                event('selection','unsupported_input');return finish()
            if result['status']=='unclassified':
                from selection.policy import all_unknown_tie
                ranking=result.get('ranking',[])
                if (len(ranking)!=len(FAMILIES) or {r.get('method') for r in ranking}!=set(FAMILIES)
                    or not all_unknown_tie(ranking) or result.get('selected_method') is not None
                    or result.get('unclassified_reason')!='all_methods_unknown_tied'):
                    raise SelectionFailure('invalid all-unknown classification')
                report.update(status='unclassified',classification_status='unclassified',
                              unclassified_reason=result['unclassified_reason'],selected_method=None,selected_route=None)
                report['selection'].update(reason=result['reason'],unclassified_reason=result['unclassified_reason'])
                event('selection','unclassified')
                if select_only or unknown_policy=='mark':
                    report['remaining_obligations']=['All methods tied with unknown applicability; no proof method was run']
                    return finish()
                from .unknown import explore
                report['exploration']=dict(status='running',trigger='all_methods_unknown_tied',
                    methods=list(FAMILIES),workers=unknown_workers,results=[],
                    budget_scope='separate per-method deadline after shared preprocessing and selection',
                    seconds_per_method=budget.seconds,max_allocated_method_seconds=len(FAMILIES)*budget.seconds,
                    stop_on_first_success=False)
                event('exploration','started')
                def completed(row):
                    report['exploration']['results'].append(row)
                    event('exploration_method',row['status'],method=row['method'])
                rows=explore(identity,source,work/'exploration',budget,runner=runner,
                             workers=unknown_workers,on_result=completed,preprocessing_view=preprocessing_view)
                report['exploration'].update(status='completed',results=rows)
                successes=[r for r in rows if r['status']=='proved']
                report.update(status='proved' if successes else 'unproved',
                              automatic_train_proofs=int(bool(successes)),
                              successful_methods=[r['method'] for r in successes],
                              remaining_obligations=[] if successes else ['All twelve methods finished without an accepted original-theorem proof; see individual reports'])
                if successes:report['proof']=successes[0]['proof']
                return finish()
            method=result.get('selected_method')
            if method not in FAMILIES:raise SelectionFailure('unregistered selected method')
            report.update(selected_method=method,selected_route=result.get('selected_route'))
            report['selection'].update(selected_method=method,selected_route=result.get('selected_route'),
                                       reason=result.get('reason'),unknown_criteria=result.get('unknown_criteria',[]))
            event('selection','selected',method=method,route=result.get('selected_route'))
            if select_only:
                report.update(status='selected',remaining_obligations=['Selection only; original theorem has not been proved'])
                return finish()
        kinds=[method if method in ('product','interpolation','noncommutative','combinatorial','difference_ring','kernel_transform','spectral','determinant','macmahon') else 'p2' if method=='coefficient' else 'p1']
        for kind in kinds:
            remaining=deadline-time.monotonic()
            if remaining<=0:break
            directory=work/'analysis'/kind
            result=runner({'action':'analyze','kind':kind,'method':method,'source':source,'work':str(directory)},directory,min(remaining,budget.analysis_seconds))
            save(directory/'result.json',result)
            report['analysis'].append({'kind':kind,'status':result['status'],'result':str(directory/'result.json')})
            check_source(source);event('analysis',result['status'],adapter=kind)
            if result['status']!='analyzed':
                exhausted=result['status'] in ('timeout','resource_exhausted') or time.monotonic()>=deadline
                report.update(status='resource_exhausted' if exhausted else 'analysis_failed',
                    failure_stage='analysis',analysis_failure_status=result['status'],
                    error=result.get('error'),remaining_obligations=result.get('remaining_obligations') or
                    ['Analysis did not complete; applicability is unknown'])
                return finish()
            for candidate in result.get('candidates',[]):
                name=candidate['backend']
                if name not in BACKENDS:raise ValueError('integrity_error: unregistered backend in analysis')
                if (candidate['applicable'] and BACKENDS[name]==method and
                        candidate.get('admission',{}).get('proof_exit')!='unavailable'):
                    report['plan'].append({'backend':name,'method':BACKENDS[name],
                        'environment':str(directory/'environment.json'),'reason':candidate['reason'],
                        'admission':candidate.get('admission')})
            report.setdefault('admission',[]).extend(result.get('candidates',[]))
        event('planning','completed',candidate_count=len(report['plan']))
        for index,candidate in enumerate(report['plan']):
            remaining=deadline-time.monotonic()
            if remaining<=0:break
            check_source(source)
            directory=work/'attempts'/f'{index:02d}_{candidate["backend"]}'
            limit=min(remaining,budget.attempt_seconds)
            if method in ('interpolation','noncommutative','combinatorial','difference_ring','kernel_transform','spectral','determinant','macmahon'):
                # Enforce the whole CAS/reconstruction budget, including SymPy
                # calls which cannot be interrupted from inside the adapter.
                limit=min(limit,budget.symbolic_seconds)
            options=asdict(budget);options['symbolic_seconds']=min(budget.symbolic_seconds,max(0.01,limit-5))
            event('attempt','started',backend=candidate['backend'])
            result=runner({'action':'prove','backend':candidate['backend'],'method':method,'source':source,
                'work':str(directory),'environment':candidate['environment'],'budget':options},directory,limit)
            save(directory/'result.json',result)
            attempt={'backend':candidate['backend'],'method':candidate['method'],'status':result['status'],
                     'result':str(directory/'result.json'),'failure_stage':None if result['status']=='proved' else failure_stage(result),
                     'error':result.get('error'),'remaining_obligations':result.get('remaining_obligations',[])}
            report['attempts'].append(attempt);check_source(source)
            if result['status']=='proved':
                try:artifact=accept_proof(result,source,directory)
                except (ValueError,OSError) as exc:
                    attempt['status']='rejected_success_claim'
                    raise ValueError('integrity_error: '+str(exc)) from exc
                if time.monotonic()>=deadline:
                    attempt['status']='verified_after_deadline'
                    report['status']='resource_exhausted'
                    break
                report.update(status='proved',selected_method=candidate['method'],selected_backend=candidate['backend'],
                              proof=artifact,automatic_train_proofs=1,remaining_obligations=[])
                event('kernel_acceptance','passed');break
            event('attempt',result['status'],backend=candidate['backend'])
        else:report['status']='unproved'
        if report['status'] not in ('proved','integrity_error'):
            report['status']='resource_exhausted' if time.monotonic()>=deadline else 'unproved'
            report['remaining_obligations']=(['No executable candidate was established; see admission checks and unresolved obligations'] if not report['plan'] else
                ['No attempted backend closed the original statement; see per-attempt obligations'])
            if not report['plan']:
                admissions=[c.get('admission',{}) for c in report.get('admission',[])]
                report['applicability_status']=('outside_current_implementation' if admissions and
                    all(a.get('core_domain')=='rejected' for a in admissions) else 'unknown')
            if len(report['attempts'])<len(report['plan']):report['remaining_obligations'].append('Unattempted backends remain after global budget exhaustion')
    except Exception as exc:
        report.update(status='preprocessing_failed' if isinstance(exc,PreprocessingFailure) else 'selection_failed' if isinstance(exc,SelectionFailure) else 'integrity_error' if report['source'] is not None else 'invalid_input',
                      error=f'{type(exc).__name__}: {exc}',automatic_train_proofs=0,
                      remaining_obligations=['Resolve reported input or integrity failure'])
    return finish()
