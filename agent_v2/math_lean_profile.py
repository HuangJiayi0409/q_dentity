"""Fixed, source-bound Lean environment for one telescoping structure profile.

This is deliberately separate from the Init checker. It compiles fresh local
Benchmark foundations and the candidate, freezes only the actual fixed import
closure, and never imports a benchmark statement or historical proof module.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import time
import uuid

from .models import Source, canonical
from .storage import IntegrityError, guard_path, verify_source

PROFILE = 'gaussian_weighted_range_v1'
FOUNDATIONS = ('Definitions', 'Auxiliary', 'Gaussian')
ARTIFACT_SUFFIXES = ('.olean', '.olean.private', '.olean.server', '.olean.sig', '.ir')


def _save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def _guard_dependency(path, checker, module=None):
    """Permit only the fixed Std HTTP helper closure's Test-named components.

    Lean's Mathlib import closure includes Std.Http.Test helpers. These are
    standard-library modules, never the held-out benchmark. This exception
    cannot be selected by a candidate and never changes the global path guard.
    """
    try:
        return guard_path(path)
    except IntegrityError:
        if not isinstance(module, str) or not re.fullmatch(r'Std\.Http\.Test(?:\.[A-Za-z0-9_]+)*', module):
            raise
        root = checker.expected_binary.parent.parent.absolute()
        stem = module.replace('.', '/')
        expected = {root / 'src/lean' / (stem + '.lean')}
        expected.update(root / 'lib/lean' / (stem + suffix) for suffix in ARTIFACT_SUFFIXES)
        path = Path(path).absolute()
        if path not in expected or '..' in path.parts:
            raise IntegrityError('Test-named dependency is outside the fixed standard-library module')
        for ancestor in [path, *path.parents]:
            if ancestor == root.parent:
                break
            if ancestor.is_symlink():
                raise IntegrityError('symlink standard-library dependency refused')
        if not path.resolve().is_relative_to(root.resolve()):
            raise IntegrityError('standard-library dependency escapes fixed toolchain')
        return path.resolve()


def _hash(path, deadline, trusted_guard=None):
    path = trusted_guard(path) if trusted_guard is not None else guard_path(path)
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            if time.monotonic() >= deadline:
                raise TimeoutError('mathematical dependency audit exhausted verification budget')
            digest.update(chunk)
    return digest.hexdigest()


def _package_roots(repository):
    manifest = guard_path(repository / 'project/lake-manifest.json')
    data = json.loads(manifest.read_text())
    if data.get('packagesDir') != '.lake/packages' or not isinstance(data.get('packages'), list):
        raise IntegrityError('unsupported fixed project package manifest')
    roots = []
    names = set()
    for package in data['packages']:
        name = package.get('name')
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', name) or name in names:
            raise IntegrityError('invalid or duplicate fixed project package')
        if package.get('subDir') is not None:
            raise IntegrityError('package source subdirectories are not supported')
        names.add(name)
        root = guard_path(repository / 'project/.lake/packages' / name)
        build = guard_path(root / '.lake/build/lib/lean')
        roots.append((root, build))
    if not roots:
        raise FileNotFoundError('fixed project package cache is empty')
    return roots, manifest


def _assert_object_resolution(module, expected_root, search_roots, *, allow_missing=False):
    """Check the same ordered LEAN_PATH lookup Lean uses, including bare objects.

    Resolving sources by module prefix is insufficient: a higher-priority root
    may contain only a same-named .olean and silently shadow the frozen source.
    Optional split artifacts are checked too, even when no source accompanies
    them. No shadowed file is read to report this rejection.
    """
    stem = module.replace('.', '/')
    for suffix in ARTIFACT_SUFFIXES:
        expected = expected_root / (stem + suffix)
        found = next((root / (stem + suffix) for root in search_roots
                      if (root / (stem + suffix)).is_file()), None)
        if found is not None and found.absolute() != expected.absolute():
            raise IntegrityError('Lean import object shadow detected: ' + module + suffix)
        if found is not None and found.resolve() != found.absolute():
            raise IntegrityError('Lean import object symlink alias refused: ' + module + suffix)
        if found is None and suffix == '.olean' and not allow_missing:
            raise FileNotFoundError('fixed Lean object unavailable on actual search path: ' + module)


def _inventory(checker, imports, package_roots, fixed_paths, deadline, local_build=None):
    """Resolve just the fixed import closure; no repository-wide search/read."""
    from .lean_checker import _NAME, _header_imports, _runtime_libraries
    binary = checker.binary
    standard = (binary.parent.parent / 'src/lean', binary.parent.parent / 'lib/lean')
    lake = (binary.parent.parent / 'src/lean/lake', binary.parent.parent / 'lib/lean')
    search_roots = ([local_build] if local_build is not None else []) + [obj for _, obj in package_roots] + [standard[1]]
    paths = {path: None for path in (*fixed_paths, binary, checker.toolchain_configuration)}
    pending, modules = list(imports), set()
    benchmark = checker.repository / 'benchmark/lean/Benchmark'
    while pending:
        if time.monotonic() >= deadline:
            raise TimeoutError('mathematical module resolution exhausted verification budget')
        module = pending.pop()
        if module in modules:
            continue
        if not _NAME.fullmatch(module):
            raise IntegrityError('invalid fixed import')
        relative = module.replace('.', '/')
        if module.startswith('Benchmark.'):
            short = module.removeprefix('Benchmark.')
            if short not in FOUNDATIONS:
                raise IntegrityError('unapproved Benchmark import: ' + module)
            source = guard_path(benchmark / (short + '.lean'))
            paths[source] = None
            if local_build is not None:
                _assert_object_resolution(module, local_build, search_roots, allow_missing=True)
        else:
            prefix = module.split('.')[0]
            roots = [lake] if prefix == 'Lake' else (
                [standard] if prefix in {'Init', 'Lean', 'Std'} else package_roots)
            matches = [(src, obj) for src, obj in roots if (src / (relative + '.lean')).is_file()]
            if len(matches) != 1:
                raise FileNotFoundError('missing or ambiguous fixed Lean module: ' + module)
            src, obj = matches[0]
            _assert_object_resolution(module, obj, search_roots)
            source = _guard_dependency(src / (relative + '.lean'), checker, module)
            paths[source] = module
            for suffix in ARTIFACT_SUFFIXES:
                artifact = _guard_dependency(obj / (relative + suffix), checker, module)
                if artifact.is_file():
                    paths[artifact] = module
                elif suffix == '.olean':
                    raise FileNotFoundError('fixed Lean object missing: ' + module)
        modules.add(module)
        pending.extend(_header_imports(source.read_text()))
    paths.update({path: None for path in _runtime_libraries(binary, deadline)})
    for name in ('/etc/ld.so.cache', '/etc/ld.so.preload'):
        if Path(name).is_file():
            paths[guard_path(name)] = None
    return {'modules': sorted(modules), 'object_search_roots': [str(root) for root in search_roots],
            'standard_library_modules_with_Test_component': sorted(m for m in modules if m.startswith('Std.Http.Test.')),
            'files': [{'path': str(path), 'sha256': _hash(path, deadline,
                       lambda p, module=paths[path]: _guard_dependency(p, checker, module))}
                      for path in sorted(paths)]}


def _compile(binary, source, output, source_root, environment, logs, deadline):
    logs.mkdir(parents=True)
    stdout, stderr = logs / 'stdout.jsonl', logs / 'stderr.txt'
    command = [str(binary), '-j', '1', '--json', '-R', str(source_root), '-o', str(output), str(source)]
    report = {'command': command, 'returncode': None, 'timed_out': False,
              'environment_error': None}
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError('no time left for Lean compilation')
    began = time.monotonic()
    with stdout.open('wb') as out, stderr.open('wb') as err:
        try:
            process = subprocess.Popen(command, cwd=source_root, env=environment,
                                       stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                       start_new_session=True)
            try:
                process.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                report['timed_out'] = True
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            report['returncode'] = process.returncode
        except OSError as error:
            report['environment_error'] = str(error)
    report['wall_seconds'] = time.monotonic() - began
    _save(logs / 'process.json', report)
    return report


def _generated_inventory(directory, run, deadline):
    from .lean_checker import _artifact
    artifacts = []
    for path in sorted(directory.rglob('*')):
        path = guard_path(path, run)
        if path.is_file():
            if time.monotonic() >= deadline:
                raise TimeoutError('generated artifact audit exhausted verification budget')
            artifacts.append(_artifact(path, run))
    return artifacts


def external_environment_digest(inventory):
    """Bind mathematical meanings across replay, excluding fresh build paths."""
    frozen = {'modules': inventory['modules'], 'files': inventory['files']}
    return hashlib.sha256(canonical(frozen).encode('utf-8')).hexdigest()


def check_train_partial(checker, candidate, context, start):
    """Return None for non-profile sources, otherwise a strict checker result."""
    from .formal_frontend import analyze_source
    from .telescoping_translation import local_proof
    from .lean_checker import _AXIOMS, _IMPORTS, _header_imports, _lean_environment, _result

    source = Source.from_dict(context['source'])
    run = guard_path(context['run_dir'])
    attempt = guard_path(context['attempt_dir'], run)
    if source.sha256 != context.get('source_sha256') or source.sha256 != candidate['source_sha256']:
        raise IntegrityError('original source context binding mismatch')
    if source.Gamma != source.declaration:
        raise IntegrityError('frozen original context differs from the source declaration')
    verify_source(source, run)
    frontend = analyze_source(source.to_dict(), run)
    if frontend.get('status') != 'applicable':
        return None
    if frontend.get('profile') != PROFILE:
        raise IntegrityError('unsupported mathematical checking profile')
    expected = frontend['local_proposition']
    if candidate['proposition'] != expected:
        return _result(start, False, 'integrity_error', 'partial', 'proposition_binding_mismatch',
                       'Candidate proposition differs from the independently reconstructed local target.')
    if candidate['proof_term'] not in (local_proof(frontend), 'by rfl', 'by exact True.intro'):
        return _result(start, False, 'incomplete', 'partial', 'unsupported_term_syntax',
                       'Only the fixed telescoping proof template and pure negative-test terms are accepted.')
    seconds = context.get('seconds')
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds):
        raise IntegrityError('finite numerical seconds budget required')
    deadline = start + seconds
    if time.monotonic() >= deadline:
        return _result(start, False, 'budget_exhausted', 'partial', 'budget_exhausted',
                       'No verification time remains.')
    binary = checker.binary
    driver = guard_path(Path(__file__).parent / 'lean/TelescopingCheck.lean')
    rules = guard_path(checker.repository / 'finite_product_framework/p1/lean/GaussianRules.lean')
    if (binary is None or checker.expected_binary is None or not binary.is_file()
            or binary.resolve() != checker.expected_binary.resolve() or not os.access(binary, os.X_OK)
            or not driver.is_file() or not rules.is_file()):
        return _result(start, False, 'environment_blocked', 'partial', 'lean_environment_unavailable',
                       'The fixed Lean toolchain, trusted driver or mathematical foundation is unavailable.')
    directory = guard_path(attempt / ('lean-telescoping-' + uuid.uuid4().hex), run)
    directory.mkdir(parents=True)
    evidence = {key: candidate[key] for key in
                ('proposition', 'proof_term', 'theorem', 'source_sha256', 'dependencies')}
    evidence.update(certificate_id=candidate['id'], profile=PROFILE, artifacts=[])
    try:
        packages, package_manifest = _package_roots(checker.repository)
        driver_text, rules_text = driver.read_text(), rules.read_text()
        imports = tuple(dict.fromkeys((*_IMPORTS, *_header_imports(rules_text))))
        fixed_paths = (driver, rules, package_manifest, checker.repository / 'project/lakefile.toml',
                       checker.repository / 'project/lean-toolchain')
        source_root, build = directory / 'sources', directory / 'build'
        (source_root / 'Benchmark').mkdir(parents=True)
        (build / 'Benchmark').mkdir(parents=True)
        dependencies = _inventory(checker, imports, packages, fixed_paths, deadline, build)
        _save(directory / 'dependencies_before.json', dependencies)
        evidence['external_environment_sha256'] = external_environment_digest(dependencies)
        if 'prior_evidence' in context:
            prior = context['prior_evidence']
            if (not isinstance(prior, dict) or
                    prior.get('external_environment_sha256') != evidence['external_environment_sha256']):
                evidence['artifacts'] = _generated_inventory(directory, run, deadline)
                return _result(start, False, 'integrity_error', 'partial', 'external_environment_changed',
                               'Saved mathematical/toolchain environment differs from fresh independent inventory; replay refused.', evidence)
        _save(directory / 'request.json', candidate)
        _save(directory / 'frontend.json', frontend)
        (directory / 'TrustedDriver.lean').write_text(driver_text)
        (directory / 'GaussianRules.lean').write_text(rules_text)
        environment = _lean_environment(binary)
        environment['LEAN_PATH'] = os.pathsep.join([str(build), *(str(obj) for _, obj in packages),
                                                   str(binary.parent.parent / 'lib/lean')])
        # Rebuild these definitions and auxiliary lemmas from current source.
        # The benchmark's existing compiled statement/proof cache is absent.
        for name in FOUNDATIONS:
            origin = guard_path(checker.repository / 'benchmark/lean/Benchmark' / (name + '.lean'))
            frozen = source_root / 'Benchmark' / (name + '.lean')
            frozen.write_bytes(origin.read_bytes())
            output = build / 'Benchmark' / (name + '.olean')
            report = _compile(binary, frozen, output, source_root, environment,
                              directory / 'setup' / name, deadline)
            if report['timed_out']:
                evidence['artifacts'] = _generated_inventory(directory, run, float('inf'))
                return _result(start, False, 'budget_exhausted', 'partial', 'lean_timeout',
                               'Lean dependency compilation exceeded the remaining budget.', evidence)
            if report['environment_error'] or report['returncode'] != 0:
                evidence['artifacts'] = _generated_inventory(directory, run, deadline)
                return _result(start, False, 'environment_blocked', 'partial', 'lean_dependency_compile_failed',
                               'A fixed mathematical dependency did not compile; setup diagnostics are retained.', evidence)
        local_dependencies = _generated_inventory(source_root, run, deadline) + _generated_inventory(build, run, deadline)
        # The initially empty build root has just acquired compiled artifacts.
        # Re-resolve every imported module before compiling the candidate, then
        # repeat below after execution to detect newly introduced shadows.
        resolved = _inventory(checker, imports, packages, fixed_paths, deadline, build)
        if resolved != dependencies:
            raise IntegrityError('fixed mathematical dependencies changed during setup')
        nonce = uuid.uuid4().hex
        without_imports = lambda text: re.sub(r'(?m)^import [A-Za-z0-9_.]+\s*\n', '', text)
        code = ('\n'.join('import ' + name for name in imports) + '\n'
                + without_imports(rules_text) + '\n' + without_imports(driver_text)
                + '\nuniverse u\n'
                + f'theorem {candidate["theorem"]} : ({candidate["proposition"]}) := {candidate["proof_term"]}\n'
                + f'def AgentV2Expected : Prop := ({expected})\n'
                + f'agent_v2_telescoping_audit {candidate["theorem"]} against AgentV2Expected nonce "{nonce}"\n')
        candidate_path = source_root / 'Candidate.lean'
        candidate_path.write_text(code)
        candidate_digest = _hash(candidate_path, deadline)
        report = _compile(binary, candidate_path, build / 'Candidate.olean', source_root,
                          environment, directory / 'candidate', deadline)
        evidence.update(returncode=report['returncode'], lean_binary=str(binary),
                        lean_binary_sha256=_hash(binary, float('inf')),
                        original_path=source.path, snapshot_path=source.snapshot_path)
        if report['timed_out']:
            evidence['artifacts'] = _generated_inventory(directory, run, float('inf'))
            return _result(start, False, 'budget_exhausted', 'partial', 'lean_timeout',
                           'Lean candidate verification exceeded the remaining budget.', evidence)
        if report['environment_error']:
            evidence['artifacts'] = _generated_inventory(directory, run, deadline)
            return _result(start, False, 'environment_blocked', 'partial', 'lean_start_failed',
                           report['environment_error'], evidence)
        verify_source(source, run)
        if _hash(candidate_path, deadline) != candidate_digest:
            raise IntegrityError('candidate source changed during Lean verification')
        for item in local_dependencies:
            if _hash(guard_path(item['path'], run), deadline) != item['sha256']:
                raise IntegrityError('fresh mathematical dependency changed during verification')
        after = _inventory(checker, imports, packages, fixed_paths, deadline, build)
        if after != dependencies:
            raise IntegrityError('fixed mathematical/toolchain dependencies changed during verification')
        _save(directory / 'dependencies_after.json', after)
        evidence['artifacts'] = _generated_inventory(directory, run, deadline)
        evidence['toolchain_dependency_count'] = len(dependencies['files'])
        evidence['standard_library_modules_with_Test_component'] = dependencies['standard_library_modules_with_Test_component']
        messages, audits = [], []
        try:
            for line in (directory / 'candidate/stdout.jsonl').read_text().splitlines():
                message = json.loads(line)
                if not isinstance(message, dict):
                    raise ValueError('Lean diagnostic is not an object')
                messages.append(message)
                if isinstance(message.get('data'), str):
                    try:
                        record = json.loads(message['data'])
                    except ValueError:
                        continue
                    if isinstance(record, dict) and record.get('agent_v2_audit_v1') == nonce:
                        audits.append(record)
        except (ValueError, UnicodeError):
            return _result(start, False, 'incomplete', 'partial', 'malformed_lean_output',
                           'Lean produced malformed candidate diagnostics.', evidence)
        good = (len(audits) == 1 and audits[0].get('theorem') == candidate['theorem']
                and audits[0].get('universe_parameters') == ['u']
                and isinstance(audits[0].get('axioms'), list) and set(audits[0]['axioms']) <= _AXIOMS)
        if good and sorted(audits[0].get('modules', [])) != dependencies['modules']:
            return _result(start, False, 'integrity_error', 'partial', 'import_dependency_mismatch',
                           'Actual imports differ from the fixed mathematical closure.', evidence)
        if (report['returncode'] != 0 or any(m.get('severity') == 'error' for m in messages)
                or not good or not (build / 'Candidate.olean').is_file()):
            return _result(start, False, 'incomplete', 'partial', 'lean_check_failed',
                           'The local theorem did not pass compilation and the trusted audit.', evidence,
                           report['returncode'])
        evidence.update(axioms=audits[0]['axioms'], audit=audits[0], source_dependencies=source.to_dict()['dependencies'])
        return _result(start, True, 'partial_lean_verified', 'partial', 'lean_verified',
                       'Original-context local proposition passed real Lean compilation and axiom audit.',
                       evidence, report['returncode'])
    except FileNotFoundError as error:
        evidence['artifacts'] = _generated_inventory(directory, run, float('inf'))
        return _result(start, False, 'environment_blocked', 'partial', 'lean_environment_unavailable', str(error), evidence)
    except TimeoutError as error:
        evidence['artifacts'] = _generated_inventory(directory, run, float('inf'))
        return _result(start, False, 'budget_exhausted', 'partial', 'integrity_check_timeout', str(error), evidence)
    except IntegrityError as error:
        try:
            evidence['artifacts'] = _generated_inventory(directory, run, float('inf'))
        except IntegrityError as artifact_error:
            # Never follow a rejected artifact in order to describe its failure.
            evidence['artifact_collection_error'] = str(artifact_error)
        return _result(start, False, 'integrity_error', 'partial', 'verification_input_changed', str(error), evidence)
