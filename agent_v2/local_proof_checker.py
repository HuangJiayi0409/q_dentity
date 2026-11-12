"""Generated local proofs share the production mathematical transaction.

The task registry is application-owned. Untrusted requests can select neither
imports nor drivers. CAS templates and generated terms use one per-Source
environment, strict production receipts, fresh compilation, and exact assembly.
"""
from dataclasses import replace
import json
import math
from pathlib import Path
import re
import time
from types import MappingProxyType

from .lean_checker import LeanChecker, _result, init_original_template
from .local_tasks import LocalTask, candidate_for, certificate_binding, dependency_name
from .models import Source, ResidualState, VerifiedCertificate, thaw
from .proof_profiles import BoundProfile, ProofProfile, PropositionBindingError
from .storage import IntegrityError, guard_path, verify_source


_FORBIDDEN = frozenset('''sorry admit axiom opaque unsafe partial import namespace end
section variable variables universe universes theorem def abbrev instance class structure
inductive mutual initialize builtin_initialize deriving syntax macro macro_rules elab elab_rules
run_tac run_elab run_meta by_elab elab_as_elim native_decide eval decide_cbv
set_option attribute open export include omit local scoped in termination_by decreasing_by
implemented_by extern unsafeCast ofReduceBool trustCompiler'''.split())


class GeneratedSyntaxError(ValueError):
    """An unsupported model proposal, not corruption of accepted state."""


def _safe_input(text):
    """Cheap rejection before creating any files; Lean does the real parsing.

    Quotes, comments and quotation syntax are unnecessary for mathematical
    propositions/proofs here. In particular no term elaborator code is allowed.
    """
    if not isinstance(text, str) or not text.strip() or len(text) > 64000:
        raise GeneratedSyntaxError('empty or oversized generated Lean term')
    if any(token in text for token in ('"', '`', '--', '/-', '-/', '$', '#', '\x00')):
        raise GeneratedSyntaxError('generated Lean term contains command, comment or quotation syntax')
    words = re.findall(r'[A-Za-z_][A-Za-z_0-9]*', text)
    if any(word in _FORBIDDEN or word.startswith(('run_', 'eval_', 'native_')) for word in words):
        raise GeneratedSyntaxError('generated Lean term contains unsupported executable or command syntax')


class _LocalProfile(ProofProfile):
    def matches_universes(self, audit, *, original=False):
        if original:
            return super().matches_universes(audit, original=True)
        # Independent closed lemmas may use fewer levels than the original;
        # the trusted driver compares to that exact independently bound type.
        names = audit.get('universe_parameters') if isinstance(audit, dict) else None
        return isinstance(names, list) and (names == [] or names == list(self.universe_parameters))


