"""Executable capability descriptions, separate from input-specific checks.

`applicable` remains a scheduling hint for older adapters. It is never a claim
that a mathematical domain or a proof has been certified. Unknown checks stay
unknown, and a configured search limit is not a mathematical impossibility.
"""
from copy import deepcopy
from .contracts import BACKENDS


def scope(syntax, bases, dimension, domain, order, exit_scope, limits=None):
    return dict(syntax=syntax, bases=bases, summation_dimension=dimension,
                coefficient_domain=domain, order=order, proof_exit_scope=exit_scope,
                implementation_limits=limits or {},
                success_criterion='original Lean theorem, source binding and axiom audit',
                guarantee='bounded construction; no universal proof or termination claim')


SCOPES = {
 'direct_q_gosper': scope('one entire finite range sum against scalar; multiplicative q-hypergeometric term',
     'one structural base', 1, 'formal rational functions, then original-domain obligations', 0,
     'native explicit sums; structured definitions need a source bridge'),
 'bibasic_gosper': scope('explicit finite sum, summand independent of outer index',
     'two independent bases', 1, 'rational bivariate shift field; specialize in Lean', 0,
     'restricted bibasic native grammar and endpoints'),
 'target_first_order': scope('native finite q-hypergeometric sum and target ratio',
     'one base', 1, 'formal field with explicit specialization', 1,
     'native first-order recurrence and initial value'),
 'general_q_zeilberger': scope('whole-side sums or registered structured sums; affine natural prefix',
     'one base', 1, 'formal rational functions and original-domain specialization', 'budget.max_order',
     'finite-order common recurrence, moving tails, initials and singular-index obligations'),
 'ore_closure': scope('registered defined sequences with certified recurrences',
     'one base', 1, 'q-Ore rational coefficient field', 'bounded closure search',
     'native second-order objects / first-order forcing; parameter-instance branch orders 1..4'),
 'multisum': scope('nested affine range sums over boxes or simplices',
     'one base', 'finite, at least 2', 'formal rational multishifts; original support still required', 'budget.max_order',
     '2D simplex, order 1 monic, multiplicative Pochhammer kernel with lengths i,j,i+j and domain hypotheses',
     {'native_dimension':2,'native_domains':['simplex'],'native_order':1}),
 'cauchy_coefficient': scope('finite conjunction/forall; certified scalar-to-polynomial lifting; PowerSeries/Polynomial coefficients, Cauchy and local Gaussian algebra',
     'no independent-base restriction on opaque scalar atoms', 'sum congruence depth 0..4',
     'commutative ring; inverses stay atoms', None, 'all-branch coefficient normalization and original-theorem ring replay; nontrivial residual sums remain obligations',
     {'sum_depth':4, 'goal_limit':128, 'views':['series','finite','polynomial'], 'polynomial_variable_candidates':8, 'cross_method_fallback':False}),
 'finite_product_indices': scope('finite range products without sums', 'no separate base restriction', 0,
     'original scalar domain', None, 'bounded index transformations and factor identities',
     {'transformation_depth':2,'finish_depth':8}),
 'polynomial_interpolation': scope('certified shifted/reciprocal q-products, signed-pair merge, finite Lagrange parameter families and certified shifted-parameter phi sums, multiplicity certificates or bounded scalar AST',
     'arbitrary field; regular q for geometric root source bridges', 1,
     'original nonzero factors, node separation, multiplicities and symbolic degree bounds', None,
     'certified parameter polynomials, roots or Lagrange weights, and original-goal transport',
     {'degree':'budget.max_degree (0..12) only for scalar AST; structural lengths remain symbolic',
      'constructors':'bounded structural schema search; no identity-ID dispatch',
      'excluded':'hypergeometric structures outside the certified shifted-parameter family; arbitrary unsupplied multiplicity construction',
      'cross_method_fallback':False}),
 'rational_principal_parts': scope('proper rational finite simple-pole family or explicit rational scalar expression with split linear poles',
     'arbitrary finite injective pole family', 1,
     'original denominator conditions and evaluation away from poles', None,
     'Lagrange principal-family reconstruction or explicit principal parts with polynomial part',
     {'degree':'symbolic numerator degree for proper family; budget.max_degree for scalar residuals',
      'excluded':'general symbolic repeated-pole families and automatic pole-collision stratification',
      'cross_method_fallback':False}),
 'operator_word_normalization': scope('finite noncommutative words and explicit natural powers', 'not a q-base test', 0,
     'original operator algebra and local relations', None, 'finite word normalization', {'explicit_power':12}),
 'weighted_bijection': scope('same-domain range/interval reflection; subset complement and disjoint blocks with optional rank filter; Gaussian reciprocal rank reflection; geometric rank fibers and binary choices; complete conjunctions', 'weights retain parameters',
     'finite objects, symbolic cardinalities', 'original weight ring; geometric representation over fields, including q=0', None,
     'object representation, inverse maps, weight proofs and all-conjunct reconstruction',
     {'conjunction_plan_combinations':32,'cross_method_solver_fallback':False}),
 'sign_reversing_involution': scope('range/interval reflection or powerset membership toggle; odd Gaussian rank cancellation; reflection with retained fixed-point sum; either equality orientation',
     'weights retain parameters', 'finite objects', 'original weight ring, including characteristic two', None,
     'involution and sign proofs; fixed points proved zero or retained with their full weights'),
 'triangular_difference_ring': scope('whole-side prefix sums over evaluable nested sum/product towers; local polynomial relations as fallback',
     'geometric products and index-independent scalar parameters', 'nested prefix towers',
     'QQ construction; original-field multiplier replay', 'local shift / invariant induction',
     'strong difference-field antidifference, evaluated shifts and endpoints; or local relation certificates; general high-order/finite algebraic source bridges remain absent',
     {'atoms':32,'invariant_indices':4,'polynomial_degree':'budget.max_degree','terms':'budget.max_unknowns'}),
 'finite_kernel_certificate': scope('concrete square finite kernels, or triangular transpose template', 'scalar parameters',
     'Fin m, m=1..5; transpose separately', 'symbolic field with original denominator proofs', None,
     'computed inverse/composition action, or verified transpose', {'matrix_size':5}),
 'finite_spectral_certificate': scope('concrete weighted finite cross pairing equal to zero', 'scalar parameters',
     'Fin m, m=1..5', 'original field with separation obligations', None,
     'computed self-adjoint separator; full-family norms are not generated', {'matrix_size':5}),
 'determinant_certificate': scope('concrete square determinant, or registered structural determinant rules', 'scalar parameters',
     'Fin m, m=1..5; structural rules separately', 'original field; division-free branch available', None,
     'PLU/Berkowitz replay or structural computation', {'matrix_size':5}),
 'finite_omega_elimination': scope('finite Laurent projection, ordered chains, rectangles', 'formal weights',
     'finite template domains', 'finite Laurent sums with explicit projection semantics', None,
     'finite templates; general graded rational Omega coefficient bridge not yet available'),
}
if set(SCOPES) != set(BACKENDS):
    raise RuntimeError('capability registry does not match active backends')


def annotate(candidate):
    result = deepcopy(candidate)
    name = result['backend']
    # A legacy Boolean alone does not certify the input domain.
    check = dict(candidate='accepted' if result['applicable'] else 'rejected',
                 core_domain='unknown', proof_exit='unknown',
                 obligations=['Certify core representation and original-domain proof obligations'])
    check.update(result.pop('admission_checks', {}))
    check.update(backend=name, method=BACKENDS[name], scope=deepcopy(SCOPES[name]),
                 evidence=result['reason'], complete_original_proof=False)
    result['admission'] = check
    return result


def multisum_exit(model):
    """Necessary pre-construction exit checks; certificates remain unchecked."""
    supported = model['dimension']==2 and model['domain']=='simplex'
    return dict(core_domain='accepted', proof_exit='unknown' if supported else 'unavailable',
                input_shape=dict(dimension=model['dimension'], domain=model['domain']),
                obligations=(['Construct order-1 monic certificate and verify kernel/domain/initial data'] if supported else
                             ['Implement complete boundary and original-domain transport for this dimension/domain']))
