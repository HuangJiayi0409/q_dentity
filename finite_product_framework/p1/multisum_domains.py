"""Finite lattice support and oriented boundaries, independent of dimension.

Enumeration is diagnostic/test machinery, not a proof for symbolic n. The
generic finite-domain divergence theorem lives in lean/MultisumRules.lean.
"""
from itertools import product
from math import comb


def support(dimension, n, kind='simplex', max_points=100000):
    if type(dimension) is not int or dimension<1 or type(n) is not int or n<0:
        raise ValueError('invalid_domain: positive dimension and natural size required')
    if kind not in ('simplex','box'):raise ValueError('unsupported_domain')
    count=comb(n+dimension,dimension) if kind=='simplex' else (n+1)**dimension
    if count>max_points:raise ValueError('resource_exhausted: support enumeration budget')
    if kind=='box':return frozenset(product(range(n+1),repeat=dimension))
    def generate(d,left):
        if d==0:
            yield ()
        else:
            for x in range(left+1):
                for tail in generate(d-1,left-x):yield (x,)+tail
    return frozenset(generate(dimension,n))


def translate(domain,vector):
    vector=tuple(vector)
    if any(len(x)!=len(vector) for x in domain):raise ValueError('invalid_domain: dimension mismatch')
    return frozenset(tuple(a+b for a,b in zip(x,vector)) for x in domain)


def boundary(domain,vector):
    shifted=translate(domain,vector)
    return {'positive':shifted-domain,'negative':domain-shifted}


def moving_shell(old,new):
    return {'positive':new-old,'negative':old-new}


def divergence(domain,fluxes):
    """Exact evaluation check on a concrete finite domain; never train coverage."""
    dimension=len(fluxes)
    vectors=[tuple(int(i==j) for j in range(dimension)) for i in range(dimension)]
    local=sum(sum(g(tuple(a+b for a,b in zip(x,v)))-g(x) for v,g in zip(vectors,fluxes)) for x in domain)
    faces=[boundary(domain,v) for v in vectors]
    total=sum(sum(g(x) for x in face['positive'])-sum(g(x) for x in face['negative'])
              for g,face in zip(fluxes,faces))
    return local,total,faces
