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


def _check_certificate_binding(certificate, run):
    """Bind dependency claims to their exact retained verification artifacts.

    These receipts only describe provenance. A self-contained proof containing
    every used dependency is compiled again below; no receipt proves a theorem.
    """
    from .lean_checker import _AXIOMS
    from .models import thaw
    evidence = thaw(certificate.evidence)
    expected = {'certificate_id': certificate.id, 'proposition': certificate.proposition,
                'proof_term': certificate.proof_term, 'source_sha256': certificate.source_sha256,
                'dependencies': list(certificate.dependencies), 'theorem': 'AgentV2Candidate.proof'}
    if any(evidence.get(key) != value for key, value in expected.items()):
        raise IntegrityError('certificate receipt differs from its source, proposition, proof or dependencies')
    audit = evidence.get('audit', {})
    if (not isinstance(audit, dict) or evidence.get('profile') != PROFILE
            or type(evidence.get('returncode')) is not int or evidence['returncode'] != 0
            or audit.get('theorem') != expected['theorem']
            or audit.get('universe_parameters') != ['u']
            or not isinstance(audit.get('axioms'), list) or not set(audit['axioms']) <= _AXIOMS):
        raise IntegrityError('certificate has no bound mathematical Lean audit')
    artifacts = evidence.get('artifacts')
    if not isinstance(artifacts, list) or not artifacts:
        raise IntegrityError('certificate has no retained verification artifacts')
    seen = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict) or set(artifact) - {'schema_version', 'path', 'sha256'}:
            raise IntegrityError('malformed certificate artifact')
        target = guard_path(artifact['path'], run)
        if target in seen or _hash(target, float('inf')) != artifact.get('sha256'):
            raise IntegrityError('certificate artifact hash mismatch or duplicate')
        seen.add(target)
    if not any(p.name == 'Candidate.olean' for p in seen) or not any(p.name == 'Candidate.lean' for p in seen):
        raise IntegrityError('certificate has no fresh compiled candidate artifacts')


def _partial_template(frontend, candidate, context):
    """Reconstruct one supported proposition and its explicit dependency set."""
    from .telescoping_translation import local_proof
    from .models import VerifiedCertificate
    if candidate['proposition'] == frontend['local_proposition']:
        if candidate['dependencies']:
            raise IntegrityError('local difference proof has unexpected dependencies')
        return local_proof(frontend)
    from .telescoping_closure import closure_blueprint, make_closure_candidate
    blueprint = closure_blueprint(frontend)
    targets = {'bridge': blueprint['bridge_proposition']}
    for task, obligation in zip(('zero_endpoint', 'upper_endpoint'), blueprint['obligations']):
        targets[task] = obligation['proposition']
    task = next((task for task, proposition in targets.items() if proposition == candidate['proposition']), None)
    if task is None:
        return None
    required = [blueprint['local_id']] if task == 'bridge' else []
    if candidate['dependencies'] != required:
        raise IntegrityError('candidate dependency set differs from the reconstructed proof dependencies')
    approved = context.get('approved_certificates', {})
    if not isinstance(approved, dict):
        raise IntegrityError('approved certificate context must be an object')
    bound = {}
    for identity in required:
        if identity not in approved:
            raise IntegrityError('required checked certificate is missing: ' + identity)
        cert = VerifiedCertificate.from_dict(approved[identity])
        if (cert.id != identity or cert.source_sha256 != frontend['source']['sha256']
                or cert.proposition != frontend['local_proposition']
                or cert.proof_term != local_proof(frontend) or cert.dependencies):
            raise IntegrityError('dependency is not the exact source-bound local difference certificate')
        _check_certificate_binding(cert, guard_path(context['run_dir']))
        bound[identity] = cert.to_dict()
    generated = make_closure_candidate(frontend, task, bound, 'checker-template')
    if list(generated.dependencies) != required or generated.proposition != candidate['proposition']:
        raise IntegrityError('closure generator and independently reconstructed target disagree')
    return generated.proof_term


def check_train_partial(checker, candidate, context, start):
    """Return None for non-profile sources, otherwise a strict checker result."""
    from .formal_frontend import analyze_source
    from .lean_checker import _result
    source = Source.from_dict(context['source'])
    run = guard_path(context['run_dir'])
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
    template = _partial_template(frontend, candidate, context)
    if template is None:
        return _result(start, False, 'integrity_error', 'partial', 'proposition_binding_mismatch',
                       'Candidate proposition differs from independently reconstructed local and closure targets.')
    if candidate['proof_term'] not in (template, 'by rfl', 'by exact True.intro'):
        return _result(start, False, 'incomplete', 'partial', 'unsupported_term_syntax',
                       'Only fixed telescoping proof templates and pure negative-test terms are accepted.')
    return _verify_train(checker, candidate, context, start, source, frontend, candidate['proposition'])


