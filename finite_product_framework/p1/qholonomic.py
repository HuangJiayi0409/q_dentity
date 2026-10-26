"""Creative telescoping in a supplied finite-rank two-shift q-module.

Column states satisfy sigma_n(Y)=U*Y, sigma_k(Y)=V*Y. For a row h, construct
sum c_j sigma_n^j(h*Y) = Delta_k(r*Y). This is conditional on the supplied
module equations, not a claim that a benchmark expression satisfies them.
"""
from itertools import count
import sympy as s
from expressions import q,Q,X,n,k,expression,shift_ratio,rationalize
from qparameterized import primitive_relation
from qrational_system import shift,field_for,solve_system
from ore import OreResourceLimit


def validate_module(U,V,h):
    U,V,h=s.Matrix(U),s.Matrix(V),s.Matrix([list(h)])
    if U.rows<1 or U.rows!=U.cols or V.shape!=U.shape or h.cols!=U.rows:
        raise ValueError('compatible square n/k matrices and observable row required')
    field_for([*U,*V,*h],X,q)
    U=U.applyfunc(s.cancel);V=V.applyfunc(s.cancel);h=h.applyfunc(s.cancel)
    if s.cancel(U.det())==0 or s.cancel(V.det())==0:
        raise ValueError('unsupported_structure: invertible shift matrices required')
    compatibility=(shift(U,X,q)*V-shift(V,Q,q)*U).applyfunc(s.cancel)
    if compatibility!=s.zeros(U.rows):raise ValueError('incompatible n/k shift matrices')
    return U,V,h


def verify_relation(U,V,h,coefficients,certificate):
    """Exact check against the input matrices, independent of scalar bounds."""
    if not coefficients or all(s.cancel(c)==0 for c in coefficients):
        raise ValueError('invalid_certificate: zero telescoper')
    row=h;total=s.zeros(1,U.rows)
    for c in coefficients:
        if s.sympify(c).has(X):raise ValueError('telescoper coefficients must be independent of X')
        total+=c*row;row=(shift(row,Q,q)*U).applyfunc(s.cancel)
    certificate=s.Matrix([list(certificate)])
    if certificate.shape!=h.shape:raise ValueError('invalid certificate row shape')
    residual=(shift(certificate,X,q)*V-certificate-total).applyfunc(s.cancel)
    if residual!=s.zeros(1,U.rows):raise ValueError('invalid_certificate: coupled module residual is nonzero')
    return '0'


def search(U,V,h,budget,*,max_order=None):
    if max_order is not None and (type(max_order) is not int or max_order<0):
        raise ValueError('max_order must be nonnegative or null')
    if s.Matrix(U).rows>budget.max_states:raise OreResourceLimit('module rank exceeds state limit')
    U,V,h=validate_module(U,V,h)
    symbols={str(t):t for t in set().union(*(v.free_symbols for v in [*U,*V,*h]),{q,Q,X})}
    parse=lambda v:s.sympify(v,locals=symbols)
    parameters=set(symbols.values())-{X};rows=[h];attempts=[]
    for order in count() if max_order is None else range(max_order+1):
        if order:rows.append((shift(rows[-1],Q,q)*U).applyfunc(s.cancel))
        try:result=solve_system(V,[list(row) for row in rows],X,q,budget,normalize_index=order)
        except OreResourceLimit as exc:
            return dict(status='resource_exhausted',reason=str(exc),attempts=attempts,failed_order=order)
        attempts.append(dict(result,order=order))
        if result['status']!='constructed':continue
        coefficients=list(map(parse,result['coefficients']))
        certificate=list(map(parse,result['certificate_row']))
        verify_relation(U,V,h,coefficients,certificate)
        primitive=primitive_relation(coefficients,s.Integer(1),parameters)
        scale=parse(primitive.pop('certificate'))
        scaled=[s.cancel(scale*r) for r in certificate]
        verify_relation(U,V,h,list(map(parse,primitive['coefficients'])),scaled)
        primitive['certificate_row']=list(map(str,scaled))
        return dict(status='constructed',algorithm='finite-rank q-module creative telescoping with complete fixed-order rational solve',
            order=order,coefficients=result['coefficients'],certificate_row=result['certificate_row'],
            primitive_relation=primitive,n_shift_rows=[[str(v) for v in row] for row in rows],
            compatibility_residual='0',residual='0',attempts=attempts,
            minimality_scope='least order in the supplied free module and rational certificate class; additional state relations not assumed')
    return dict(status='search_exhausted',attempts=attempts,max_order=max_order,
        reason='no rational-certificate telescoper through max_order; no claim about all orders')


