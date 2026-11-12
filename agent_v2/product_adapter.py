"""Source-only L2 finite-product execution; no Lean candidate is exported."""
import json
from pathlib import Path
import sys
import time
from .models import Artifact,Source,canonical,digest
from .process import guard_artifact,prepare_attempt,run_process,validate_seconds,write_json
from .product_frontend import analyze_source
from .product_worker import ROOT,core_inventory,load_core
from .storage import IntegrityError,sha256_file,verify_source

VERSION='2.0'


def dependencies():
    names=('finite_product_framework/product/index_construct.py',
           'benchmark/lean/Benchmark/Definitions.lean',
           'agent_v2/product_worker.py','agent_v2/product_frontend.py',
           'agent_v2/product_check.py','agent_v2/product_adapter.py')
    return tuple(Artifact(str(ROOT/name),sha256_file(ROOT/name)) for name in names)


def execute_core_request(request,attempt_dir,seconds):
    """Internal typed worker boundary; it has no formal Source or state."""
    from .cas_adapter import adapter_result
    started=time.monotonic();attempt=None
    try:
        validate_seconds(seconds);attempt=prepare_attempt(attempt_dir)
        if any(attempt.iterdir()):raise ValueError('product core attempt must be empty')
        try:load_core().validate_request(request)
        except ValueError as error:
            write_json(attempt/'rejection.json',{'code':'not_applicable','message':str(error)},attempt)
            return adapter_result(started,'incomplete','not_applicable',str(error),attempt=attempt)
        write_json(attempt/'request.json',request,attempt)
        before=core_inventory();write_json(attempt/'dependencies_before.json',before,attempt)
        remaining=seconds-(time.monotonic()-started)
        if remaining<=0:return adapter_result(started,'budget_exhausted','timeout','Product export exhausted budget.',attempt=attempt)
        command=[sys.executable,'-B','-m','agent_v2.product_worker','--input',str(attempt/'request.json'),
                 '--output',str(attempt/'construction.json')]
        process=run_process(command,ROOT,remaining,attempt/'stdout.txt',attempt/'stderr.txt')
        write_json(attempt/'process.json',process,attempt)
        if process.get('cleanup_survivors'):
            return adapter_result(started,'environment_blocked','cleanup_failed','Product worker descendants were not cleaned.',diagnostics=[process],attempt=attempt)
        if process.get('timed_out'):
            return adapter_result(started,'budget_exhausted','timeout','Product worker exhausted wall-clock budget.',diagnostics=[process],attempt=attempt)
        if process.get('environment_error'):
            return adapter_result(started,'environment_blocked','process_error','Product worker could not execute.',diagnostics=[process],attempt=attempt)
        output=guard_artifact(attempt/'construction.json',attempt)
        if not output.is_file():
            return adapter_result(started,'environment_blocked','core_output_missing','Product worker produced no result.',diagnostics=[process],attempt=attempt)
        if output.stat().st_size>1000000:raise IntegrityError('oversized product output')
        try:raw=json.loads(output.read_text())
        except (ValueError,UnicodeError) as error:
            return adapter_result(started,'integrity_error','malformed_core_output',str(error),attempt=attempt)
        after=core_inventory();write_json(attempt/'dependencies_after.json',after,attempt)
        if before!=after:raise IntegrityError('product constructor changed during execution')
        if (not isinstance(raw,dict) or type(raw.get('schema_version')) is not int or raw['schema_version']!=1
                or set(raw)-{'schema_version','method','request_sha256','original_identity_proved','python_version',
                             'source_before','source_after','status','construction','error'}
                or raw.get('method')!='product' or raw.get('request_sha256')!=digest(request)
                or raw.get('source_before')!=before or raw.get('source_after')!=after
                or raw.get('python_version')!=sys.version.split()[0] or raw.get('original_identity_proved') is not False):
            raise IntegrityError('product worker source/request/output binding mismatch')
        status=raw.get('status')
        if process['returncode']!=0 and status=='constructed':raise IntegrityError('product construction after abnormal process exit')
        if process['returncode']!=0 or status=='environment_blocked':
            return adapter_result(started,'environment_blocked','core_execution_failed','Product worker failed.',raw_result=raw,diagnostics=[process],attempt=attempt)
        if status not in ('constructed','search_exhausted','budget_exhausted'):
            raise IntegrityError('unknown product constructor status')
        if not isinstance(raw.get('construction'),dict) or raw['construction'].get('status')!=status:
            raise IntegrityError('product construction status mismatch')
        if status=='budget_exhausted':
            return adapter_result(started,'budget_exhausted','resource_exhausted','Product map search reached its explicit bound.',raw_result=raw,attempt=attempt)
        if status=='search_exhausted':
            return adapter_result(started,'incomplete','search_exhausted','No compatible index map was constructed.',raw_result=raw,attempt=attempt)
        from .product_check import check
        checked=check(request,raw['construction'])
        write_json(attempt/'independent_check.json',checked,attempt)
        return adapter_result(started,'symbolic_constructed','translation_pending',
            'A finite-index and weight certificate was constructed and checked symbolically; Lean translation is unavailable.',
            stage='symbolic_core',backend_status='constructed',raw_result=dict(raw,independent_symbolic_check=checked),attempt=attempt)
    except (OSError,ValueError,TypeError,KeyError,RecursionError) as error:
        return adapter_result(started,'integrity_error','artifact_integrity',str(error),attempt=attempt)


