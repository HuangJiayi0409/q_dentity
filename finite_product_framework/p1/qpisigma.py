"""Rational first-order parameterized equations in certified PiSigma* fields.

Recursive exact factor orbits, denominator bounds, multiplicative coboundaries,
degree bounds and coefficient descent. All recursion in an orbit/degree test
goes to a STRICTLY smaller field. No guessed orbit radius or degree is used.
"""
import sympy as s
import re
from expressions import X,q
from qdifference import rational_read,laurent_coefficients
from qrational_system import solve_system,field_for
from ore import OreResourceLimit
from qgosper import UnsupportedDomain


def unit_signature(value):
    """K*/torsion over the purely transcendental constant field K over QQ."""
    variables=sorted(s.sympify(value).free_symbols|{q},key=str)
    result={}; scalar=s.Integer(1)
    for part,sign in zip(s.fraction(s.cancel(value)),(1,-1)):
        unit,factors=s.Poly(part,*variables,domain=s.QQ).factor_list();scalar*=unit**sign
        for factor,e in factors:
            scalar*=factor.LC()**(sign*e);key=str(factor.monic().as_expr())
            result[key]=result.get(key,0)+sign*e
    scalar=abs(s.Rational(scalar))
    for integer,sign in [(scalar.p,1),(scalar.q,-1)]:
        for prime,e in s.factorint(integer).items():
            key='prime:'+str(prime);result[key]=result.get(key,0)+sign*e
    return {k:v for k,v in result.items() if v}


