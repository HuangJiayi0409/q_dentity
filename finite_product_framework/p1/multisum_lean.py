"""Certificate-driven triangular Pochhammer proof compiler.

All kernels, recurrence coefficients, and fluxes come from native expressions
and the current construction. No identity identifiers or stored answers occur.
"""
import sympy as s
from expressions import expression,Poch,n,q,Q
from multisum import rationalize,derive,verify
from exact_linear import rational_normal_form
from lean_pipeline import HERE,find_nodes


class Compiler:
    def __init__(self,model,construction,hypotheses):
        if model['domain']!='simplex' or model['dimension']!=2 or construction['order']!=1:
            raise ValueError('representation_gap: first triangular emitter requires dimension two and order one')
        self.model=model
        self.i,self.j=s.symbols('i0 i1')
        self.X,self.Y=s.symbols('X0 X1')
        self.F=expression(model['summand']);self.T=expression(model['target'])
        self.names={v:k for k,v in model['names'].items()}
        self.params=sorted(self.F.free_symbols-{n,self.i,self.j,q},key=str)
        self.atoms=sorted(self.F.atoms(Poch),key=str)
        powers=self.F.as_powers_dict()
        if any(powers.get(a) not in (-1,1) or a.args[1]!=q for a in self.atoms):
            raise ValueError('representation_gap: multiplicative single-base Pochhammer kernel required')
        self.bottom=[a for a in self.atoms if powers[a]==-1]
        for atom in self.atoms:
            if atom.args[2] not in (self.i,self.j,self.i+self.j):
                raise ValueError('representation_gap: triangular linear Pochhammer lengths required')
        problem={'schema_version':1,'source_id':'proof-compiler','indices':['i0','i1'],'summand':model['summand']}
        _,V,U=derive(problem)
        loc={str(x):x for x in self.F.free_symbols|{q,Q,self.X,self.Y}}
        self.cs=[s.sympify(c,locals=loc) for c in construction['coefficients']]
        self.R=[s.sympify(c,locals=loc) for c in construction['certificates']]
        verify(V,U,(self.X,self.Y),self.cs,self.R)
        if self.cs[1]!=1:raise ValueError('invalid_certificate: monic recurrence required')
        self.C=s.factor(-self.cs[0])
        self.H=[s.factor(rational_normal_form(r/V)) for r in self.R]
        self.domain=next((h['name'] for h in hypotheses if h['type']['op']=='forall'
                         and find_nodes(h['type'],'FiniteQBenchmark.pochList')),None)
        self.nonzero=next((h['name'] for h in hypotheses if h['type']['op']=='Ne'
                          and find_nodes(h['type'],'HMul.hMul')),None)
        if self.domain is None or self.nonzero is None:
            raise ValueError('domain_unresolved: native product-domain assumptions required')

    def field(self,e,N='msn',J='msj',K='msk'):
        if e.is_Integer:return f'({int(e)} : K)'
        if e.is_Rational:return f'(({e.p}:K) / ({e.q}:K))'
        if e.is_Symbol:
            if e==Q:return f'({self.names["q"]}^{N})'
            if e==self.X:return f'({self.names["q"]}^{J})'
            if e==self.Y:return f'({self.names["q"]}^{K})'
            return self.names[str(e)]
        if e.func==Poch:
            return f'(poch {self.field(e.args[0],N,J,K)} {self.field(e.args[1],N,J,K)} {self.nat(e.args[2],N,J,K)})'
        if e.is_Add:
            positives=[t for t in e.args if not t.could_extract_minus_sign()]
            negatives=[-t for t in e.args if t.could_extract_minus_sign()]
            head=' + '.join(self.field(t,N,J,K) for t in positives) or '(0:K)'
            return '('+head+''.join(' - '+self.field(t,N,J,K) for t in negatives)+')'
        if e.is_Mul:
            if e.could_extract_minus_sign():return '(-'+self.field(-e,N,J,K)+')'
            return '('+' * '.join(self.field(t,N,J,K) for t in e.args)+')'
        if e.is_Pow:
            base,power=e.args
            if power.is_Integer:
                body=self.field(base,N,J,K) if abs(power)==1 else f'({self.field(base,N,J,K)} ^ {abs(int(power))})'
                return body if power>=0 else f'({body})⁻¹'
            if base==q:
                poly=s.Poly(s.expand(power),n,self.i,self.j)
                if poly.total_degree()>1:raise ValueError('representation_gap: nonlinear q exponent')
                factors=[]
                for symbol,label in ((n,N),(self.i,J),(self.j,K)):
                    c=poly.coeff_monomial(symbol)
                    if not c.is_Integer:raise ValueError('representation_gap: nonintegral exponent')
                    if c:
                        value=f'({self.names["q"]}^{label})'
                        if abs(c)!=1:value=f'({value}^{abs(int(c))})'
                        factors.append(value if c>0 else f'({value})⁻¹')
                constant=poly.coeff_monomial(1)
                if constant:factors.append(self.field(q**constant,N,J,K))
                return '('+' * '.join(factors)+')' if factors else '(1:K)'
            return f'({self.field(base,N,J,K)} ^ {self.nat(power,N,J,K)})'
        raise ValueError('representation_gap: scalar printer '+str(e))

    def nat(self,e,N,J,K):
        if e.is_Integer and e>=0:return str(e)
        if e==n:return N
        if e==self.i:return J
        if e==self.j:return K
        if e.is_Add:return '('+' + '.join(self.nat(t,N,J,K) for t in e.args)+')'
        raise ValueError('representation_gap: natural index '+str(e))

    def normalize(self):
        return ('pochList_cons, pochList_nil, mul_one, one_mul, zpow_sub₀ msq0, '
                'zpow_add₀ msq0, zpow_neg, zpow_natCast, zpow_one, '
                'div_eq_mul_inv, mul_inv_rev, inv_inv, mul_assoc, mul_left_comm, mul_comm')

    def known_parameters(self):
        lines=[f'  have msreg : regular {self.names["q"]} := by assumption',
               f'  have msq0 : {self.names["q"]} ≠ 0 := msreg.1']
        for index,p in enumerate(self.params):
            lines.append(f'  have msp{index} : {self.field(p)} ≠ 0 := by\n'
                         f'    intro hz\n    have hh := {self.nonzero}\n    simp [hz] at hh')
        return lines

    def factor_field(self,value,N,J,K):
        coefficient,factors=s.factor_list(value)
        pieces=[self.field(coefficient,N,J,K)]
        for f,power in factors:
            item=self.field(f,N,J,K)
            if power!=1:item=f'({item}^{power})'
            pieces.append(item)
        return '('+' * '.join(pieces)+')'

    def scalar_facts(self,known,N,J,K,indent='    '):
        """Turn known nonzero rational expressions into nonzero polynomial factors."""
        lines=[];names=[]
        units=['msq0']+[f'msp{i}' for i in range(len(self.params))]
        for number,(value,proof) in enumerate(known):
            r=rational_normal_form(rationalize(value,(self.i,self.j),(self.X,self.Y)))
            num,den=s.fraction(r);num=s.factor(num);den=s.factor(den)
            eq=f'mseq{number}';nz=f'msnz{number}'
            lines += [f'{indent}have msknown{number} : {self.field(value,N,J,K)} ≠ 0 := by',
                      f'{indent}  convert {proof} using 1 <;> (try simp only [pow_add, pow_succ]) <;> ring',
                      f'{indent}have {eq} : {self.field(value,N,J,K)} = '
                      f'{self.factor_field(num,N,J,K)} / {self.factor_field(den,N,J,K)} := by',
                      f'{indent}  try simp only [pow_add, pow_succ]',
                      f'{indent}  field_simp [{", ".join(units)}]',f'{indent}  <;> ring',
                      f'{indent}have {nz} : {self.field(num,N,J,K)} ≠ 0 := by',
                      f'{indent}  intro hz',f'{indent}  apply msknown{number}',
                      f'{indent}  rw [{eq}]',
                      f'{indent}  have hf : {self.factor_field(num,N,J,K)}=0 := by convert hz using 1 <;> ring',
                      f'{indent}  rw [hf]',f'{indent}  simp']
            names.extend([nz,f'msknown{number}'])
            for f,_ in s.factor_list(num)[1]:
                name=f'msden{len(names)}'
                lines += [f'{indent}have {name} : {self.field(f,N,J,K)} ≠ 0 := by',
                          f'{indent}  intro hz',f'{indent}  apply {nz}',f'{indent}  linear_combination {self.field(s.cancel(num/f),N,J,K)} * hz']
                canon=name+'Canonical'
                lines += [f'{indent}have {canon} := {name}', f'{indent}try ring_nf at {canon}']
                names.extend([name,canon])
        self.local_rewrites=[f'mseq{i}' for i in range(len(known))]
        return lines,names

    def domain_facts(self,N):
        base=self.names['q'];lines=[]
        norm=self.normalize()+', msExp, pow_succ, poch_zero, Nat.add_zero, Nat.zero_add, mul_ne_zero_iff'
        for i,atom in enumerate(self.bottom):
            a,_,length=atom.args
            A=a.subs(n,n+1)
            j,k=('mst','0') if length.has(self.i) else ('0','mst')
            lines += [f'    have msD{i} : ∀ mst ≤ {N}+1, poch {self.field(A,N)} {base} mst ≠ 0 := by',
                      '      intro mst ht',
                      f'      have hs := ({self.domain} {j} (by simp only [Finset.mem_range]; omega)).1 {k} (by simp only [Finset.mem_range]; omega)',
                      f'      simp only [{norm}] at hs ⊢', '      tauto']
            if a.has(n):
                if rational_normal_form(rationalize(a/A-q,(self.i,self.j),(self.X,self.Y)))!=0:
                    raise ValueError('representation_gap: only negative unit n-shift of Pochhammer starts supported')
                lines += [f'    have msStart{i} : {self.field(a,N)} = {self.field(A,N)} * {base} := by',
                          '      try simp only [pow_succ]',
                          '      field_simp [msq0]', '      <;> ring',
                          f'    have msOld{i} : ∀ mst ≤ {N}, poch {self.field(a,N)} {base} mst ≠ 0 := by',
                          '      intro mst ht',f'      rw [msStart{i}]',
                          f'      exact FiniteQP1.multisum_poch_prefix_ne _ _ mst {N} ht (FiniteQP1.multisum_poch_shift_ne _ _ {N} (msD{i} ({N}+1) le_rfl))']
            else:
                lines += [f'    have msOld{i} : ∀ mst ≤ {N}, poch {self.field(a,N)} {base} mst ≠ 0 := by',
                          f'      intro mst ht; exact msD{i} mst (by omega)']
        return lines

    def instantiate_old_domain(self,N):
        norm=self.normalize()+', poch_zero, mul_ne_zero_iff'
        lines=['    have msPrevious := msIH (by',
               '      intro msj hj','      constructor','      · intro msk hk',
               '        simp only [Finset.mem_range] at hj hk']
        for i,atom in enumerate(self.bottom):
            length=self.nat(atom.args[2],N,'msj','msk')
            lines.append(f'        have hd{i} := msOld{i} {length} (by omega)')
        lines += [f'        simp only [{norm}] at '+ ' '.join(f'hd{i}' for i in range(len(self.bottom)))+' ⊢', '        tauto',
                  '      · have hd0 := msOld0 0 (by omega)']
        for i,atom in enumerate(self.bottom):
            if not atom.args[0].has(n):lines.append(f'        have hdT{i} := msOld{i} {N} le_rfl')
        lines += [f'        simp only [{norm}] at '+ ' '.join(f'hdT{i}' for i,a in enumerate(self.bottom) if not a.args[0].has(n))+' ⊢','        tauto)']
        return lines

    def algebra_facts(self,N,J,K,mode='local',indent='      '):
        base=self.names['q'];lines=[];known=[];poch_names=[]
        lines += [f'{indent}have msQN : {base}^{N} ≠ 0 := pow_ne_zero _ msq0',
                  f'{indent}have msQJ : {base}^{J} ≠ 0 := pow_ne_zero _ msq0',
                  f'{indent}have msQK : {base}^{K} ≠ 0 := pow_ne_zero _ msq0',
                  f'{indent}have msTermHead : 1-({base}^({N}+1))⁻¹ ≠ 0 := by',
                  f'{indent}  apply sub_ne_zero.mpr',f'{indent}  intro hh',
                  f'{indent}  have hh2 := congrArg (fun x : K => x⁻¹) hh',
                  f'{indent}  simp only [inv_one, inv_inv] at hh2',
                  f'{indent}  exact msreg.2 ({N}+1) (by omega) hh2.symm']
        known.append((1-q**(-n-1),'msTermHead'))
        for i,atom in enumerate(self.bottom):
            a,_,length=atom.args;A=a.subs(n,n+1)
            lines += [f'{indent}have msHead{i} : 1-{self.field(A,N,J,K)} ≠ 0 := by',
                      f'{indent}  simpa only [pow_zero, mul_one] using (FiniteQP1.multisum_poch_factor_ne {self.field(A,N,J,K)} {base} 0 ({N}+1) (by omega) (msD{i} ({N}+1) le_rfl))']
            known.append((1-A,f'msHead{i}'))
            if not a.has(n):
                lines += [f'{indent}have msLastN{i} := FiniteQP1.multisum_poch_factor_ne {self.field(A,N,J,K)} {base} {N} ({N}+1) (by omega) (msD{i} ({N}+1) le_rfl)']
                known.append((1-A*q**n,f'msLastN{i}'))
            if mode=='local':
                L=self.nat(length,N,J,K)
                lines += [f'{indent}have msP{i} := msD{i} {L} (by omega)',
                          f'{indent}have msLast{i} := FiniteQP1.multisum_poch_factor_ne {self.field(A,N,J,K)} {base} {L} ({N}+1) (by omega) (msD{i} ({N}+1) le_rfl)']
                poch_names.append(f'msP{i}')
                known.append((1-A*q**length,f'msLast{i}'))
            elif mode=='upper' and length in (self.i,self.j):
                L=self.nat(length,N,J,K)
                lines += [f'{indent}have msLast{i} := FiniteQP1.multisum_poch_factor_ne {self.field(A,N,J,K)} {base} {L} ({N}+1) (by omega) (msD{i} ({N}+1) le_rfl)']
                known.append((1-A*q**length,f'msLast{i}'))
        extra,names=self.scalar_facts(known,N,J,K,indent)
        lines+=extra
        return lines,['msq0','msQN','msQJ','msQK','msPole']+[f'msp{i}' for i in range(len(self.params))]+names+poch_names

    def abstract_products(self,N,units):
        lines=[]
        for i,atom in enumerate(self.atoms):
            A=atom.subs(n,n+1)
            loc=''
            if atom in self.bottom:loc=f'msP{self.bottom.index(atom)} '
            lines.append(f'      generalize msAtom{i} : {self.field(A,N)} = msAP{i} at {loc}⊢')
        return lines

    def scalar_local(self,N,units):
        """Verify the scalar relation before multiplying the shared Pochhammer monomial.

        Splitting this step prevents denominator clearing from expanding every
        copy of the same finite products into an enormous polynomial.
        """
        units=[u for u in units if not (u.startswith('msP') and u[3:].isdigit())]
        powers=self.F.as_powers_dict()
        weight=self.F.xreplace({a:s.S.One for a in self.atoms})
        def amp(dn,dj,dk):
            answer=weight.subs({n:n+dn,self.i:self.i+dj,self.j:self.j+dk},simultaneous=True)
            for atom in self.atoms:
                a,_,L=atom.args;A=a.subs(n,n+1)
                if dn==0 and a.has(n):factor=(1-A*q**L)/(1-A)
                elif dj or dk:
                    change=s.expand(L.subs({self.i:self.i+dj,self.j:self.j+dk},simultaneous=True)-L)
                    factor=1-A*q**L if change==1 else s.S.One
                else:factor=s.S.One
                answer*=factor**powers[atom]
            return answer
        old,new,jumpj,jumpk=amp(0,0,0),amp(1,0,0),amp(1,1,0),amp(1,0,1)
        terms=[new,self.C*old,jumpj*self.H[0].subs(self.X,self.X*q),new*self.H[0],jumpk*self.H[1].subs(self.Y,self.Y*q),new*self.H[1]]
        normal=[s.factor(rational_normal_form(rationalize(t,(self.i,self.j),(self.X,self.Y)))) for t in terms]
        def relation(values):
            v=[self.field(t,N) for t in values]
            return f'{v[0]}-{v[1]} = ({v[2]}-{v[3]})+({v[4]}-{v[5]})'
        lines=[f'      have msScalarLocal : {relation(terms)} := by',
               '        clear msIH', '        clear * - '+ ' '.join(units+self.local_rewrites)]
        for number,(raw,normalized) in enumerate(zip(terms,normal)):
            lines += [f'        have msScalarTerm{number} : {self.field(raw,N)}={self.field(normalized,N)} := by',
                      '          try simp only ['+', '.join(self.local_rewrites)+', div_eq_mul_inv, mul_inv_rev, inv_inv, inv_neg, neg_mul, mul_neg, pow_one, mul_one, one_mul]',
                      '          all_goals try simp only [pow_add, pow_succ]']
            for value,name in ((f'{self.names["q"]}^{N}','msQQ'),(f'{self.names["q"]}^msj','msXX'),(f'{self.names["q"]}^msk','msYY')):
                lines.append(f'          all_goals generalize {value} = {name} at '+ ' '.join(units)+' ⊢')
            lines += ['          all_goals field_simp ['+', '.join(units)+']',
                      '          all_goals try ring_nf',
                      '          all_goals try field_simp ['+', '.join(units)+']',
                      '          all_goals ring']
        lines += ['        rw ['+', '.join('msScalarTerm'+str(i) for i in (2,3,4,5,1,0))+']']
        for value,name in ((f'{self.names["q"]}^{N}','msQQ'),(f'{self.names["q"]}^msj','msXX'),(f'{self.names["q"]}^msk','msYY')):
            lines.append(f'        generalize {value} = {name} at '+ ' '.join(units)+' ⊢')
        lines += ['        field_simp ['+', '.join(units)+']',
                  '        all_goals try ring_nf',
                  '        all_goals try field_simp ['+', '.join(units)+']',
                  '        all_goals ring',
                  '      simp only [div_eq_mul_inv, mul_inv_rev, inv_inv]',
                  '      ac_nf at msScalarLocal ⊢']
        common=s.prod(s.Symbol(f'msAP{i}')**powers[a] for i,a in enumerate(self.atoms))
        oldnames=self.names
        self.names={**self.names,**{f'msAP{i}':f'msAP{i}' for i in range(len(self.atoms))}}
        lines.append(f'      linear_combination {self.field(common,N)} * msScalarLocal')
        self.names=oldnames
        return lines

    def upper_proof(self,N):
        lines=[f'    have msUpper : ∀ msj, msj ≤ {N}+1 →',
               f'        msG {N} msj ({N}+1-msj)+msH {N} msj ({N}+1-msj)+msF ({N}+1) msj ({N}+1-msj)=0 := by',
               '      clear msLocal msPrevious msPreviousN msIH',
               '      intro msj hj',
               f'      let msk := {N}+1-msj',
               f'      have msSum : msj+msk={N}+1 := by dsimp [msk]; omega',
               '      change msG _ msj msk+msH _ msj msk+msF _ msj msk=0',
               '      by_cases msj0 : msj=0']
        for mode in ('left','right','interior'):
            indent='        ' if mode=='left' else '          '
            if mode=='left':
                lines+=['      · subst msj',f'        have mskN : msk={N}+1 := by omega','        subst msk']
                J,K='0',f'({N}+1)';hs=[h.subs(self.X,1).subs(self.Y,Q*s.Symbol('q')) for h in self.H]
            else:
                if mode=='right':
                    lines+=['      · by_cases msk0 : msk=0','        · have msjN : msj='+N+'+1 := by omega','          subst msk','          subst msj']
                    J,K=f'({N}+1)','0';hs=[h.subs(self.Y,1).subs(self.X,Q*s.Symbol('q')) for h in self.H]
                else:
                    lines+=['        · have hjn : msj ≤ '+N+' := by omega','          have hkn : msk ≤ '+N+' := by omega']
                    J,K='msj','msk';hs=self.H
            facts,units=self.algebra_facts(N,J,K,'upper' if mode=='interior' else 'endpoint',indent)
            lines+=facts
            scalar=s.factor(rational_normal_form(sum(hs)+1));num,den=s.fraction(scalar)
            if mode!='interior':
                lines += [indent+'dsimp only [msG,msH]',indent+'simp only [Nat.sub_zero, Nat.sub_self, pow_zero, pow_succ, mul_zero, zero_mul, one_mul, mul_one, sub_self, add_neg_cancel, neg_add_cancel, inv_zero]',indent+'field_simp ['+', '.join(units)+']',indent+'<;> ring']
            else:
                edge=self.X*self.Y-Q*q
                lines += [indent+f'have msEdge : {self.field(edge,N,J,K)}=0 := by',
                          indent+'  have hh : '+self.names['q']+'^msj*'+self.names['q']+'^msk='+self.names['q']+f'^{N}*'+self.names['q']+' := by rw [← pow_add, msSum, pow_succ]',
                          indent+'  linear_combination hh',
                          indent+f'have msScalar : {self.field(self.H[0],N,J,K)}+{self.field(self.H[1],N,J,K)}+1=0 := by',
                          indent+f'  calc _ = {self.field(num,N,J,K)}/{self.field(den,N,J,K)} := by',
                          indent+'          field_simp ['+', '.join(units)+']',indent+'          <;> ring',
                          indent+'       _ = 0 := by',
                          indent+f'          have hz : {self.field(num,N,J,K)}=0 := by linear_combination {self.field(s.cancel(num/edge),N,J,K)} * msEdge',
                          indent+'          rw [hz, zero_div]',
                          indent+'dsimp only [msG,msH]',indent+'linear_combination msF ('+N+'+1) msj msk * msScalar']
        return lines

    def emit(self):
        base=self.names['q'];N=self.model['index']
        poles=set()
        for h in self.H:
            for f,_ in s.factor_list(s.fraction(h)[1])[1]:
                if not f.has(Q,self.X,self.Y,q) and f not in self.params:poles.add(f)
        if len(poles)!=1:raise ValueError('domain_unresolved: current emitter expects one linear parameter pole')
        pole=poles.pop();symbols=sorted(pole.free_symbols,key=str)
        solutions=s.solve(pole,symbols[0])
        if len(symbols)!=2 or solutions!=[symbols[1]]:
            raise ValueError('domain_unresolved: unsupported pole specialization')
        a,b=map(self.field,symbols)
        lines=['  classical']+self.known_parameters()
        lines += [f'  let msF : ℕ → ℕ → ℕ → K := fun msn msj msk => {self.field(self.F)}',
                  f'  let msT : ℕ → K := fun msn => {self.field(self.T)}',
                  f'  let msC : ℕ → K := fun msn => {self.field(self.C)}',
                  f'  let msG : ℕ → ℕ → ℕ → K := fun msn msj msk => msF (msn+1) msj msk * {self.field(self.H[0])}',
                  f'  let msH : ℕ → ℕ → ℕ → K := fun msn msj msk => msF (msn+1) msj msk * {self.field(self.H[1])}',
                  f'  by_cases msEqual : {a}={b}',f'  · subst {a}',
                  f'    have msDT := ({self.domain} 0 (by simp)).2.2',
                  f'    simp only [pochList_cons, pochList_nil, mul_one] at msDT ⊢',
                  f'    have msCancel : ∀ x : K, {b}*x/{b}=x := by intro x; field_simp',
                  f'    simp [msCancel, FiniteQP1.multisum_poch_one, ite_mul, mul_ite, ite_div, msDT, '+', '.join(f'msp{i}' for i in range(len(self.params)))+']',
                  f'  have msPole : {self.field(pole)} ≠ 0 := by',
                  '    intro hz','    apply msEqual','    linear_combination hz',
                  f'  revert {self.domain}',f'  induction {N} with',
                  f'  | zero => intro {self.domain}; simp [pochList, poch]',
                  f'  | succ {N} msIH =>',f'    intro {self.domain}',
                  f'    have msExp : (1-(({N}+1 : ℕ):ℤ)) = -({N}:ℤ) := by omega']
        new_names=[]
        for i,atom in enumerate(self.atoms):
            a=atom.args[0]
            if a.has(n):
                lines += [f'    have msNormalize{i} : {self.field(a,"("+N+"+1)")} = {self.field(a.subs(n,n+1),N)} := by',
                          '      try simp only [pow_succ]', '      field_simp [msq0]', '      <;> ring']
                new_names.append(f'msNormalize{i}')
        lines+=self.domain_facts(N)
        lines+=self.instantiate_old_domain(N)
        norm=self.normalize()
        scalar_norm=norm.replace(', mul_assoc, mul_left_comm, mul_comm','')
        lines += [f'    have msPreviousN : FiniteQP1.triangleSum (msF {N}) {N} = msT {N} := by',
                  '      dsimp only [FiniteQP1.triangleSum, msF, msT]',
                  '      convert msPrevious using 1',
                  '      · apply Finset.sum_congr rfl; intro j hj',
                  '        apply Finset.sum_congr rfl; intro k hk',
                  f'        simp only [{scalar_norm}]',
                  '        ac_rfl',
                  f'      · simp only [{scalar_norm}]',
                  '        ac_rfl',
                  f'    have msLocal : ∀ msj msk, msj+msk ≤ {N} →',
                  f'        msF ({N}+1) msj msk-msC {N}*msF {N} msj msk =',
                  f'        (msG {N} (msj+1) msk-msG {N} msj msk)+(msH {N} msj (msk+1)-msH {N} msj msk) := by',
                  '      intro msj msk hbound']
        facts,units=self.algebra_facts(N,'msj','msk')
        lines+=facts
        shifts=[];local_new=[]
        for i,atom in enumerate(self.atoms):
            a,_,length=atom.args
            if not a.has(n):continue
            A=a.subs(n,n+1)
            if rational_normal_form(rationalize(a/A-q,(self.i,self.j),(self.X,self.Y)))!=0:raise ValueError('representation_gap: unsupported atom start shift')
            head='msTermHead' if a==q**(-n) else f'msHead{self.bottom.index(atom)}'
            lines += [f'      have msNew{i} : {self.field(a,"("+N+"+1)")} = {self.field(A,N)} := by',
                      '        try simp only [pow_succ]',
                      '        field_simp [msq0]', '        <;> ring']
            local_new.append(f'msNew{i}')
            lines += [f'      have msA{i} : {self.field(a,N)} = {self.field(A,N)} * {base} := by',
                      '        try simp only [pow_succ]','        field_simp [msq0]','        <;> ring',
                      f'      have msShift{i} : {self.field(atom,N)} =',
                      f'          poch {self.field(A,N)} {base} {self.nat(length,N,"msj","msk")} *',
                      f'          (1-{self.field(A,N)}*{base}^{self.nat(length,N,"msj","msk")})/(1-{self.field(A,N)}) := by',
                      f'        conv_lhs => rw [msA{i}]',f'        apply FiniteQP1.multisum_poch_shift',
                      f'        simpa only [pow_succ, mul_inv_rev, mul_comm] using {head}']
            shifts.append(f'msShift{i}')
        lines += ['      dsimp only [msG, msH, msC, msF]']
        lines += [f'      simp only [{name}]' for name in reversed(local_new)]
        lines += [f'      simp only [{", ".join(shifts)}, show msj+1+msk=msj+msk+1 by omega, show msj+(msk+1)=msj+msk+1 by omega, poch_succ, pow_succ, pow_add]',
                  *self.abstract_products(N,units),
                  *self.scalar_local(N,units),
                  f'    have msGzero : ∀ k, msG {N} 0 k=0 := by intro k; simp [msG]',
                  f'    have msHzero : ∀ j, msH {N} j 0=0 := by intro j; simp [msH]']
        lines+=self.upper_proof(N)
        lines += [f'    have msStep := FiniteQP1.triangle_homogeneous msF (msG {N}) (msH {N}) (msC {N}) {N} msLocal msGzero msHzero msUpper',
                  f'    have msTarget : msT ({N}+1)=msC {N}*msT {N} := by',
                  '      clear msLocal msStep msUpper msPrevious msPreviousN msIH']
        facts,units=self.algebra_facts(N,'0','0','endpoint')
        lines+=facts
        for i,atom in enumerate(self.bottom):
            if not atom.args[0].has(n):
                lines.append(f'      have msTP{i} := msD{i} {N} (by omega)')
                units.append(f'msTP{i}')
        lines += ['      dsimp only [msT,msC]','      simp only [poch_succ,pow_succ]',
                  '      field_simp ['+', '.join(units)+']',
                  '      all_goals try ring_nf',
                  '      all_goals try field_simp ['+', '.join(units)+']',
                  '      all_goals ring',
                  f'    have msResult : FiniteQP1.triangleSum (msF ({N}+1)) ({N}+1)=msT ({N}+1) := by',
                  '      rw [msStep,msPreviousN,msTarget]',
                  '    convert msResult using 1',
                  '    · dsimp only [FiniteQP1.triangleSum, msF]',
                  '      apply Finset.sum_congr rfl; intro j hj',
                  '      apply Finset.sum_congr rfl; intro k hk',
                  * [f'      simp only [{name}]' for name in reversed(new_names)],
                  f'      simp only [{scalar_norm}, msExp, pow_succ]',
                  '      ac_nf <;> ring',
                  '    · dsimp only [msT]',
                  f'      simp only [{scalar_norm}, msExp, pow_succ]',
                  '      ac_nf <;> ring']
        # Nonzero conditions have already been proved from the original domain.
        # Restrict discharge to those facts; recursive default simplification can
        # repeatedly unfold large unrelated local proofs in the combined theorem.
        import re
        text='\n'.join(lines)+'\n'
        return re.sub(r'field_simp \[[^\n]*?\]',
            'field_simp (discharger := (first | assumption | (apply pow_ne_zero; assumption) | (apply inv_ne_zero.mpr; assumption) | norm_num))', text)