class ProductAdapter:
    """The original broad standalone request remains unsupported, explicitly."""
    def execute(self,identity,method,source,attempt_dir,seconds):
        from .cas_adapter import adapter_result
        from .executor import normalize_result
        started=time.monotonic();attempt=None
        try:
            validate_seconds(seconds);attempt=prepare_attempt(attempt_dir)
            if any(attempt.iterdir()):raise ValueError('product source attempt must be empty')
            bound=Source.from_dict(source)
            if identity!=bound.identity or method!='product':raise IntegrityError('product source/method identity mismatch')
            run_root=Path(bound.snapshot_path).parent.parent;verify_source(bound,run_root)
            write_json(attempt/'method_request.json',{'method':method,'version':VERSION,'identity':identity,
                'source':source,'seconds':seconds,'scope':'source_symbolic_only'},attempt)
            front=analyze_source(source,run_root);write_json(attempt/'frontend.json',front,attempt)
            if front['status']!='applicable':
                return adapter_result(started,'incomplete','not_applicable','Source is outside the finite residue-product contract.',raw_result={'frontend':front},attempt=attempt)
            write_json(attempt/'mapping.json',front['mapping'],attempt)
            write_json(attempt/'definition_binding.json',front['definition_binding'],attempt)
            write_json(attempt/'cas_request.json',front['core_request'],attempt)
            remaining=seconds-(time.monotonic()-started)
            if remaining<=0:return adapter_result(started,'budget_exhausted','timeout','Source export exhausted budget.',attempt=attempt)
            core_raw=execute_core_request(front['core_request'],attempt/'core',remaining)
            write_json(attempt/'cas_return.json',core_raw,attempt);core=normalize_result(core_raw)
            verify_source(bound,run_root)
            if canonical(analyze_source(source,run_root))!=canonical(front):raise IntegrityError('product source or definition changed during construction')
            raw={'execution_scope':'source_symbolic_only','source_sha256':bound.sha256,
                 'frontend_profile':front['profile'],'method_version':VERSION,'core':core.to_dict()['raw_result'],
                 'remaining_work':front['remaining_work'],'lean_verified':False,'formal_obligations_exported':False}
            if core.status=='symbolic_constructed':
                raw['independent_symbolic_check']=raw['core']['independent_symbolic_check']
                write_json(attempt/'symbolic_certificate.json',raw['core']['construction'],attempt)
            if time.monotonic()-started>=seconds and core.status not in ('integrity_error','environment_blocked'):
                return adapter_result(started,'budget_exhausted','timeout','Product source execution exhausted budget.',raw_result=raw,attempt=attempt)
            return adapter_result(started,core.status,core.sigma.code,core.sigma.message,
                stage=core.sigma.stage,backend_status=core.sigma.backend_status,raw_result=raw,
                diagnostics=list(core.diagnostics),attempt=attempt)
        except (OSError,ValueError,TypeError,KeyError,RecursionError) as error:
            return adapter_result(started,'integrity_error','artifact_integrity',str(error),attempt=attempt)
