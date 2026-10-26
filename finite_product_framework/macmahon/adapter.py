"""Source-bound affine finite sums -> positively graded rational Omega.

Only a small, explicitly parsed Lean expression grammar is accepted. Symbolic
natural bounds become coefficient variables, never concrete sample sizes.
Every summed variable is shifted to a nonnegative variable, all affine bounds
become Omega constraints, and a temporary grading marker ensures convergence.
This constructs a local GF bridge candidate, not an original Lean proof.
"""
import re
import sympy as s


class OmegaInputGap(ValueError):pass


def tokens(text):
    pattern=r'\s*(Finset\.(?:range|Icc)|[A-Za-z_\u0370-\u03ff][A-Za-z_0-9\u0370-\u03ff]*|[0-9]+|⁻¹|[()+*/^,:∑∈ℕℤℂℚ]|[-−])'
    out=[];position=0
    while position<len(text):
        if not text[position:].strip():break
        m=re.match(pattern,text[position:])
        if not m:raise OmegaInputGap('unsupported token near '+text[position:position+35])
        out.append(m[1]);position+=m.end()
    return out


class Parser:
    def __init__(self,text,types):self.ts=tokens(text);self.i=0;self.types=dict(types)
    def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
    def take(self,expected=None):
        value=self.peek()
        if value is None or (expected is not None and value!=expected):raise OmegaInputGap('expected '+str(expected)+', got '+str(value))
        self.i+=1;return value
    def expression(self,minimum=0):
        token=self.take()
        if token=='(':
            left=self.expression()
            if self.peek()==':':
                self.take();kind=self.take()
                if kind not in ('ℕ','ℤ','K','ℂ','ℚ'):raise OmegaInputGap('unsupported cast '+kind)
                left={'op':'cast','arg':left,'type':kind}
            self.take(')')
        elif token in ('-','−'):
            left={'op':'neg','arg':self.expression(25),'type':'ℤ'}
        elif token=='∑':
            binder=self.take();self.take('∈');domain=self.take()
            if domain=='Finset.range':
                upper=self.expression(0);lower={'op':'int','value':0,'type':'ℕ'};kind='ℕ'
            elif domain=='Finset.Icc':
                # Function application arguments must be atoms/parenthesized;
                # unparenthesized additive bounds are deliberately rejected.
                lower=self.expression(41);upper=self.expression(41)
                kind='ℤ' if lower.get('type')=='ℤ' or upper.get('type')=='ℤ' else 'ℕ'
            else:raise OmegaInputGap('unsupported finite domain '+domain)
            self.take(',');previous=self.types.get(binder);self.types[binder]=kind
            body=self.expression()
            if previous is None:self.types.pop(binder,None)
            else:self.types[binder]=previous
            left={'op':'sum','binder':binder,'domain':domain,'lower':lower,'upper':upper,'body':body,'type':'K'}
        elif token.isdigit():left={'op':'int','value':int(token),'type':'ℕ'}
        elif re.fullmatch(r'[A-Za-z_\u0370-\u03ff][A-Za-z_0-9\u0370-\u03ff]*',token):
            if token not in self.types:raise OmegaInputGap('undeclared scalar/function '+token)
            left={'op':'var','name':token,'type':self.types[token]}
        else:raise OmegaInputGap('unexpected token '+token)
        precedences={'+':10,'-':10,'−':10,'*':20,'/':20,'^':30}
        while True:
            op=self.peek()
            if op=='⁻¹':
                self.take();left={'op':'pow','args':[left,{'op':'int','value':-1,'type':'ℤ'}],'type':'K'};continue
            precedence=precedences.get(op,-1)
            if precedence<minimum:break
            self.take();right=self.expression(precedence if op=='^' else precedence+1)
            kind='K' if 'K' in (left.get('type'),right.get('type')) or any(t in ('ℂ','ℚ') for t in (left.get('type'),right.get('type'))) else 'ℤ' if 'ℤ' in (left.get('type'),right.get('type')) else 'ℕ'
            left={'op':{'+':'add','-':'sub','−':'sub','*':'mul','/':'div','^':'pow'}[op],'args':[left,right],'type':kind}
        return left
    def parse(self):
        out=self.expression()
        if self.peek() is not None:raise OmegaInputGap('unsupported function application or trailing token '+str(self.peek()))
        return out


