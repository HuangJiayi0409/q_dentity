"""Exact coupled first-order systems over certified rational PiSigma fields.

Row convention: sigma(y) V - y = sum(c_i f_i), sigma(c_i)=c_i.
Strongly connected blocks are solved in dependency order, retaining all
homogeneous directions and shared parameters. General blocks use coordinate
uncoupling and complete higher-order PLDE; exact diagonal unrolling remains a
fast path for monomial/projectively periodic blocks. No degree guessing.
"""
import math
import sympy as s
from expressions import X,q
from qdifference import rational_read
from qgosper import UnsupportedDomain
from ore import OreResourceLimit
from qpisigma import PiSigma,parse_problem,add_product_block
from qrational_system import solve_system


def constant_nullspace(rows,variables,width,tower=None):
    """Relations with coefficients in the declared constant field, not F."""
    if not rows:return []
    equations=[];normal=s.cancel if tower is None else tower.normal
    for j in range(width):
        values=[normal(v[j]) for v in rows]
        den=s.prod(s.fraction(v)[1] for v in values)
        polys=[s.Poly(normal(v*den),*variables) if tower is None else tower.polynomial(normal(v*den),variables) for v in values]
        monomials=sorted(set().union(*(set(p.monoms()) for p in polys)))
        equations.extend([[p.coeff_monomial(m) for p in polys] for m in monomials])
    matrix=s.Matrix(equations)
    if not equations:matrix=s.zeros(0,len(rows))
    return matrix.nullspace() if tower is None else tower.nullspace(matrix)


def components(V):
    """Topological SCC order for edges i -> j when V[i,j] is nonzero."""
    n=V.rows;edges=[[j for j in range(n) if j!=i and V[i,j]!=0] for i in range(n)]
    index={};low={};stack=[];active=set();blocks=[]
    def visit(i):
        index[i]=low[i]=len(index);stack.append(i);active.add(i)
        for j in edges[i]:
            if j not in index:visit(j);low[i]=min(low[i],low[j])
            elif j in active:low[i]=min(low[i],index[j])
        if low[i]==index[i]:
            block=[]
            while True:
                j=stack.pop();active.remove(j);block.append(j)
                if j==i:break
            blocks.append(sorted(block))
    for i in range(n):
        if i not in index:visit(i)
    return list(reversed(blocks))


def unrolling_order(V,tower):
    n=V.rows
    if n==1:return 1
    positions=[[j for j in range(n) if V[i,j]!=0] for i in range(n)]
    if all(len(p)==1 for p in positions) and len({p[0] for p in positions})==n:
        permutation=[p[0] for p in positions];pending=set(range(n));order=1
        while pending:
            start=min(pending);i=start;length=0
            while i in pending:pending.remove(i);length+=1;i=permutation[i]
            order=math.lcm(order,length)
        return order
    # A scalar rational multiplier times a finite constant automorphism.
    # The multiplier need not itself be periodic.
    scale=next(v for v in V if v!=0);constant=(V/scale).applyfunc(s.cancel)
    from qfinite import finite_order
    orders=[];limited=None
    for candidate in (V,constant,-constant):
        try:order=finite_order(candidate,[t for t,k,a in tower.nodes],tower.budget)
        except OreResourceLimit as exc:limited=exc;continue
        if order is not None:orders.append(order)
    if orders:return min(orders)
    if limited is not None:raise limited
    raise UnsupportedDomain('irreducible nonperiodic PiSigma matrix block needs a general higher-order PLDE solver')


