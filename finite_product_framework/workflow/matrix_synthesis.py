"""Transport for independent matrix constructors, with original-goal replay.

Each method supplies its own constructor. This module only exports expressions,
enforces budgets, runs Lean, and binds successful artifacts to their sources.
"""
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path
from workflow.contracts import HERE, ROOT, save, sha
from workflow import structural
from product.pipeline import assemble, lean


def prepare(source, work, spec):
    candidates = structural.prepare(source, work, spec)
    file = work/'environment.json'
    data = json.loads(file.read_text())
    for path in (HERE/'workflow/MatrixExport.lean', HERE/'workflow/matrix_symbolic.py',
                 Path(__file__), HERE/spec['method']/'construct.py'):
        data['dependencies'].append(dict(path=str(path.relative_to(ROOT)), sha256=sha(path)))
    if candidates[0]['applicable'] and 'lean_path' in data:
        env=dict(os.environ,LEAN_PATH=data['lean_path'])
        raw=extract_input(source,work,env,spec)
        # Structural fallbacks have their own obligations. Rejection by the
        # matrix exporter must not turn off a valid transpose/structure route.
        checked=raw is not None
        candidates[0]['admission_checks']=dict(
            core_domain='accepted' if checked else 'unknown' if spec['plans'] else 'rejected',
            proof_exit='conditional' if checked else 'unknown' if spec['plans'] else 'unavailable',
            branches=dict(finite_matrix='accepted' if checked else 'rejected',
                          structural_templates='candidate' if spec['plans'] else 'absent'),
            obligations=['Construct witness and prove original-domain transport in Lean'],
            input_shape=raw.get('size',raw.get('n')) if checked else None)
        candidates[0]['reason']=('Concrete finite matrix shape exported; scalar/domain obligations remain' if checked else
            'Concrete matrix shape rejected; structural templates remain candidates' if spec['plans'] else
            'No supported concrete matrix shape exported')
        candidates[0]['applicable']=checked or bool(spec['plans'])
    save(file, data)
    return candidates


def extract_input(text,work,env,spec,timeout=120):
    probe=work/'SynthesisInput.lean'
    probe.write_text(assemble((HERE/'workflow/MatrixExport.lean').read_text(),
        structural.slot(text, '  matrix_synthesis_export "'+spec['method']+'"', spec['module'])))
    extracted=lean(probe,env,timeout=timeout)
    save(work/'synthesis_extraction.json',extracted)
    lines=[line.split('MATRIX_SYNTHESIS_JSON:',1)[1] for line in extracted['output'].splitlines()
           if 'MATRIX_SYNTHESIS_JSON:' in line]
    if (len(lines)==1 and 'MATRIX_SYNTHESIS_EXPORT_ONLY' in extracted['output'] and
            len(re.findall(r'\berror:',extracted['output']))==1):
        raw=json.loads(lines[0]);save(work/'synthesis_input.json',raw)
        return raw
    if ('SYNTHESIS_UNSUPPORTED:' in extracted['output'] and
            len(re.findall(r'\berror:',extracted['output']))==1):
        return None
    raise RuntimeError('matrix exporter did not complete; see synthesis_extraction.json')


def prove_source(text, source, work, env, data, budget, spec, constructor):
    if hashlib.sha256(text.encode()).hexdigest() != data['source_text_sha256']:
        raise ValueError('analysis/source mismatch')
    deadline = time.monotonic() + budget['symbolic_seconds']
    report = dict(backend=spec['backend'], dependencies=data['dependencies'],
                  status='search_exhausted', attempts=[], construction={},
                  remaining_obligations=['Construct a supported certificate and close the original goal'])
    try:
        raw=extract_input(text,work,env,spec,timeout=max(.01,deadline-time.monotonic()))
        if raw is not None:
            # CAS construction is under the outer worker process-group timeout.
            plans = constructor(raw)
            report['construction'] = dict(status='constructed', source='computed_from_original_expression',
                                          candidates=plans)
            save(work/'construction.json', report['construction'])
            for number, plan in enumerate(plans):
                if time.monotonic() >= deadline:
                    report['status'] = 'resource_exhausted'
                    break
                file = work/f'Synthesized{number}.lean'
                file.write_text(assemble('import Mathlib.Tactic\n',
                    structural.slot(text, plan['proof_script'], spec['module']))+
                    '\n#print axioms '+source['theorem']+'\n')
                result = lean(file, env, timeout=max(.01, deadline-time.monotonic()))
                save(work/f'synthesized{number}.json', result)
                report['attempts'].append(dict(plan=plan['plan'], exit_code=result['exit_code'],
                                               log=str(work/f'synthesized{number}.json')))
                if result['exit_code'] or 'sorryAx' in result['output']:
                    continue
                proof = work/'Proof.lean'
                proof.write_bytes(file.read_bytes())
                cert = work/'certificate.json'
                save(cert, dict(schema_version=2, kind=spec['backend'],
                    source_sha256=source['sha256'], proof_sha256=sha(proof),
                    certificate_origin='computed_witness', input=raw, plan=plan['plan'],
                    construction=plan['certificate'], proof_script=plan['proof_script'],
                    remaining_obligations=[]))
                report.update(status='proved', remaining_obligations=[],
                    certificate=dict(path=str(cert),sha256=sha(cert)),
                    verification=dict(proof_file=str(proof),proof_sha256=sha(proof),lean=result))
                break
        else:
            report['construction'] = dict(status='unsupported_representation',
                reason='finite matrix synthesis requires its supported original expression',
                log=str(work/'synthesis_extraction.json'))
    except subprocess.TimeoutExpired:
        report['status'] = 'resource_exhausted'
    except (ValueError, NotImplementedError, ZeroDivisionError) as exc:
        report['construction'] = dict(status='construction_failed',error=str(exc))
    if report['status'] != 'proved' and spec['plans'] and time.monotonic() < deadline:
        # Only method-local computational templates remain here. Context-only
        # inverse/operator/LU certificate replay is deliberately not a fallback.
        remaining = dict(budget,symbolic_seconds=deadline-time.monotonic())
        fallback = structural.prove_source(text,source,work,env,data,remaining,spec)
        fallback['construction'] = report['construction']
        fallback['attempts'] = report['attempts'] + fallback['attempts']
        report = fallback
    save(work/(spec['method']+'_report.json'), report)
    return report
