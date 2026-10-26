"""Versioned structural rules for every live backend, without invoking it.

These are conservative selection signals, not copies of the mathematical
solvers. Each route keeps its own four scores and unresolved obligations.
"""
from .scoring import exact, interval
from .features import SCALAR

RULE_VERSION = 'structural-rules/1'
Q_ATOMS = {'FiniteQBenchmark.poch', 'FiniteQBenchmark.pochInt',
           'FiniteQBenchmark.pochList', 'FiniteQBenchmark.pochListInt',
           'FiniteQBenchmark.gaussian', 'FiniteQBenchmark.gaussianInt',
           'FiniteQBenchmark.gaussianQuotient', 'FiniteQBenchmark.phi'}
POCH = {s for s in Q_ATOMS if '.poch' in s}
GAUSSIAN = Q_ATOMS - POCH - {'FiniteQBenchmark.phi'}
OMEGA = {'FiniteQMacMahon.omegaGE', 'FiniteQMacMahon.omegaAll',
         'FiniteQBenchmark.rectangleWeight', 'FiniteQMacMahon.rectangleSeries',
         'FiniteQMacMahon.coneProduct', 'FiniteQMacMahon.geometric',
         'FiniteQMacMahon.gaussianSeries'}

# Every entry corresponds to a live method-local construction route. A failed
# computed matrix route does not eliminate the separate structural fallback.
ROUTES = (
    ('gosper', 'direct_q_gosper', 'telescoping', 'p1/GENERAL_SUMMATION.md'),
    ('bibasic', 'bibasic_gosper', 'telescoping', 'p1/bibasic_pipeline.py'),
    ('first_order', 'target_first_order', 'recurrence', 'p1/lean_pipeline.py'),
    ('zeilberger', 'general_q_zeilberger', 'recurrence', 'p1/GENERAL_SUMMATION.md'),
    ('ore', 'ore_closure', 'recurrence', 'p1/DEFINED_RELATION.md'),
    ('multisum', 'multisum', 'recurrence', 'p1/multisum_pipeline.py'),
    ('coefficient', 'cauchy_coefficient', 'coefficient', 'p2/run.py'),
    ('product', 'finite_product_indices', 'product', 'product/pipeline.py'),
    ('primitive_root_product', 'finite_product_indices', 'product', 'product/COMPLETION.md'),
    ('polynomial', 'polynomial_interpolation', 'interpolation', 'interpolation/pipeline.py'),
    ('principal_parts', 'rational_principal_parts', 'interpolation', 'interpolation/pipeline.py'),
    ('operator_word', 'operator_word_normalization', 'noncommutative', 'noncommutative/pipeline.py'),
    ('bijection', 'weighted_bijection', 'combinatorial', 'combinatorial/pipeline.py'),
    ('involution', 'sign_reversing_involution', 'combinatorial', 'combinatorial/pipeline.py'),
    ('difference_tower', 'triangular_difference_ring', 'difference_ring', 'difference_ring/pipeline.py'),
    ('kernel_matrix', 'finite_kernel_certificate', 'kernel_transform', 'workflow/matrix_synthesis.py'),
    ('kernel_transpose', 'finite_kernel_certificate', 'kernel_transform', 'kernel_transform/pipeline.py'),
    ('spectral_matrix', 'finite_spectral_certificate', 'spectral', 'spectral/pipeline.py'),
    ('determinant_matrix', 'determinant_certificate', 'determinant', 'workflow/matrix_synthesis.py'),
    ('determinant_structure', 'determinant_certificate', 'determinant', 'determinant/pipeline.py'),
    ('omega', 'finite_omega_elimination', 'macmahon', 'macmahon/pipeline.py'),
)