class PiSigma:
    normal=staticmethod(s.cancel)
    ground=s.QQ

    def __init__(self,budget,base_ratio=q):
        self.budget=budget
        self.nodes=[(X,'product',s.sympify(base_ratio))]
        self.trace=[];self.cache={};self.orbit_cache={};self.mult_cache={}
        self.aliases={};self.constants={};self.records=[];self.occupied={'X','q','Q'}
        self.generated_definitions={}
        self.torsion=[]

    def clear_cache(self):
        self.cache.clear();self.orbit_cache.clear();self.mult_cache.clear()

    def constant_signature(self,values):
        columns=list(map(unit_signature,values));keys=sorted(set().union(*(set(c) for c in columns)))
        return s.Matrix([[c.get(k,0) for c in columns] for k in keys]) if keys else s.zeros(0,len(values))

    def polynomial(self,value,variables):
        parameters=sorted((s.sympify(value).free_symbols|{q})-set(variables),key=str)
        return s.Poly(value,*variables,domain=self.ground.frac_field(*parameters))

    def nullspace(self,matrix):
        from sympy.polys.matrices import DomainMatrix
        symbols=sorted(set().union(*(v.free_symbols for v in matrix),{q}),key=str)
        field=self.ground.frac_field(*symbols)
        rows=[[field.from_sympy(v) for v in row] for row in matrix.tolist()]
        dm=DomainMatrix(rows,matrix.shape,field)
        result=dm.nullspace(divide_last=True).to_Matrix()
        return [result.row(i).T.applyfunc(self.normal) for i in range(result.rows)]

    def fresh(self,definition):
        i=0
        while 'PSConstant'+str(i) in self.occupied:i+=1
        c=s.Symbol('PSConstant'+str(i));self.occupied.add(str(c));self.constants[c]=definition
        return c

    def sigma(self,value,depth=None,j=1):
        depth=len(self.nodes) if depth is None else depth
        if abs(j)>self.budget.max_normal_form_degree:
            raise OreResourceLimit('exact shift distance exceeds operation budget')
        substitutions={}
        for t,kind,a in self.nodes[:depth]:
            if j>=0:substitutions[t]=t+a if kind=='sum' else t*a
            else:
                inverse_a=a.xreplace(substitutions)
                substitutions[t]=t-inverse_a if kind=='sum' else t/inverse_a
        value=s.sympify(value)
        for _ in range(abs(j)):value=self.normal(value.xreplace(substitutions))
        return value

    def poly(self,value,t):
        value=self.normal(value)
        field=self.ground.frac_field(*sorted((value.free_symbols|{q})-{t},key=str))
        return s.Poly(value,t,domain=field)

    def monic(self,value,depth):
        return self.poly(value,self.nodes[depth-1][0]).monic().as_expr()

    def orbit(self,p,r,depth):
        """Unique integer j with monic(sigma**j(p))=r, or None."""
        p=self.monic(p,depth);r=self.monic(r,depth);key=(depth,p,r)
        if key in self.orbit_cache:return self.orbit_cache[key]
        t,kind,a=self.nodes[depth-1];pp=self.poly(p,t);rr=self.poly(r,t)
        result=None
        if pp.degree()==rr.degree():
            degree=int(pp.degree())
            if p==r:result=0
            elif kind=='sum':
                difference=self.normal((rr.nth(degree-1)-pp.nth(degree-1))/degree)
                basis=self.solve(1,-1,[a,difference],depth-1)
                relation=next((cs for cs,g in basis if cs[1]!=0),None)
                if relation is not None:
                    candidate=self.normal(-relation[0]/relation[1])
                    if candidate.is_Integer:result=int(candidate)
            elif pp.nth(0)!=0 and rr.nth(0)!=0:
                candidate=self.exponent(a,self.normal(rr.nth(0)/pp.nth(0)),depth-1)
                if candidate is not None and (candidate/degree).is_Integer:result=-int(candidate/degree)
            if result is not None and self.monic(self.sigma(p,depth,result),depth)!=r:result=None
        self.orbit_cache[key]=result
        return result

    def multiplicative_parts(self,values,depth):
        t,kind,a=self.nodes[depth-1]
        representatives=[];rows=[];units=[];witnesses=[]
        for value in values:
            counts={};h=s.Integer(1);valuation=0
            for part,sign in zip(s.fraction(self.normal(value)),(1,-1)):
                poly=self.poly(part,t)
                if poly.degree()>self.budget.max_normal_form_degree:
                    raise OreResourceLimit('multiplicative factor degree exceeds budget')
                for factor,e in poly.factor_list()[1]:
                    factor=factor.monic().as_expr();e*=sign
                    if kind=='product' and factor==t:valuation+=e;continue
                    index=None;offset=0
                    for k,representative in enumerate(representatives):
                        candidate=self.orbit(representative,factor,depth)
                        if candidate is not None:index=k;offset=candidate;break
                    if index is None:index=len(representatives);representatives.append(factor)
                    if abs(offset)*abs(e)*int(s.degree(factor,t))>self.budget.max_normal_form_degree:
                        raise OreResourceLimit('multiplicative orbit witness exceeds budget')
                    if offset>=0:w=s.prod(self.sigma(representatives[index],depth,j) for j in range(offset))
                    else:w=1/s.prod(self.sigma(representatives[index],depth,j) for j in range(offset,0))
                    h=self.normal(h*w**e);counts[index]=counts.get(index,0)+e
            unit=self.normal(value*h/self.sigma(h,depth)/t**valuation/
                          s.prod(representatives[k]**e for k,e in counts.items()))
            if unit.has(t):raise ArithmeticError('multiplicative orbit reduction left the top variable')
            rows.append((valuation,counts));units.append(unit);witnesses.append(h)
        matrix=s.Matrix([[v for v,c in rows]]+
                        [[c.get(k,0) for v,c in rows] for k in range(len(representatives))])
        return matrix,units,witnesses

    def signature(self,values,depth):
        values=tuple(map(self.normal,values));key=(depth,values)
        if key in self.mult_cache:return self.mult_cache[key]
        if any(v==0 for v in values):raise ValueError('multiplicative signature requires nonzero elements')
        if depth==0:
            matrix=self.constant_signature(values)
        else:
            top,units,_=self.multiplicative_parts(values,depth)
            t,kind,a=self.nodes[depth-1]
            if kind=='product':
                lower=self.signature([*units,a],depth-1)
                annihilator=lower[:,-1:].T.nullspace()
                projection=s.Matrix.vstack(*(v.T for v in annihilator)) if annihilator else s.zeros(0,lower.rows)
                lower=projection*lower[:,:-1]
            else:lower=self.signature(units,depth-1)
            matrix=top.col_join(lower)
        self.mult_cache[key]=matrix
        return matrix

    def exponent(self,alpha,value,depth):
        """The unique rational e with [value]=e[alpha] modulo radical coboundaries."""
        matrix=self.signature([alpha,value],depth)
        pivot=next((i for i in range(matrix.rows) if matrix[i,0]!=0),None)
        if pivot is None:raise ArithmeticError('pseudo-orbit alpha is not a certified Pi ratio')
        e=self.normal(matrix[pivot,1]/matrix[pivot,0])
        return e if all(self.normal(matrix[i,1]-e*matrix[i,0])==0 for i in range(matrix.rows)) else None

    def hyper(self,value,depth):
        """Find nonzero h with sigma(h)/h=value, or decide none in this field."""
        value=self.normal(value)
        if value==0:return None
        if depth==0:return s.Integer(1) if value==1 else None
        top,units,witnesses=self.multiplicative_parts([value],depth)
        if any(top):return None
        t,kind,a=self.nodes[depth-1];unit=units[0];exponent=s.Integer(0)
        if kind=='product':
            exponent=self.exponent(a,unit,depth-1)
            if exponent is None or not exponent.is_Integer:return None
            unit=self.normal(unit/a**exponent)
        lower=self.hyper(unit,depth-1)
        if lower is None:return None
        result=self.normal(witnesses[0]*t**exponent*lower)
        if self.normal(self.sigma(result,depth)/result-value)!=0:raise ArithmeticError('multiplicative certificate residual')
        return result

    def clear_denominators(self,values,t):
        values=list(map(self.normal,values));symbols=set().union(*(v.free_symbols for v in values),{q})-{t}
        field=self.ground.frac_field(*sorted(symbols,key=str));den=s.Poly(1,t,domain=field)
        for value in values:
            den=den.lcm(s.Poly(s.fraction(value)[1],t,domain=field))
            if den.degree()>self.budget.max_normal_form_degree:raise OreResourceLimit('clearing denominator degree exceeds budget')
        polys=[s.Poly(self.normal(v*den.as_expr()),t,domain=field) for v in values]
        content=polys[0]
        for poly in polys[1:]:content=content.gcd(poly)
        if not content.is_zero:polys=[p.exquo(content) for p in polys]
        if max((p.degree() for p in polys),default=0)>self.budget.max_normal_form_degree:
            raise OreResourceLimit('cleared equation degree exceeds budget')
        return polys

    def bounds(self,A,B,rhs,depth):
        t,kind,a=self.nodes[depth-1]
        aa,bb,*ff=self.clear_denominators([A,B,*rhs],t)
        ordinary=lambda poly:poly.exquo(s.Poly(t**min(m[0] for m in poly.monoms()),t,domain=poly.domain)) if kind=='product' else poly
        left,right=ordinary(bb),ordinary(aa);overlaps=[]
        for p,_ in left.factor_list()[1]:
            for r,_ in right.factor_list()[1]:
                j=self.orbit(p.as_expr(),r.as_expr(),depth)
                if j is not None and j>=0:overlaps.append(j)
        radius=max(overlaps,default=0)-1
        if max(0,radius+1)*left.degree()>self.budget.max_normal_form_degree:
            raise OreResourceLimit('derived universal tower denominator exceeds budget')
        D=s.Integer(1)
        for j in range(max(0,radius+1)):D=self.normal(D*self.monic(self.sigma(left.as_expr(),depth,j),depth))
        aa,bb,*ff=self.clear_denominators([aa.as_expr()/self.sigma(D,depth),bb.as_expr()/D,
                                          *[f.as_expr() for f in ff]],t)
        upper_rhs=max([int(f.degree()) for f in ff if not f.is_zero],default=None)
        high=max(int(aa.degree()),int(bb.degree()));upper=[]
        if upper_rhs is not None:upper.append(upper_rhs-high)
        resonances=[]
        if aa.degree()==bb.degree():
            ratio=self.normal(-bb.LC()/aa.LC())
            if kind=='product':
                degree=self.exponent(a,ratio,depth-1)
                if degree is not None and degree.is_Integer and self.hyper(ratio/a**degree,depth-1) is not None:
                    upper.append(int(degree));resonances.append(int(degree))
            else:
                leading=self.hyper(ratio,depth-1)
                if leading is not None:
                    gamma=self.normal((aa.nth(high-1)*ratio+bb.nth(high-1))/bb.LC()) if high else s.Integer(0)
                    relations=self.solve(1,-1,[gamma,a],depth-1)
                    vector=next((cs for cs,g in relations if cs[0]!=0),None)
                    if vector is not None:
                        degree=self.normal(-vector[1]/vector[0])
                        if degree.is_Integer and degree>=0:upper.append(int(degree));resonances.append(int(degree))
                    # If degree equals RHS-high+1, the second coefficient can be forced by RHS.
                    if upper_rhs is not None:upper.append(upper_rhs-high+1)
        lower=0
        if kind=='product':
            va=min(m[0] for m in aa.monoms());vb=min(m[0] for m in bb.monoms());low=min(va,vb);lows=[]
            if any(not f.is_zero for f in ff):lows.append(min(min(m[0] for m in f.monoms()) for f in ff if not f.is_zero)-low)
            if va==vb:
                ratio=self.normal(-bb.nth(low)/aa.nth(low));degree=self.exponent(a,ratio,depth-1)
                if degree is not None and degree.is_Integer and self.hyper(ratio/a**degree,depth-1) is not None:lows.append(int(degree))
            lower=min(lows) if lows else 0
        upper=max(upper,default=lower-1)
        trace=dict(kind='rational_tower_bounds',variable=str(t),extension=kind,
                   denominator=str(D),pole_offsets=sorted(set(overlaps)),pole_radius=radius,
                   lower=lower,upper=upper,high_resonances=resonances,
                   transformed_coefficients=[str(aa.as_expr()),str(bb.as_expr())],
                   transformed_rhs=list(map(lambda f:str(f.as_expr()),ff)))
        self.trace.append(trace)
        return D,lower,upper,aa,bb,ff

    def constrain(self,basis,residuals,depth):
        if not basis:return []
        variables=[t for t,kind,a in self.nodes[:depth]]
        common=s.prod(s.fraction(self.normal(r))[1] for r in residuals)
        polynomials=[self.normal(r*common) for r in residuals]
        if variables:
            polys=[self.polynomial(p,variables) for p in polynomials]
            monomials=set().union(*(set(p.monoms()) for p in polys))
            matrix=s.Matrix([[p.coeff_monomial(m) for p in polys] for m in sorted(monomials)])
        else:matrix=s.Matrix([polynomials])
        if matrix.rows*matrix.cols>self.budget.max_unknowns**2:raise OreResourceLimit('constant constraint matrix exceeds budget')
        result=[]
        for v in self.nullspace(matrix):
            cs=tuple(self.normal(sum(w*pair[0][j] for w,pair in zip(v,basis))) for j in range(len(basis[0][0])))
            g=self.normal(sum(w*pair[1] for w,pair in zip(v,basis)));result.append((cs,g))
        return result

    def solve(self,A,B,rhs,depth=None):
        """Complete (c,g) basis for A*sigma(g)+B*g=sum c_i*f_i."""
        depth=len(self.nodes) if depth is None else depth
        A,B=map(self.normal,(A,B));rhs=tuple(map(self.normal,rhs));key=(depth,A,B,rhs)
        if key in self.cache:return self.cache[key]
        if not rhs:raise ValueError('nonempty RHS basis required')
        if len(rhs)>self.budget.max_unknowns:raise OreResourceLimit('parameter space exceeds budget')
        identity=[tuple(s.Integer(i==j) for i in range(len(rhs))) for j in range(len(rhs))]
        if A==0 and B==0:raise ValueError('nonzero first-order operator required')
        if depth==0:
            if A+B!=0:basis=[(c,self.normal(rhs[j]/(A+B))) for j,c in enumerate(identity)]
            else:
                basis=self.constrain([(c,s.Integer(0)) for c in identity],rhs,0)
                basis.append((tuple(s.Integer(0) for _ in rhs),s.Integer(1)))
        elif A==0:basis=[(c,self.normal(rhs[j]/B)) for j,c in enumerate(identity)]
        elif B==0:basis=[(c,self.sigma(rhs[j]/A,depth,-1)) for j,c in enumerate(identity)]
        elif depth==1 and self.nodes[0][0]==X and self.nodes[0][2]==q and self.ground==s.QQ:
            raw=solve_system([[-A/B]],[[-f/B] for f in rhs],X,q,self.budget,include_basis=True)
            basis=[(tuple(map(rational_read,row['coefficients'])),rational_read(row['certificate_row'][0])) for row in raw['solution_basis']]
            self.trace.append(dict(kind='q_rational_base',result=raw))
        else:
            D,lo,hi,aa,bb,ff=self.bounds(A,B,rhs,depth)
            if hi-lo+1>self.budget.max_normal_form_degree or hi-lo+1+len(rhs)>self.budget.max_unknowns:
                raise OreResourceLimit('derived tower coefficient range exceeds budget')
            t,kind,a=self.nodes[depth-1];top=max(int(aa.degree()),int(bb.degree()))
            basis=[(c,s.Integer(0)) for c in identity]
            for d in range(hi,lo-1,-1):
                targets=[]
                for cs,g in basis:
                    residual=self.normal(sum(c*f.as_expr() for c,f in zip(cs,ff))-aa.as_expr()*self.sigma(g,depth)-bb.as_expr()*g)
                    # Laurent coefficient extraction by an exact monomial shift.
                    targets.append(laurent_coefficients(residual,[t]).get((d+top,),s.Integer(0)))
                lower=self.solve(aa.nth(top)*(a**d if kind=='product' else 1),bb.nth(top),targets,depth-1)
                updated=[]
                for weights,coefficient in lower:
                    cs=tuple(self.normal(sum(w*pair[0][j] for w,pair in zip(weights,basis))) for j in range(len(rhs)))
                    g=self.normal(sum(w*pair[1] for w,pair in zip(weights,basis))+coefficient*t**d)
                    updated.append((cs,g))
                basis=updated
                if not basis:break
            residuals=[self.normal(aa.as_expr()*self.sigma(g,depth)+bb.as_expr()*g-
                              sum(c*f.as_expr() for c,f in zip(cs,ff))) for cs,g in basis]
            basis=self.constrain(basis,residuals,depth)
            basis=[(cs,self.normal(g/D)) for cs,g in basis]
        for cs,g in basis:
            if any(c.has(*[t for t,_,_ in self.nodes[:depth]]) for c in cs) if depth else False:
                raise ArithmeticError('coefficient is not in constant field')
            if self.normal(A*self.sigma(g,depth)+B*g-sum(c*f for c,f in zip(cs,rhs)))!=0:
                raise ArithmeticError('first-order tower residual')
        self.cache[key]=basis
        return basis

    def add(self,t,kind,value):
        value=self.normal(s.sympify(value).xreplace(self.aliases));depth=len(self.nodes)
        if any(value.has(z) for z,c,definition in self.torsion):
            raise UnsupportedDomain('PiSigma shift depends on a periodic generator; component-field construction remains required')
        record=dict(name=str(t),kind=kind,shift_value=str(value))
        if kind=='sum':
            basis=self.solve(1,-1,[value]);pair=next(((cs,g) for cs,g in basis if cs[0]!=0),None)
            if pair:
                cs,g=pair;g=self.normal(g/cs[0]);c=self.fresh(t-g);self.aliases[t]=g+c
                record.update(action='constant_reduction',alias=str(g+c),constant=str(c),definition=str(t-g))
            else:
                self.nodes.append((t,kind,value));record.update(action='sigma_star_extension')
        else:
            if value==0:raise ValueError('nonzero product ratio required')
            signature=self.signature([value],depth)
            if any(signature):
                self.nodes.append((t,kind,value));record.update(action='pi_extension')
            else:
                h=self.hyper(value,depth)
                if h is None:
                    h=self.hyper(-value,depth)
                    if h is None:
                        from qconstant import normalize_product
                        if normalize_product(self,t,value):return True
                        record.update(action='algebraic_or_torsion_dependency')
                        self.records.append(record);return False
                    i=0
                    while 'PSRoot'+str(i) in self.occupied:i+=1
                    z=s.Symbol('PSRoot'+str(i));self.occupied.add(str(z))
                    c=self.fresh((t/h)**2);self.torsion.append((z,c,self.normal(t/h)));self.aliases[t]=h*z
                    record.update(action='quadratic_periodic_extension',alias=str(h*z),generator=str(z),
                                  invariant=str(c),invariant_definition=str((t/h)**2),relation=str(z**2-c))
                    self.records.append(record);self.clear_cache();return True
                c=self.fresh(t/h);self.aliases[t]=c*h
                record.update(action='constant_reduction',alias=str(c*h),constant=str(c),definition=str(t/h),nonzero_constant=True)
        self.records.append(record);self.clear_cache();return True