def statement_parts(source):
    start=source.index('theorem statement')+len('theorem statement')
    end=source.index(':= by',start);depth=0;separator=None
    for i in range(start,end):
        ch=source[i]
        if ch in '({[':depth+=1
        elif ch in ')}]':depth-=1
        elif ch==':' and depth==0:separator=i;break
    if separator is None:raise OmegaInputGap('cannot locate theorem target')
    header=source[start:separator];types={}
    for names,kind in re.findall(r'\(([^():]+)\s*:\s*(ℕ|ℤ|K|ℂ|ℚ)\s*\)',header):
        for name in names.split():
            if re.fullmatch(r'[A-Za-z_\u0370-\u03ff][A-Za-z_0-9\u0370-\u03ff]*',name):types[name]=kind
    return source[separator+1:end],separator+1,types


def source_sums(source):
    target,offset,types=statement_parts(source);accepted=[];rejected=[];covered=-1
    for m in re.finditer('∑',target):
        if m.start()<covered:continue
        # Read exactly the finite-sum subexpression, respecting surrounding
        # parentheses. Only top-level goal separators delimit an unwrapped sum.
        depth=0;end=len(target)
        for j in range(m.start(),len(target)):
            ch=target[j]
            if ch=='(':depth+=1
            elif ch==')':
                if depth==0:end=j;break
                depth-=1
            elif depth==0 and ch in '=∧→':end=j;break
        fragment=target[m.start():end].strip()
        try:
            ast=Parser(fragment,types).parse()
            if ast['op']!='sum':raise OmegaInputGap('fragment is not a complete sum')
            accepted.append(dict(ast=ast,source_span=[offset+m.start(),offset+end],source_fragment=fragment,parameter_types=types))
            covered=end
        except OmegaInputGap as exc:
            rejected.append(dict(source_span=[offset+m.start(),offset+end],reason=str(exc),fragment=fragment[:160]))
    return accepted,rejected


def walk(ast):
    yield ast
    for v in ast.get('args',[]):yield from walk(v)
    if 'arg' in ast:yield from walk(ast['arg'])
    if ast['op']=='sum':
        for name in ('lower','upper','body'):yield from walk(ast[name])


def nonnegative(value,variables,constraints):
    def trivial(v):
        p=s.Poly(s.expand(v),*variables)
        return p.total_degree()<=1 and all(c>=0 for c in p.coeffs())
    return trivial(value) or any(trivial(value-c) for c in constraints)


def affine(ast,env,variables,constraints):
    op=ast['op']
    if op=='int':return s.Integer(ast['value'])
    if op=='var':
        if ast['name'] not in env:raise OmegaInputGap('non-index symbol in affine expression')
        return env[ast['name']]
    if op=='cast':
        if ast['type'] not in ('ℕ','ℤ'):raise OmegaInputGap('field cast cannot be an affine index')
        return affine(ast['arg'],env,variables,constraints)
    if op=='neg':return -affine(ast['arg'],env,variables,constraints)
    if op not in ('add','sub','mul','div','pow'):raise OmegaInputGap('non-arithmetic affine bound')
    a,b=[affine(v,env,variables,constraints) for v in ast['args']]
    if op=='add':v=a+b
    elif op=='sub':
        v=a-b
        if ast.get('type')=='ℕ' and not nonnegative(v,variables,constraints):
            raise OmegaInputGap('natural subtraction may truncate; no nonnegative affine certificate')
    elif op=='mul':v=a*b
    elif op=='div':
        if b==0 or b.free_symbols:raise OmegaInputGap('nonconstant affine divisor')
        v=a/b
    else:
        if b not in (0,1):raise OmegaInputGap('nonlinear index exponent')
        v=a**b
    p=s.Poly(s.expand(v),*variables)
    if p.total_degree()>1 or any(not c.is_Integer for c in p.coeffs()):
        raise OmegaInputGap('nonlinear or nonintegral affine index expression')
    return p.as_expr()


