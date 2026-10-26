"""Independent source → public representation → equivalence evidence workflow.

Nothing in this module runs on import. `prepare` copies sources only; `run`
explicitly invokes Lean. Neither operation dispatches to a proving method.
"""
import json
import os
from pathlib import Path
import subprocess
import time

from . import SCHEMA_VERSION
from .representation import standardize
from .wire import pack, unpack
from .source import REPO, digest, load, probe_text

HERE = Path(__file__).resolve().parent
MAX_JSON_BYTES = 64 * 1024 * 1024


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n')


def prepare(identity: str, output: Path, *, support_modules=(), view="structured"):
    if view not in ("structured", "expanded"): raise ValueError("unknown_preprocessing_view")
    """Snapshot current Train and shared definitions into a new isolated directory."""
    source = load(identity, support_modules)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    files, modules = {}, []

    def copy_bytes(relative, data):
        dest = output / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        files[relative] = digest(data)

    copy_bytes('original.lean', source.text.encode())
    for dep in source.dependencies:
        data = (REPO / dep['path']).read_bytes()
        if digest(data) != dep['sha256']:
            raise ValueError('dependency_changed_during_snapshot: ' + dep['module'])
        relative = 'src/' + dep['module'].replace('.', '/') + '.lean'
        copy_bytes(relative, data)
        modules.append(dict(module=dep['module'], source=relative))
    for name in ('Rules', 'Wire', 'Export'):
        relative = f'src/FiniteQPreprocess/{name}.lean'
        copy_bytes(relative, (HERE / f'lean/FiniteQPreprocess/{name}.lean').read_bytes())
        modules.append(dict(module=f'FiniteQPreprocess.{name}', source=relative))
    copy_bytes('src/Probe.lean', probe_text(source.text, 'preprocess_export_expanded' if view == 'expanded' else 'preprocess_export').encode())
    for name in ('lean-toolchain', 'lake-manifest.json'):
        data = (REPO / 'benchmark/lean' / name).read_bytes()
        if data != (REPO / 'project' / name).read_bytes():
            raise ValueError('toolchain_or_library_manifest_mismatch: ' + name)
        copy_bytes(name, data)
    implementation = {
        str(p.relative_to(HERE)): digest(p.read_bytes())
        for p in sorted(HERE.rglob('*')) if p.suffix in ('.py', '.lean')
    }
    request = dict(schema_version=SCHEMA_VERSION, status='prepared_unverified',
                   source=source.evidence(), files=files, modules=modules,
                   implementation=implementation,
                   policy=dict(method_neutral=True, classifier=False, normalization_view=view,
                               new_assumptions=False, target_proof=False,
                               global_simp_rules=False, test_split_access=False))
    write_json(output / 'request.json', request)
    write_json(output / 'status.json', dict(status='prepared_unverified',
                                          identity_proved=False, lean_executed=False))
    return request


def check_snapshot(output, request):
    for relative, expected in request['files'].items():
        if digest((output / relative).read_bytes()) != expected:
            raise ValueError('snapshot_changed: ' + relative)
    for relative, expected in request['implementation'].items():
        if digest((HERE / relative).read_bytes()) != expected:
            raise ValueError('implementation_changed: ' + relative)
    current = load(request['source']['identity'], request['source'].get('support_modules', ()))
    if current.evidence() != request['source']:
        raise ValueError('current_source_or_dependencies_changed')
    return current


def read_messages(log):
    if log.stat().st_size > MAX_JSON_BYTES:
        raise ValueError('lean_output_budget')
    messages = []
    for line in log.read_text().splitlines():
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError('unexpected_non_json_lean_output') from exc
        if not isinstance(message, dict):
            raise ValueError('unexpected_lean_message')
        messages.append(message)
    return messages


def payload(messages, marker, sentinel, code):
    """A deliberate final tactic error is not a theorem proof or a compiler pass."""
    errors = [m.get('data', '') for m in messages if m.get('severity') == 'error']
    if code != 1 or len(errors) != 1 or errors[0].strip() != sentinel:
        raise ValueError('lean_probe_failed: expected only ' + sentinel)
    values = [m['data'][len(marker):] for m in messages
              if m.get('severity') == 'information' and m.get('data', '').startswith(marker)]
    if len(values) != 1:
        raise ValueError('missing_or_duplicate_payload: ' + marker)
    result = json.loads(values[0])
    if not isinstance(result, dict):
        raise ValueError('invalid_payload')
    return unpack(result) if marker == 'PREPROCESS_JSON:' else result


