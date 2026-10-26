"""Actual Lean compilation of positive/negative structural regression inputs."""
import copy,hashlib,json,re,uuid
from pathlib import Path
from workflow.contracts import HERE,ROOT,save,sha,accept_proof
from workflow.structural import slot
from workflow.worker import prepared_environment
from product.pipeline import lean,assemble

def run(spec,cases,prepare,prove,*,required_constructions=None):
    work=HERE/'generated'/(spec['method']+'_checks')/uuid.uuid4().hex;work.mkdir(parents=True)
    report=dict(status='started',cases=[],work_directory=str(work),train_proofs_counted=0,test_files_read=0)
    def source_text(context,target):return f"import Benchmark.{spec['module']}\nopen scoped BigOperators\nnamespace StructuralRegression\nset_option autoImplicit false\ntheorem statement {context} :\n {target} := by\n  sorry\nend StructuralRegression\n"
    try:
        setup=work/'setup';setup.mkdir()
        prepare(source_text(cases[0][1],cases[0][2]),setup)
        data=json.loads((setup/'environment.json').read_text());env=prepared_environment(data)
        positives=[]
        for name,ctx,target,expected in cases:
            case=work/name;case.mkdir();text=source_text(ctx,target);file=case/'source.lean';file.write_text(text)
            source=dict(path=str(file.relative_to(ROOT)),snapshot=str(file),sha256=sha(file),theorem='StructuralRegression.statement')
            extract=case/'Extract.lean';extract.write_text(assemble((HERE/'workflow/StructuralExport.lean').read_text(),slot(text,'  structural_export',spec['module'])))
            r=lean(extract,env);save(case/'extraction.json',r)
            lines=[l.split('STRUCTURAL_JSON:',1)[1] for l in r['output'].splitlines() if 'STRUCTURAL_JSON:' in l]
            if len(lines)!=1 or len(re.findall(r'\berror:',r['output']))!=1:raise ValueError('invalid test expression: '+r['output'])
            local=copy.deepcopy(data);local.update(expression=json.loads(lines[0]),source_text_sha256=hashlib.sha256(text.encode()).hexdigest())
            result=prove(text,source,case,env,local,dict(symbolic_seconds=100,max_degree=5,max_unknowns=10000))
            if result['status']=='proved':
                accept_proof(result,source,case);positives.append((result,source,case))
                required=(required_constructions or {}).get(name)
                if required:
                    certificate=json.loads(Path(result['certificate']['path']).read_text())
                    if certificate.get('certificate_origin')!='computed_witness' or certificate.get('plan')!=required:
                        raise AssertionError(name+': required an automatically constructed certificate, not a fallback proof')
            passed=(result['status']=='proved')==expected
            report['cases'].append(dict(name=name,status=result['status'],passed=passed,
                required_construction=(required_constructions or {}).get(name),report=str(case/(spec['method']+'_report.json'))))
            save(work/'report.json',report)
            if not passed:raise AssertionError(name)
        result,source,case=positives[0]
        bad=copy.deepcopy(result);bad['certificate']['sha256']='0'*64
        try:accept_proof(bad,source,case)
        except ValueError as exc:
            if 'certificate' not in str(exc):raise
        else:raise AssertionError('tampered certificate accepted')
        report.update(status='passed',certificate_tampering_rejected=True)
    except Exception as exc:report.update(status='failed',error=str(exc))
    save(work/'report.json',report);save(HERE/'generated'/(spec['method']+'_validation.json'),report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='passed' else 1
