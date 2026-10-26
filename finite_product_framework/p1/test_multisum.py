#!/usr/bin/env python3
"""Generic symbolic and finite-boundary tests; no synthetic train proof counts."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import sympy as s
from multisum import (construct,derive,verify,search,full_rank_specialization,
                      evaluation_full_rank,reduce_pair_equations,MultisumBudget,q,Q)
from multisum_domains import support,boundary,divergence,moving_shell
from multisum_pipeline import frontend,synthesize
from lean_pipeline import HERE,ROOT
from exact_linear import flint_available, nullspace, rational_normal_form


def kernel(d):
    return {'schema_version':1,'source_id':'synthetic','indices':[f'i{i}' for i in range(d)],
            'summand':['mul',*[['div',['poch',['pow','q',['add','n',1]],'q',f'i{i}'],
                                   ['poch','q','q',f'i{i}']] for i in range(d)]]}


class MultisumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.problem=kernel(2)
        cls.result=construct(cls.problem,MultisumBudget(max_order=1))['construction']

    @unittest.skipUnless(flint_available(), 'optional python-flint backend')
    def test_exact_rational_nullspace_and_projection(self):
        a,b=s.symbols('a b')
        rows=[[a,s.S.One,s.S.Zero],[s.S.Zero,b,s.S.One]]
        basis=nullspace(rows)
        self.assertEqual(basis.shape,(1,3))
        self.assertEqual(s.simplify(s.Matrix(rows)*basis.T),s.zeros(2,1))
        projected=nullspace(rows,transform=s.diag(a*b,b,1),normalize_index=2)
        self.assertEqual(projected,s.Matrix([[1,-1,1]]))
        self.assertEqual(rational_normal_form((a+b)**2/(a+b)-(a+b)),0)

    @unittest.skipUnless(flint_available(), 'optional python-flint backend')
    def test_exact_solver_recovers_degenerate_modular_rows(self):
        a=s.Symbol('a')
        # The modular probe at a=3 loses a row; exact verification must recover it.
        rows=[[s.S.One,s.S.Zero,s.S.Zero],[s.S.Zero,a-3,s.S.Zero]]
        basis=nullspace(rows)
        self.assertEqual(basis.shape,(1,3))
        self.assertEqual(s.simplify(s.Matrix(rows)*basis.T),s.zeros(2,1))

    def test_two_nonzero_direction_certificates(self):
        r=self.result
        self.assertEqual(r['status'],'constructed')
        self.assertTrue(all(s.sympify(x,locals={'Q':Q,'q':q})!=0 for x in r['certificates']))
        self.assertFalse(r['target_used_in_search'])
        self.assertEqual(r['proof_status'],'local_rational_identity_only')

    def test_three_dimensional_search(self):
        p=kernel(3)
        p['summand']=['pow','q',['mul','n',['add','i0','i1','i2']]]
        r=construct(p,MultisumBudget(max_order=1,max_degree=3))['construction']
        self.assertEqual(r['status'],'constructed')
        self.assertEqual(len(r['certificates']),3)

    def test_tampered_direction_rejected(self):
        xs,V,U=derive(self.problem)
        env={'q':q,'Q':Q,**{str(x):x for x in xs}}
        cs=[s.sympify(x,locals=env) for x in self.result['coefficients']]
        rs=[s.sympify(x,locals=env) for x in self.result['certificates']]
        rs[1]+=1
        with self.assertRaisesRegex(ValueError,'residual'):verify(V,U,xs,cs,rs)

    def test_missing_direction_rejected(self):
        xs,V,U=derive(self.problem)
        with self.assertRaisesRegex(ValueError,'dimensions'):verify(V,U,xs,[s.Integer(1)],[])

    def test_metadata_does_not_select_relation(self):
        p=copy.deepcopy(self.problem);p['source_id']='arbitrary-other-name'
        self.assertEqual(derive(p),derive(self.problem))

    def test_target_and_hint_inputs_rejected(self):
        for key in ('target','certificate','coefficients'):
            p=copy.deepcopy(self.problem);p[key]=1
            with self.assertRaisesRegex(ValueError,'invalid_problem'):derive(p)

    def test_budget_is_not_unsummability(self):
        r=construct(self.problem,MultisumBudget(max_unknowns=1))['construction']
        self.assertEqual(r['status'],'resource_exhausted')
        r=construct(self.problem,MultisumBudget(max_order=1,max_degree=0))['construction']
        self.assertEqual(r['status'],'search_exhausted')
        self.assertFalse(r['complete_search'])

    def test_specialization_only_certifies_full_rank(self):
        a=s.Symbol('a')
        self.assertIsNotNone(full_rank_specialization([[a,s.S.One],[s.S.One,a]],[a]))
        self.assertIsNone(full_rank_specialization([[a,a],[a,a]],[a]))
        self.assertIsNone(full_rank_specialization([[1/(a-3)]],[a]))

    def test_evaluation_minor_and_degenerate_specialization(self):
        a,x,y=s.symbols('a X Y')
        witness=evaluation_full_rank([s.S.One,x,y,x*y,x*x,y*y],(x,y),(a,))
        self.assertEqual(witness['rank'],6)
        matrix=s.Matrix([[e.subs({a:3,x:u,y:v}) for e in [s.S.One,x,y,x*y,x*x,y*y]]
                         for u,v in witness['points']])
        self.assertNotEqual(int(matrix.det())%witness['prime'],0)
        self.assertIsNone(evaluation_full_rank([s.S.One,(a-3)*x],(x,),(a,)))

    def test_float_rejected(self):
        with self.assertRaisesRegex(ValueError,'exact rational'):
            search(s.Float(1.2),[q,q],s.symbols('X0 X1'))

    def test_exact_pair_elimination(self):
        a,b=s.symbols('a b')
        for original in ([[a,s.S.One,s.S.Zero],[s.S.Zero,b,s.S.One]],
                         [[a,s.S.One,s.S.Zero],[s.S.Zero,b,s.S.One],[a,s.S.One,s.S.One]]):
            reduced,expansion=reduce_pair_equations(original)
            self.assertFalse(reduced)
            self.assertEqual((s.Matrix(original)*expansion).applyfunc(s.cancel),
                             s.zeros(len(original),expansion.cols))

    def test_two_and_three_dimensional_boundaries(self):
        for d in (2,3):
            for kind in ('simplex','box'):
                for n in (0,1,3):
                    D=support(d,n,kind)
                    gs=[lambda x,i=i:sum((j+2)*a*a for j,a in enumerate(x))+x[i]+1 for i in range(d)]
                    lhs,rhs,_=divergence(D,gs)
                    self.assertEqual(lhs,rhs)

    def test_simplex_faces_and_corners(self):
        for d in (2,3):
            D=support(d,3)
            for i in range(d):
                face=boundary(D,tuple(int(i==j) for j in range(d)))
                self.assertEqual(face['negative'],{x for x in D if x[i]==0})
                self.assertEqual(face['positive'],{x for x in support(d,4) if sum(x)==4 and x[i]>=1})
                # Omitting an entire negative face changes a constant-flux result.
                self.assertNotEqual(len(face['positive']),len(face['positive'])-len(face['negative']))

    def test_moving_shell(self):
        for d in (2,3):
            old,new=support(d,2),support(d,3)
            shell=moving_shell(old,new)
            self.assertFalse(shell['negative'])
            self.assertEqual(shell['positive'],{x for x in new if sum(x)==3})

    def test_support_budget(self):
        with self.assertRaisesRegex(ValueError,'resource_exhausted'):support(8,30,max_points=100)

    def test_native_triangle_frontend(self):
        work=HERE/'generated/runs/FQI-SRC-GR2-10.Ex18'
        raw=json.loads((work/'lean_expression.json').read_text())
        report=json.loads((work/'report.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT/report['source']['path']).read_bytes()).hexdigest(),
                         report['source']['sha256'])
        if 'lean_expression_sha256' in report:
            self.assertEqual(hashlib.sha256((work/'lean_expression.json').read_bytes()).hexdigest(),
                             report['lean_expression_sha256'])
        p,m=frontend(raw,'native-front-end-check')
        self.assertEqual(m['domain'],'simplex');self.assertEqual(m['dimension'],2)
        xs,V,U=derive(p)
        self.assertEqual(len(xs),2)
        self.assertTrue(all(u.has(*xs) for u in U))
        from expressions import expression,Poch,n
        F=expression(p['summand'])
        assignment={n:4,s.Symbol('i0'):1,s.Symbol('i1'):1,q:2,
                    **{s.Symbol(f'p{i}'):v for i,v in zip(range(4,9),(3,7,11,13,5))}}
        def at(values):
            value=F.subs(values)
            return value.replace(lambda t:t.func==Poch,
                lambda t:s.prod(1-t.args[0]*t.args[1]**j for j in range(int(t.args[2]))))
        rational_assignment={**assignment,Q:16,xs[0]:2,xs[1]:2}
        for index,ratio in zip((n,s.Symbol('i0'),s.Symbol('i1')),(V,*U)):
            moved={**assignment,index:assignment[index]+1}
            self.assertEqual(s.cancel(at(moved)/at(assignment)-ratio.subs(rational_assignment)),0)
        # A renamed source must canonicalize to exactly the same problem.
        def rename(t):
            t=copy.deepcopy(t)
            if t.get('op') in ('var','lambda'):t['name']='renamed_'+t['name']
            if 'args' in t:t['args']=[rename(a) for a in t['args']]
            if 'body' in t:t['body']=rename(t['body'])
            return t
        p2,m2=frontend(rename(raw),'native-front-end-check')
        self.assertEqual(p,p2)
        malformed=copy.deepcopy(raw)
        malformed['args'][0]['args'][0]={'op':'Finset.Icc','args':[]}
        with self.assertRaises(ValueError):frontend(malformed,'bad')

    def test_no_unproved_native_success(self):
        model={'dimension':2,'domain':'simplex','bounds':['n','n'],
               'summand':self.problem['summand']}
        with tempfile.TemporaryDirectory(prefix='p1-multisum-') as tmp:
            r=synthesize('',model,self.result,Path(tmp),{})
            self.assertNotEqual(r['status'],'proved')
            self.assertFalse(r['lean_proof_generated'])
            self.assertFalse(r['boundary_plan']['rule_instantiated_for_original_source'])

    def test_generic_lean_boundary_rules(self):
        p=subprocess.run(['lake','env','lean',str(HERE/'lean/MultisumRules.lean')],
            cwd=ROOT/'project',text=True,capture_output=True,timeout=180)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertNotIn('sorryAx',p.stdout+p.stderr)
        for name in ('directional_boundary','multisum_boundary','moving_support_difference','triangle_homogeneous'):
            self.assertIn("'FiniteQP1."+name+"' depends on axioms:",p.stdout)


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(MultisumTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'status':'passed' if result.wasSuccessful() else 'failed','tests':result.testsRun,
            'failures':len(result.failures),'errors':len(result.errors),
            'synthetic_tests_count_as_train_proofs':False,'new_train_proofs':0,
            'original_target_end_to_end':json.loads((HERE/'generated/runs/FQI-SRC-GR2-10.Ex18/report.json').read_text())['status'],
            'flint_backend_available':flint_available(),
            'code_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in
                ('multisum.py','multisum_pipeline.py','multisum_domains.py','exact_linear.py','multisum_lean.py','lean/MultisumRules.lean','lean/MultisumProductRules.lean','test_multisum.py')}}
    (HERE/'generated/multisum_tests.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