def column_basis(matrix):
    """Unimodular column operations: independent columns followed by zero columns."""
    matrix=s.Matrix(matrix);U=s.eye(matrix.cols);pivot=0
    common=s.ilcm(*[v.q for v in matrix]) if len(matrix)>1 else (matrix[0].q if len(matrix) else 1)
    matrix=matrix*common
    for row in range(matrix.rows):
        index=next((j for j in range(pivot,matrix.cols) if matrix[row,j]!=0),None)
        if index is None:continue
        matrix.col_swap(index,pivot);U.col_swap(index,pivot)
        for j in range(pivot+1,matrix.cols):
            a,b=matrix[row,pivot],matrix[row,j]
            if b==0:continue
            u,v,g=s.gcdex(a,b)
            for target in (matrix,U):
                left,right=target[:,pivot],target[:,j]
                target[:,pivot]=u*left+v*right
                target[:,j]=-b/g*left+a/g*right
        pivot+=1
        if pivot==matrix.cols:break
    if abs(U.det())!=1:raise ArithmeticError('product basis transformation not unimodular')
    return U,pivot


def add_product_block(tower,block):
    values=[tower.normal(v.xreplace(tower.aliases)) for t,k,v in block]
    signature=tower.signature(values,len(tower.nodes))
    if signature.rank()==len(block):
        return all(tower.add(t,k,v) for t,k,v in block)
    U,rank=column_basis(signature);new=[];original=[t for t,k,v in block]
    for j in range(len(block)):
        i=0
        while 'PSProduct'+str(i) in tower.occupied:i+=1
        symbol=s.Symbol('PSProduct'+str(i));tower.occupied.add(str(symbol));new.append(symbol)
        definition=s.prod(t**U[i,j] for i,t in enumerate(original))
        tower.generated_definitions[symbol]=definition
        ratio=tower.normal(s.prod(v**U[i,j] for i,v in enumerate(values)))
        if not tower.add(symbol,'product',ratio):return False
    inverse=U.inv()
    for i,t in enumerate(original):
        tower.aliases[t]=tower.normal(s.prod(tower.aliases.get(new[j],new[j])**inverse[j,i] for j in range(len(new))))
    tower.records.append(dict(action='unimodular_product_basis',original=list(map(str,original)),
        transformed=list(map(str,new)),matrix=[list(map(int,U.row(j))) for j in range(U.rows)],
        rank=rank,aliases={str(t):str(tower.aliases[t]) for t in original}))
    tower.clear_cache();return True


