"""Immutable, content-bound local proof requests; no proof grants acceptance."""
from dataclasses import dataclass
import hashlib

from .models import Model, Source, Obligation, Candidate, ContractError, digest


def certificate_binding(certificate):
    return digest({key: getattr(certificate, key) for key in
                   ('id', 'proposition', 'proof_term', 'source_sha256', 'dependencies')})


def dependency_name(certificate_id):
    """Stable Lean alias, independent of model-supplied spelling or receipts."""
    return 'AgentV2Dependency.c' + hashlib.sha256(certificate_id.encode()).hexdigest()


@dataclass(frozen=True)
class LocalTask(Model):
    id: str
    source: Source
    representation_id: str
    parent: Obligation
    proposition: str
    dependencies: tuple[str, ...]
    dependency_bindings: dict[str, str]
    children: tuple[Obligation, ...]
    closes: str | None

    def __post_init__(self):
        super().__post_init__()
        from .executor import connection_type
        if not self.representation_id or not self.proposition.strip() or len(self.proposition) > 64000:
            raise ContractError('empty representation or unsupported local proposition size')
        if self.parent.source_sha256 != self.source.sha256 or self.source.Gamma != self.source.declaration:
            raise ContractError('local task original context differs')
        if len(set(self.dependencies)) != len(self.dependencies) or set(self.dependency_bindings) != set(self.dependencies):
            raise ContractError('local task dependency bindings differ')
        if len(self.children) > 16 or len({c.id for c in self.children}) != len(self.children):
            raise ContractError('invalid local task children')
        if any(c.source_sha256 != self.source.sha256 or c.id == self.parent.id for c in self.children):
            raise ContractError('foreign or cyclic local child')
        if self.closes is not None:
            if self.closes != self.parent.id or self.proposition != connection_type(self.parent, self.children):
                raise ContractError('local task does not prove its exact parent connection')
        elif self.children:
            raise ContractError('independent lemma cannot replace obligations')
        data = self.to_dict(); del data['id']
        if self.id != 'local-' + digest(data):
            raise ContractError('local task content hash differs')


def make_task(state, representation_id, obligation_id, *, children=(), proposition=None, dependencies=()):
    from .executor import connection_type, validate_invariant
    validate_invariant(state)
    if representation_id != state.r:
        raise ContractError('local task representation differs from selected state')
    parent = next((o for o in state.O if o.id == obligation_id), None)
    if parent is None:
        raise ContractError('local task target is not an open obligation')
    children = tuple(children)
    expected = connection_type(parent, children)
    proposition = expected if proposition is None else proposition
    dependencies = tuple(dependencies)
    approved = {c.id: c for c in state.C}
    if any(identity not in approved for identity in dependencies):
        raise ContractError('local task dependency is not checked')
    data = dict(source=state.G, representation_id=representation_id, parent=parent,
        proposition=proposition, dependencies=dependencies,
        dependency_bindings={identity: certificate_binding(approved[identity]) for identity in dependencies},
        children=children, closes=parent.id if proposition == expected else None)
    return LocalTask('local-' + digest({'schema_version': 1, **data}), **data)


def candidate_for(task, proof_term):
    if not isinstance(task, LocalTask):
        raise ContractError('registered typed local task required')
    return Candidate(task.id, task.proposition, proof_term, 'AgentV2Candidate.proof',
        task.source.sha256, task.dependencies, task.closes, task.children)
