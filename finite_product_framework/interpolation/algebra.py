"""Untrusted exact symbolic construction; every certificate is rebuilt in Lean."""
import sympy as s

OPS={'HAdd.hAdd':lambda a,b:a+b,'HSub.hSub':lambda a,b:a-b,
     'HMul.hMul':lambda a,b:a*b,'HDiv.hDiv':lambda a,b:a/b}


def walk(node):
    yield node
    for child in node.get('args',[]):yield from walk(child)
    if 'arg' in node:yield from walk(node['arg'])


def atoms(goal):
    return {x['key']:x['display'] for side in ('lhs','rhs') for x in walk(goal[side]) if x['op']=='atom'}


def symbolic(node):
    op=node['op']
    if op=='integer':return s.Integer(node['value'])
    if op=='atom':return s.Symbol('a'+str(node['key']))
    if op in OPS:return OPS[op](*(symbolic(x) for x in node['args']))
    if op=='neg':return -symbolic(node['arg'])
    if op=='inv':return 1/symbolic(node['arg'])
    if op=='pow':return symbolic(node['arg'])**node['exponent']
    raise ValueError('unsupported algebra node '+op)


def degree(node,key):
    op=node['op']
    if op=='integer':return 0
    if op=='atom':return int(node['key']==key)
    if op in ('HAdd.hAdd','HSub.hSub'):return max(degree(x,key) for x in node['args'])
    if op=='HMul.hMul':return sum(degree(x,key) for x in node['args'])
    if op=='neg':return degree(node['arg'],key)
    if op=='pow':return node['exponent']*degree(node['arg'],key)
    raise ValueError('denominator clearing did not expose a polynomial')


def poly(node,key,ty):
    op=node['op']
    if op=='integer':return f'({node["value"]} : Polynomial ({ty}))'
    if op=='atom':
        return 'Polynomial.X' if node['key']==key else f'(Polynomial.C ({node["display"]}))'
    if op in ('HAdd.hAdd','HSub.hSub','HMul.hMul'):
        sign={'HAdd.hAdd':'+','HSub.hSub':'-','HMul.hMul':'*'}[op]
        return '('+(' '+sign+' ').join(poly(x,key,ty) for x in node['args'])+')'
    if op=='neg':return '(-'+poly(node['arg'],key,ty)+')'
    if op=='pow':return '('+poly(node['arg'],key,ty)+f' ^ {node["exponent"]})'
    raise ValueError('non-polynomial node')


def zero_certificate(goal,max_degree):
    names=atoms(goal)
    choices=sorted((max(degree(goal['lhs'],k),degree(goal['rhs'],k)),k) for k in names)
    if not choices:choices=[(0,-1)]
    d,key=choices[0]
    if d>max_degree:raise ValueError(f'degree bound {d} exceeds budget {max_degree}')
    variable=s.Symbol('a'+str(key));difference=symbolic(goal['lhs'])-symbolic(goal['rhs'])
    # Node family is part of the certificate; never infer CharZero from regular q.
    geometric=goal.get('geometric_nodes',[])
    char_zero=goal.get('char_zero',True)
    use_geometric=not char_zero and d>1 and bool(geometric)
    if not char_zero and d>1 and not geometric:
        raise ValueError('NODE_SEPARATION_UNAVAILABLE: need d+1 distinct nodes in the original field')
    samples=[]
    node_points=[s.Symbol('interpolation_node_base')**i if use_geometric else s.Integer(i) for i in range(d+1)]
    for index,point in enumerate(node_points):
        residual=s.expand(difference.subs(variable,point))
        if residual!=0:raise ValueError(f'nonzero symbolic node residual at {point}: {residual}')
        samples.append({'node':str(point),'exact_residual':'0'})
    ty=goal['type'];left=poly(goal['lhs'],key,ty);right=poly(goal['rhs'],key,ty)
    point=names.get(key,'0')
    if use_geometric:
        base=geometric[0]['base'];hyp=geometric[0]['hypothesis']
        node_function=f'(fun i : Fin ({d}+1) => ({base})^i.val)'
        injection=f'((FiniteQInterpolation.powers_injective ({base}) ({hyp}).1 ({hyp}).2).comp Fin.val_injective)'
        distinctness='geometric powers injective from original regular hypothesis'
    else:
        node_function=f'(fun i : Fin ({d}+1) => (i.val : {ty}))'
        injection='(by intro i j h; exact Fin.ext (Nat.cast_injective h))' if char_zero else '(by intro i j h; fin_cases i <;> fin_cases j <;> norm_num at *)'
        distinctness='Nat.cast_injective via CharZero' if char_zero else '0/1 node separation in nontrivial field'
    proof=f'''let ip : Polynomial ({ty}) := {left} - {right}
have iz : ip = 0 := FiniteQInterpolation.zero_of_nodes ip {d} {node_function}
  {injection}
  (by dsimp [ip]; compute_degree)
  (by intro i; fin_cases i <;> norm_num [ip] <;> ring)
have iv := congrArg (Polynomial.eval ({point})) iz
apply sub_eq_zero.mp
simpa only [ip, Polynomial.eval_sub, Polynomial.eval_add, Polynomial.eval_mul,
  Polynomial.eval_pow, Polynomial.eval_neg, Polynomial.eval_X, Polynomial.eval_C,
  Polynomial.eval_natCast, Polynomial.eval_ofNat, Polynomial.eval_zero,
  Polynomial.eval_one] using iv'''
    return {'kind':'finite_zero_certificate','variable_atom':key,'variable_expression':point,
            'degree_upper_bound':d,'nodes':samples,'node_distinctness':distinctness,
            'polynomial':left+' - '+right,'proof_script':proof},proof