def parse_problem(data,budget,parse):
    if not isinstance(data,dict) or set(data) not in ({'extensions','rhs_basis'},{'extensions','rhs_basis','operator'}):
        raise ValueError('extensions, rhs_basis and optional first-order operator required; no proof hints')
    if not isinstance(data['extensions'],list) or not isinstance(data['rhs_basis'],list) or not data['rhs_basis']:
        raise ValueError('extension list and nonempty RHS basis required')
    if len(data['extensions'])+1>budget.max_states or len(data['rhs_basis'])>budget.max_unknowns:
        raise OreResourceLimit('difference field input dimension exceeds budget')
    parsed=[];names=set()
    for row in data['extensions']:
        if not isinstance(row,dict) or row.get('kind') not in ('sum','product'):raise ValueError('sum/product extension required')
        key='increment' if row['kind']=='sum' else 'ratio';name=row.get('name')
        if set(row)!={'name','kind',key}:raise ValueError('unexpected extension fields')
        if not isinstance(name,str) or not re.fullmatch('[A-Za-z][A-Za-z0-9_]*',name) or name in names|{'X','q','Q','n','k'}:
            raise ValueError('unique nonreserved extension names required')
        names.add(name);parsed.append((s.Symbol(name),row['kind'],parse(row[key])))
    rhs=list(map(parse,data['rhs_basis']));operator=data.get('operator',[1,-1])
    if not isinstance(operator,list) or len(operator)!=2:raise ValueError('operator is [A,B] for A*sigma(g)+B*g')
    A,B=map(parse,operator)
    if A==B==0:raise ValueError('nonzero first-order operator required')
    seen=set();all_names={t for t,k,v in parsed}
    for t,k,v in parsed:
        if v.free_symbols&(all_names-seen):raise ValueError('extension may only depend on preceding variables')
        seen.add(t)
    field_for([A,B,*rhs,*[v for t,k,v in parsed]],X,q)
    return parsed,rhs,A,B