def _original_declaration(source, frontend):
    """Replace only the parsed proof token; preserve original declaration bytes.

    Comments are masked without changing offsets, so a comment containing
    `sorry` or `import` cannot select a replacement location. Source grammar is
    fully checked by the caller before this renderer is used.
    """
    from .formal_frontend import _TOKEN
    text = source.declaration
    clean, i, depth = list(text), 0, 0
    while i < len(text):
        pair = text[i:i+2]
        if pair == '/-':
            depth += 1; clean[i:i+2] = '  '; i += 2
        elif depth and pair == '-/':
            depth -= 1; clean[i:i+2] = '  '; i += 2
        elif not depth and pair == '--':
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            clean[i:end] = ' ' * (end-i); i = end
        else:
            if depth and clean[i] != '\n': clean[i] = ' '
            i += 1
    if depth:
        raise IntegrityError('unterminated comment in frozen source')
    tokens = [match for match in _TOKEN.finditer(''.join(clean)) if not match.group().isspace()]
    replacements = []
    for index, token in enumerate(tokens):
        if token.group() == 'import':
            end = tokens[index+1].end()
            if text[end:end+1] == '\n': end += 1
            replacements.append((token.start(), end, ''))
    sorry = [token for token in tokens if token.group() == 'sorry']
    if len(sorry) != 1 or [token.group() for token in tokens[-5:]] != [':=', 'by', 'sorry', 'end', source.theorem.rpartition('.')[0]]:
        raise IntegrityError('original declaration has no unique parsed proof placeholder')
    arguments = ' '.join(binder['name'] for binder in frontend['binders'] if binder['kind'] == 'explicit')
    replacements.append((sorry[0].start(), sorry[0].end(), 'exact _root_.AgentV2Assembled ' + arguments))
    for left, right, replacement in sorted(replacements, reverse=True):
        text = text[:left] + replacement + text[right:]
    return text


def check_train_original(checker, report, source_data, run, attempt, start):
    from .formal_frontend import analyze_source, _Parser, _Unsupported
    from .executor import assemble_term, validate_invariant
    from .models import ResidualState
    # Init and unknown source languages retain their existing final-check path.
    try:
        _Parser(source_data['declaration']).source()
    except _Unsupported:
        return None
    source = Source.from_dict(dict(source_data, schema_version=1))
    frontend = analyze_source(source.to_dict(), run)
    if frontend.get('status') != 'applicable':
        return None
    if source.proposition != frontend['original_proposition']:
        raise IntegrityError('original proposition is not the frozen source proposition')
    state = ResidualState.from_dict(report.get('state'))
    if state.G != source or state.Gamma != source.declaration:
        raise IntegrityError('final state source or original context differs from frozen source')
    validate_invariant(state)
    term = assemble_term(state)
    proof = report.get('candidate', report)
    if (not isinstance(proof, dict) or proof.get('proof_term') != term
            or proof.get('theorem', source.theorem) != source.theorem
            or proof.get('proposition', source.proposition) != source.proposition
            or proof.get('source_sha256', source.sha256) != source.sha256
            or proof.get('dependencies', [])):
        raise IntegrityError('final proof differs from the complete bound proof tree or original target')
    context = {'run_dir': str(run), 'attempt_dir': str(attempt), 'source_sha256': source.sha256,
               'source': source.to_dict(), 'seconds': report.get('seconds', 30.0), 'approved_certificates': {}}
    # Validate all retained dependencies in topological order. The following
    # compilation then rechecks their inline terms without trusting receipts.
    for cert in state.C:
        request = {'id': cert.id, 'proposition': cert.proposition, 'proof_term': cert.proof_term,
                   'theorem': 'AgentV2Candidate.proof', 'source_sha256': cert.source_sha256,
                   'dependencies': list(cert.dependencies)}
        if _partial_template(frontend, request, context) != cert.proof_term:
            raise IntegrityError('final proof tree contains an uncontrolled proof template')
        _check_certificate_binding(cert, run)
        context['approved_certificates'][cert.id] = cert.to_dict()
    candidate = {'id': 'original', 'proposition': source.proposition, 'proof_term': term,
                 'theorem': source.theorem, 'source_sha256': source.sha256, 'dependencies': []}
    return _verify_train(checker, candidate, context, start, source, frontend,
                         frontend['original_proposition'], original=True)