def block_solve(tower,V,rhs):
    n=V.rows;width=len(rhs);budget=tower.budget
    if n==1:
        pairs=tower.solve(V[0,0],-1,[row[0] for row in rhs])
        return [(cs,s.Matrix([[g]])) for cs,g in pairs],dict(order=1,kind='scalar PLDE')
    if tower.ground!=s.QQ:return general_block_solve(tower,V,rhs)
    try:order=unrolling_order(V,tower)
    except UnsupportedDomain:return general_block_solve(tower,V,rhs)
    if order>budget.max_normal_form_degree:raise OreResourceLimit('matrix unrolling order exceeds budget')
    M=s.eye(n);targets=[s.zeros(1,n) for _ in rhs]
    for j in range(order):
        targets=[(f+s.Matrix([r]).applyfunc(lambda v:tower.sigma(v,j=j))*M).applyfunc(tower.normal)
                 for f,r in zip(targets,rhs)]
        M=(V.applyfunc(lambda v:tower.sigma(v,j=j))*M).applyfunc(tower.normal)
    if any(M[i,j]!=0 for i in range(n) for j in range(n) if i!=j):
        raise ArithmeticError('certified matrix unrolling failed to diagonalize')
    lifted=PiSigma(budget,base_ratio=tower.nodes[0][2]**order)
    lifted.nodes=[(t,k,tower.normal(tower.sigma(t,j=order)-t) if k=='sum'
                   else tower.normal(tower.sigma(t,j=order)/t)) for t,k,a in tower.nodes]
    basis=[(tuple(s.Integer(i==j) for i in range(width)),s.zeros(1,n)) for j in range(width)]
    for j in range(n):
        forcing=[tower.normal(sum(c*f[j] for c,f in zip(cs,targets))) for cs,g in basis]
        updated=[]
        for weights,h in lifted.solve(M[j,j],-1,forcing):
            cs=tuple(tower.normal(sum(w*b[0][i] for w,b in zip(weights,basis))) for i in range(width))
            g=sum((w*b[1] for w,b in zip(weights,basis)),s.zeros(1,n));g[j]+=h
            updated.append((cs,g.applyfunc(tower.normal)))
        basis=updated
        if not basis:break
    residuals=[list((g.applyfunc(tower.sigma)*V-g-
                    sum((c*s.Matrix([f]) for c,f in zip(cs,rhs)),s.zeros(1,n))).applyfunc(tower.normal)) for cs,g in basis]
    answer=[]
    for weights in constant_nullspace(residuals,[t for t,k,a in tower.nodes],n,tower):
        cs=tuple(tower.normal(sum(w*b[0][i] for w,b in zip(weights,basis))) for i in range(width))
        g=sum((w*b[1] for w,b in zip(weights,basis)),s.zeros(1,n)).applyfunc(tower.normal)
        answer.append((cs,g))
    return answer,dict(order=order,kind='semilinear matrix unrolling and original-system constraints',
                      diagonal=list(map(str,M.diagonal())),scalar_trace=lifted.trace)


def general_block_solve(tower,V,rhs):
    """Coordinate uncoupling, full scalar PLDE bases, original constraints."""
    from qplde import solve as scalar_solve
    normal=tower.normal;n=V.rows;width=len(rhs)
    A=V.T.inv().applyfunc(normal);G=(A*s.Matrix(rhs).T).applyfunc(normal)
    scalar=[];traces=[]
    for index in range(n):
        row=s.zeros(1,n);row[index]=1;rows=[row];forcing=[s.zeros(1,width)]
        for order in range(1,n+1):
            shifted=rows[-1].applyfunc(tower.sigma)
            forcing.append((forcing[-1].applyfunc(tower.sigma)+shifted*G).applyfunc(normal))
            rows.append((shifted*A).applyfunc(normal))
            kernel=tower.nullspace(s.Matrix.vstack(*rows).T)
            vector=next((v for v in kernel if v[-1]!=0),None)
            if vector is None:continue
            coefficients=[normal(v/vector[-1]) for v in vector]
            if coefficients[0]==0:raise ArithmeticError('uncoupling of invertible system lost endpoint')
            target=sum((v*f for v,f in zip(coefficients,forcing)),s.zeros(1,width)).applyfunc(normal)
            scalar.append((coefficients,list(target)))
            traces.append(dict(coordinate=index,order=order,operator=list(map(str,coefficients)),rhs_basis=list(map(str,target))))
            break
        else:raise ArithmeticError('higher-order coordinate uncoupling failed')
    basis=[(tuple(s.Integer(i==j) for i in range(width)),s.zeros(1,n)) for j in range(width)]
    for index,(operator,targets) in enumerate(scalar):
        if not basis:break
        forcing=[normal(sum(c*f for c,f in zip(cs,targets))) for cs,g in basis];updated=[]
        for weights,h in scalar_solve(tower,operator,forcing):
            cs=tuple(normal(sum(w*b[0][i] for w,b in zip(weights,basis))) for i in range(width))
            g=sum((w*b[1] for w,b in zip(weights,basis)),s.zeros(1,n));g[index]+=h
            updated.append((cs,g.applyfunc(normal)))
        basis=updated
    residuals=[list((g.applyfunc(tower.sigma)*V-g-sum((c*s.Matrix([f]) for c,f in zip(cs,rhs)),s.zeros(1,n))).applyfunc(normal)) for cs,g in basis]
    answer=[]
    for weights in constant_nullspace(residuals,[t for t,k,a in tower.nodes],n,tower):
        cs=tuple(normal(sum(w*b[0][i] for w,b in zip(weights,basis))) for i in range(width))
        g=sum((w*b[1] for w,b in zip(weights,basis)),s.zeros(1,n)).applyfunc(normal)
        answer.append((cs,g))
    return answer,dict(kind='general higher-order PiSigma PLDE uncoupling',coordinate_equations=traces)