def module_from_summands(nodes,budget):
    """Build a diagonal module and merge demonstrably rational-equivalent terms.

    Only exact quotients representable in the existing source IR are merged.
    No assertion of independence is made for groups that remain separate.
    """
    if not isinstance(nodes,list) or not nodes:raise ValueError('nonempty summands list required')
    if len(nodes)>budget.max_unknowns:raise OreResourceLimit('source term count exceeds limit')
    bases=[];weights=[];members=[];mapping=[]
    for index,node in enumerate(nodes):
        F=expression(node)
        if F.has(s.Float,s.nan,s.zoo,s.oo,-s.oo):raise ValueError('unsupported_domain: finite exact summands required')
        if F==0:
            mapping.append(dict(source_index=index,group=None,multiplier='0'));continue
        for group,base in enumerate(bases):
            try:ratio=rationalize(s.cancel(F/base))
            except ValueError:continue
            field_for([ratio],X,q)
            restored=ratio.subs({Q:q**n,X:q**k})
            if s.cancel(s.powsimp(F/(base*restored),force=True)-1)!=0:continue
            weights[group]=s.cancel(weights[group]+ratio);members[group].append(index)
            mapping.append(dict(source_index=index,group=group,multiplier=str(ratio)))
            break
        else:
            if len(bases)>=budget.max_states:raise OreResourceLimit('derived source module rank exceeds state limit')
            bases.append(F);weights.append(s.Integer(1));members.append([index])
            mapping.append(dict(source_index=index,group=len(bases)-1,multiplier='1'))
    if not bases:bases=[s.Integer(1)];weights=[s.Integer(0)];members=[[]]
    Us=[rationalize(shift_ratio(F,n)) for F in bases]
    Vs=[rationalize(shift_ratio(F,k)) for F in bases]
    U,V,h=validate_module(s.diag(*Us),s.diag(*Vs),weights)
    return U,V,h,dict(basis_expressions=list(map(str,bases)),group_members=members,source_mapping=mapping,
        reduction_policy='exact rational quotient recognition in the existing expression IR; unmerged groups are not certified independent')


def compute(solver,data,budget,parse):
    frontend=None
    source_input=solver=='q_holonomic' and isinstance(data,dict) and set(data)=={'summands'}
    expected={'k_matrix','rhs_basis'} if solver=='parameterized_q_system' else {'n_matrix','k_matrix','observable'}
    if not source_input and (not isinstance(data,dict) or set(data)!=expected):
        raise ValueError('unexpected matrix solver input; targets, certificates, and guessed bounds are not accepted')
    def matrix(node,square=False):
        if not isinstance(node,list) or not node or any(not isinstance(row,list) or not row for row in node):
            raise ValueError('nonempty matrix rows required')
        width=len(node[0])
        if any(len(row)!=width for row in node) or (square and len(node)!=width):
            raise ValueError('rectangular matrix with compatible dimensions required')
        if width>budget.max_states or (square and len(node)>budget.max_states):
            raise OreResourceLimit('matrix dimension exceeds state limit')
        if not square and len(node)>budget.max_unknowns:
            raise OreResourceLimit('RHS count exceeds unknown limit')
        return s.Matrix([[parse(v) for v in row] for row in node])
    if source_input:
        U,V,h,frontend=module_from_summands(data['summands'],budget)
    else:V=matrix(data['k_matrix'],True)
    inputs=list(V)
    if solver=='parameterized_q_system':
        H=matrix(data['rhs_basis'])
        if H.cols!=V.rows:raise ValueError('RHS rows must have k_matrix dimension')
        inputs+=list(H)
        raw=solve_system(V,[list(H.row(j)) for j in range(H.rows)],X,q,budget,include_basis=True)
        normalized=dict(k_matrix=[[str(v) for v in V.row(j)] for j in range(V.rows)],
                        rhs_basis=[[str(v) for v in H.row(j)] for j in range(H.rows)])
    else:
        if not source_input:
            U=matrix(data['n_matrix'],True)
            if not isinstance(data['observable'],list) or len(data['observable'])!=V.rows:
                raise ValueError('observable row must have matrix dimension')
            h=[parse(v) for v in data['observable']]
        inputs+=list(U)+list(h)
        raw=search(U,V,h,budget,max_order=budget.max_order)
        normalized=dict(n_matrix=[[str(v) for v in U.row(j)] for j in range(U.rows)],
            k_matrix=[[str(v) for v in V.row(j)] for j in range(V.rows)],observable=list(map(str,h)))
    output=dict(status=raw['status'],solver=solver,result=raw,normalized_input=normalized)
    if frontend is not None:output['source_frontend']=frontend
    symbols={str(t):t for t in set().union(*(v.free_symbols for v in inputs),{q,Q,X})}
    read=lambda v:s.sympify(v,locals=symbols)
    outputs=[]
    if raw['status']=='constructed':
        relation=raw.get('primitive_relation',raw)
        outputs+=list(map(read,relation['coefficients']+relation['certificate_row']))
        if solver=='q_holonomic':
            output['operator']=dict(variable='n',shift='n -> n+1; Q -> q*Q',order=raw['order'],
                coefficients=relation['coefficients'],leading_coefficient=relation['leading_coefficient'])
    denoms=lambda values:sorted({str(s.factor(s.fraction(s.cancel(v))[1])) for v in values if s.fraction(s.cancel(v))[1]!=1})
    output['domain']=dict(coefficient_field='QQ(q,Q,independent parameters)(X)',
        base='q is an indeterminate; characteristic zero',normalized_input_denominators=denoms(inputs),
        output_denominators=denoms(outputs),input_module_equations_are_premises=solver=='q_holonomic' and not source_input,
        specialization_policy='generic formal field only; singular parameter values not discharged',
        algorithm_scope='complete rational solve for each fixed RHS basis; outer telescoper order search is resource bounded',
        boundary_policy='finite-sum boundaries, initial values, and source-to-module derivation remain external')
    return output
