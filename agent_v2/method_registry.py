"""Versioned method contracts. Registration declares capabilities, never proofs."""
from dataclasses import dataclass
import importlib
import math
import re
from typing import Any, Literal

from .models import ContractError, Model


def resolve(entry):
    if not isinstance(entry, str) or not re.fullmatch(r'agent_v2\.[a-z_]+:[A-Za-z][A-Za-z0-9_]*', entry):
        raise ContractError('method entry must be an explicit v2 callable')
    module, name = entry.split(':')
    try:
        value = getattr(importlib.import_module(module), name)
    except (ImportError, AttributeError) as error:
        raise ContractError('method implementation unavailable: ' + entry) from error
    if not callable(value):
        raise ContractError('method entry is not callable: ' + entry)
    return value


@dataclass(frozen=True)
class MethodSpec(Model):
    id: str
    version: str
    family: str
    supported_structures: tuple[str, ...]
    accepted_kinds: tuple[str, ...]
    semantic_domains: tuple[str, ...]
    index_ranges: tuple[str, ...]
    required_assumptions: tuple[str, ...]
    parameters: dict[str, Any]
    certificate_types: tuple[str, ...]
    local_lean: bool
    full_original: bool
    capability_level: Literal['L0', 'L1', 'L2', 'L3']
    estimated_seconds: float
    resource_limits: dict[str, Any]
    frontend: str
    adapter: str
    dependency_provider: str
    lean_profile: str
    scopes: tuple[str, ...]
    tasks: tuple[str, ...]
    limitations: tuple[str, ...]

    def __post_init__(self):
        super().__post_init__()
        if not re.fullmatch('[a-z][a-z0-9_]*', self.id) or not self.version:
            raise ContractError('invalid method identity/version')
        if not self.supported_structures or not self.accepted_kinds or not self.scopes:
            raise ContractError('method requires explicit input contracts')
        if self.estimated_seconds < 0 or not math.isfinite(self.estimated_seconds):
            raise ContractError('invalid method estimate')
        if self.capability_level == 'L3' and not self.local_lean:
            raise ContractError('L3 requires actual local Lean translation')
        if self.capability_level in ('L0', 'L2') and (self.local_lean or self.full_original):
            raise ContractError('declared capability contradicts verification support')

    def factory(self):
        return resolve(self.adapter)

    def validate_parameters(self, values):
        allowed = {'method', 'method_version', 'scope', 'task', 'produces_certificate', *self.parameters}
        if not set(values) <= allowed:
            raise ContractError('unknown method parameters')
        if values.get('method', self.id) != self.id or values.get('method_version', self.version) != self.version:
            raise ContractError('method/version mismatch')
        if values.get('scope', 'local') not in self.scopes:
            raise ContractError('unsupported method scope')
        if 'task' in values and values['task'] not in self.tasks:
            raise ContractError('unsupported local method task')
        if 'produces_certificate' in values and not isinstance(values['produces_certificate'], str):
            raise ContractError('produced certificate ID must be a string')
        for key, rule in self.parameters.items():
            if key not in values:
                continue
            value = values[key]
            if (type(value) not in (int, float) or not math.isfinite(value)
                    or value <= rule['exclusive_min'] or value > rule['maximum']):
                raise ContractError('invalid method resource parameter: ' + key)


class MethodRegistry:
    def __init__(self):
        self._methods = {}

    def register(self, spec):
        if not isinstance(spec, MethodSpec) or spec.id in self._methods:
            raise ContractError('invalid or duplicate method registration')
        if spec.capability_level != 'L0':
            factory = spec.factory()
            if not hasattr(factory(), 'execute'):
                raise ContractError('method adapter has no execute boundary')
            resolve(spec.frontend)
            resolve(spec.dependency_provider)
        self._methods[spec.id] = spec

    def get(self, identity):
        if identity not in self._methods:
            raise ContractError('unregistered method: ' + str(identity))
        return self._methods[identity]

    def ids(self):
        return tuple(self._methods)

    def to_dict(self):
        return {'schema_version': 1, 'methods': [spec.to_dict() for spec in self._methods.values()]}