def solve(tower,V,rhs):
    V=s.Matrix(V).applyfunc(tower.normal);rhs=[list(map(tower.normal,r)) for r in rhs]
    n=V.rows;width=len(rhs);budget=tower.budget
    if n==0 or V.cols!=n or not rhs or any(len(r)!=n for r in rhs):raise ValueError('square matrix and nonempty matching RHS rows required')
    if n>budget.max_states or n+width>budget.max_unknowns:raise OreResourceLimit('coupled PiSigma dimension exceeds budget')
    if tower.normal(V.det())==0:raise ValueError('invertible difference matrix required')
    if len(tower.nodes)==1 and tower.nodes[0][0]==X and tower.nodes[0][2]==q and tower.ground==s.QQ:
        raw=solve_system(V,rhs,X,q,budget,include_basis=True)
        return [(tuple(map(rational_read,r['coefficients'])),s.Matrix([list(map(rational_read,r['certificate_row']))]))
                for r in raw['solution_basis']],dict(algorithm='complete rational q-system',system=raw)
    basis=[(tuple(s.Integer(i==j) for i in range(width)),s.zeros(1,n)) for j in range(width)]
    traces=[];done=[]
    for block in components(V):
        forcing=[]
        for cs,g in basis:
            forcing.append([tower.normal(sum(c*f[j] for c,f in zip(cs,rhs))-
                                     sum(tower.sigma(g[i])*V[i,j] for i in done)) for j in block])
        if not basis:break
        local,trace=block_solve(tower,V.extract(block,block),forcing)
        updated=[]
        for weights,h in local:
            cs=tuple(tower.normal(sum(w*b[0][i] for w,b in zip(weights,basis))) for i in range(width))
            g=sum((w*b[1] for w,b in zip(weights,basis)),s.zeros(1,n))
            for j,value in zip(block,h):g[j]+=value
            updated.append((cs,g.applyfunc(tower.normal)))
        basis=updated;done.extend(block);traces.append(dict(coordinates=block,**trace))
    for cs,g in basis:
        residual=(g.applyfunc(tower.sigma)*V-g-sum((c*s.Matrix([f]) for c,f in zip(cs,rhs)),s.zeros(1,n))).applyfunc(tower.normal)
        if residual!=s.zeros(1,n) or any(tower.sigma(c)!=c for c in cs):raise ArithmeticError('coupled PiSigma certificate residual')
    return basis,dict(algorithm='exact SCC coefficient propagation',blocks=traces,scalar_trace=tower.trace)


def build_tower(parsed,values,budget,tower=None,normalize_base=False):
    if normalize_base:
        tower=PiSigma(budget) if tower is None else tower
        if len(tower.nodes)!=1:raise ValueError('base normalization requires a fresh tower')
        parsed=[tower.nodes[0],*parsed];tower.nodes=[]
    remaining=list(parsed);ordered=[];seen=set();variables={t for t,k,v in parsed}
    while remaining:
        ready=[row for row in remaining if not row[2].free_symbols&(variables-seen)]
        if not ready:raise ValueError('cyclic free extension dependency')
        row=next((row for row in ready if row[1]=='product'),ready[0])
        ordered.append(row);remaining.remove(row);seen.add(row[0])
    parsed=ordered
    tower=PiSigma(budget) if tower is None else tower
    tower.occupied|={str(z) for f in [*values,*[v for t,k,v in parsed]] for z in f.free_symbols}|{str(t) for t,k,v in parsed}
    index=0
    while index<len(parsed):
        t,k,v=parsed[index]
        if k=='sum':tower.add(t,k,v);index+=1
        else:
            end=index+1
            while end<len(parsed) and parsed[end][1]=='product' and not parsed[end][2].free_symbols&{t for t,k,v in parsed[index:end]}:end+=1
            if not add_product_block(tower,parsed[index:end]):raise UnsupportedDomain('coupled tower needs algebraic product normalization')
            index=end
        if tower.torsion:raise UnsupportedDomain('coupled free tower has periodic constants; declare a finite algebra explicitly')
    return tower


