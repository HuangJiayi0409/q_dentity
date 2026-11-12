"""Independent, fail-closed Lean certification for the new v2 agent.

Closed Init propositions retain their small pure term language. A separate
fixed telescoping profile verifies supported Train local certificates in their
original polymorphic context. Neither path permits candidate-provided imports.
Original acceptance supports only ``init_original_template`` sources; other
source layouts remain explicitly unsupported.
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

from .storage import IntegrityError, guard_path


_CANDIDATE_THEOREM = 'AgentV2Candidate.proof'
_SHA = re.compile(r'[0-9a-f]{64}')
_NAME = re.compile(r'[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*')
_CONSTANTS = frozenset('''True False Nat Bool Prop And Or Not Iff Eq
True.intro False.elim And.intro And.left And.right Or.inl Or.inr Or.elim
Iff.intro Iff.mp Iff.mpr Eq.refl Eq.symm Eq.trans
Nat.zero Nat.succ Nat.add Nat.mul Nat.sub Bool.true Bool.false'''.split())
_TERM_WORDS = frozenset('fun forall by exact rfl intro intros constructor assumption apply left right'.split())
_TOKEN = re.compile(r'\s+|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|=>|->|[(){}:,;+*=<>]|[→∀∧∨¬↔λ]')
_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
_IMPORTS = ('Init', 'Lean.Elab.Command', 'Lean.Elab.ElabRules', 'Lean.Util.CollectAxioms')


def _safe_expression(text, *, proof):
    """Lexical allowlist closes all IO, elaborator and command escape hatches.

    This intentionally rejects many mathematically safe Lean expressions. It is
    a supported input language, not a general-purpose Lean security sandbox.
    Lean still parses, elaborates, and kernel-checks every accepted expression.
    """
    if not isinstance(text, str) or not text.strip() or len(text) > 16000:
        return False
    position = 0
    for match in _TOKEN.finditer(text):
        if match.start() != position:
            return False
        token = match.group()
        position = match.end()
        if token[0].isalpha() and token.isascii():
            if token not in _CONSTANTS and token not in ({'forall', 'fun'} | (_TERM_WORDS if proof else set())):
                # A fixed local-variable alphabet cannot name any extension,
                # reflection facility, executable command, or external module.
                if not re.fullmatch(r'[hmpqnabxyz][0-9]*', token):
                    return False
        if token.isdecimal() and len(token) > 128:
            return False
    return position == len(text)


def init_original_template(theorem, proposition):
    """Produce the only original-source format accepted by this MVP.

    The placeholder is never compiled or imported. Acceptance substitutes a
    checked term into the exact declared type under the same theorem name.
    """
    if not isinstance(theorem, str) or not _NAME.fullmatch(theorem):
        raise ValueError('invalid theorem name')
    if not _safe_expression(proposition, proof=False):
        raise ValueError('unsupported proposition syntax')
    namespace, _, short = theorem.rpartition('.')
    if namespace:
        return f'import Init\n\nnamespace {namespace}\n\ntheorem {short} : {proposition} := by\n  sorry\n\nend {namespace}\n'
    return f'import Init\n\ntheorem {theorem} : {proposition} := by\n  sorry\n'


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _artifact(path, run):
    # Never dereference a compiler-created symlink, including failed outputs.
    path = guard_path(path, run)
    return {'path': str(path), 'sha256': _sha(path.read_bytes())}


def _header_imports(text):
    # Stop at the first declaration, before strings or quoted syntax in the
    # body. Nested module doc comments and end-of-line comments are allowed.
    depth, index, line, imports = 0, 0, [], []
    while index < len(text):
        pair = text[index:index + 2]
        if pair == '/-': depth += 1; index += 2
        elif pair == '-/' and depth: depth -= 1; index += 2
        elif pair == '--' and not depth:
            end = text.find('\n', index)
            index = len(text) if end < 0 else end
        elif text[index] == '\n' and not depth:
            value = ''.join(line).strip(); line.clear(); index += 1
            if not value or value in {'module', 'prelude'}: continue
            match = re.fullmatch(r'(?:(?:public|meta)\s+)*import\s+(?:all\s+)?([A-Za-z0-9_.]+)', value)
            if match: imports.append(match.group(1))
            else: return imports
        else:
            if not depth: line.append(text[index])
            index += 1
    if depth: raise IntegrityError('unclosed standard-library header comment')
    return imports


def _standard_modules(binary):
    src = binary.parent.parent / 'src' / 'lean'
    pending, modules, sources = list(_IMPORTS), set(), set()
    while pending:
        name = pending.pop()
        if name in modules: continue
        if not _NAME.fullmatch(name) or name.split('.')[0] not in {'Init', 'Lean', 'Std'}:
            raise IntegrityError('nonstandard import in trusted driver closure')
        path = guard_path(src / (name.replace('.', '/') + '.lean'))
        imports = _header_imports(path.read_text())
        sources.add(path); modules.add(name)
        pending.extend(imports)
    return modules, sources


def _lean_environment(binary):
    return {'PATH': str(binary.parent) + ':/usr/bin:/bin',
            'LEAN_PATH': str(binary.parent.parent / 'lib' / 'lean'),
            'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8'}


def _runtime_libraries(binary, deadline):
    """Ask the fixed platform loader for actual DT_NEEDED resolution.

    ``--list`` resolves dependencies without entering the Lean program. Its
    clean environment exactly matches compilation, so RUNPATH shadows and
    loader-cache changes cannot silently evade the before/after manifest.
    """
    loader = guard_path('/lib64/ld-linux-x86-64.so.2')
    remaining = deadline - time.monotonic()
    if remaining <= 0: raise TimeoutError('runtime dependency audit exhausted the time budget')
    try:
        result = subprocess.run([str(loader), '--list', str(binary)],
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, env=_lean_environment(binary),
                                timeout=remaining, check=False)
    except subprocess.TimeoutExpired as error:
        raise TimeoutError('runtime dependency audit exhausted the time budget') from error
    if result.returncode != 0:
        raise IntegrityError('platform loader cannot resolve Lean runtime dependencies')
    paths = {loader}
    for line in result.stdout.decode('utf-8', errors='strict').splitlines():
        if 'not found' in line: raise IntegrityError('Lean runtime dependency is missing')
        match = re.search(r'(?:=>\s*)?(/[^\s]+)\s+\(0x[0-9a-f]+\)', line)
        if match: paths.add(guard_path(match.group(1)))
    if len(paths) < 2: raise IntegrityError('platform loader returned no runtime dependencies')
    return sorted(paths)


def _toolchain_manifest(binary, configuration, deadline):
    """Bind only the standard toolchain, never scan a project or benchmark.

    Lean 4.35 loads split .olean.private/.server files and .ir in addition to
    .olean. Include the fixed imports' transitive Init/Lean/Std artifacts,
    and the platform loader/runtime files. The inventory itself is compared
    after execution, detecting both changes and newly introduced files.
    """
    lib = binary.parent.parent / 'lib'
    paths = {configuration, binary}
    modules, sources = _standard_modules(binary)
    paths.update(sources)
    for module in modules:
        stem = module.replace('.', '/')
        for suffix in ('.olean', '.olean.private', '.olean.server', '.olean.sig', '.ir'):
            path = lib / 'lean' / (stem + suffix)
            if path.is_file(): paths.add(path)
            elif suffix == '.olean': raise IntegrityError('standard module artifact missing')
    runtime_libraries = _runtime_libraries(binary, deadline)
    paths.update(runtime_libraries)
    for path in (Path('/etc/ld.so.cache'), Path('/etc/ld.so.preload')):
        if path.is_file(): paths.add(path)
    records = []
    for path in sorted(paths):
        path = guard_path(path)
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            while chunk := stream.read(1024 * 1024):
                if time.monotonic() >= deadline:
                    raise TimeoutError('toolchain integrity verification exhausted the time budget')
                digest.update(chunk)
        records.append({'path': str(path), 'sha256': digest.hexdigest()})
    return {'modules': sorted(modules), 'runtime_libraries': [str(p) for p in runtime_libraries], 'files': records}


def _result(start, accepted, status, stage, code, message, evidence=None, backend=None):
    return {'schema_version': 1, 'accepted': accepted, 'status': status,
            'sigma': {'stage': stage, 'code': code, 'message': message, 'backend_status': None if backend is None else str(backend)},
            'evidence': evidence or {}, 'cost': {'wall_seconds': time.monotonic() - start, 'actions': 0}}


class LeanChecker:
    def __init__(self, repository=None, lean_binary=None):
        self.repository = Path(repository or Path(__file__).resolve().parents[1])
        self.driver = Path(__file__).resolve().parent / 'lean' / 'PartialCheck.lean'
        toolchain = self.repository / 'benchmark' / 'lean' / 'lean-toolchain'
        self.toolchain_configuration = toolchain
        try:
            version = toolchain.read_text().strip()
            if not re.fullmatch(r'leanprover/lean4:v[0-9A-Za-z.+-]+', version):
                raise ValueError('unsupported toolchain identifier')
            self.expected_binary = Path.home() / '.elan' / 'toolchains' / version.replace('/', '--').replace(':', '---') / 'bin' / 'lean'
        except (OSError, ValueError):
            self.expected_binary = None
        self.binary = Path(lean_binary) if lean_binary is not None else self.expected_binary

    def check_partial(self, candidate, context):
        start = time.monotonic()
        try:
            if not isinstance(candidate, dict) or not isinstance(context, dict):
                raise IntegrityError('candidate and context must be objects')
            required = {'id', 'proposition', 'proof_term', 'theorem', 'source_sha256', 'dependencies'}
            if not required.issubset(candidate) or set(candidate) - required - {'schema_version'}:
                raise IntegrityError('candidate schema mismatch')
            if candidate.get('schema_version', 1) != 1 or isinstance(candidate.get('schema_version'), bool):
                raise IntegrityError('candidate schema version mismatch')
            if not isinstance(candidate['id'], str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,128}', candidate['id']):
                raise IntegrityError('invalid certificate identifier')
            if candidate['theorem'] != _CANDIDATE_THEOREM:
                raise IntegrityError('candidate theorem name mismatch')
            digest = candidate['source_sha256']
            if not isinstance(digest, str) or not _SHA.fullmatch(digest) or digest != context.get('source_sha256'):
                raise IntegrityError('candidate source hash mismatch')
            if not isinstance(candidate['dependencies'], list):
                raise IntegrityError('dependency schema mismatch')
            if context.get('source') is not None:
                from .math_lean_profile import check_train_partial
                checked = check_train_partial(self, candidate, context, start)
                if checked is not None:
                    return checked
            if candidate['dependencies']:
                return _result(start, False, 'environment_blocked', 'partial', 'unsupported_dependencies',
                               'This checker requires a self-contained proof term.')
            return self._verify(candidate, context, start, original=False)
        except TimeoutError as error:
            return _result(start, False, 'budget_exhausted', 'partial', 'integrity_check_timeout', str(error))
        except (IntegrityError, TypeError, ValueError, KeyError, OSError) as error:
            return _result(start, False, 'integrity_error', 'partial', 'invalid_request', str(error))

    def accept_original(self, report, source, attempt_dir):
        start = time.monotonic()
        try:
            if not isinstance(report, dict) or not isinstance(source, dict):
                raise IntegrityError('report and source must be objects')
            required = {'identity', 'path', 'snapshot_path', 'sha256', 'theorem', 'declaration', 'Gamma'}
            if not required.issubset(source):
                raise IntegrityError('original source schema mismatch')
            if source.get('schema_version', 1) != 1:
                raise IntegrityError('source schema version mismatch')
            run = guard_path(report.get('run_dir', Path(source['snapshot_path']).parent))
            attempt = guard_path(attempt_dir, run)
            snapshot = guard_path(source['snapshot_path'], run)
            original = guard_path(source['path'])
            digest = source['sha256']
            if not isinstance(digest, str) or not _SHA.fullmatch(digest):
                raise IntegrityError('invalid original source hash')
            for path in (original, snapshot):
                if _sha(path.read_bytes()) != digest:
                    raise IntegrityError('original source or snapshot hash mismatch')
            if not isinstance(source['declaration'], str) or _sha(source['declaration'].encode()) != digest:
                raise IntegrityError('original declaration hash mismatch')
            dependencies = source.get('dependencies', [])
            if not isinstance(dependencies, (list, tuple)):
                raise IntegrityError('source dependency list malformed')
            for dependency in dependencies:
                if not isinstance(dependency, dict) or set(dependency) - {'schema_version', 'path', 'sha256'}:
                    raise IntegrityError('source dependency schema mismatch')
                if dependency.get('schema_version', 1) != 1:
                    raise IntegrityError('source dependency version mismatch')
                if _sha(guard_path(dependency['path']).read_bytes()) != dependency['sha256']:
                    raise IntegrityError('source dependency hash mismatch')
            proposition = source.get('proposition')
            # Mathematical originals are reconstructed from the frozen source
            # and a complete derivation tree, then independently compiled.
            from .math_lean_profile import check_train_original
            checked = check_train_original(self, report, source, run, attempt, start)
            if checked is not None:
                return checked
            try:
                template = init_original_template(source['theorem'], proposition)
            except (TypeError, ValueError):
                template = None
            if source['declaration'] != template:
                return _result(start, False, 'environment_blocked', 'original', 'unsupported_original_translation',
                               'Only the exact Init-only single-theorem source template is supported; original obligation remains open.')
            if source['Gamma'] not in ({}, [], '', source['declaration']):
                raise IntegrityError('original context differs from canonical empty context')
            proof = report.get('candidate', report)
            if not isinstance(proof, dict) or not isinstance(proof.get('proof_term'), str):
                raise IntegrityError('no original proof term supplied')
            if 'theorem' in proof and proof['theorem'] != source['theorem']:
                raise IntegrityError('original theorem name mismatch')
            if 'proposition' in proof and proof['proposition'] != proposition:
                raise IntegrityError('original statement mismatch')
            if 'source_sha256' in proof and proof['source_sha256'] != digest:
                raise IntegrityError('original proof source hash mismatch')
            if proof.get('dependencies', []):
                raise IntegrityError('original proof must be self-contained')
            # Supplied artifacts/logs/acceptance flags are not verification
            # inputs. If paths are supplied, refuse escapes before any read.
            for artifact in report.get('artifacts', []):
                guard_path(artifact['path'], run)
            candidate = {'id': 'original', 'proposition': proposition, 'proof_term': proof['proof_term'],
                         'theorem': source['theorem'], 'source_sha256': digest, 'dependencies': []}
            context = {'run_dir': str(run), 'attempt_dir': str(attempt),
                       'seconds': report.get('seconds', 30.0), 'source_sha256': digest}
            result = self._verify(candidate, context, start, original=True)
            if result['accepted']:
                # Recheck originals and dependencies after Lean to detect edits
                # during verification; accepted evidence describes this exact view.
                for path in (original, snapshot):
                    if _sha(path.read_bytes()) != digest:
                        raise IntegrityError('original changed during Lean verification')
                for dep in dependencies:
                    if _sha(guard_path(dep['path']).read_bytes()) != dep['sha256']:
                        raise IntegrityError('source dependency changed during Lean verification')
                result['evidence']['source_dependencies'] = dependencies
                result['evidence']['original_path'] = str(original)
                result['evidence']['snapshot_path'] = str(snapshot)
            return result
        except TimeoutError as error:
            return _result(start, False, 'budget_exhausted', 'original', 'integrity_check_timeout', str(error))
        except (IntegrityError, TypeError, ValueError, KeyError, OSError) as error:
            return _result(start, False, 'integrity_error', 'original', 'invalid_original', str(error))

    def _verify(self, candidate, context, start, *, original):
        stage = 'original' if original else 'partial'
        seconds = context.get('seconds')
        if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds):
            raise IntegrityError('finite numerical seconds budget required')
        remaining = seconds - (time.monotonic() - start)
        if remaining <= 0:
            return _result(start, False, 'budget_exhausted', stage, 'budget_exhausted', 'No verification time remains.')
        run = guard_path(context['run_dir'])
        attempt = guard_path(context['attempt_dir'], run)
        if not run.is_dir():
            raise IntegrityError('run directory must exist')
        if not _safe_expression(candidate['proof_term'], proof=True) or not _safe_expression(candidate['proposition'], proof=False):
            return _result(start, False, 'incomplete', stage, 'unsupported_term_syntax',
                           'Expression is outside the closed Init proof language; no Lean code was executed.')
        binary = self.binary
        if (binary is None or self.expected_binary is None or not binary.is_file()
                or binary.resolve() != self.expected_binary.resolve() or not os.access(binary, os.X_OK)
                or not self.driver.is_file()):
            return _result(start, False, 'environment_blocked', stage, 'lean_environment_unavailable',
                           'The configured project Lean toolchain or trusted driver is unavailable.')
        binary_digest = _sha(binary.read_bytes())
        integrity_start = time.monotonic()
        dependencies = _toolchain_manifest(binary, self.toolchain_configuration, start + seconds)
        integrity_seconds = time.monotonic() - integrity_start
        driver_bytes = self.driver.read_bytes()
        directory = guard_path(attempt / ('lean-' + uuid.uuid4().hex), run)
        directory.mkdir(parents=True)
        nonce = uuid.uuid4().hex
        namespace, _, short = candidate['theorem'].rpartition('.')
        declaration = f'theorem {short or candidate["theorem"]} : ({candidate["proposition"]}) := {candidate["proof_term"]}\n'
        if namespace:
            declaration = f'namespace {namespace}\n' + declaration + f'end {namespace}\n'
        code = (driver_bytes.decode() + '\n' + declaration
                + f'def AgentV2Expected : Prop := ({candidate["proposition"]})\n'
                + f'agent_v2_audit {candidate["theorem"]} against AgentV2Expected nonce "{nonce}"\n')
        source_path = directory / 'Candidate.lean'; source_path.write_text(code)
        driver_path = directory / 'TrustedDriver.lean'; driver_path.write_bytes(driver_bytes)
        request_path = directory / 'request.json'
        request_path.write_text(json.dumps(candidate, ensure_ascii=False, sort_keys=True) + '\n')
        olean = directory / 'Candidate.olean'
        stdout_path = directory / 'stdout.jsonl'; stderr_path = directory / 'stderr.txt'
        source_digest = _sha(source_path.read_bytes())
        env = _lean_environment(binary)
        timed_out = False
        remaining = seconds - (time.monotonic() - start)
        if remaining <= 0:
            return _result(start, False, 'budget_exhausted', stage, 'budget_exhausted', 'Verification setup exhausted the budget.')
        try:
            with stdout_path.open('wb') as out, stderr_path.open('wb') as err:
                process = subprocess.Popen([str(binary), '-j', '1', '--json', '-o', str(olean), str(source_path)],
                                           cwd=directory, env=env, stdout=out, stderr=err, start_new_session=True)
                try:
                    process.wait(timeout=remaining)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
        except OSError as error:
            return _result(start, False, 'environment_blocked', stage, 'lean_start_failed', str(error))
        paths = [source_path, driver_path, request_path, stdout_path, stderr_path]
        # Check containment before is_file/read_text/hash follows any output.
        for path in [*paths, olean]: guard_path(path, run)
        if olean.is_file(): paths.append(olean)
        evidence = {key: candidate[key] for key in ('proposition', 'proof_term', 'theorem', 'source_sha256', 'dependencies')}
        evidence.update(certificate_id=candidate['id'], artifacts=[_artifact(p, run) for p in paths],
                        lean_binary=str(binary), lean_binary_sha256=binary_digest,
                        driver_sha256=_sha(driver_bytes), returncode=process.returncode)
        if _sha(binary.read_bytes()) != binary_digest or _sha(source_path.read_bytes()) != source_digest or self.driver.read_bytes() != driver_bytes:
            return _result(start, False, 'integrity_error', stage, 'verification_input_changed',
                           'Verification inputs changed during execution.', evidence)
        if timed_out:
            return _result(start, False, 'budget_exhausted', stage, 'lean_timeout', 'Lean exceeded the remaining wall-clock budget.', evidence, 'timeout')
        integrity_start = time.monotonic()
        if dependencies != _toolchain_manifest(binary, self.toolchain_configuration, start + seconds):
            return _result(start, False, 'integrity_error', stage, 'toolchain_dependency_changed',
                           'Lean toolchain configuration or imported/runtime dependencies changed.', evidence)
        dependency_path = directory / 'toolchain_dependencies.json'
        dependency_path.write_text(json.dumps(dependencies, sort_keys=True) + '\n')
        evidence['toolchain_manifest'] = _artifact(dependency_path, run)
        evidence['toolchain_dependency_count'] = len(dependencies['files'])
        evidence['integrity_wall_seconds'] = integrity_seconds + time.monotonic() - integrity_start
        evidence['artifacts'].append(evidence['toolchain_manifest'])
        records = []
        messages = []
        try:
            for line in stdout_path.read_text().splitlines():
                message = json.loads(line)
                if not isinstance(message, dict): raise ValueError('diagnostic must be an object')
                messages.append(message)
                data = message.get('data')
                if isinstance(data, str):
                    try: record = json.loads(data)
                    except ValueError: continue
                    if isinstance(record, dict) and record.get('agent_v2_audit_v1') == nonce:
                        records.append(record)
        except (ValueError, UnicodeError):
            return _result(start, False, 'incomplete', stage, 'malformed_lean_output', 'Lean produced malformed diagnostics.', evidence, process.returncode)
        good_audit = (len(records) == 1 and records[0].get('theorem') == candidate['theorem']
                      and isinstance(records[0].get('axioms'), list) and set(records[0]['axioms']) <= _AXIOMS)
        if good_audit and sorted(records[0].get('modules', [])) != dependencies['modules']:
            return _result(start, False, 'integrity_error', stage, 'import_dependency_mismatch',
                           'Actual Lean imports differ from the frozen standard-library closure.', evidence)
        if process.returncode != 0 or any(m.get('severity') == 'error' for m in messages) or not good_audit or not olean.is_file():
            return _result(start, False, 'incomplete', stage, 'lean_check_failed',
                           'The exact theorem did not pass Lean compilation and trusted axiom audit.', evidence, process.returncode)
        evidence['axioms'] = records[0]['axioms']
        evidence['audit'] = records[0]
        return _result(start, True, 'original_theorem_proved' if original else 'partial_lean_verified',
                       stage, 'lean_verified', 'Exact closed proposition and proof passed Lean and axiom audit.', evidence, process.returncode)


def check_partial(candidate, context):
    return LeanChecker().check_partial(candidate, context)


def accept_original(report, source, attempt_dir):
    return LeanChecker().accept_original(report, source, attempt_dir)
