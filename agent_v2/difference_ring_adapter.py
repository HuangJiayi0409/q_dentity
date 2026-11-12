"""One real source-derived evaluated difference-ring construction, pending common Lean check."""
from pathlib import Path
import time
from .difference_ring_frontend import analyze_source
from .models import Artifact,Source
from .process import prepare_attempt,validate_seconds,write_json
from .storage import sha256_file,verify_source

VERSION='2.0'


def dependencies():
    from .symbolic_methods import difference_ring_dependencies
    root=Path(__file__).resolve().parents[1]
    names=['benchmark/lean/Benchmark/'+name+'.lean' for name in
           ('Definitions','Auxiliary','Gaussian')]
    names+=['agent_v2/lean/DifferenceRingRules.lean','benchmark/lean/lean-toolchain',
            'benchmark/lean/lakefile.toml','project/lean-toolchain','project/lakefile.toml','project/lake-manifest.json']
    return difference_ring_dependencies()+tuple(Artifact(str(root/name),sha256_file(root/name)) for name in names)


class DifferenceRingAdapter:
    def execute_request(self,request,attempt_dir,seconds):
        from .symbolic_methods import SymbolicAdapter
        return SymbolicAdapter('difference_ring').execute_request(request,attempt_dir,seconds)

    def execute(self,identity,method,source,attempt_dir,seconds):
        from .cas_adapter import adapter_result
        from .difference_ring_translation import translate_candidate
        from .executor import normalize_result
        from .symbolic_methods import SymbolicAdapter
        started=time.monotonic();attempt=None
        try:
            validate_seconds(seconds);attempt=prepare_attempt(attempt_dir)
            if any(attempt.iterdir()):raise ValueError('difference_ring attempt directory must be empty')
            bound=Source.from_dict(source)
            if identity!=bound.identity or method!='difference_ring':
                raise ValueError('difference_ring method/source identity mismatch')
            run_root=Path(bound.snapshot_path).parent.parent;verify_source(bound,run_root)
            write_json(attempt/'method_request.json',{'method':method,'version':VERSION,
                'identity':identity,'source':source,'seconds':seconds,'scope':'local'},attempt)
            front=analyze_source(source,run_root);write_json(attempt/'frontend.json',front,attempt)
            if front['status']!='applicable':
                return adapter_result(started,'incomplete','not_applicable',
                    'Source is outside the controlled Pochhammer evaluated-difference contract.',
                    raw_result={'frontend':front},attempt=attempt)
            write_json(attempt/'mapping.json',{'atoms':front['mapping'],
                'step_relation':front['step_relation'],'local_proposition':front['local_proposition'],
                'relation_origin':front['relation_origin']},attempt)
            write_json(attempt/'cas_request.json',front['core_request'],attempt)
            remaining=seconds-(time.monotonic()-started)
            if remaining<=0:
                return adapter_result(started,'budget_exhausted','timeout','Source export exhausted budget.',attempt=attempt)
            core_raw=SymbolicAdapter('difference_ring').execute_request(front['core_request'],attempt/'core',remaining)
            write_json(attempt/'cas_return.json',core_raw,attempt);core=normalize_result(core_raw)
            verify_source(bound,run_root)
            raw={'frontend_profile':front['profile'],'source_sha256':bound.sha256,
                 'method_version':VERSION,'core':core.to_dict()['raw_result'],
                 'execution_scope':'local_certificate_only'}
            if core.status!='symbolic_constructed':
                return adapter_result(started,core.status,core.sigma.code,core.sigma.message,
                    stage=core.sigma.stage,raw_result=raw,diagnostics=list(core.diagnostics),attempt=attempt)
            translation=translate_candidate(front,raw['core']);write_json(attempt/'translation.json',translation,attempt)
            raw.update(translation=translation,remaining_work={'formal_obligations_exported':False,
                'open_obligation':'original','explanation':'Initial-factor/tail parameter shift and original equality remain open.'})
            if time.monotonic()-started>=seconds:
                return adapter_result(started,'budget_exhausted','timeout','Independent translation exhausted budget.',raw_result=raw,attempt=attempt)
            if translation['status']!='candidate_ready':
                return adapter_result(started,'symbolic_constructed','translation_pending',
                    'Core output has no accepted source-bound difference_ring translation.',
                    stage='translation',raw_result=raw,attempt=attempt)
            write_json(attempt/'candidate.json',translation['candidate'],attempt);verify_source(bound,run_root)
            result=adapter_result(started,'symbolic_constructed','local_candidate_ready',
                'One source product-increment candidate awaits independent Lean verification.',
                stage='translation',backend_status='constructed',raw_result=raw,attempt=attempt)
            result['C_partial']=[translation['candidate']]
            return result
        except (OSError,ValueError,TypeError) as error:
            return adapter_result(started,'integrity_error','artifact_integrity',str(error))
