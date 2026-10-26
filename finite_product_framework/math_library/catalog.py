"""One JSON-serializable source of mathematical templates and proof references.

These are definitions and local structural properties, never target identities
or another method's certificate-search algorithm. Typed operators distinguish
Nat subtraction/division, integer powers and field arithmetic.
"""

SCHEMA = 'finite-q-math-library/1'


def op(name, *args):
    return [name, *args]


def call(name, *args):
    return ['call', 'FiniteQBenchmark.' + name, *args]


def lit(n, sort='Nat'):
    return ['literal', sort, n]


def rule(key, subject, purpose, parameters, lhs, rhs, *, requires=(), ring='CommRing',
         proof=None, kind='local_relation'):
    return dict(id=key, subject='FiniteQBenchmark.' + subject if '.' not in subject else subject,
                purpose=purpose, parameters=[dict(name=n, sort=s) for n,s in parameters],
                algebra=ring, lhs=lhs, rhs=rhs, requires=list(requires), kind=kind,
                lean=dict(name='FiniteQMathLibrary.' + (proof or key), module='Benchmark.MathLibraryRules',
                          source='finite_product_framework/math_library/lean/Rules.lean'),
                method_core=False)


a,q,n,m,k,d = ('$'+v for v in ('a','q','n','m','k','d'))
zero,one = lit(0),lit(1)
scalar_zero,scalar_one = lit(0,'K'),lit(1,'K')
add=lambda x,y:op('nat_add',x,y)
mul=lambda x,y:op('mul',x,y)
pow=lambda x,y:op('pow',x,y)
poch=lambda x,y,z:call('poch',x,y,z)
range_sum=lambda bound,body:op('sum_range',bound,'i',body)