def run(identity: str, output: Path, timeout=600, *, support_modules=(), view="structured"):
    """Explicit future execution entry: compile, construct, replay, then publish.

    `timeout` is one total wall-clock budget including dependency compilation.
    Failure preserves diagnostics and never emits a verified standard artifact.
    """
    if timeout <= 0:
        raise ValueError('timeout_must_be_positive')
    output = Path(output).resolve()
    start = time.monotonic()
    request = prepare(identity, output, support_modules=support_modules, view=view)
    steps = []
    phase, lean_executed = 'environment', False
    try:
        source = check_snapshot(output, request)
        toolchain = (output / 'lean-toolchain').read_text().strip()
        exe = Path.home() / '.elan/toolchains' / toolchain.replace('/', '--').replace(':', '---') / 'bin/lean'
        if not exe.is_file():
            raise ValueError('local_lean_toolchain_missing')
        packages = sorted((REPO / 'project/.lake/packages').glob('*/.lake/build/lib/lean'))
        if not packages:
            raise ValueError('local_mathlib_cache_missing')
        build = output / 'build'
        build.mkdir()
        (output / 'logs').mkdir()
        env = os.environ.copy()
        env['LEAN_PATH'] = os.pathsep.join(str(p) for p in [build, *packages])
        env['LEAN_ABORT_ON_PANIC'] = '1'
        executable_sha256 = digest(exe.read_bytes())

        def invoke(name, path, target=None):
            nonlocal lean_executed
            remaining = timeout - (time.monotonic() - start)
            if remaining <= 0:
                raise TimeoutError('preprocessing_total_timeout')
            command = [str(exe), '--json', '-j1', '-DautoImplicit=false',
                       '-DmaxRecDepth=8192', '-DmaxHeartbeats=2000000']
            if target is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                command.extend(['-o', str(target)])
            command.append(str(path))
            log = output / 'logs' / (name + '.jsonl')
            lean_executed = True
            tick = time.monotonic()
            with log.open('wb') as stream:
                result = subprocess.run(command, cwd=output / 'src', env=env,
                                        stdout=stream, stderr=subprocess.STDOUT, timeout=remaining)
            messages = read_messages(log)
            steps.append(dict(name=name, exit_code=result.returncode,
                              seconds=round(time.monotonic() - tick, 3),
                              log_sha256=digest(log.read_bytes())))
            return result.returncode, messages

        phase = 'compile_dependencies'
        for module in request['modules']:
            target = build / (module['module'].replace('.', '/') + '.olean')
            code, messages = invoke(module['module'], output / module['source'], target)
            if code or any(m.get('severity') == 'error' for m in messages):
                raise ValueError('dependency_compile_failed: ' + module['module'])
        phase = 'export_and_normalize'
        code, messages = invoke('export', output / 'src/Probe.lean')
        bundle = payload(messages, 'PREPROCESS_JSON:', 'PREPROCESS_EXPORT_ONLY', code)
        if bundle.get('wire_version') != 1:
            raise ValueError('unsupported_wire_version')
        write_json(output / 'bundle.json', pack(bundle))
        bundle_hash = digest((output / 'bundle.json').read_bytes())
        candidate = standardize(bundle, request['source'])
        write_json(output / 'candidate.json', candidate)

        phase = 'replay_original_context'
        # The quoted relative path is fixed, avoiding code injection via output paths.
        replay = probe_text(source.text, 'preprocess_replay "../bundle.json"')
        (output / 'src/Replay.lean').write_text(replay)
        code, messages = invoke('replay', output / 'src/Replay.lean')
        verification = payload(messages, 'PREPROCESS_REPLAY_JSON:', 'PREPROCESS_REPLAY_ONLY', code)
        if verification.get('bridge_kernel_checked') is not True or verification.get('original_context_matched') is not True:
            raise ValueError('incomplete_equivalence_verification')
        check_snapshot(output, request)
        if digest((output / 'bundle.json').read_bytes()) != bundle_hash:
            raise ValueError('bundle_changed_during_replay')
        if digest(exe.read_bytes()) != executable_sha256:
            raise ValueError('lean_executable_changed')
        phase = 'publish'
        result = standardize(bundle, request['source'], verified=True)
        result['evidence'] = dict(verification=verification, bundle_sha256=bundle_hash,
                                  executable_sha256=executable_sha256,
                                  request_sha256=digest((output / 'request.json').read_bytes()),
                                  original_theorem_proved=False)
        write_json(output / 'standard.json', result)
        status = dict(status=result['status'], identity_proved=False, lean_executed=True,
                      verification=verification, steps=steps,
                      seconds=round(time.monotonic() - start, 3))
        write_json(output / 'status.json', status)
        return status
    except Exception as exc:
        write_json(output / 'status.json', dict(status='failed', phase=phase,
                   error_type=type(exc).__name__, reason=str(exc), steps=steps,
                   identity_proved=False, lean_executed=lean_executed,
                   seconds=round(time.monotonic() - start, 3)))
        raise