def builtin_registry():
    registry = MethodRegistry()
    registry.register(MethodSpec(
        id='telescoping', version='2.0', family='差分／望远镜',
        supported_structures=('Gaussian weighted prefix sum with complete original binders',),
        accepted_kinds=('lean_source', 'closed_prop'), semantic_domains=('arbitrary Field',),
        index_ranges=('j ∈ Finset.range (n+1)',), required_assumptions=('exact original context; no added hypotheses',),
        parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
        certificate_types=('local difference', 'finite-sum conditional connection', 'formal endpoints'),
        local_lean=True, full_original=True, capability_level='L3', estimated_seconds=45.0,
        resource_limits={'max_unknowns': 10000, 'max_normal_form_degree': 10000, 'max_states': 128,
                         'actions_per_execution': 1},
        frontend='agent_v2.formal_frontend:analyze_source', adapter='agent_v2.cas_adapter:TelescopingAdapter',
        dependency_provider='agent_v2.cli:telescoping_dependencies',
        lean_profile='gaussian_weighted_range_v1', scopes=('local', 'full'),
        tasks=('local', 'bridge', 'zero_endpoint', 'upper_endpoint'),
        limitations=('only the stated structural family', 'no model-driven transformations',
                     'fixed safe proof templates; CAS construction alone never certifies a theorem')))
    registry.register(MethodSpec(
        id='recurrence', version='1.0', family='递推关系与唯一性',
        supported_structures=('alternating geometric weight times one Gaussian over range(n+1)',),
        accepted_kinds=('lean_source', 'closed_prop'), semantic_domains=('arbitrary Field',),
        index_ranges=('k ∈ Finset.range (n+1); forward n-shifts; support zero above n',),
        required_assumptions=('exact original binders; no extra regularity assumptions',),
        parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
        certificate_types=('q-Zeilberger operator and rational certificate',
                           'closed second-order finite-sum recurrence'),
        local_lean=True, full_original=False, capability_level='L3', estimated_seconds=45.0,
        resource_limits={'max_unknowns': 10000, 'max_normal_form_degree': 10000,
                         'max_states_core_argument': 128, 'max_order': None,
                         'search_stop': 'wall-clock and linear-system limits', 'actions_per_execution': 1},
        frontend='agent_v2.recurrence_frontend:analyze_source',
        adapter='agent_v2.recurrence_adapter:RecurrenceAdapter',
        dependency_provider='agent_v2.recurrence_adapter:dependencies',
        lean_profile='gaussian_geometric_recurrence_v1', scopes=('local',), tasks=(),
        limitations=('native Lean translation requires monic polynomial order two and supported flux',
                     'original RHS recurrence, two initial values and uniqueness connection remain open',
                     'other constructed operators are translation_pending, never checked certificates')))
    from .symbolic_methods import METHODS
    for identity, info in METHODS.items():
        registry.register(MethodSpec(
            id=identity,version='1.0',family=info['family'],supported_structures=(info['structure'],),
            accepted_kinds=('core_request',),semantic_domains=(info['domain'],),
            index_ranges=('explicit bounded mathematical input; see typed request contract',),
            required_assumptions=('no original theorem assumptions inferred from a standalone request',),
            parameters={'seconds':{'exclusive_min':0,'maximum':86400}},
            certificate_types=('unverified symbolic construction and residual diagnostics',),
            local_lean=False,full_original=False,capability_level=info.get('level','L2'),
            estimated_seconds=0.0 if info.get('level')=='L0' else 1.0,
            resource_limits={'input_nodes':4096,'input_depth':32,'actions_per_execution':1},
            frontend='agent_v2.symbolic_methods:analyze_source',
            adapter='agent_v2.symbolic_methods:'+identity+'_adapter',
            dependency_provider='agent_v2.symbolic_methods:'+identity+'_dependencies',lean_profile='none',
            scopes=('local',),tasks=(),limitations=(info['limits'],
                'standalone core request only; Train export and local Lean bridge unavailable',
                'historical full workflow is not invoked; constructed never enters C')))
    return registry
