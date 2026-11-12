"""Closed mathematical profiles selected only by reconstructing frozen Source.

Receipts bind provenance; all accepted terms still pass the production Lean
transaction. There is no candidate-selected import, driver or profile registry.
"""
from dataclasses import dataclass
import json
import time
from typing import Callable

from .models import Candidate, Source, VerifiedCertificate, thaw
from .storage import IntegrityError, guard_path, verify_source


class PropositionBindingError(IntegrityError):
    pass


@dataclass(frozen=True)
class ProofProfile:
    id: str
    version: str
    method: str
    analyze_source: Callable
    reconstruct_candidate: Callable
    foundations: tuple[str, ...]
    rules: tuple[str, ...]
    partial_driver: str = 'TelescopingCheck.lean'
    original_driver: str = 'OriginalTrainCheck.lean'
    partial_command: str = 'agent_v2_telescoping_audit'
    original_command: str = 'agent_v2_original_train_audit'
    universe_parameters: tuple[str, ...] = ('u',)

    def matches_universes(self, audit, *, original=False):
        """The trusted Source profile fixes arity; an original may rename levels."""
        if not isinstance(audit, dict):
            return False
        names = audit.get('universe_parameters')
        if not original:
            return names == list(self.universe_parameters)
        return (type(audit.get('universe_parameter_count')) is int
                and audit['universe_parameter_count'] == len(self.universe_parameters)
                and isinstance(names, list) and len(names) == len(self.universe_parameters)
                and all(isinstance(name, str) and name for name in names)
                and len(set(names)) == len(names))


@dataclass(frozen=True)
class BoundProfile:
    profile: ProofProfile
    source: Source
    frontend: dict


def _telescoping_candidate(frontend, request, approved):
    from .telescoping_translation import local_proof
    from .telescoping_closure import closure_blueprint, make_closure_candidate
    plan = closure_blueprint(frontend)
    if request['proposition'] == frontend['local_proposition']:
        # The single pre-existing direct-check alias is retained for compatibility.
        # It is not accepted by the source-derived closure dependency contract.
        identity = ('telescoping_local' if request['id'] == 'telescoping_local'
                    else plan['local_id'])
        return Candidate(identity, frontend['local_proposition'], local_proof(frontend),
                         'AgentV2Candidate.proof', frontend['source']['sha256'])
    targets = {'bridge': plan['bridge_proposition'], **{
        task: obligation['proposition'] for task, obligation in
        zip(('zero_endpoint', 'upper_endpoint'), plan['obligations'])}}
    task = next((task for task, proposition in targets.items()
                 if proposition == request['proposition']), None)
    if task is None:
        return None
    required = [plan['local_id']] if task == 'bridge' else []
    if request['dependencies'] != required:
        raise IntegrityError('candidate dependency set differs from reconstructed dependencies')
    return make_closure_candidate(frontend, task, approved, 'checker-template')


def registered_profiles():
    """Only real implemented profiles; source reconstruction detects ambiguity."""
    from . import (coefficient_frontend, interpolation_frontend, determinant_frontend,
                   kernel_transform_frontend, difference_ring_frontend, macmahon_frontend,
                   formal_frontend, recurrence_frontend, recurrence_lean_profile)
    common = ('Definitions', 'Auxiliary', 'Gaussian')
    gaussian = 'finite_product_framework/p1/lean/GaussianRules.lean'
    return (
        ProofProfile(formal_frontend.PROFILE, '1', 'telescoping', formal_frontend.analyze_source,
                     _telescoping_candidate, common, (gaussian,)),
        ProofProfile(recurrence_frontend.PROFILE, '1', 'recurrence', recurrence_frontend.analyze_source,
                     recurrence_lean_profile.reconstruct_profile_candidate, common,
                     (gaussian, 'finite_product_framework/p1/lean/Shared.lean')),
        ProofProfile(coefficient_frontend.PROFILE, '1', 'coefficient', coefficient_frontend.analyze_source,
                     _coefficient_candidate, common, ('agent_v2/lean/CoefficientRules.lean',)),
        ProofProfile(interpolation_frontend.PROFILE, '1', 'interpolation', interpolation_frontend.analyze_source,
                     _interpolation_candidate, (*common, 'BatchDefinitions'), ('agent_v2/lean/InterpolationRules.lean',)),
        ProofProfile(determinant_frontend.PROFILE, '1', 'determinant', determinant_frontend.analyze_source,
                     _determinant_candidate, common, ('agent_v2/lean/DeterminantRules.lean',)),
        ProofProfile(kernel_transform_frontend.PROFILE, '1', 'kernel_transform', kernel_transform_frontend.analyze_source,
                     _kernel_transform_candidate, common,
                     ('finite_product_framework/kernel_transform/lean/Rules.lean', 'agent_v2/lean/KernelTransformRules.lean')),
        ProofProfile(difference_ring_frontend.PROFILE, '1', 'difference_ring', difference_ring_frontend.analyze_source,
                     _difference_ring_candidate, common, ('agent_v2/lean/DifferenceRingRules.lean',)),
        ProofProfile(macmahon_frontend.PROFILE, '1', 'macmahon', macmahon_frontend.analyze_source,
                     _macmahon_candidate, (*common, 'BatchDefinitions'), ('agent_v2/lean/MacMahonRules.lean',),
                     partial_driver='MonomorphicCheck.lean', original_driver='MonomorphicCheck.lean',
                     partial_command='agent_v2_monomorphic_audit', original_command='agent_v2_monomorphic_audit',
                     universe_parameters=()),
    )