def tree(v):
    v=s.sympify(v)
    if v.is_Integer:return int(v)
    if v.is_Rational:return ['div',int(v.p),int(v.q)]
    if v.is_Symbol:return str(v)
    if v.is_Add:return ['add',*map(tree,v.args)]
    if v.is_Mul:return ['mul',*map(tree,v.args)]
    if v.is_Pow and v.exp.is_Integer:return ['pow',tree(v.base),int(v.exp)]
    raise OmegaInputGap('not an exact rational-tree expression')


def encode(candidate):
    ast=candidate['ast'];types=candidate['parameter_types']
    binder_names={a['binder'] for a in walk(ast) if a['op']=='sum'}
    parameter_names=sorted({a['name'] for a in walk(ast) if a['op']=='var' and a['name'] not in binder_names and types.get(a['name']) in ('ℕ','ℤ')})
    if any(types[name]!='ℕ' for name in parameter_names):raise OmegaInputGap('integer external bound parameters need a declared chamber')
    params=[s.Symbol('p'+str(i)) for i in range(len(parameter_names))]
    variables=list(params);env=dict(zip(parameter_names,params));constraints=list(params);bounds=[];index_names=[]
    current=ast
    while current['op']=='sum':
        if current['binder'] in env or current['binder'] in index_names:raise OmegaInputGap('shadowed summation binder')
        lower=affine(current['lower'],env,variables or [s.Symbol('unused')],constraints)
        upper=affine(current['upper'],env,variables or [s.Symbol('unused')],constraints)
        if current['domain']=='Finset.range':upper-=1
        u=s.Symbol('u'+str(len(index_names)));variables.append(u);index_names.append(current['binder'])
        env[current['binder']]=lower+u
        inequality=s.expand(upper-lower-u);constraints.append(inequality)
        bounds.append(dict(binder=current['binder'],new_variable=str(u),lower=str(lower),upper=str(upper),inequality=str(inequality)))
        current=current['body']
    if any(a['op']=='sum' for a in walk(current)):raise OmegaInputGap('sum must be a nested finite prefix; distributive conversion is pending')
    if not params: # A literal-sized finite sum is permitted, not a sample of a symbolic theorem.
        constraints_for_projection=[s.sympify(b['inequality'],locals={str(v):v for v in variables}) for b in bounds]
    else:constraints_for_projection=constraints[len(params):]
    external_names=sorted({a['name'] for a in walk(current) if a['op']=='var' and a['name'] not in env})
    externals={name:s.Symbol('W'+str(i)) for i,name in enumerate(external_names)}
    if any(types.get(name) not in ('K','ℂ','ℚ') for name in externals):raise OmegaInputGap('unsupported scalar parameter type')

    def weight(a):
        # A finite sum of exponential-linear monomials is represented by
        # (scalar prefactor, ratios for each nonnegative counting variable).
        op=a['op']
        if op=='int':return [(s.Integer(a['value']),[s.S.One]*len(variables))]
        if op=='var':
            if a['name'] not in externals:raise OmegaInputGap('polynomial index weight needs a moment operator')
            return [(externals[a['name']],[s.S.One]*len(variables))]
        if op=='cast':
            if not any(v['op']=='var' and v['name'] in env for v in walk(a['arg'])):return weight(a['arg'])
            raise OmegaInputGap('nonconstant cast in multiplicative weight')
        if op=='neg':return [(-c,r) for c,r in weight(a['arg'])]
        if op in ('add','sub'):
            left,right=map(weight,a['args'])
            return left+[(c if op=='add' else -c,r) for c,r in right]
        if op in ('mul','div'):
            left,right=map(weight,a['args'])
            if op=='div':
                if any(r!=1 for _,ratios in right for r in ratios):raise OmegaInputGap('index-dependent nonmonomial denominator')
                c=sum(c for c,_ in right)
                if c==0:raise OmegaInputGap('zero scalar denominator')
                right=[(1/c,[s.S.One]*len(variables))]
            return [(s.cancel(a*b),[s.cancel(x*y) for x,y in zip(ar,br)]) for a,ar in left for b,br in right]
        if op=='pow':
            bases=weight(a['args'][0])
            exponent=affine(a['args'][1],env,variables,constraints)
            if len(bases)!=1 or any(v!=1 for v in bases[0][1]):raise OmegaInputGap('nonconstant exponential base')
            base=bases[0][0]
            if base==0:raise OmegaInputGap('zero exponential base requires piecewise support')
            powers=base.as_powers_dict()
            # Input geometric weights must remain Laurent monomials.
            residual=base
            for symbol in externals.values():
                power=powers.get(symbol,s.S.Zero)
                if not power.is_Integer:raise OmegaInputGap('nonintegral scalar power')
                residual/=symbol**power
            if s.cancel(residual).is_Rational is not True:raise OmegaInputGap('nonmonomial exponential base')
            constant=exponent.subs(dict.fromkeys(variables,0))
            return [(base**constant,[base**s.expand(exponent).coeff(v) for v in variables])]
        raise OmegaInputGap('non-geometric weight node '+op)

    terms=weight(current);markers=[s.Symbol('C'+str(i)) for i in range(len(params))]
    rho=s.Symbol('Grade');aux=[s.Symbol('L'+str(i)) for i in range(len(constraints_for_projection))]
    requests=[];bindings=[]
    for coefficient,ratios in terms:
        if coefficient==0:continue
        numerator=s.prod(z**s.expand(f).subs(dict.fromkeys(variables,0)) for z,f in zip(aux,constraints_for_projection))
        monomials=[]
        for i,v in enumerate(variables):
            marker=markers[i] if i<len(params) else rho
            monomials.append(marker*ratios[i]*s.prod(z**s.expand(f).coeff(v) for z,f in zip(aux,constraints_for_projection)))
        grading={str(v):1 for v in [*markers,rho]};grading.update({str(v):0 for v in externals.values()})
        req=dict(schema_version=1,solver='rational_omega',input=dict(numerator=tree(numerator),
            denominator_monomials=list(map(tree,monomials)),grading=grading,
            eliminate=[dict(variable=str(z),operator='ge') for z in aux]))
        requests.append(req);bindings.append(dict(scalar_prefactor=str(coefficient),variable_weights=list(map(str,ratios))))
    if not requests:raise OmegaInputGap('zero weight: no nontrivial Omega computation')
    binding=dict(kind='affine_finite_sum_generating_function',source_span=candidate['source_span'],source_fragment=candidate['source_fragment'],
        source_parameter_types=types,index_substitutions={name:str(env[name]) for name in index_names},bounds=bounds,
        parameters={name:str(v) for name,v in zip(parameter_names,params)},coefficient_variables={name:str(v) for name,v in zip(parameter_names,markers)},
        scalar_parameters={name:str(v) for name,v in externals.items()},constraints=list(map(str,constraints_for_projection)),branches=bindings,
        regulator=str(rho),regulator_removal='substitute Grade=1 after all Omega projections; finite nested intervals certify finite fibers',
        result_meaning='coefficient in C variables at the original symbolic natural parameters equals the selected finite sum',
        original_identity_proved=False,remaining_obligations=['Lean source parsing/encoding bridge','target comparison','parameter specialization'])
    return requests,binding


def reconstruct(outputs,binding):
    from qdifference import rational_read
    if len(outputs)!=len(binding['branches']):raise ValueError('all weight branches must be solved')
    total=s.S.Zero
    for output,branch in zip(outputs,binding['branches']):
        if output['status']!='constructed':raise ValueError('Omega branch not constructed')
        total+=rational_read(branch['scalar_prefactor'])*rational_read(output['result']['value'])
    rho=s.Symbol(binding['regulator'])
    total=s.cancel(total).subs(rho,1)
    if total.has(s.zoo,s.nan,s.oo,-s.oo):raise OmegaInputGap('unresolved grading specialization pole')
    return s.factor(total)