RULES = [
    rule('poch_definition','poch','finite_product',[('a','K'),('q','K'),('n','Nat')],
         poch(a,q,n),op('prod_range',n,'i',op('sub',scalar_one,mul(a,pow(q,'@i')))),kind='definition'),
    rule('poch_zero','poch','initial_value',[('a','K'),('q','K')],poch(a,q,zero),scalar_one),
    rule('poch_successor','poch','length_shift',[('a','K'),('q','K'),('n','Nat')],
         poch(a,q,add(n,one)),mul(poch(a,q,n),op('sub',scalar_one,mul(a,pow(q,n))))),
    rule('poch_split','poch','split_product',[('a','K'),('q','K'),('m','Nat'),('n','Nat')],
         poch(a,q,add(m,n)),mul(poch(a,q,m),poch(mul(a,pow(q,m)),q,n))),
    rule('poch_shift_cross','poch','parameter_shift_without_division',
         [('a','K'),('q','K'),('d','Nat'),('k','Nat')],
         mul(poch(mul(a,pow(q,d)),q,k),poch(a,q,d)),
         mul(poch(a,q,k),poch(mul(a,pow(q,k)),q,d))),
    rule('poch_shift_quotient','poch','parameter_shift_quotient',
         [('a','K'),('q','K'),('d','Nat'),('k','Nat')],
         poch(mul(a,pow(q,d)),q,k),op('div',mul(poch(a,q,k),poch(mul(a,pow(q,k)),q,d)),poch(a,q,d)),
         requires=[op('ne',poch(a,q,d),scalar_zero)],ring='Field'),
    rule('pochList_nil','pochList','literal_list',[('q','K'),('n','Nat')],
         call('pochList',op('nil'),q,n),scalar_one,kind='definition'),
    rule('pochList_cons','pochList','literal_list',[('a','K'),('as','ListK'),('q','K'),('n','Nat')],
         call('pochList',op('cons',a,'$as'),q,n),mul(poch(a,q,n),call('pochList','$as',q,n)),kind='definition'),
    rule('rogersSzego_sum','rogersSzego','finite_sum',[('t','K'),('q','K'),('n','Nat')],
         call('rogersSzego','$t',q,n),range_sum(add(n,one),mul(call('gaussian',q,n,'@i'),pow('$t','@i'))),kind='definition'),
    rule('phi_sum','phi','finite_sum',[('as','ListK'),('bs','ListK'),('q','K'),('z','K'),('n','Nat')],
         call('phi','$as','$bs',q,'$z',n),range_sum(add(n,one),call('phiTerm','$as','$bs',q,'$z','@i')),
         ring='Field',kind='definition'),
    rule('phiTerm_definition','phiTerm','hypergeometric_term',
         [('as','ListK'),('bs','ListK'),('q','K'),('z','K'),('k','Nat')],
         call('phiTerm','$as','$bs',q,'$z',k),
         mul(op('div',call('pochList','$as',q,k),call('pochList',op('cons',q,'$bs'),q,k)),
             mul(op('zpow',mul(pow(op('neg',scalar_one),k),
                              pow(q,op('nat_div',op('nat_mul',k,op('nat_sub',k,one)),lit(2)))),
                    op('int_sub',op('int_add',lit(1,'Int'),op('length_int','$bs')),op('length_int','$as'))),
                 pow('$z',k))),ring='Field',kind='definition'),
    rule('baileySum_sum','baileySum','finite_sum',[('a','K'),('q','K'),('alpha','NatToK'),('n','Nat')],
         call('baileySum',a,q,'$alpha',n),range_sum(add(n,one),
             op('div',op('apply','$alpha','@i'),mul(poch(q,q,op('nat_sub',n,'@i')),poch(mul(a,q),q,add(n,'@i'))))),
         ring='Field',kind='definition'),
    rule('geometric_sum','geometric','finite_sum',[('q','K'),('n','Nat')],
         call('geometric',q,n),range_sum(n,pow(q,'@i')),ring='Field',kind='definition'),
    rule('unitBailey_zero','unitBailey','initial_value',[('a','K'),('q','K')],
         call('unitBailey',a,q,zero),scalar_one,ring='Field'),
    rule('unitBailey_positive','unitBailey','positive_branch',[('a','K'),('q','K'),('n','Nat')],
         call('unitBailey',a,q,n),op('div',
             mul(mul(mul(pow(op('neg',scalar_one),n),pow(q,op('nat_div',op('nat_mul',n,op('nat_sub',n,one)),lit(2)))),
                     op('sub',scalar_one,mul(a,pow(q,op('nat_mul',lit(2),n))))),poch(mul(a,q),q,op('nat_sub',n,one))),
             poch(q,q,n)),requires=[op('ne',n,zero)],ring='Field'),
    rule('gaussian_successor','gaussian','local_recurrence',[('q','K'),('n','Nat'),('k','Nat')],
         call('gaussian',q,add(n,one),add(k,one)),
         op('add',call('gaussian',q,n,k),mul(pow(q,add(k,one)),call('gaussian',q,n,add(k,one))))),
    rule('sum_Ico','Finset.sum','interval_to_range',[('f','NatToK'),('a','Nat'),('b','Nat')],
         op('sum_Ico',a,'$b','i',op('apply','$f','@i')),
         range_sum(op('nat_sub','$b',a),op('apply','$f',add(a,'@i')))),
    rule('sum_Icc','Finset.sum','interval_to_range',[('f','NatToK'),('a','Nat'),('b','Nat')],
         op('sum_Icc',a,'$b','i',op('apply','$f','@i')),
         range_sum(op('nat_sub',add('$b',one),a),op('apply','$f',add(a,'@i')))),
]

# Source signatures come from actual Lean declarations, not spelling heuristics.
# This prefix currently applies only to these explicitly registered definitions.
OBJECTS = {
    'poch': (['K','K','Nat'], 'CommRing', 'Definitions'),
    'pochList': (['ListK','K','Nat'], 'CommRing', 'Definitions'),
    'rogersSzego': (['K','K','Nat'], 'CommRing', 'Definitions'),
    'phi': (['ListK','ListK','K','K','Nat'], 'Field', 'Definitions'),
    'phiTerm': (['ListK','ListK','K','K','Nat'], 'Field', 'Definitions'),
    'baileySum': (['K','K','NatToK','Nat'], 'Field', 'Definitions'),
    'geometric': (['K','Nat'], 'Field', 'Batch3Definitions'),
    'unitBailey': (['K','K','Nat'], 'Field', 'Definitions'),
    'gaussian': (['K','Nat','Nat'], 'CommRing', 'Definitions'),
}
OBJECTS = { 'FiniteQBenchmark.'+name: dict(
    symbol='FiniteQBenchmark.'+name, arguments=types, result='K', algebra=ring,
    implicit_prefix=2, source='benchmark/lean/Benchmark/'+module+'.lean',
    declaration=name, rule_ids=[r['id'] for r in RULES if r['subject']=='FiniteQBenchmark.'+name])
    for name,(types,ring,module) in OBJECTS.items() }

# Only this newly supported wrapper is unfolded at the original P1 entry.
# Existing phi/Rogers-Szegő routes retain their established reconstruction.
ENTRY_UNFOLDS = ['geometric_sum']