def periodic_field_compute(parsed,rhs,budget,A=s.Integer(1),B=s.Integer(-1)):
    """Unroll torsion in rational towers, then descend by finite-order averaging.

    The original variables remain transcendental: a sign variable is NOT
    specialized to a square equal to one. New invariants retain their values.
    """
    sigma={X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in parsed}}
    def shift(value,n=1):
        for _ in range(n):value=s.cancel(s.sympify(value).xreplace(sigma))
        return value
    A,B=map(s.sympify,(A,B))
    if A==0 or B==0:
        # Multiplication and an invertible triangular shift have no homogeneous
        # kernel. The standard RHS vectors generate over the ORIGINAL fixed
        # field, including any periodic invariants.
        if A==B==0:raise ValueError('nonzero first-order operator required')
        inverse={}
        for t,k,v in [(X,'product',q),*parsed]:
            v=s.sympify(v).xreplace(inverse)
            inverse[t]=t-v if k=='sum' else t/v
        pairs=[(tuple(s.Integer(i==j) for i in range(len(rhs))),
                s.cancel(f/B) if A==0 else s.cancel((f/A).xreplace(inverse))) for j,f in enumerate(rhs)]
        encoded=[]
        for cs,g in pairs:
            if s.cancel(A*shift(g)+B*g-sum(c*f for c,f in zip(cs,rhs)))!=0:
                raise ArithmeticError('one-term periodic operator residual')
            encoded.append(dict(coefficients=list(map(str,cs)),certificate=str(g),
                original_coefficients=list(map(str,cs)),original_certificate=str(g),residual='0',original_residual='0'))
        return dict(status='constructed',solver='difference_field',
                    result=dict(solution_basis=encoded,**encoded[0],completeness='complete over the original fixed field'),
                    domain=dict(algorithm='invertible one-term operator',input_shift_relations_are_premises=True))
    ratio=s.cancel(-B/A);forcing=[s.cancel(f/A) for f in rhs]
    order=2;attempts=[]
    while True:
        if order>budget.max_normal_form_degree:raise OreResourceLimit('periodic unrolling order exceeds budget')
        lifted=PiSigma(budget,base_ratio=q**order)
        lifted.occupied|={str(t) for t,k,v in parsed}|{str(z) for f in [A,B,*rhs,*[v for t,k,v in parsed]] for z in f.free_symbols}
        transformed=[(t,k,s.cancel(shift(t,order)-t) if k=='sum' else s.cancel(shift(t,order)/t)) for t,k,v in parsed]
        success=True;index=0
        try:
            while index<len(transformed):
                t,k,v=transformed[index]
                if k=='sum':lifted.add(t,k,v);index+=1;continue
                end=index+1
                while end<len(transformed) and transformed[end][1]=='product' and not (transformed[end][2].free_symbols&{r[0] for r in transformed[index:end]}):end+=1
                if not add_product_block(lifted,transformed[index:end]):
                    raise UnsupportedDomain('unrolled field still needs nonrational algebraic constant-field construction')
                index=end
        except UnsupportedDomain as exc:
            if 'periodic generator' not in str(exc):raise
            success=False
        attempts.append(dict(order=order,periodic_generators=len(lifted.torsion)))
        if success and not lifted.torsion:break
        order*=2
    # sigma(g)=r*g+c.h => sigma^ell(g)=R*g+c.F.  The products are
    # ordered by shift index; telescoping is the special case r=1.
    multiplier=s.Integer(1);targets=[s.Integer(0)]*len(rhs)
    for j in range(order):
        rj=shift(ratio,j)
        targets=[s.cancel(rj*f+shift(h,j)) for f,h in zip(targets,forcing)]
        multiplier=s.cancel(rj*multiplier)
    targets=[s.cancel(f.xreplace(lifted.aliases)) for f in targets]
    basis=lifted.solve(1,-s.cancel(multiplier.xreplace(lifted.aliases)),targets)
    definitions=dict(lifted.generated_definitions)
    for c,v in lifted.constants.items():definitions[c]=s.cancel(v.xreplace(definitions))
    basis=[(tuple(s.cancel(c.xreplace(definitions)) for c in cs),s.cancel(g.xreplace(definitions))) for cs,g in basis]
    generators=[definitions[c] for c in lifted.constants]
    divisors=list(s.divisors(order))
    constant_order=next(d for d in divisors if all(s.cancel(shift(c,d)-c)==0 for c in generators))
    primitive=s.Integer(0)
    if constant_order>1:
        for trial in range(1,budget.max_unknowns+1):
            primitive=s.cancel(sum((i+1)**trial*c for i,c in enumerate(generators)))
            if all(s.cancel(shift(primitive,d)-primitive)!=0 for d in s.divisors(constant_order) if d<constant_order):break
        else:raise OreResourceLimit('finite invariant-field primitive element construction exceeds budget')
    candidates=[]
    for cs,g in basis:
        for exponent in range(constant_order):
            current_cs=[s.cancel(c*primitive**exponent) for c in cs];current_g=s.cancel(g*primitive**exponent)
            total_cs=[s.Integer(0)]*len(rhs);total_g=s.Integer(0)
            for _ in range(order):
                total_cs=[s.cancel(a+b) for a,b in zip(total_cs,current_cs)];total_g=s.cancel(total_g+current_g)
                current_cs=list(map(shift,current_cs))
                current_g=s.cancel((shift(current_g)-sum(c*f for c,f in zip(current_cs,forcing)))/ratio)
            total_cs=tuple(s.cancel(c/order) for c in total_cs);total_g=s.cancel(total_g/order)
            if any(total_cs) or total_g!=0:candidates.append((total_cs,total_g))
    # Invariant vectors are independent over the fixed field iff independent
    # after scalar extension to the unrolled constant field (Galois descent).
    variables=[t for t,k,v in lifted.nodes];equations=[]
    for coordinate in range(len(rhs)+1):
        values=[(cs[coordinate] if coordinate<len(rhs) else g).xreplace(lifted.aliases) for cs,g in candidates]
        den=s.prod(s.fraction(s.cancel(v))[1] for v in values)
        polys=[s.Poly(s.cancel(v*den),*variables) for v in values]
        monomials=set().union(*(set(p.monoms()) for p in polys)) if polys else set()
        equations.extend([[p.coeff_monomial(m) for p in polys] for m in monomials])
    pivots=s.Matrix(equations).rref()[1] if equations else []
    def encode(cs,g):
        if any(s.cancel(shift(c)-c)!=0 for c in cs):raise ArithmeticError('periodic descent coefficient not invariant')
        if s.cancel(A*shift(g)+B*g-sum(c*f for c,f in zip(cs,rhs)))!=0:raise ArithmeticError('periodic descent residual')
        return dict(coefficients=list(map(str,cs)),certificate=str(g),original_coefficients=list(map(str,cs)),
                    original_certificate=str(g),residual='0',original_residual='0')
    answer=[candidates[i] for i in pivots]
    result=dict(solution_basis=[encode(cs,g) for cs,g in answer],
        unrolling_attempts=attempts,unrolling_order=order,constant_automorphism_order=constant_order,
        constant_primitive_element=str(primitive),unrolled_constant_definitions={str(c):str(definitions[c]) for c in lifted.constants},
        unrolled_multiplier=str(multiplier),operator=list(map(str,(A,B))),
        reduction_trace=lifted.trace,completeness='complete first-order PLDE after certified PiSigma unrolling and finite-order descent')
    candidate=next(((cs,g) for cs,g in answer if any(cs)),None)
    if candidate:
        cs,g=candidate;pivot=next(c for c in cs if c!=0)
        result.update(encode(tuple(s.cancel(c/pivot) for c in cs),s.cancel(g/pivot)))
    return dict(status='constructed' if candidate else 'no_relation_in_declared_basis',solver='difference_field',result=result,
        domain=dict(algorithm='periodic rational-field unrolling and invariant descent',
                    constants='fixed field of the explicitly checked finite automorphism on unrolled constants',
                    input_shift_relations_are_premises=True,original_product_initial_values_preserved=True,
                    obligations='source semantics, initial values, singular specializations and Lean remain external'))