def assess(features):
    f = features; symbols = set(f['symbols']); direct = set(f['direct_symbols'])
    eq = f['goal_head'] == 'Eq'; opaque = bool(f['unknown_symbols'])
    hidden = opaque or bool(f['definition_expansions'])
    sums = [o for o in f['objects'] if o['kind'] == 'Finset.sum' and not o['expansion']]
    products = [o for o in f['objects'] if o['kind'] == 'Finset.prod' and not o['expansion']]
    has_sum = bool(sums) or 'FiniteQBenchmark.phi' in direct
    has_product = bool(products) or bool(POCH & direct)
    prefix = bool(sums or products) and all(o['domain'] == 'Finset.range' for o in sums+products)
    nested = any(o['depth'] > 0 for o in sums)
    q = bool(Q_ATOMS & direct); gaussian = bool(GAUSSIAN & direct)
    nat = f['natural_parameter_count'] > 0
    finite_matrix = bool(f['fin_sizes']) and all(n is not None and 1 <= n <= 5 for n in f['fin_sizes'])
    determinant_sizes=[d['size'] for d in f['dimensions'] if d['kind']=='Matrix.det' and d['top_level'] and not d['expansion']]
    determinant_finite=bool(determinant_sizes) and all(n is not None and 1<=n<=5 for n in determinant_sizes)
    outside_determinant=bool(determinant_sizes) and all(n is not None and not 1<=n<=5 for n in determinant_sizes)
    sides = f['side_heads']; paired_sums = sides == ['Finset.sum', 'Finset.sum']
    scalar = f['scalar_grammar']
    division = bool({'HDiv.hDiv', 'Inv.inv'} & direct)
    result = []
    for route, backend, method, source in ROUTES:
        signal = False; strong = False; reconstruction = None; steps = None
        conditions = interval(reason='Input/domain obligations not fully determined by cheap inspection')
        obligations = ['Construct a certificate, discharge all actual side conditions, and verify the original theorem']
        reason = ''; hard = None
        if route == 'gosper':
            signal = has_sum
            strong = eq and signal and q and prefix and not nested and not nat and not opaque
            reason = 'Finite sum; direct q-Gosper still has to construct an antidifference'
            if signal: reconstruction = .5
        elif route == 'bibasic':
            signal = has_sum and q
            reason = 'q-product sum; two independent bases and the bibasic grammar remain unchecked'
        elif route == 'first_order':
            signal = gaussian and nat
            reason = 'Gaussian expression with a natural parameter; first-order relation is not assumed'
            if signal: reconstruction = .5
        elif route == 'zeilberger':
            signal = has_sum and nat
            strong = eq and signal and q and not nested and (prefix or 'FiniteQBenchmark.phi' in direct)
            reason = 'Parameterized finite q-sum; recurrence order, tails and singular coefficients remain obligations'
            if signal: reconstruction = .5
            if 'FiniteQBenchmark.phi' in direct:
                obligations.append('Actual phi bridge, moving lengths, denominator and support transport must succeed')
        elif route == 'ore':
            signal = 'FiniteQBenchmark.rogersSzego' in direct or gaussian or has_sum and nat
            strong = eq and 'FiniteQBenchmark.rogersSzego' in direct
            reason = 'Sequence/parameter structure; only implemented source-to-Ore bridges are usable'
            if signal: reconstruction = .5
        elif route == 'multisum':
            signal = nested and q
            reason = 'Nested q-sum; native multisum support must still be established'
        elif route == 'coefficient':
            signal = bool({'Polynomial.coeff', 'PowerSeries.coeff'} & direct) or has_sum or has_product
            strong = eq and bool({'Polynomial.coeff', 'PowerSeries.coeff'} & direct)
            reason = 'Coefficient or finite expansion structure; supported coefficient normalization must expose it'
            if strong: reconstruction = .5
        elif route == 'product':
            signal = has_product
            product_grammar = direct <= (SCALAR | POCH | {'Finset.prod', 'Finset.range'})
            strong = eq and signal and not has_sum and not opaque and product_grammar
            reason = 'Finite products/Pochhammer; bounded index and pointwise factor reconstruction'
            if signal: reconstruction = .5
            if strong and products and prefix: steps = 0
            if strong and not products and POCH & direct: steps = 1
        elif route == 'primitive_root_product':
            root = f['root_product']; signal = root is not None; strong = eq and signal
            reason = 'Exact prod(1-x*w^j)=1-x^m structure with scope-aware parameter matching'
            if root:
                known = int(root['positive'])+int(root['primitive'])
                conditions = interval(known/2, 1, reason='Positive order and matching IsPrimitiveRoot; missing facts stay unknown',
                    evidence=root['positive_evidence']+root['primitive_evidence'])
                reconstruction = 1.; steps = 0
                obligations.append('No use of w^m=1 as a replacement for IsPrimitiveRoot w m')
        elif route in ('polynomial', 'principal_parts'):
            signal = scalar and (division if route == 'principal_parts' else True)
            strong = eq and signal
            reason = 'Scalar algebraic syntax; characteristic-zero, degree/pole and domain obligations remain'
            if signal: reconstruction = .5; steps = 0 if not division else None
            if signal:
                domain=f['scalar_domain']; count=int(domain['field'])+int(domain['char_zero'])
                total=3 if division else 2
                conditions=interval(count/total, 1,
                    reason='Matching carrier Field and CharZero; source denominator conditions remain unknown when present',
                    evidence=domain['evidence'])
        elif route == 'operator_word':
            signal = bool({'FiniteQBenchmark.kacX', 'FiniteQBenchmark.kacM'} & direct) or 'HMul.hMul' in direct
            strong = eq and bool({'FiniteQBenchmark.kacX', 'FiniteQBenchmark.kacM'} & direct)
            reason = 'Multiplicative words/operator action; only bounded explicit powers and supported local relations'
            if strong: reconstruction = .5
        elif route == 'bijection':
            signal = paired_sums or bool({'Finset.powersetCard', 'Finset.powerset'} & direct)
            strong = eq and gaussian and 'Finset.powersetCard' in direct
            reason = 'Finite weighted objects or two sums; map/inverse/weight identities are not known yet'
            if signal: reconstruction = .5
        elif route == 'involution':
            signal = has_sum and bool({'Finset.powerset', 'Finset.range', 'Finset.Icc'} & direct)
            reason = 'Finite sum with available reflection/toggle templates; cancellation/fixed points unchecked'
            if signal: reconstruction = .5
        elif route == 'difference_tower':
            signal = has_sum or has_product or 'FiniteQBenchmark.fineC' in direct
            strong = eq and signal and prefix and nested
            reason = 'Evaluated sum/product tower; only existing local shift/invariant reconstruction'
            if signal: reconstruction = .5
        elif route in ('kernel_matrix', 'spectral_matrix'):
            signal = has_sum
            strong = eq and signal and finite_matrix
            if route == 'kernel_matrix': strong = strong and nested
            reason = 'Concrete Fin 1..5 matrix construction; kernel/pairing expression and certificate still unchecked'
            # Mixed/nested sum dimensions can be scalar entries, not the matrix
            # dimension. They must not cause a hard rejection of this route.
            if strong: reconstruction = .5
        elif route == 'kernel_transpose':
            signal = nested
            reason = 'Nested finite sum; triangular support transposition is a separate route from matrix inversion'
            if signal: reconstruction = .5
        elif route == 'determinant_matrix':
            signal = 'Matrix.det' in direct
            strong = eq and signal and determinant_finite
            reason = 'Explicit determinant with computed PLU/Berkowitz certificate, followed by Lean reconstruction'
            if outside_determinant: hard = 'Concrete dimension outside the 1..5 computed-matrix route'
            if strong: reconstruction = .5
        elif route == 'determinant_structure':
            signal = 'Matrix.det' in direct
            reason = 'Determinant structural evaluation; explicit formula pattern still unchecked'
            if signal: reconstruction = .5
        elif route == 'omega':
            signal = bool(OMEGA & direct); strong = eq and signal
            reason = 'Explicit Omega/chain object; only finite Omega and certified chain patterns'
            if signal: reconstruction = .5; steps = 0
        else: raise AssertionError('missing route assessor: '+route)
        # Non-equalities and opaque definitions cannot be rejected merely by the
        # absence of a visible symbol. Definitions may hide a supported object.
        if not eq:
            signal = False; strong = False; hard = None
        if hard:
            status = 'unsupported'; reason = hard
        elif signal:
            status = 'structural_match'
        elif hidden or not eq:
            status = 'unknown'
        else:
            status = 'unsupported'
            reason = 'Required visible structure absent in inspected transparent target: '+reason
        scores = dict(
            structure=exact(1. if strong else .5, reason, [f['target_node']]) if signal else interval(reason=reason),
            conditions=conditions,
            reconstruction=exact(reconstruction, 'Known source-form coverage only; construction and proof obligations remain')
                if reconstruction is not None else interval(reason='No complete static reconstruction assessment'),
            conversion=exact(1/(1+steps), 'Known entry conversion count: '+str(steps))
                if steps is not None else interval(reason='Conversion path not completely known'))
        if status=='structural_match' and not strong:
            obligations.append('Partial structural match only; complete frontend acceptance is not established')
        result.append(dict(route=route, backend=backend, method=method, status=status,
                           reason=reason, criteria=scores, contract=source, obligations=obligations))
    return result
