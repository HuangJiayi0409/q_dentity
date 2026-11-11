"""Strict immutable wire contracts. Unknown fields and coercions are rejected."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import types
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal, Union, get_args, get_origin, get_type_hints


class ContractError(ValueError):
    pass


def thaw(value):
    if isinstance(value, Model):
        return value.to_dict()
    if isinstance(value, Mapping):
        return {k: thaw(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [thaw(v) for v in value]
    return value


def canonical(value):
    return json.dumps(thaw(value), ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def _json(value):
    if value is None or type(value) in (str, bool, int):
        return value
    if type(value) is float and math.isfinite(value):
        return value
    if isinstance(value, Mapping) and all(type(k) is str for k in value):
        return types.MappingProxyType({k: _json(v) for k, v in value.items()})
    if isinstance(value, (tuple, list)):
        return tuple(_json(v) for v in value)
    raise ContractError('not finite JSON data')


def _decode(value, expected):
    origin, args = get_origin(expected), get_args(expected)
    if expected is Any:
        return _json(value)
    if origin in (Union, types.UnionType):
        for option in args:
            try:
                return _decode(value, option)
            except ContractError:
                pass
        raise ContractError(f'expected {expected}')
    if origin is Literal:
        if not any(type(value) is type(a) and value == a for a in args):
            raise ContractError(f'unknown enum {value!r}')
        return value
    if origin is tuple:
        if not isinstance(value, (tuple, list)):
            raise ContractError('expected array')
        return tuple(_decode(v, args[0]) for v in value)
    if origin is dict:
        if not isinstance(value, Mapping):
            raise ContractError('expected object')
        return types.MappingProxyType({_decode(k, args[0]): _decode(v, args[1])
                                       for k, v in value.items()})
    if isinstance(expected, type) and issubclass(expected, Model):
        return value if isinstance(value, expected) else expected.from_dict(value)
    if expected is float:
        if type(value) not in (float, int) or not math.isfinite(value):
            raise ContractError('expected finite number')
        return float(value)
    if type(value) is not expected:
        raise ContractError(f'expected {expected}, got {type(value)}')
    return value


class Model:
    def __post_init__(self):
        hints = get_type_hints(type(self))
        for field in dataclasses.fields(self):
            object.__setattr__(self, field.name, _decode(getattr(self, field.name), hints[field.name]))

    def to_dict(self):
        return {'schema_version': 1, **{f.name: thaw(getattr(self, f.name))
                                       for f in dataclasses.fields(self)}}

    @classmethod
    def from_dict(cls, data):
        keys = {f.name for f in dataclasses.fields(cls)}
        if not isinstance(data, Mapping) or set(data) != keys | {'schema_version'}:
            raise ContractError(f'{cls.__name__}: missing or unknown fields')
        if type(data['schema_version']) is not int or data['schema_version'] != 1:
            raise ContractError('unsupported schema version')
        return cls(**{key: data[key] for key in keys})


@dataclass(frozen=True)
class Artifact(Model):
    path: str
    sha256: str


@dataclass(frozen=True)
class Source(Model):
    identity: str
    path: str
    snapshot_path: str
    sha256: str
    theorem: str
    declaration: str
    Gamma: str
    proposition: str | None
    dependencies: tuple[Artifact, ...] = ()


@dataclass(frozen=True)
class Budget(Model):
    seconds: float
    actions: int

    def __post_init__(self):
        super().__post_init__()
        if self.seconds < 0 or self.actions < 0:
            raise ContractError('negative budget')

    def charge(self, seconds, actions=1):
        if seconds < 0 or actions < 0:
            raise ContractError('negative cost')
        return Budget(max(0.0, self.seconds - seconds), max(0, self.actions - actions))


@dataclass(frozen=True)
class RepresentationInstance(Model):
    id: str
    kind: Literal['lean_source', 'closed_prop', 'core_request']
    payload: dict[str, Any]
    semantic_domain: str | None
    index_ranges: tuple[str, ...]
    lean_anchor: str | None
    provenance: tuple[str, ...]
    source_sha256: str


@dataclass(frozen=True)
class Obligation(Model):
    id: str
    kind: Literal['original', 'subgoal', 'bridge', 'boundary']
    proposition: str | None
    lean_anchor: str
    source_sha256: str
    origin_action: str | None = None
    dependencies: tuple[str, ...] = ()


@dataclass(frozen=True)
class Candidate(Model):
    id: str
    proposition: str
    proof_term: str
    theorem: str
    source_sha256: str
    dependencies: tuple[str, ...] = ()
    closes: str | None = None
    replaces: tuple[Obligation, ...] = ()


@dataclass(frozen=True)
class VerifiedCertificate(Model):
    id: str
    proposition: str
    proof_term: str
    source_sha256: str
    dependencies: tuple[str, ...]
    evidence: dict[str, Any]


@dataclass(frozen=True)
class ProofLink(Model):
    parent: Obligation
    children: tuple[Obligation, ...]
    certificate_id: str


@dataclass(frozen=True)
class Attempt(Model):
    fingerprint: str
    action_id: str
    code: str
    round: int


@dataclass(frozen=True)
class ResidualState(Model):
    G: Source
    Gamma: str
    r: str
    C: tuple[VerifiedCertificate, ...]
    O: tuple[Obligation, ...]
    b: Budget
    root: Obligation
    links: tuple[ProofLink, ...] = ()
    attempts: tuple[Attempt, ...] = ()
    round_index: int = 0
    status: Literal['running', 'incomplete', 'budget_exhausted', 'environment_blocked',
                    'integrity_error', 'original_theorem_proved'] = 'running'

    def __post_init__(self):
        super().__post_init__()
        if self.Gamma != self.G.Gamma or self.round_index < 0:
            raise ContractError('original context changed or invalid round')


@dataclass(frozen=True)
class JointAction(Model):
    id: str
    T: str
    source: str
    target: str
    M: Literal['CAS', 'LLM']
    backend: str
    theta: dict[str, Any]


@dataclass(frozen=True)
class FailureSignature(Model):
    stage: str
    code: str
    message: str
    backend_status: str | None


@dataclass(frozen=True)
class Cost(Model):
    wall_seconds: float
    actions: int

    def __post_init__(self):
        super().__post_init__()
        if self.wall_seconds < 0 or self.actions < 0:
            raise ContractError('negative actual cost')


@dataclass(frozen=True)
class ExecutionResult(Model):
    status: Literal['symbolic_constructed', 'incomplete', 'environment_blocked',
                    'budget_exhausted', 'integrity_error']
    C_partial: tuple[Candidate, ...]
    O_res: tuple[Obligation, ...]
    sigma: FailureSignature
    cost: Cost
    raw_result: dict[str, Any]
    artifacts: tuple[Artifact, ...]
    diagnostics: tuple[Any, ...]
    original_identity_proved: Literal[False]


def initial_state(source, budget):
    root = Obligation('original', 'original', source.proposition, source.theorem, source.sha256)
    representation = RepresentationInstance('original', 'closed_prop' if source.proposition else 'lean_source',
        {'declaration': source.declaration, 'proposition': source.proposition}, None, (), source.theorem, ('source_snapshot',), source.sha256)
    return ResidualState(source, source.Gamma, representation.id, (), (root,), budget, root), representation


def state_fingerprint(state):
    # Time, attempt history and action counters are deliberately excluded: paying
    # for a failure is not mathematical progress and cannot unlock blind retries.
    certificates = [{'id': c.id, 'proposition': c.proposition,
                     'source_sha256': c.source_sha256, 'dependencies': c.dependencies}
                    for c in state.C]
    # Fresh replay paths, nonces and equivalent proof terms are evidence for the
    # same theorem, not new mathematical progress that permits a failed retry.
    return digest({'G': state.G, 'Gamma': state.Gamma, 'r': state.r, 'C': certificates,
                   'O': state.O, 'links': state.links})


def action_fingerprint(state, action):
    semantic_action = action.to_dict()
    del semantic_action['id']
    return digest({'state': state_fingerprint(state), 'action': semantic_action})