def scalar(expr,names,ty):
    if expr.is_Symbol:return '('+names[int(str(expr)[1:])]+')'
    if expr.is_Integer:return f'({int(expr)} : {ty})'
    if expr.is_Rational:return f'({expr.p} / {expr.q} : {ty})'
    if expr.is_Add:return '('+' + '.join(scalar(x,names,ty) for x in expr.args)+')'
    if expr.is_Mul:return '('+' * '.join(scalar(x,names,ty) for x in expr.args)+')'
    if expr.is_Pow and expr.exp.is_Integer:
        base=s.factor(expr.base) if expr.exp<0 else expr.base
        value='('+scalar(base,names,ty)+f' ^ {abs(int(expr.exp))})'
        return '('+value+')⁻¹' if expr.exp<0 else value
    raise ValueError('unsupported partial fraction output '+str(expr))


def partial_parts(expression,variable):
    decomposed=s.apart(expression,variable)
    polynomial=s.Integer(0);parts=[];reconstructed=s.Integer(0)
    for term in s.Add.make_args(decomposed):
        numerator,denominator=s.fraction(term)
        if variable not in denominator.free_symbols:
            s.Poly(term,variable)
            polynomial+=term;continue
        content,factors=s.factor_list(denominator,variable)
        if len(factors)!=1 or s.degree(factors[0][0],variable)!=1 or variable in numerator.free_symbols:
            raise ValueError('principal parts require split linear poles in this version')
        factor,multiplicity=factors[0]
        leading=s.Poly(factor,variable).LC();pole=-factor.subs(variable,0)/leading
        coefficient=s.cancel(numerator/(content*leading**multiplicity))
        parts.append({'pole':str(pole),'order':int(multiplicity),'coefficient':str(coefficient)})
        reconstructed+=coefficient/(variable-pole)**multiplicity
    reconstructed+=polynomial
    if s.cancel(expression-reconstructed)!=0:raise ValueError('partial fraction reconstruction mismatch')
    return {'polynomial_part':str(polynomial),'principal_parts':parts},reconstructed


def principal_certificate(goal):
    left,right=map(lambda side:symbolic(goal[side]),('lhs','rhs'))
    names=atoms(goal);ty=goal['type'];failures=[]
    # Use original denominators before cancellation to select candidates.
    keys=sorted(names)
    for key in keys:
        variable=s.Symbol('a'+str(key))
        if not any(variable in s.denom(s.together(e)).free_symbols for e in (left,right)):continue
        try:
            lc,common=partial_parts(left,variable);rc,other=partial_parts(right,variable)
            if not lc['principal_parts'] and not rc['principal_parts']:continue
            if s.cancel(common-other)!=0:raise ValueError('principal parts or polynomial parts differ')
            text=scalar(common,names,ty)
            return {'kind':'principal_parts_reconstruction','variable_atom':key,'variable_expression':names[key],
                    'left':lc,'right':rc,'common_expression':text,
                    'verification':'both bridges checked on original domain; polynomial residuals use finite-zero certificates'},text
        except (ValueError,NotImplementedError,s.PolynomialError) as exc:failures.append(str(exc))
    raise ValueError('no supported split-pole decomposition: '+'; '.join(failures))
