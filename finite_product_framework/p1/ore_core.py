"""Standard-input adapter for exact univariate q-Ore constructions.

Recurrences supplied here are premises. A summand telescoper is NOT silently
promoted to a homogeneous finite-sum annihilator: boundary terms remain external.
"""
import re
import sympy as s
from expressions import q,Q,X
from qgosper import UnsupportedDomain
from qparameterized import primitive_relation
from ore import (clean,divide,greatest_common_right_divisor,common_left_multiple,
                 companion,sigma,iterate_row,graded_polynomial_closure,eliminate,
                 OreResourceLimit)


def normalized_operator(values):
    values=clean(values)
    if values==[0]:
        return dict(coefficients=['0'],order=None,leading_coefficient='0',scaling_factor='1')
    parameters=set().union(*(v.free_symbols for v in values),{q,Q})
    result=primitive_relation(values,s.Integer(1),parameters)
    result.pop('certificate')
    result.update(order=len(values)-1,variable='n',shift='n -> n+1; Q -> q*Q')
    return result


def compute(data,budget,parse):
    if not isinstance(data,dict) or 'operation' not in data:
        raise ValueError('q_ore input requires operation')
    operation=data['operation'];tracked=[];leading=[]

    def track(values):
        values=clean(values)
        if any(v.has(X) for v in values):
            raise UnsupportedDomain('q-Ore coefficients use Q and parameters; X is reserved for summation')
        tracked.extend(values)
        return values

    def operator(nodes):
        if not isinstance(nodes,list) or not nodes:
            raise ValueError('nonempty ascending operator coefficient array required')
        if len(nodes)>budget.max_unknowns:
            raise OreResourceLimit('input operator coefficient count exceeds limit')
        values=track(list(map(parse,nodes)))
        if values!=[0]:leading.append(values[-1])
        return values

    if operation in ('right_division','left_division','gcrd','lclm'):
        if set(data)!={'operation','a','b'}:raise ValueError('operation requires only a and b')
        a,b=operator(data['a']),operator(data['b'])
        if operation.endswith('division'):
            side=operation.split('_')[0]
            quotient,remainder=divide(a,b,side)
            track(quotient);track(remainder)
            raw=dict(quotient=list(map(str,quotient)),remainder=list(map(str,remainder)),
                     identity='a = quotient*b + remainder' if side=='right' else 'a = b*quotient + remainder',
                     residual='0')
        else:
            raw=(greatest_common_right_divisor(a,b) if operation=='gcrd' else
                 common_left_multiple(a,b,budget.max_unknowns))
            symbols={str(t):t for t in set().union(*(v.free_symbols for v in tracked),{q,Q})}
            for values in raw.values():
                if isinstance(values,list):track([s.sympify(v,locals=symbols) for v in values])
        normalized_input=dict(a=list(map(str,a)),b=list(map(str,b)))
    elif operation=='normalize':
        if set(data)!={'operation','a'}:raise ValueError('normalize requires only a')
        a=operator(data['a']);raw=dict(operator=list(map(str,a)),residual='0')
        normalized_input=dict(a=list(map(str,a)))
    elif operation=='closure':
        if set(data)!={'operation','sequences','observable'}:
            raise ValueError('closure requires sequences and observable')
        sequences=data['sequences']
        if not isinstance(sequences,dict) or not sequences:
            raise ValueError('nonempty named sequence recurrences required')
        if any(not isinstance(name,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',name)
               for name in sequences):raise ValueError('invalid sequence name')
        recurrences={name:operator(nodes) for name,nodes in sorted(sequences.items())}
        if any(len(cs)<2 for cs in recurrences.values()):
            raise ValueError('unsupported_structure: closure requires positive-order recurrences')
        dimension=sum(len(cs)-1 for cs in recurrences.values())
        if dimension>budget.max_states:raise OreResourceLimit('input state dimension exceeds limit')
        M=s.diag(*(companion(cs) for cs in recurrences.values()))
        track(list(M))
        variables=tuple(s.Dummy(f'state{i}') for i in range(dimension))
        positions={};start=0
        for name,cs in recurrences.items():
            positions[name]=(start,len(cs)-1);start+=len(cs)-1
        references={}

        def observable(node):
            if not isinstance(node,list):return parse(node)
            if len(node)==3 and node[0]=='seq':
                name,shift=node[1:]
                if not isinstance(name,str) or name not in positions or type(shift) is not int:
                    raise ValueError('seq requires a declared name and integer shift')
                if abs(shift)>budget.max_unknowns:
                    raise OreResourceLimit('observable shift exceeds limit')
                if (name,shift) not in references:
                    offset,size=positions[name];block=M[offset:offset+size,offset:offset+size]
                    row=s.zeros(1,size);row[0]=1
                    if shift>=0:row=iterate_row(row,block,shift)
                    else:
                        if recurrences[name][0]==0:
                            raise ValueError('unsupported_structure: backward shift needs invertible recurrence')
                        inverse=sigma(block,-1).inv();track(list(inverse))
                        for _ in range(-shift):row=(sigma(row,-1)*inverse).applyfunc(s.cancel)
                    track(list(row))
                    references[name,shift]=(row* s.Matrix(variables[offset:offset+size]))[0]
                return references[name,shift]
            if len(node)<2:raise ValueError('invalid observable tree')
            op,*children=node
            if op=='pow':
                if len(children)!=2 or type(children[1]) is not int:
                    raise ValueError('observable powers require integer literals')
                base=observable(children[0]);power=children[1]
                if power<0 and base.has(*variables):
                    raise ValueError('unsupported_structure: rational sequence observables are not polynomial')
                if base==0 and power<0:raise ValueError('zero denominator')
                return base**power
            args=list(map(observable,children))
            if op=='add':return s.Add(*args)
            if op=='mul':return s.Mul(*args)
            if op=='neg' and len(args)==1:return -args[0]
            if op in ('sub','div') and len(args)==2:
                if op=='sub':return args[0]-args[1]
                if args[1]==0:raise ValueError('zero denominator')
                if args[1].has(*variables):
                    raise ValueError('unsupported_structure: polynomial sequence observable required')
                return args[0]/args[1]
            raise ValueError('invalid observable operation')

        expr=observable(data['observable'])
        track(s.Poly(expr,*variables).coeffs())
        T,row,powers=graded_polynomial_closure(M,expr,variables,budget.max_states)
        track(list(T));track(list(row))
        # The first row dependence gives minimal order for this formal state module.
        raw=eliminate(T,row)
        raw['operator']=raw.pop('coefficients')
        symbols={str(t):t for t in set().union(*(v.free_symbols for v in tracked),{q,Q})}
        track([s.sympify(v,locals=symbols) for r in raw['shifted_rows'] for v in r])
        raw.update(input_transition=[[str(v) for v in M.row(i)] for i in range(M.rows)],
            state_layout={name:dict(offset=offset,order=size) for name,(offset,size) in positions.items()},
            monomial_exponents=[list(m) for m in powers],
            transition=[[str(v) for v in T.row(i)] for i in range(T.rows)],
            observable_row=list(map(str,row)),state_dimension=T.rows,
            recurrence_premises={name:list(map(str,cs)) for name,cs in recurrences.items()},
            input_recurrences_are_assumptions=True,
            minimality_scope='formal independent states; extra sequence relations and initial values not used')
        normalized_input=dict(sequences=raw['recurrence_premises'],observable=data['observable'])
    else:raise ValueError('unknown q_ore operation')

    output=dict(status='constructed',solver='q_ore',operation=operation,
                normalized_input=normalized_input,result=raw)
    if 'operator' in raw:
        symbols={str(t):t for t in set().union(*(v.free_symbols for v in tracked),{q,Q})}
        cs=track([s.sympify(v,locals=symbols) for v in raw['operator']])
        output['operator']=normalized_operator(cs)
        if cs!=[0]:
            leading.append(s.sympify(output['operator']['leading_coefficient'],locals=symbols))
            track([s.sympify(output['operator']['scaling_factor'],locals=symbols)])
    output['domain']=dict(coefficient_field='QQ(q,Q,independent parameters)',
        base='q is an indeterminate; E*a(Q)=a(q*Q)*E',
        encountered_denominators=sorted({str(s.factor(s.fraction(v)[1])) for v in tracked if s.fraction(v)[1]!=1}),
        leading_coefficients=list(dict.fromkeys(str(s.factor(v)) for v in leading)),
        specialization_policy='generic rational-function construction; denominator and leading-coefficient zeros not discharged',
        condition_scope='normalized inputs and constructed witnesses; pre-cancellation syntax and all integer shifts not enumerated')
    return output
