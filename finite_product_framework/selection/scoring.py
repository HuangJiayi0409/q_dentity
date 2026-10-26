"""AHP weights and fixed-reference TOPSIS, with explicit uncertainty intervals."""
import math

CRITERIA = ('structure', 'conditions', 'reconstruction', 'conversion')
# Engineering judgements, not fitted success frequencies. Ratios correspond to
# priorities 4:2:4:1, so consistency is exact. AHP consistency is not accuracy.
PAIRWISE = ((1, 2, 1, 4), (.5, 1, .5, 2), (1, 2, 1, 4), (.25, .5, .25, 1))


def ahp(matrix=PAIRWISE):
    n = len(matrix)
    if n != 4 or any(len(row) != n for row in matrix):
        raise ValueError('AHP requires a four-by-four matrix')
    a = [[float(x) for x in row] for row in matrix]
    if any(not math.isfinite(x) or x <= 0 for row in a for x in row):
        raise ValueError('AHP entries must be finite and positive')
    if any(abs(a[i][i]-1) > 1e-9 or any(abs(a[i][j]*a[j][i]-1) > 1e-9
               for j in range(n)) for i in range(n)):
        raise ValueError('AHP matrix must be reciprocal with unit diagonal')
    w = [1/n]*n
    for _ in range(1000):
        v = [sum(a[i][j]*w[j] for j in range(n)) for i in range(n)]
        total = sum(v)
        if not math.isfinite(total): raise ValueError('AHP numerical overflow')
        v = [x/total for x in v]
        delta = max(abs(x-y) for x, y in zip(w, v)); w = v
        if delta < 1e-13: break
    else: raise ValueError('AHP iteration did not converge')
    eigenvalue = sum(sum(a[i][j]*w[j] for j in range(n))/w[i] for i in range(n))/n
    ci = max(0., (eigenvalue-n)/(n-1)); cr = ci/.90
    if cr > .10: raise ValueError('AHP consistency ratio exceeds 0.10')
    return dict(matrix=a, weights=dict(zip(CRITERIA, w)), lambda_max=eigenvalue,
                consistency_index=ci, consistency_ratio=cr, random_index=.90,
                origin='declared engineering priorities; no performance training')


def interval(lower=0., upper=1., *, reason, evidence=()):
    lo, hi = float(lower), float(upper)
    if not (math.isfinite(lo) and math.isfinite(hi) and 0 <= lo <= hi <= 1):
        raise ValueError('invalid score interval')
    return dict(lower=lo, upper=hi, known=lo == hi, reason=reason, evidence=list(evidence))


def exact(value, reason, evidence=()):
    return interval(value, value, reason=reason, evidence=evidence)


def topsis(values, weights):
    """Euclidean distances after weighting: v_j=w_j*s_j, ideals w and 0.

    The scale and ideals do not depend on the candidate set. This function is
    coordinatewise monotone, so interval endpoints give valid score bounds.
    """
    if set(values) != set(CRITERIA) or set(weights) != set(CRITERIA):
        raise ValueError('criterion mismatch')
    if any(not math.isfinite(weights[k]) or weights[k] <= 0 for k in CRITERIA):
        raise ValueError('positive finite weights required')
    if any(not math.isfinite(values[k]) or not 0 <= values[k] <= 1 for k in CRITERIA):
        raise ValueError('scores must be in [0,1]')
    positive = math.sqrt(sum((weights[k]*(1-values[k]))**2 for k in CRITERIA))
    negative = math.sqrt(sum((weights[k]*values[k])**2 for k in CRITERIA))
    return negative/(positive+negative)


def bounds(criteria, weights):
    for k in CRITERIA:
        interval(criteria[k]['lower'], criteria[k]['upper'], reason='validation')
    return dict(lower=topsis({k: criteria[k]['lower'] for k in CRITERIA}, weights),
                upper=topsis({k: criteria[k]['upper'] for k in CRITERIA}, weights))
