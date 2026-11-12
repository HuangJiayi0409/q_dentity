"""Source-bound weighted choices for the actual finite q-binomial product.

The Gaussian-to-subset representation is retained as an explicit pending
bridge. Matching its syntax does not assume that representation theorem.
"""
from pathlib import Path
import re
from .formal_frontend import _Unsupported,_closed_prefix,_node,_num,_var
from .models import Source
from .recurrence_frontend import RecurrenceParser,_bounded_ast,_check,lean
from .storage import IntegrityError,verify_source,sha256_file

PROFILE='qbinomial_ranked_choices_v1'


def core_request():
    selected={'coefficient':-1,'z_power':1,'q_index_multiplier':1}
    return {'schema_version':1,'method':'combinatorial','input':{
        'operation':'ranked_boolean_choices','scalar_domain':'commutative_field',
        'domain':{'kind':'range','bound':'n'},'rank_upper_offset':1,
        'selected_weight':dict(selected),'factor':{'constant':1,'selected':dict(selected)},
        'rank_weight':{'sign_base':-1,'z_rank_multiplier':1,'q_index_multiplier':1},
        'max_candidates':2}}


def definition_binding():
    path=Path(__file__).resolve().parents[1]/'benchmark/lean/Benchmark/Definitions.lean'
    text=path.read_text();declarations={}
    patterns={
        'poch':r'(?m)^def poch \{K : Type\*\} \[CommRing K\] \(a q : K\) \(n : ℕ\) : K :=\s*\n\s*∏ j ∈ Finset\.range n, \(1 - a \* q \^ j\)\s*\n',
        'gaussian':r'(?m)^def gaussian \{K : Type\*\} \[CommRing K\] \(q : K\) : ℕ → ℕ → K\s*\n  \| _, 0 => 1\s*\n  \| 0, _\+1 => 0\s*\n  \| n\+1, k\+1 => gaussian q n k \+ q\^\(k\+1\) \* gaussian q n \(k\+1\)\s*\n'}
    for name,pattern in patterns.items():
        matches=list(re.finditer(pattern,text))
        if len(matches)!=1 or 'namespace FiniteQBenchmark' not in text[:matches[0].start()]:
            raise IntegrityError('fixed combinatorial source definition differs: '+name)
        declarations[name]=matches[0].group().strip()
    return {'path':str(path),'sha256':sha256_file(path),'declarations':declarations,
        'poch_role':'source factor extraction by the actual finite-product definition',
        'gaussian_role':'source object identification only; its subset representation remains pending',
        'formal_verification':'not performed; definition-derived symbolic provenance only'}


def analyze_source(source,run_root=None):
    bound=Source.from_dict(source);verify_source(bound,run_root)
    if bound.Gamma!=bound.declaration:raise IntegrityError('combinatorial original context binding mismatch')
    failure={'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem,field,binders,equation=RecurrenceParser(bound.declaration).source();_bounded_ast(equation)
        if theorem!=bound.theorem:raise IntegrityError('combinatorial theorem binding mismatch')
        names=[b['name'] for b in binders if b['name']]
        context={b['name']:b['type'] for b in binders[2:]}
        if len(names)!=len(set(names)) or any(t not in (field,'ℕ','True') for t in context.values()):
            raise _Unsupported('unsupported original parameter domain or hypothesis')
        if equation['op']!='=' or not all(_check(a,field,context,field) for a in equation['args']):
            raise _Unsupported('typed scalar equality required')
        left,right=equation['args'];total,target=(left,right) if left['op']=='sum' else (right,left)
        if total['op']!='sum' or target['op']!='poch':
            raise _Unsupported('finite Gaussian generating sum and Pochhammer product required')
        z,q,n=target['args']
        if any(x['op']!='var' for x in (z,q,n)) or len({x['name'] for x in (z,q,n)})!=3:
            raise _Unsupported('distinct original scalar/base/length binders required')
        if [context.get(x['name']) for x in (z,q,n)]!=[field,field,'ℕ']:
            raise _Unsupported('Pochhammer parameter domains differ')
        k=_var(total['index'])
        expected=_node('*',_node('*',_node('*',_node('^',_node('neg',_num(1)),k),
            _node('^',z,k)),_node('^',q,_node('/',_node('*',k,_node('-',k,_num(1))),_num(2)))),
            _node('gaussian',q,n,k))
        if total['range']!=_node('Finset.range',_node('+',n,_num(1))) or total['body']!=expected:
            raise _Unsupported('unsupported rank range, sign, triangular exponent or Gaussian coefficient')
        original=_closed_prefix(binders)+', '+lean(equation)
        if bound.proposition is not None and bound.proposition!=original:
            raise IntegrityError('combinatorial original proposition binding mismatch')
        qname,zname,nname=(x['name'] for x in (q,z,n))
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'symbols':{'field':field,'base':qname,'parameter':zname,'bound':nname,'index':total['index']},
            'original_proposition':original,'equation':equation,
            'orientation':'sum_equals_target' if total is left else 'target_equals_sum',
            'core_request':core_request(),'definition_binding':definition_binding(),
            'mapping':{'n':nname,'q':qname,'z':zname,'scalar_target':lean(target),
                'ground_set':'Finset.range '+nname,'rank_range':'Finset.range ('+nname+'+1)',
                'source_factor':'1 - '+zname+' * '+qname+'^i',
                'selected_factor':'(-1) * '+zname+' * '+qname+'^i',
                'rank_weight':'(-1)^k * '+zname+'^k * ∏ i ∈ s, '+qname+'^i',
                'source_triangular_exponent':'natural truncated subtraction and natural division retained',
                'ranked_subset_domain':'pairs (k,s) with s ⊆ range n and card(s)=k',
                'choice_domain':'Boolean-valued functions on the symbolic finite range n',
                'source_slice':'actual Pochhammer product; no Gaussian-to-subset bridge assumed'},
            'gaussian_subset_bridge':{'status':'pending','verified':False,
                'source_coefficient':lean(_node('*',expected['args'][0]['args'][1],_node('gaussian',q,n,k))),
                'required_statement':'fixed-rank subset q-weight equals q^(k*(k-1)/2)*gaussian q n k',
                'used_as_assumption':False},
            'involution_scope':{'construction':'weight-preserving bijection',
                'sign_reversal_used':False,'fixed_point_cancellation_used':False},
            'bound_specialized':False,'adds_original_assumptions':False,'formal_bridge_available':False,
            'remaining_work':['Gaussian fixed-rank subset weight bridge remains pending.',
                'Lean verification of finite domain bijections, weighted sum transport, product expansion and original theorem remains pending.']}
    except (_Unsupported,RecursionError,KeyError,IndexError) as error:
        return dict(failure,reason=str(error))