def _verify_train(checker, candidate, context, start, source, frontend, expected, *, original=False,
                  additional_rules=(), profile=PROFILE):
    from .lean_checker import _AXIOMS, _IMPORTS, _header_imports, _lean_environment, _result
    run = guard_path(context['run_dir'])
    attempt = guard_path(context['attempt_dir'], run)
    stage = 'original' if original else 'partial'
    seconds = context.get('seconds')
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds):
        raise IntegrityError('finite numerical seconds budget required')
    deadline = start + seconds
    if time.monotonic() >= deadline:
        return _result(start, False, 'budget_exhausted', stage, 'budget_exhausted',
                       'No verification time remains.')
    binary = checker.binary
    driver = guard_path(Path(__file__).parent / 'lean' / ('OriginalTrainCheck.lean' if original else 'TelescopingCheck.lean'))
    rules = guard_path(checker.repository / 'finite_product_framework/p1/lean/GaussianRules.lean')
    if (binary is None or checker.expected_binary is None or not binary.is_file()
            or binary.resolve() != checker.expected_binary.resolve() or not os.access(binary, os.X_OK)
            or not driver.is_file() or not rules.is_file()):
        return _result(start, False, 'environment_blocked', stage, 'lean_environment_unavailable',
                       'The fixed Lean toolchain, trusted driver or mathematical foundation is unavailable.')
    directory = guard_path(attempt / ('lean-telescoping-' + uuid.uuid4().hex), run)
    directory.mkdir(parents=True)
    evidence = {key: candidate[key] for key in
                ('proposition', 'proof_term', 'theorem', 'source_sha256', 'dependencies')}
    evidence.update(certificate_id=candidate['id'], profile=profile, artifacts=[])
    try:
        packages, package_manifest = _package_roots(checker.repository)
        extra_paths = tuple(guard_path(path) for path in additional_rules)
        driver_text = driver.read_text()
        rule_texts = [path.read_text() for path in (rules, *extra_paths)]
        rules_text = '\n'.join(rule_texts)
        imports = tuple(dict.fromkeys((*_IMPORTS, *(name for text in rule_texts
                                                   for name in _header_imports(text)))))
        fixed_paths = (driver, rules, *extra_paths, package_manifest, checker.repository / 'project/lakefile.toml',
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
                return _result(start, False, 'integrity_error', stage, 'external_environment_changed',
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
                return _result(start, False, 'budget_exhausted', stage, 'lean_timeout',
                               'Lean dependency compilation exceeded the remaining budget.', evidence)
            if report['environment_error'] or report['returncode'] != 0:
                evidence['artifacts'] = _generated_inventory(directory, run, deadline)
                return _result(start, False, 'environment_blocked', stage, 'lean_dependency_compile_failed',
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
        declaration = (f'theorem AgentV2Assembled : ({expected}) := {candidate["proof_term"]}\n'
                       + _original_declaration(source, frontend)) if original else (
                       f'theorem {candidate["theorem"]} : ({candidate["proposition"]}) := {candidate["proof_term"]}\n')
        command = 'agent_v2_original_train_audit' if original else 'agent_v2_telescoping_audit'
        code = ('\n'.join('import ' + name for name in imports) + '\n'
                + without_imports(rules_text) + '\n' + without_imports(driver_text)
                + '\nopen scoped BigOperators\nuniverse u\n' + declaration
                + f'\ndef AgentV2Expected : Prop := ({expected})\n'
                + f'{command} {candidate["theorem"]} against AgentV2Expected nonce "{nonce}"\n')
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
            return _result(start, False, 'budget_exhausted', stage, 'lean_timeout',
                           'Lean candidate verification exceeded the remaining budget.', evidence)
        if report['environment_error']:
            evidence['artifacts'] = _generated_inventory(directory, run, deadline)
            return _result(start, False, 'environment_blocked', stage, 'lean_start_failed',
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
            return _result(start, False, 'incomplete', stage, 'malformed_lean_output',
                           'Lean produced malformed candidate diagnostics.', evidence)
        good = (len(audits) == 1 and audits[0].get('theorem') == candidate['theorem']
                and (audits[0].get('universe_parameter_count') == 1 if original else
                     audits[0].get('universe_parameters') == ['u'])
                and isinstance(audits[0].get('axioms'), list) and set(audits[0]['axioms']) <= _AXIOMS)
        if good and sorted(audits[0].get('modules', [])) != dependencies['modules']:
            return _result(start, False, 'integrity_error', stage, 'import_dependency_mismatch',
                           'Actual imports differ from the fixed mathematical closure.', evidence)
        if (report['returncode'] != 0 or any(m.get('severity') == 'error' for m in messages)
                or not good or not (build / 'Candidate.olean').is_file()):
            return _result(start, False, 'incomplete', stage, 'lean_check_failed',
                           'The local theorem did not pass compilation and the trusted audit.', evidence,
                           report['returncode'])
        evidence.update(axioms=audits[0]['axioms'], audit=audits[0], source_dependencies=source.to_dict()['dependencies'])
        return _result(start, True, 'original_theorem_proved' if original else 'partial_lean_verified', stage, 'lean_verified',
                       'Frozen original theorem passed independent Lean compilation and axiom audit.' if original else
                       'Original-context local proposition passed real Lean compilation and axiom audit.',
                       evidence, report['returncode'])
    except FileNotFoundError as error:
        evidence['artifacts'] = _generated_inventory(directory, run, float('inf'))
        return _result(start, False, 'environment_blocked', stage, 'lean_environment_unavailable', str(error), evidence)
    except TimeoutError as error:
        evidence['artifacts'] = _generated_inventory(directory, run, float('inf'))
        return _result(start, False, 'budget_exhausted', stage, 'integrity_check_timeout', str(error), evidence)
    except IntegrityError as error:
        try:
            evidence['artifacts'] = _generated_inventory(directory, run, float('inf'))
        except IntegrityError as artifact_error:
            # Never follow a rejected artifact in order to describe its failure.
            evidence['artifact_collection_error'] = str(artifact_error)
        return _result(start, False, 'integrity_error', stage, 'verification_input_changed', str(error), evidence)