def compute(data,budget,parse):
    expected={'extensions','matrix','rhs_basis'}
    if not isinstance(data,dict) or set(data) not in (expected,expected|{'algebraic_extensions'}):
        raise ValueError('difference_system requires extensions, matrix and RHS rows')
    matrix=data['matrix'];rows=data['rhs_basis']
    if not isinstance(matrix,list) or not matrix or not all(isinstance(r,list) and len(r)==len(matrix) for r in matrix):
        raise ValueError('nonempty square matrix required')
    if not isinstance(rows,list) or not rows or not all(isinstance(r,list) and len(r)==len(matrix) for r in rows):
        raise ValueError('nonempty matching RHS rows required')
    if len(matrix)>budget.max_states or len(matrix)+len(rows)>budget.max_unknowns:
        raise OreResourceLimit('coupled input dimensions exceed budget')
    if 'algebraic_extensions' in data:
        from qfinite import prepare
        from qnumberfield import fixed_constant_system,periodic_constant_system
        parsed,flat,_,_,algebra=prepare(dict(extensions=data['extensions'],algebraic_extensions=data['algebraic_extensions'],
                                            rhs_basis=[v for row in rows+matrix for v in row]),budget,parse)
        V=s.Matrix([[parse(v) for v in row] for row in matrix]).applyfunc(algebra.normal)
        rhs=[[algebra.normal(parse(v)) for v in row] for row in rows]
        if algebra.multiplication(algebra.normal(V.det())).det()==0:raise ValueError('invertible matrix over the finite algebra required')
        try:native=fixed_constant_system(algebra,parsed,V,rhs,budget)
        except UnsupportedDomain:native=periodic_constant_system(algebra,parsed,V,rhs,budget)
        if native is None:native=periodic_constant_system(algebra,parsed,V,rhs,budget)
        if native is None:raise UnsupportedDomain('algebraic matrix input requires an admitted finite number algebra')
        pairs,trace=native
        def encode(cs,g):
            allowed=set(algebra.field.symbols)|set(algebra.variables)
            if any(s.sympify(v).free_symbols-allowed for v in [*cs,*g]):raise ArithmeticError('unrestored algebraic matrix symbol')
            residual=(g.applyfunc(algebra.sigma)*V-g-sum((c*s.Matrix([f]) for c,f in zip(cs,rhs)),s.zeros(1,V.rows))).applyfunc(algebra.normal)
            if residual!=s.zeros(1,V.rows) or any(algebra.normal(algebra.sigma(c)-c)!=0 for c in cs):
                raise ArithmeticError('original algebraic matrix residual')
            return dict(coefficients=list(map(str,cs)),certificate_row=list(map(str,g)),residual=['0']*V.rows)
        result=dict(solution_basis=[encode(cs,g) for cs,g in pairs],reduction_trace=trace,
                    completeness='full solution module over the invariant number-algebra constant ring')
        selected=next(((cs,g) for cs,g in pairs if any(cs)),None)
        if selected:result.update(encode(*selected))
        return dict(status='constructed' if selected else 'no_relation_in_declared_basis',solver='difference_system',result=result,
                    domain=dict(defining_relations_are_input_objects=True,algorithm=trace['algorithm']))
    parsed,flat,_,_=parse_problem(dict(extensions=data['extensions'],rhs_basis=[x for r in rows+matrix for x in r]),budget,parse)
    V=s.Matrix([[parse(v) for v in r] for r in matrix]);rhs=[[parse(v) for v in r] for r in rows]
    try:tower=build_tower(parsed,flat,budget)
    except UnsupportedDomain:
        from qnumberfield import rational_periodic_algebra,periodic_constant_system
        algebra=rational_periodic_algebra(parsed,flat,budget)
        pairs,trace=periodic_constant_system(algebra,parsed,V,rhs,budget);tower=PiSigma(budget)
    else:pairs,trace=solve(tower,V.applyfunc(lambda v:s.cancel(v.xreplace(tower.aliases))),
                           [[s.cancel(v.xreplace(tower.aliases)) for v in r] for r in rhs])
    definitions=dict(tower.generated_definitions)
    for c,v in tower.constants.items():definitions[c]=s.cancel(v.xreplace(definitions))
    shift={X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in parsed}}
    def encode(cs,g):
        cs=[s.cancel(c.xreplace(definitions)) for c in cs];g=g.applyfunc(lambda v:s.cancel(v.xreplace(definitions)))
        residual=(g.applyfunc(lambda v:v.xreplace(shift))*V-g-sum((c*s.Matrix([r]) for c,r in zip(cs,rhs)),s.zeros(1,V.rows))).applyfunc(s.cancel)
        if residual!=s.zeros(1,V.rows) or any(s.cancel(c.xreplace(shift)-c)!=0 for c in cs):raise ArithmeticError('original coupled system residual')
        return dict(coefficients=list(map(str,cs)),certificate_row=list(map(str,g)),residual=list(map(str,residual)))
    result=dict(solution_basis=[encode(cs,g) for cs,g in pairs],reduction_trace=trace,
                completeness='complete over the invariant field of the certified PiSigma-star tower')
    candidate=next(((cs,g) for cs,g in pairs if any(cs)),None)
    if candidate:result.update(encode(*candidate))
    return dict(status='constructed' if candidate else 'no_relation_in_declared_basis',solver='difference_system',result=result,
                domain=dict(algorithm='general coupled PiSigma PLDE',excluded='singular matrices; uncertified constant-changing towers',
                            original_shift_equations_are_premises=True))