class LocalLeanChecker(LeanChecker):
    def __init__(self, repository=None, lean_binary=None, *, tasks=()):
        super().__init__(repository, lean_binary)
        self._tasks = {}
        values = tasks.values() if hasattr(tasks, 'values') else tasks
        for task in values:
            self.register_task(task)

    @property
    def tasks(self):
        return MappingProxyType(self._tasks)

    def register_task(self, task):
        task = task if isinstance(task, LocalTask) else LocalTask.from_dict(task)
        # Always reconstruct the immutable contract, even if a caller bypassed
        # ordinary dataclass construction via object.__setattr__.
        task = LocalTask.from_dict(task.to_dict())
        if task.id in self._tasks and self._tasks[task.id] != task:
            raise IntegrityError('registered task identity cannot change')
        _safe_input(task.proposition)
        self._tasks[task.id] = task
        return task

    def _bound(self, source, run):
        from .proof_profiles import registered_profiles, reconstruct_bound_candidate
        verify_source(source, run)
        if source.Gamma != source.declaration:
            raise IntegrityError('original context differs from frozen declaration')
        matches = []
        for profile in registered_profiles():
            frontend = profile.analyze_source(source.to_dict(), run)
            if frontend.get('status') == 'applicable':
                if frontend.get('source') != source.to_dict() or frontend.get('original_proposition') != source.proposition:
                    raise IntegrityError('formal Source reconstruction differs from exact original')
                matches.append(BoundProfile(profile, source, frontend))
        if matches:
            # Equivalent capabilities do not make the Source ambiguous. This
            # fixed registration order chooses the environment deterministically.
            if len({b.frontend['original_proposition'] for b in matches}) != 1:
                raise IntegrityError('conflicting formal meanings for original Source')
            base = matches[0]
            frontend = base.frontend
            foundations = tuple(dict.fromkeys(name for b in matches for name in b.profile.foundations))
            rules = tuple(dict.fromkeys(name for b in matches for name in b.profile.rules))
            universes = base.profile.universe_parameters
            if any(b.profile.universe_parameters != universes for b in matches):
                raise IntegrityError('conflicting original universe parameters')
            identity = '+'.join(b.profile.id for b in matches)
        else:
            try:
                template = init_original_template(source.theorem, source.proposition)
            except (ValueError, TypeError):
                template = None
            if source.declaration != template:
                raise IntegrityError('Source has no implemented formal original translation')
            frontend = {'source': source.to_dict(), 'original_proposition': source.proposition, 'binders': []}
            foundations, rules, universes, identity = (), ('agent_v2/lean/PartialCheck.lean',), (), 'init'

        def reconstruct(front, request, approved):
            task = self._tasks.get(request['id'])
            if task is not None:
                if task.source != source:
                    raise IntegrityError('registered local task belongs to a different Source or context')
                for key in task.dependencies:
                    if key not in approved:
                        raise IntegrityError('required checked certificate is missing: ' + key)
                    certificate = VerifiedCertificate.from_dict(approved[key])
                    if certificate.id != key or certificate_binding(certificate) != task.dependency_bindings[key]:
                        raise IntegrityError('local task checked dependency changed')
                _safe_input(request['proof_term'])
                return candidate_for(task, request['proof_term'])
            for possible in matches:
                try:
                    return reconstruct_bound_candidate(possible, request, approved, allow_negative=True)
                except (PropositionBindingError, ValueError):
                    continue
            raise IntegrityError('candidate is neither a registered local task nor a bound CAS template')

        profile = _LocalProfile('generated_local_v1+' + identity, '1', 'local', lambda *_: frontend,
            reconstruct, foundations, rules, partial_driver='LocalProofCheck.lean', original_driver='LocalProofCheck.lean',
            partial_command='agent_v2_local_audit', original_command='agent_v2_local_audit', universe_parameters=universes)
        return BoundProfile(profile, source, frontend)

    def _renderer(self, approved, used_dependencies):
        def declaration(name, proposition, proof, *, generated):
            command = 'agent_v2_local_declaration' if generated else 'agent_v2_local_assembled'
            return f'{command} {name} {json.dumps(proposition, ensure_ascii=False)} {json.dumps(proof, ensure_ascii=False)}\n'

        # Resolve only declared ancestors. Extra approved entries never become
        # invisible premises, and aliases cannot smuggle in unlisted proofs.
        ordered, active, seen = [], set(), set()
        def visit(identity):
            if identity in active: raise IntegrityError('cyclic local proof dependencies')
            if identity in seen: return
            if identity not in approved: raise IntegrityError('required checked certificate is missing: ' + identity)
            active.add(identity)
            cert = VerifiedCertificate.from_dict(approved[identity])
            for child in cert.dependencies: visit(child)
            ordered.append(cert); active.remove(identity); seen.add(identity)
        for identity in used_dependencies: visit(identity)

        def render(candidate, expected, source, frontend, original):
            from .math_lean_profile import _original_declaration
            code = ''.join(declaration(dependency_name(cert.id), cert.proposition, cert.proof_term,
                generated=cert.id in self._tasks) for cert in ordered)
            if original:
                code += declaration('AgentV2Assembled', expected, candidate['proof_term'], generated=False)
                code += _original_declaration(source, frontend)
            else:
                code += declaration(candidate['theorem'], candidate['proposition'], candidate['proof_term'],
                                    generated=candidate['id'] in self._tasks)
            return code, '\nagent_v2_local_expected ' + json.dumps(expected, ensure_ascii=False) + '\n'
        return render

    def check_partial(self, candidate, context):
        start = time.monotonic()
        try:
            from .math_lean_profile import _verify_train
            from .proof_profiles import reconstruct_bound_candidate, check_required_certificates
            required = {'id', 'proposition', 'proof_term', 'theorem', 'source_sha256', 'dependencies'}
            if not isinstance(candidate, dict) or set(candidate) - required - {'schema_version'} or not required <= set(candidate):
                raise IntegrityError('candidate schema mismatch')
            if type(candidate.get('schema_version', 1)) is not int or candidate.get('schema_version', 1) != 1:
                raise IntegrityError('candidate schema version mismatch')
            if 'source' not in context:
                if candidate['id'] in self._tasks:
                    raise IntegrityError('registered local task requires its exact Source context')
                return super().check_partial(candidate, context)
            source = Source.from_dict(context['source'])
            if source.sha256 != context.get('source_sha256') or candidate['source_sha256'] != source.sha256:
                raise IntegrityError('candidate source binding mismatch')
            run = guard_path(context['run_dir']); guard_path(context['attempt_dir'], run)
            bound = self._bound(source, run)
            approved = context.get('approved_certificates', {})
            rebuilt = reconstruct_bound_candidate(bound, candidate, approved, allow_negative=True)
            seconds = context.get('seconds')
            if type(seconds) not in (float, int) or not math.isfinite(seconds):
                raise IntegrityError('finite numerical seconds required')
            check_required_certificates(bound, rebuilt, approved, run, deadline=start + seconds)
            return _verify_train(self, candidate, context, start, source, bound.frontend, rebuilt.proposition,
                bound=bound, declaration_renderer=self._renderer(approved, candidate['dependencies']),
                open_scopes=('BigOperators',) if bound.profile.foundations else ())
        except TimeoutError as error:
            return _result(start, False, 'budget_exhausted', 'partial', 'integrity_check_timeout', str(error))
        except GeneratedSyntaxError as error:
            return _result(start, False, 'incomplete', 'partial', 'unsupported_term_syntax', str(error))
        except IntegrityError as error:
            return _result(start, False, 'integrity_error', 'partial', 'invalid_request', str(error))
        except (ValueError, TypeError, KeyError, OSError) as error:
            return _result(start, False, 'integrity_error', 'partial', 'unsupported_term_syntax', str(error))

    def accept_original(self, report, source, attempt_dir):
        start = time.monotonic()
        try:
            from .executor import assemble_term, validate_invariant
            from .math_lean_profile import _verify_train
            from .proof_profiles import check_certificate_binding
            source = Source.from_dict(source)
            run = guard_path(report.get('run_dir', Path(source.snapshot_path).parent))
            attempt = guard_path(attempt_dir, run)
            bound = self._bound(source, run)
            state = ResidualState.from_dict(report['state'])
            if state.G != source or state.Gamma != source.Gamma:
                raise IntegrityError('final state original Source or context differs')
            validate_invariant(state)
            term = assemble_term(state)
            proof = report.get('candidate', report)
            if (proof.get('proof_term') != term or proof.get('theorem', source.theorem) != source.theorem
                or proof.get('proposition', source.proposition) != source.proposition
                or proof.get('source_sha256', source.sha256) != source.sha256 or proof.get('dependencies', [])):
                raise IntegrityError('final proof differs from exact original bound proof tree')
            seconds = report.get('seconds', 30.0)
            if type(seconds) not in (float, int) or not math.isfinite(seconds):
                raise IntegrityError('finite numerical seconds required')
            approved = {}
            for cert in state.C:
                check_certificate_binding(cert, bound, run, approved, deadline=start + seconds)
                approved[cert.id] = cert.to_dict()
            candidate = {'id': 'original', 'proposition': source.proposition, 'proof_term': term,
                'theorem': source.theorem, 'source_sha256': source.sha256, 'dependencies': []}
            context = {'source': source.to_dict(), 'source_sha256': source.sha256, 'run_dir': str(run),
                'attempt_dir': str(attempt), 'seconds': seconds, 'approved_certificates': approved}
            return _verify_train(self, candidate, context, start, source, bound.frontend, source.proposition,
                original=True, bound=bound, declaration_renderer=self._renderer(approved, tuple(approved)),
                open_scopes=('BigOperators',) if bound.profile.foundations else ())
        except TimeoutError as error:
            return _result(start, False, 'budget_exhausted', 'original', 'integrity_check_timeout', str(error))
        except (ValueError, TypeError, KeyError, OSError) as error:
            return _result(start, False, 'integrity_error', 'original', 'invalid_original', str(error))