def _coefficient_candidate(frontend, request, approved):
    # Candidate identity/type/dependencies and submitted proof body are checked
    # by the common binding layer; this method only reconstructs its template.
    from .coefficient_translation import make_candidate
    return make_candidate(frontend)


def _interpolation_candidate(frontend, request, approved):
    from .interpolation_translation import make_candidate
    return make_candidate(frontend)


def _determinant_candidate(frontend, request, approved):
    from .determinant_translation import make_candidate
    return make_candidate(frontend)


def _kernel_transform_candidate(frontend, request, approved):
    from .kernel_transform_translation import make_candidate
    return make_candidate(frontend)


def _difference_ring_candidate(frontend, request, approved):
    from .difference_ring_translation import make_candidate
    return make_candidate(frontend)


def _macmahon_candidate(frontend, request, approved):
    from .macmahon_translation import make_candidate
    return make_candidate(frontend)


def resolve_source_profile(source, run):
    """Return the unique supported profile; unknown syntax remains unsupported."""
    source = source if isinstance(source, Source) else Source.from_dict(source)
    verify_source(source, run)
    matches = []
    seen = set()
    for profile in registered_profiles():
        if profile.id in seen:
            raise IntegrityError('ambiguous duplicate mathematical profile registration')
        seen.add(profile.id)
        frontend = profile.analyze_source(source.to_dict(), run)
        if not isinstance(frontend, dict) or frontend.get('status') not in ('applicable', 'not_applicable'):
            raise IntegrityError('invalid mathematical frontend status')
        if frontend.get('profile') != profile.id or frontend.get('source') != source.to_dict():
            raise IntegrityError('frontend profile or frozen Source binding mismatch')
        if frontend['status'] == 'applicable':
            if source.proposition is not None and frontend.get('original_proposition') != source.proposition:
                raise IntegrityError('frontend original proposition binding mismatch')
            matches.append(BoundProfile(profile, source, frontend))
    if len(matches) > 1:
        raise IntegrityError('ambiguous mathematical Source profiles')
    verify_source(source, run)
    return matches[0] if matches else None


def reconstruct_bound_candidate(bound, request, approved_certificates, *, allow_negative=False):
    """Return the correct canonical candidate, never substitute it for a bad term."""
    if not isinstance(approved_certificates, dict):
        raise IntegrityError('approved certificate context must be an object')
    if not isinstance(request.get('proof_term'), str) or not isinstance(request.get('proposition'), str):
        raise IntegrityError('candidate proposition and proof must be strings')
    dependencies = request.get('dependencies')
    if (not isinstance(dependencies, list) or any(not isinstance(identity, str) for identity in dependencies)
            or len(set(dependencies)) != len(dependencies)):
        raise IntegrityError('candidate dependencies must be distinct certificate identifiers')
    for identity in dependencies:
        if identity not in approved_certificates:
            raise IntegrityError('required checked certificate is missing: ' + identity)
    candidate = bound.profile.reconstruct_candidate(bound.frontend, request, approved_certificates)
    if candidate is None:
        raise PropositionBindingError('Candidate proposition differs from reconstructed profile targets.')
    expected = {key: thaw(getattr(candidate, key)) for key in
                ('id', 'proposition', 'theorem', 'source_sha256', 'dependencies')}
    if request.get('proposition') != expected['proposition']:
        raise PropositionBindingError('Candidate proposition differs from reconstructed profile target.')
    if any(request.get(key) != value for key, value in expected.items()):
        raise IntegrityError('candidate identity, source, theorem or dependencies differ from reconstructed profile')
    term = request.get('proof_term')
    negative = term in ('by rfl', 'by exact True.intro')
    if bound.profile.method == 'recurrence' and candidate.id.startswith('recurrence-local-'):
        negative = (isinstance(term, str) and term.partition('\n')[0] == candidate.proof_term.partition('\n')[0]
                    and term.partition('\n')[2] in ('by rfl', 'by exact True.intro'))
    if term != candidate.proof_term and not (allow_negative and negative):
        raise ValueError('Only the reconstructed profile template or bounded negative proof terms are accepted.')
    return candidate