def compute(data,budget,parse):
    parsed,rhs,A,B=parse_problem(data,budget,parse)
    # Independent products can be declared after sums. Put all currently-ready
    # products first so a primitive multiplicative basis is not order-dependent.
    remaining=list(parsed);ordered=[];seen=set();variables={t for t,k,v in parsed}
    while remaining:
        ready=[row for row in remaining if not (row[2].free_symbols&variables-seen)]
        row=next((row for row in ready if row[1]=='product'),ready[0])
        ordered.append(row);remaining.remove(row);seen.add(row[0])
    parsed=ordered
    tower=PiSigma(budget)
    tower.occupied|={str(v) for f in [A,B,*rhs,*[v for t,k,v in parsed]] for v in f.free_symbols}|{str(t) for t,k,v in parsed}
    index=0
    while index<len(parsed):
        t,kind,value=parsed[index]
        if kind=='sum':
            try:tower.add(t,kind,value)
            except UnsupportedDomain as exc:
                if 'periodic generator' in str(exc):return periodic_field_compute(parsed,rhs,budget,A,B)
                raise
            index+=1;continue
        end=index+1
        while end<len(parsed) and parsed[end][1]=='product' and not (parsed[end][2].free_symbols&{v[0] for v in parsed[index:end]}):end+=1
        try:admitted=add_product_block(tower,parsed[index:end])
        except UnsupportedDomain as exc:
            if 'periodic generator' in str(exc):return periodic_field_compute(parsed,rhs,budget,A,B)
            raise
        if not admitted:
            return dict(status='unsupported_domain',solver='difference_field',tower=tower.records,
                        reason='finite algebraic/periodic coefficient extension required; use finite_difference_ring for explicit algebraic models')
        index=end
    original_rhs=rhs;normalized=[s.cancel(v.xreplace(tower.aliases)) for v in [A,B,*rhs]]
    if tower.torsion:
        return periodic_field_compute(parsed,original_rhs,budget,A,B)
    else:basis=tower.solve(*normalized[:2],normalized[2:])
    definitions=dict(tower.generated_definitions)
    for c,definition in tower.constants.items():definitions[c]=s.cancel(definition.xreplace(definitions))
    for z,c,definition in tower.torsion:definitions[z]=s.cancel(definition.xreplace(definitions))
    sigma={X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in parsed}}
    def encode(cs,g):
        restored_cs=[s.cancel(c.xreplace(definitions)) for c in cs];restored_g=s.cancel(g.xreplace(definitions))
        if any(s.cancel(c.xreplace(sigma)-c)!=0 for c in restored_cs):raise ArithmeticError('restored coefficient is not invariant')
        residual=s.cancel(A*restored_g.xreplace(sigma)+B*restored_g-sum(c*f for c,f in zip(restored_cs,original_rhs)))
        if residual!=0:raise ArithmeticError('original difference field certificate residual')
        return dict(coefficients=list(map(str,cs)),certificate=str(g),residual='0',
                    original_coefficients=list(map(str,restored_cs)),original_certificate=str(restored_g),original_residual='0')
    result=dict(solution_basis=[encode(cs,g) for cs,g in basis],reduction_trace=tower.trace,
        constant_definitions={str(c):str(v) for c,v in tower.constants.items()},
        generated_variable_definitions={str(c):str(v) for c,v in tower.generated_definitions.items()},
        completeness='complete rational first-order parameterized solve in the certified PiSigma-star tower')
    candidate=next(((cs,g) for cs,g in basis if any(cs)),None)
    if candidate:
        cs,g=candidate;pivot=next(c for c in cs if c!=0)
        result.update(encode(tuple(s.cancel(c/pivot) for c in cs),s.cancel(g/pivot)))
    return dict(status='constructed' if candidate else 'no_relation_in_declared_basis',solver='difference_field',
        result=result,tower=tower.records,normalized_input=dict(operator=list(map(str,normalized[:2])),rhs_basis=list(map(str,normalized[2:]))),
        domain=dict(base='QQ(q,independent parameters)(X)',q='transcendental',
                    algorithm='rational first-order PLDE, arbitrary certified triangular PiSigma-star tower',
                    input_shift_relations_are_premises=True,
                    excluded='finite algebraic/periodic coefficient rings use finite_difference_ring; higher-order operators use difference_equation',
                    obligations='source evaluation, initial values, singular specializations and Lean remain external'))
