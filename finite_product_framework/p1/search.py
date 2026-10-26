"""q-WZ target-guided construction using the q-Gosper antidifference algorithm."""
import sympy as s
from qgosper import Budget, UnsupportedDomain, antidifference


def search(n_shift, k_shift, coefficient, x, base, budget=Budget()):
    # D(n,k) = F(n,k) * W(q^k). The q-Gosper input is D, not F alone.
    W = s.cancel(n_shift-coefficient)
    if W == 0:
        return {'status': 'constructed', 'algorithm': 'q-Gosper zero-difference case',
                'certificate': '0', 'rational_residual': '0'}
    down_ratio = s.cancel(k_shift.subs(x, x/base)*W/W.subs(x, x/base))
    try:
        result = antidifference(down_ratio, x, base, budget)
    except UnsupportedDomain as exc:
        return {'status': 'unsupported_domain', 'reason': str(exc), 'algorithm': 'q-Gosper'}
    result['difference_over_summand'] = str(W)
    if result['status'] != 'constructed':
        return result
    S = result['antidifference_ratio']
    R = s.cancel(S*W)
    if s.cancel(k_shift*R.subs(x, base*x)-R-W) != 0:
        raise ArithmeticError('q-WZ local relation verification failed')
    result.update(antidifference_ratio=str(S), certificate=str(R),
                  q_wz_residual='0', sympy_version=s.__version__)
    return result