def check_certificate_binding(certificate, bound, run, approved_certificates, *, deadline=None, _active=None):
    """Strict receipt binding shared by dependencies, recovery and final checks."""
    from .lean_checker import _AXIOMS
    from .math_lean_profile import _hash, external_environment_digest
    deadline = time.monotonic() + 300 if deadline is None else deadline
    active = set() if _active is None else _active
    if certificate.id in active:
        raise IntegrityError('cyclic certificate dependency')
    active.add(certificate.id)
    try:
        request = {'id': certificate.id, 'proposition': certificate.proposition,
                   'proof_term': certificate.proof_term, 'theorem': 'AgentV2Candidate.proof',
                   'source_sha256': certificate.source_sha256, 'dependencies': list(certificate.dependencies)}
        reconstruct_bound_candidate(bound, request, approved_certificates)
        evidence = thaw(certificate.evidence)
        expected = {key: value for key, value in request.items() if key != 'id'}
        expected['certificate_id'] = certificate.id
        if any(evidence.get(key) != value for key, value in expected.items()):
            raise IntegrityError('certificate receipt differs from its source, proposition, proof or dependencies')
        if evidence.get('profile') != bound.profile.id or evidence.get('profile_version') != bound.profile.version:
            raise IntegrityError('certificate receipt profile differs from reconstructed Source profile')
        audit = evidence.get('audit', {})
        if (type(evidence.get('returncode')) is not int or evidence['returncode'] != 0
                or not isinstance(audit, dict) or audit.get('theorem') != request['theorem']
                or not bound.profile.matches_universes(audit)
                or not isinstance(audit.get('axioms'), list) or not set(audit['axioms']) <= _AXIOMS):
            raise IntegrityError('certificate has no bound mathematical Lean audit')
        artifacts = evidence.get('artifacts')
        if not isinstance(artifacts, list) or not artifacts:
            raise IntegrityError('certificate has no retained verification artifacts')
        seen = set()
        for artifact in artifacts:
            if (not isinstance(artifact, dict) or set(artifact) - {'schema_version', 'path', 'sha256'}
                    or artifact.get('schema_version', 1) != 1):
                raise IntegrityError('malformed certificate artifact')
            target = guard_path(artifact['path'], run)
            if target in seen or _hash(target, deadline) != artifact.get('sha256'):
                raise IntegrityError('certificate artifact hash mismatch or duplicate')
            seen.add(target)
        # Require a single complete production transaction, not unrelated files
        # sharing Candidate.lean/Candidate.olean basenames.
        requests = [p for p in seen if p.name == 'request.json']
        if len(requests) != 1:
            raise IntegrityError('certificate has no unique retained candidate request')
        root = requests[0].parent
        required = {root / 'sources/Candidate.lean', root / 'build/Candidate.olean',
                    root / 'dependencies_before.json', root / 'dependencies_after.json',
                    root / 'candidate/stdout.jsonl', root / 'candidate/process.json', root / 'frontend.json'}
        if not required <= seen or json.loads(requests[0].read_text()) != request:
            raise IntegrityError('certificate candidate artifacts are incomplete or request differs')
        before = json.loads((root / 'dependencies_before.json').read_text())
        after = json.loads((root / 'dependencies_after.json').read_text())
        if (before != after or external_environment_digest(before) != evidence.get('external_environment_sha256')
                or sorted(audit.get('modules', [])) != before.get('modules')):
            raise IntegrityError('certificate import/dependency inventory differs from bound audit')
        if json.loads((root / 'frontend.json').read_text()) != bound.frontend:
            raise IntegrityError('certificate frontend differs from reconstructed Source')
        process = json.loads((root / 'candidate/process.json').read_text())
        if (process.get('returncode') != 0 or process.get('timed_out') is not False
                or process.get('environment_error') is not None):
            raise IntegrityError('certificate retained process did not succeed')
        audits = []
        for line in (root / 'candidate/stdout.jsonl').read_text().splitlines():
            message = json.loads(line)
            if not isinstance(message, dict) or message.get('severity') == 'error':
                raise IntegrityError('certificate retained Lean diagnostics contain errors')
            if isinstance(message.get('data'), str):
                try:
                    record = json.loads(message['data'])
                except ValueError:
                    continue
                if isinstance(record, dict) and 'agent_v2_audit_v1' in record:
                    audits.append(record)
        if audits != [audit] or evidence.get('axioms') != audit['axioms']:
            raise IntegrityError('certificate receipt audit differs from retained Lean audit')
        for identity in certificate.dependencies:
            if identity not in approved_certificates:
                raise IntegrityError('required checked certificate is missing: ' + identity)
            dependency = VerifiedCertificate.from_dict(approved_certificates[identity])
            if dependency.id != identity:
                raise IntegrityError('approved certificate key differs from identity')
            check_certificate_binding(dependency, bound, run, approved_certificates,
                                      deadline=deadline, _active=active)
    finally:
        active.remove(certificate.id)


def check_required_certificates(bound, candidate, approved_certificates, run, *, deadline):
    for identity in candidate.dependencies:
        if identity not in approved_certificates:
            raise IntegrityError('required checked certificate is missing: ' + identity)
        certificate = VerifiedCertificate.from_dict(approved_certificates[identity])
        if certificate.id != identity:
            raise IntegrityError('approved certificate key differs from identity')
        check_certificate_binding(certificate, bound, run, approved_certificates, deadline=deadline)
