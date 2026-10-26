"""Exact multivariate linear algebra with primitive fraction-free elimination.

Optional python-flint accelerates polynomial arithmetic. Every returned vector
is checked against every original row; no specialized matrix is trusted.
"""
import sympy as s
from functools import lru_cache


def rational_normal_form(expression):
    """Normalize an exact rational arithmetic tree in a multivariate FLINT field."""
    from flint import fmpq_mpoly_ctx,fmpq
    parameters=sorted(expression.free_symbols,key=str)
    ctx=fmpq_mpoly_ctx.get(tuple(map(str,parameters)) or ('unused',))
    one=ctx.constant(1)
    def reduced(a,b):
        if not b:raise ZeroDivisionError('zero rational denominator')
        g=a.gcd(b)
        return a/g,b/g
    @lru_cache(None)
    def visit(e):
        if e.is_Rational:return ctx.constant(fmpq(int(e.p),int(e.q))),one
        if e.is_Symbol:return ctx.gen(parameters.index(e)),one
        if e.is_Add:
            a,b=ctx.constant(0),one
            for child in e.args:
                c,d=visit(child);a,b=reduced(a*d+c*b,b*d)
            return a,b
        if e.is_Mul:
            a,b=one,one
            for child in e.args:
                c,d=visit(child);a,b=reduced(a*c,b*d)
            return a,b
        if e.is_Pow and e.exp.is_Integer:
            a,b=visit(e.base);power=int(e.exp)
            return reduced(a**power,b**power) if power>=0 else reduced(b**(-power),a**(-power))
        raise ValueError('unsupported exact rational expression')
    a,b=visit(expression)
    def back(poly):
        return s.Add(*(s.Rational(int(c.p),int(c.q))*s.prod(x**e for x,e in zip(parameters,m))
                       for m,c in poly.terms()))
    return back(a)/back(b)


def flint_available():
    try:
        import flint
        return True
    except ImportError:
        return False


def nullspace(rows,transform=None,normalize_index=None,_all_rows=False):
    from flint import fmpq_mpoly_ctx,fmpq
    if not rows:
        raise ValueError('empty linear system requires an explicit column dimension')
    entries=[e for row in rows for e in row]+(list(transform) if transform is not None else [])
    parameters=sorted(set().union(*(e.free_symbols for e in entries)),key=str)
    # FLINT's multivariate contexts require at least one formal generator.
    names=tuple(map(str,parameters)) or ('unused',)
    ctx=fmpq_mpoly_ctx.get(names)
    zero,one=ctx.constant(0),ctx.constant(1)
    def poly(e):
        if not parameters:return ctx.constant(fmpq(int(e.p),int(e.q)))
        return ctx.from_dict({m:fmpq(int(c.p),int(c.q)) for m,c in s.Poly(e,*parameters).terms()})
    original=[]
    for row in rows:
        fractions=[tuple(map(poly,s.fraction(e))) for e in row]
        common=one
        for _,den in fractions:common=common*den/common.gcd(den)
        cleared=[num*(common/den) for num,den in fractions]
        content=zero
        for e in cleared:content=content.gcd(e)
        original.append([e/content for e in cleared] if content else cleared)
    selected=list(range(len(original)))
    if not _all_rows:
        modular={};selected=[];prime=32003
        values=[2*i+3 for i in range(len(names))]
        for idx in sorted(range(len(original)),key=lambda i:sum(len(x) for x in original[i])):
            evaluated=[x(*values) for x in original[idx]]
            try:row=[int(x.p)*pow(int(x.q)%prime,-1,prime)%prime for x in evaluated]
            except ValueError:continue
            for col,basis in sorted(modular.items()):
                c=row[col];row=[(a-c*b)%prime for a,b in zip(row,basis)]
            col=next((i for i,v in enumerate(row) if v),None)
            if col is not None:
                inv=pow(row[col],-1,prime)
                modular[col]=[a*inv%prime for a in row];selected.append(idx)
        if not selected:selected=list(range(len(original)))
    matrix=[original[i][:] for i in selected]
    pivot=0;pivots=[]
    for col in range(len(matrix[0])):
        choices=[i for i in range(pivot,len(matrix)) if matrix[i][col]]
        if not choices:continue
        chosen=min(choices,key=lambda i:len(matrix[i][col]))
        matrix[pivot],matrix[chosen]=matrix[chosen],matrix[pivot]
        value=matrix[pivot][col]
        for i in range(pivot+1,len(matrix)):
            coefficient=matrix[i][col]
            if not coefficient:continue
            for j in range(col+1,len(matrix[i])):
                matrix[i][j]=value*matrix[i][j]-coefficient*matrix[pivot][j]
            matrix[i][col]=zero
            content=zero
            for e in matrix[i][col+1:]:content=content.gcd(e)
            if content:
                for j in range(col+1,len(matrix[i])):matrix[i][j]=matrix[i][j]/content
        pivots.append(col);pivot+=1
        if pivot==len(matrix):break
    class Rat:
        def __init__(self,a,b=one):
            if not b:raise ZeroDivisionError('zero polynomial denominator')
            common=a.gcd(b)
            self.a,self.b=a/common,b/common
        def __add__(self,other):return Rat(self.a*other.b+other.a*self.b,self.b*other.b)
        def negative(self):return Rat(-self.a,self.b)
        def mul(self,p):return Rat(self.a*p,self.b)
        def div(self,p):return Rat(self.a,self.b*p)
        def times(self,other):return Rat(self.a*other.a,self.b*other.b)
        def quotient(self,other):return Rat(self.a*other.b,self.b*other.a)
    def back(poly):
        return s.Add(*(s.Rational(int(c.p),int(c.q))*s.prod(x**e for x,e in zip(parameters,m))
                       for m,c in poly.terms()))
    solutions=[]
    projection=([[Rat(*map(poly,s.fraction(e))) for e in transform.row(i)]
                  for i in range(transform.rows)] if transform is not None else None)
    for free in [i for i in range(len(matrix[0])) if i not in pivots]:
        vector=[Rat(zero) for _ in matrix[0]];vector[free]=Rat(one)
        for i,col in reversed(list(enumerate(pivots))):
            total=Rat(zero)
            for j in range(col+1,len(vector)):total=total+vector[j].mul(matrix[i][j])
            vector[col]=total.negative().div(matrix[i][col])
        for row in original:
            total=Rat(zero)
            for a,v in zip(row,vector):total=total+v.mul(a)
            if total.a:
                if not _all_rows:return nullspace(rows,transform,normalize_index,True)
                raise ArithmeticError('exact nullspace residual failed')
        if projection is not None:
            vector=[sum((a.times(v) for a,v in zip(row,vector)),Rat(zero)) for row in projection]
        if normalize_index is not None:
            top=vector[normalize_index]
            if not top.a:continue
            vector=[v.quotient(top) for v in vector]
        solutions.append([back(v.a)/back(v.b) for v in vector])
    return s.Matrix(solutions) if solutions else s.zeros(0,len(projection) if projection is not None else len(matrix[0]))
