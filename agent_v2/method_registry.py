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
        id='recurrence', version='2.0', family='递推关系与唯一性',
        supported_structures=('alternating geometric weight times one Gaussian over range(n+1)',),
        accepted_kinds=('lean_source', 'closed_prop'), semantic_domains=('arbitrary Field',),
        index_ranges=('k ∈ Finset.range (n+1); forward n-shifts; support zero above n',),
        required_assumptions=('exact original binders; no extra regularity assumptions',),
        parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
        certificate_types=('q-Zeilberger operator and rational certificate',
                           'closed second-order finite-sum recurrence',
                           'conditional uniqueness connection', 'RHS recurrence and two initial values'),
        local_lean=True, full_original=True, capability_level='L3', estimated_seconds=45.0,
        resource_limits={'max_unknowns': 10000, 'max_normal_form_degree': 10000,
                         'max_states_core_argument': 128, 'max_order': None,
                         'search_stop': 'wall-clock and linear-system limits', 'actions_per_execution': 1},
        frontend='agent_v2.recurrence_frontend:analyze_source',
        adapter='agent_v2.recurrence_adapter:RecurrenceAdapter',
        dependency_provider='agent_v2.recurrence_adapter:dependencies',
        lean_profile='gaussian_geometric_recurrence_v1', scopes=('local', 'full'),
        tasks=('local', 'uniqueness_bridge', 'rhs_recurrence', 'initial_zero', 'initial_one'),
        limitations=('native Lean translation requires monic polynomial order two and supported flux',
                     'full scope requires the source-parsed parity/Pochhammer RHS and exact approved recurrence',
                     'five fixed tasks only; no automatic mathematical graph expansion',
                     'other constructed operators are translation_pending, never checked certificates')))
    from .symbolic_methods import METHODS
    for identity, info in METHODS.items():
        if identity == 'combinatorial':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('finite q-binomial product with ranked weighted Boolean choices',),
                accepted_kinds=('lean_source', 'closed_prop'),
                semantic_domains=('original commutative Field; no scalar cancellation or extra assumptions',),
                index_ranges=('subsets and Boolean choices of symbolic range n; ranks in range(n+1)',),
                required_assumptions=('complete original q,z,n context; Gaussian subset bridge remains pending',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('unverified finite bijections, rank bounds and multiplicative weight transport',),
                local_lean=False, full_original=False, capability_level='L2', estimated_seconds=1.0,
                resource_limits={'source_nodes':4096,'source_depth':64,'core_candidates':2,
                                 'checker_nodes':12000,'checker_depth':32,'actions_per_execution':1},
                frontend='agent_v2.combinatorial_frontend:analyze_source',
                adapter='agent_v2.combinatorial_adapter:CombinatorialAdapter',
                dependency_provider='agent_v2.combinatorial_adapter:dependencies',
                lean_profile='none', scopes=('local',),tasks=(),
                limitations=('source-only symbolic execution of product-side weighted choices; no Lean certificate',
                             'Gaussian fixed-rank subset representation and original theorem remain open',
                             'weight-preserving bijection only; no sign-reversing involution or fixed-point cancellation',
                             'legacy broad standalone combinatorial requests remain unavailable')))
            continue
        if identity == 'noncommutative':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('polynomial q-substitution and multiplication operator commutation',),
                accepted_kinds=('lean_source', 'closed_prop'),
                semantic_domains=('polynomials over the original commutative Field; ordered operator composition',),
                index_ranges=('arbitrary natural monomial degree; finite polynomial support',),
                required_assumptions=('original q != 0 and q != 1 retained; no assumed operator commutation',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('unverified ordered monomial-action trace and exact operator normal forms',),
                local_lean=False, full_original=False, capability_level='L2', estimated_seconds=1.0,
                resource_limits={'source_nodes':4096,'source_depth':64,'core_terms_per_side':16,
                                 'core_word_length':32,'core_steps':4096,'actions_per_execution':1},
                frontend='agent_v2.noncommutative_frontend:analyze_source',
                adapter='agent_v2.noncommutative_adapter:NoncommutativeAdapter',
                dependency_provider='agent_v2.noncommutative_adapter:dependencies',
                lean_profile='none', scopes=('local',),tasks=(),
                limitations=('source-only symbolic execution; no Lean certificate or original proof',
                             'definition expansion and finite linear extension still need a Lean bridge',
                             'legacy broad standalone noncommutative requests remain unavailable')))
            continue
        if identity == 'product':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('Pochhammer product split into symbolic residue classes',),
                accepted_kinds=('lean_source', 'closed_prop'),
                semantic_domains=('original commutative Field; natural powers; no scalar cancellation',),
                index_ranges=('k < m*n and (j < m, i < n); symbolic m,n including n=0',),
                required_assumptions=('original m > 0 for quotient and remainder; no q != 0 requirement',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('unverified mixed-radix index equivalence and factor exponent normal forms',),
                local_lean=False, full_original=False, capability_level='L2', estimated_seconds=1.0,
                resource_limits={'source_nodes':4096,'source_depth':64,'core_candidates':2,'actions_per_execution':1},
                frontend='agent_v2.product_frontend:analyze_source',
                adapter='agent_v2.product_adapter:ProductAdapter',
                dependency_provider='agent_v2.product_adapter:dependencies',
                lean_profile='none', scopes=('local',),tasks=(),
                limitations=('source-only symbolic execution; no Lean certificate or original proof',
                             'finite product reindexing and source definition replay still need a Lean bridge',
                             'legacy broad standalone product requests remain unavailable')))
            continue
        if identity == 'macmahon':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('complex ultraspherical boundary with an arbitrary-length finite Laurent sum',),
                accepted_kinds=('lean_source', 'closed_prop', 'core_request'),
                semantic_domains=('original Complex domain; formal power series with finite coefficient fibers',),
                index_ranges=('every original n; k in range(n+1), integer exponent n-2*k',),
                required_assumptions=('complete original regular q and z != 0 hypotheses retained',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('graded rational Omega decomposition, formal denominator inverse and source coefficient',),
                local_lean=True, full_original=False, capability_level='L3', estimated_seconds=90.0,
                resource_limits={'source_nodes':4096,'source_depth':64,'core_factors':2,
                                 'core_auxiliary_variables':1,'actions_per_execution':1},
                frontend='agent_v2.macmahon_frontend:analyze_source',
                adapter='agent_v2.macmahon_adapter:MacMahonAdapter',
                dependency_provider='agent_v2.macmahon_adapter:dependencies',
                lean_profile='chebyshev_laurent_omega_v1', scopes=('local',),tasks=(),
                limitations=('local formal generating-function realization only; all original ultraspherical conjuncts remain open',
                             'regulator removal requires a finite fiber; no analytic convergence claim',
                             'standalone core requests remain nonformal L2 executions')))
            continue
        if identity == 'difference_ring':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('positive-length Pochhammer first-factor identity with evaluated last-step tower',),
                accepted_kinds=('lean_source', 'closed_prop', 'core_request'),
                semantic_domains=('arbitrary Field; independently checked integer polynomial multipliers',),
                index_ranges=('original symbolic n with 1 <= n and natural index n-1',),
                required_assumptions=('complete original context; tower relation proved in Lean from original product',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('original-relation multiplier and evaluated source product increment',),
                local_lean=True, full_original=False, capability_level='L3', estimated_seconds=60.0,
                resource_limits={'source_nodes':4096,'source_depth':64,'core_degree':3,
                                 'core_unknowns':1000,'actions_per_execution':1},
                frontend='agent_v2.difference_ring_frontend:analyze_source',
                adapter='agent_v2.difference_ring_adapter:DifferenceRingAdapter',
                dependency_provider='agent_v2.difference_ring_adapter:dependencies',
                lean_profile='pochhammer_evaluated_difference_v1', scopes=('local',),tasks=(),
                limitations=('local evaluated last-step difference only; first-factor/tail connection remains open',
                             'rational multipliers and general difference towers have no source-bound Lean bridge',
                             'standalone core requests remain nonformal L2 executions')))
            continue
        if identity == 'kernel_transform':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('triangular finite kernel transpose with arbitrary sequence factors',),
                accepted_kinds=('lean_source', 'closed_prop', 'core_request'),
                semantic_domains=('arbitrary CommRing; natural subtraction with verified index guards',),
                index_ranges=('symbolic N; mutually inverse triangular finite domains including N=0',),
                required_assumptions=('complete original source context; no extra assumptions',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('coordinate permutation with bidirectional affine domain and index witnesses',),
                local_lean=True, full_original=False, capability_level='L3', estimated_seconds=60.0,
                resource_limits={'source_nodes':4096,'source_depth':64,'core_depth':32,'actions_per_execution':1},
                frontend='agent_v2.kernel_transform_frontend:analyze_source',
                adapter='agent_v2.kernel_transform_adapter:KernelTransformAdapter',
                dependency_provider='agent_v2.kernel_transform_adapter:dependencies',
                lean_profile='bailey_triangular_kernel_v1', scopes=('local',),tasks=(),
                limitations=('local triangular transpose only; original RHS rearrangement remains open',
                             'bounded coordinate and affine-witness search; no general kernel discovery',
                             'standalone core requests remain nonformal L2 executions')))
            continue
        if identity == 'determinant':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('Carlitz finite matrix with integer Gaussian entries; arbitrary selected 2x2 minor',),
                accepted_kinds=('lean_source', 'closed_prop', 'core_request'),
                semantic_domains=('arbitrary Field; division-free minor expansion without pivot assumptions',),
                index_ranges=('arbitrary original dimension k; four universally quantified selectors in Fin k',),
                required_assumptions=('complete original positivity and Antitone hypotheses retained',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('Berkowitz minor determinant checked independently by Leibniz expansion',),
                local_lean=True, full_original=False, capability_level='L3', estimated_seconds=60.0,
                resource_limits={'source_nodes':4096,'source_depth':64,'core_depth':32,'actions_per_execution':1},
                frontend='agent_v2.determinant_frontend:analyze_source',
                adapter='agent_v2.determinant_adapter:DeterminantAdapter',
                dependency_provider='agent_v2.determinant_adapter:dependencies',
                lean_profile='carlitz_matrix_minor_v1', scopes=('local',),tasks=(),
                limitations=('local minor only; arbitrary-size determinant and planePi identity remain open',
                             'symbolic LU outputs are retained but not adopted as formal certificates',
                             'standalone matrix requests remain nonformal L2 executions')))
            continue
        if identity == 'interpolation':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('Pochhammer tail quotient with original integer shift and finite range',),
                accepted_kinds=('lean_source', 'closed_prop', 'core_request'),
                semantic_domains=('arbitrary Field; two distinct nodes 0 and 1; no CharZero assumption',),
                index_ranges=('every j in the original natural tail range n-k',),
                required_assumptions=('complete original regular, order, parameter and denominator hypotheses retained',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('degree-one finite-node certificate and source factor bridge',),
                local_lean=True, full_original=False, capability_level='L3', estimated_seconds=90.0,
                resource_limits={'source_nodes':4096,'source_depth':64,'core_depth':32,'actions_per_execution':1},
                frontend='agent_v2.interpolation_frontend:analyze_source',
                adapter='agent_v2.interpolation_adapter:InterpolationAdapter',
                dependency_provider='agent_v2.interpolation_adapter:dependencies',
                lean_profile='poch_tail_factor_interpolation_v1', scopes=('local',),tasks=(),
                limitations=('local factor interpolation only; product assembly and original quotient identity remain open',
                             'standalone finite-node requests remain nonformal L2 executions')))
            continue
        if identity == 'coefficient':
            registry.register(MethodSpec(
                id=identity, version='2.0', family=info['family'],
                supported_structures=('finite Gaussian generating sum with Pochhammer product target',),
                accepted_kinds=('lean_source', 'closed_prop', 'core_request'),
                semantic_domains=('arbitrary Field; source-free ring requests remain nonformal',),
                index_ranges=('all natural product lengths and coefficient indices; finite Cauchy convolution',),
                required_assumptions=('exact original ordered binders; no added assumptions',),
                parameters={'seconds': {'exclusive_min': 0, 'maximum': 86400}},
                certificate_types=('source evaluation bridge and zero/successor product coefficients',),
                local_lean=True, full_original=False, capability_level='L3', estimated_seconds=45.0,
                resource_limits={'input_nodes':4096,'input_depth':32,'actions_per_execution':1},
                frontend='agent_v2.coefficient_frontend:analyze_source',
                adapter='agent_v2.coefficient_adapter:CoefficientAdapter',
                dependency_provider='agent_v2.coefficient_adapter:dependencies',
                lean_profile='qbinomial_product_coefficients_v1', scopes=('local',),tasks=(),
                limitations=('local Pochhammer coefficient relations only; Gaussian coefficient formula remains open',
                             'standalone core requests never export formal certificates')))
            continue
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
