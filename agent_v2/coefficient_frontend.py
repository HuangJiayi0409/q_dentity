"""Fully consumed finite q-binomial Source and its product coefficient slice.

The finite product is a representation of the actual Pochhammer target. Its
evaluation and coefficient bridges remain untrusted until one Lean candidate
proves them. No parameter is sampled and no Gaussian coefficient is assumed.
"""
from .formal_frontend import _Unsupported,_closed_prefix,_node,_num,_var
from .models import Source
from .recurrence_frontend import RecurrenceParser,_bounded_ast,_check,lean
from .storage import IntegrityError,verify_source

PROFILE='qbinomial_product_coefficients_v1'


def coefficient_request():
    atom=lambda key,name:{'op':'atom','key':key,'display':name}
    binary=lambda op,a,b:{'op':op,'args':[a,b]}
    u,v,w,z0=(atom(i,name) for i,name in enumerate(('u','v','w','z0')))
    one={'op':'integer','value':1}
    mul=lambda a,b:binary('HMul.hMul',a,b)
    add=lambda a,b:binary('HAdd.hAdd',a,b)
    sub=lambda a,b:binary('HSub.hSub',a,b)
    return {'schema_version':1,'method':'coefficient','input':{'goals':[
        {'lhs':add(mul(v,one),mul(u,{'op':'neg','arg':w})),
         'rhs':sub(v,mul(w,u))},
        {'lhs':mul(z0,one),'rhs':z0}]}}


def analyze_source(source,run_root=None):
    bound=Source.from_dict(source);verify_source(bound,run_root)
    if bound.Gamma!=bound.declaration:raise IntegrityError('coefficient original context binding mismatch')
    failure={'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem,field,binders,equation=RecurrenceParser(bound.declaration).source()
        _bounded_ast(equation)
        if theorem!=bound.theorem:raise IntegrityError('coefficient theorem binding mismatch')
        names=[b['name'] for b in binders if b['name']]
        context={b['name']:b['type'] for b in binders[2:]}
        if len(names)!=len(set(names)) or any(t not in (field,'ℕ','True') for t in context.values()):
            raise _Unsupported('unsupported original parameter domain or hypothesis')
        if equation['op']!='=' or not all(_check(a,field,context,field) for a in equation['args']):
            raise _Unsupported('typed scalar equality required')
        left,right=equation['args']
        total,target=(left,right) if left['op']=='sum' else (right,left)
        if total['op']!='sum' or target['op']!='poch':
            raise _Unsupported('finite Gaussian generating sum and Pochhammer target required')
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
            raise _Unsupported('unsupported generating coefficient, finite range, or natural triangular exponent')
        original=_closed_prefix(binders)+', '+lean(equation)
        if bound.proposition is not None and bound.proposition!=original:
            raise IntegrityError('coefficient original proposition binding mismatch')
        qname,zname,nname=(x['name'] for x in (q,z,n))
        index='qv2degree'
        while index in names or index==total['index']:index+='x'
        polynomial=f'AgentV2Coefficient.pochPolynomial {qname} {nname}'
        atoms={
            'u':{'meaning':'coefficient at the arbitrary natural index','lean':f'({polynomial}).coeff {index}'},
            'v':{'meaning':'coefficient at the successor natural index','lean':f'({polynomial}).coeff ({index}+1)'},
            'w':{'meaning':'coefficient of the next actual Pochhammer factor','lean':f'{qname}^{nname}'},
            'z0':{'meaning':'zero coefficient of the same product','lean':f'({polynomial}).coeff 0'}}
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'symbols':{'field':field,'base':qname,'parameter':zname,'bound':nname,'index':total['index']},
            'coefficient_index':index,'original_proposition':original,'equation':equation,
            'orientation':'sum_equals_target' if total is left else 'target_equals_sum',
            'core_request':coefficient_request(),'coefficient_atoms':atoms,
            'representation':{'polynomial':polynomial,'scalar_target':lean(target),
                'evaluation_parameter':zname,'factor_index_range':'Finset.range '+nname,
                'next_factor':f'(1 - Polynomial.C ({qname}^{nname}) * Polynomial.X)'},
            'finite_convolution':{'zero_index_separate':True,'positive_index':index+'+1',
                'surviving_factor_degrees':[0,1],'higher_factor_coefficients':0,
                'source_triangular_exponent':'natural truncated subtraction and natural division retained verbatim'},
            'all_natural_indices':True,'adds_original_assumptions':False,
            'remaining_work':['Gaussian coefficient relation and original identity remain open']}
    except (_Unsupported,RecursionError) as error:
        return dict(failure,reason=str(error))
