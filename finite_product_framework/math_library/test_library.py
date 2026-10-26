"""Behavioural checks for guarded rewrites, binding and source consumption."""
import copy
import unittest

from .catalog import RULES
from .registry import Library, LibraryError
from .source_views import finite_sum_view, expand_terms
from .frontend import entry_views, extractor_text


def v(name):return dict(op='var',name=name)
def num(n):return dict(op='nat',value=n)
def node(name,*args):return dict(op=name,args=list(args))
def li(*items):
    out=node('List.nil')
    for x in reversed(items):out=node('List.cons',x,out)
    return out


class LibraryChecks(unittest.TestCase):
    def setUp(self):self.lib=Library()

    def test_exact_symbol_identity_and_unknown(self):
        self.assertEqual(self.lib.lookup('poch'),self.lib.lookup('FiniteQBenchmark.poch'))
        self.assertEqual(self.lib.lookup('Other.poch')['status'],'unknown')
        self.assertEqual(self.lib.lookup('alpha')['status'],'unknown')

    def test_query_does_not_assert_method_applicability(self):
        result=self.lib.lookup('gaussian','local_recurrence')
        self.assertEqual(len(result['rules']),1)
        self.assertEqual(result['rules'][0]['id'],'gaussian_successor')
        self.assertNotIn('proved',result)

    def test_quotient_requires_actual_nonzero_fact(self):
        args={x:v(x) for x in ('a','q','d','k')}
        pending=self.lib.instantiate('poch_shift_quotient',args)
        self.assertEqual(pending['status'],'conditions_unresolved')
        wrong=node('Ne',v('q'),num(0))
        self.assertEqual(self.lib.instantiate('poch_shift_quotient',args,facts=[wrong])['status'],'conditions_unresolved')
        matched=self.lib.instantiate('poch_shift_quotient',args,facts=pending['requires'])
        self.assertEqual(matched['status'],'candidate')
        self.assertEqual(matched['proof_status'],'requires_Lean_replay')

    def test_division_free_shift_accepts_singular_parameters(self):
        args=dict(a=num(1),q=num(0),d=num(1),k=v('k'))
        result=self.lib.instantiate('poch_shift_cross',args)
        self.assertEqual(result['requires'],[])
        self.assertEqual(result['status'],'candidate')

    def test_positive_branch_not_unconditional(self):
        result=self.lib.instantiate('unitBailey_positive',dict(a=v('a'),q=v('q'),n=num(0)))
        self.assertEqual(result['status'],'conditions_unresolved')

    def test_parameter_and_sort_errors_rejected(self):
        with self.assertRaises(LibraryError):self.lib.instantiate('poch_zero',dict(a=v('a')))
        rules=copy.deepcopy(RULES);rules[0]['rhs']=['literal','Nat',1]
        with self.assertRaises(LibraryError):Library(rules)
        rules=copy.deepcopy(RULES);rules[0]['rhs']=['call','Unknown.poch','$a','$q','$n']
        with self.assertRaises(LibraryError):Library(rules)

    def test_reference_and_method_core_tampering_rejected(self):
        for key,value in [('method_core',True),('lean',dict(name='KnownTarget.solution'))]:
            rules=copy.deepcopy(RULES);rules[0][key]=value
            with self.assertRaises(LibraryError):Library(rules)

    def test_capturing_binders_are_freshened(self):
        src=node('FiniteQBenchmark.rogersSzego',v('ml_i'),v('q'),v('n'))
        view=finite_sum_view(src,avoid=['ml_ix'])
        self.assertEqual(view['binder'],'ml_ixx')
        self.assertIn(v('ml_i'),view['body']['args'][1]['args'])

    def test_phi_empty_lists_and_integer_power(self):
        src=node('FiniteQBenchmark.phi',li(),li(),v('q'),v('z'),v('n'))
        view=finite_sum_view(src)
        self.assertEqual(view['domain'],node('Finset.range',node('HAdd.hAdd',v('n'),num(1))))
        self.assertEqual(view['body']['args'][1]['args'][0]['args'][1],num(1))
        self.assertTrue(any(x['rule']=='phiTerm_definition' for x in view['library_trace']))
        negative=node('FiniteQBenchmark.phi',li(v('a'),v('b')),li(),v('q'),v('z'),v('n'))
        power=finite_sum_view(negative)['body']['args'][1]['args'][0]['args'][1]
        self.assertEqual(power,node('Neg.neg',num(1)))
        self.assertEqual(finite_sum_view(negative)['body']['args'][1]['args'][0]['exponent_sort'],'Int')

    def test_symbolic_parameter_list_keeps_gap_explicit(self):
        src=node('FiniteQBenchmark.phi',v('as'),li(),v('q'),v('z'),v('n'))
        with self.assertRaisesRegex(LibraryError,'literal_parameter_list_required'):finite_sum_view(src)

    def test_arbitrary_sequence_is_not_replaced_by_a_guess(self):
        src=node('FiniteQBenchmark.baileySum',v('a'),v('q'),v('alpha'),v('n'))
        view=finite_sum_view(src)
        self.assertEqual(view['body']['args'][0]['op'],'math_library.apply')
        self.assertEqual(view['body']['args'][0]['args'][0],v('alpha'))

    def test_reversed_natural_interval_is_empty(self):
        result=self.lib.instantiate('sum_Icc',dict(f=v('f'),a=num(3),b=num(1)))
        self.assertEqual(result['rhs']['args'][0],node('Finset.range',num(0)))

    def test_entry_unfold_is_selective_and_keeps_source(self):
        old=node('FiniteQBenchmark.phi',li(),li(),v('q'),v('z'),v('n'))
        raw=node('Eq',node('FiniteQBenchmark.geometric',v('q'),v('n')),old)
        before=copy.deepcopy(raw);after,trace=entry_views(raw)
        self.assertEqual(raw,before)
        self.assertEqual(after['args'][0]['op'],'Finset.sum')
        self.assertEqual(after['args'][1],old)
        self.assertEqual([x['rule'] for x in trace],['geometric_sum'])

    def test_catalog_mutation_does_not_escape_instances(self):
        before=self.lib.sha256
        self.lib.rules['poch_zero']['rhs']=['literal','K',99]
        self.assertEqual(self.lib.rules['poch_zero']['rhs'],['literal','K',1])
        self.assertEqual(self.lib.sha256,before)
        self.assertEqual(Library().rules['poch_zero']['rhs'],['literal','K',1])

    def test_malformed_binding_rejected(self):
        for bad in [dict(op='nat',value=-1),dict(op='nat',value=True),dict(op='var'),{'op':'x','args':{}}]:
            with self.assertRaises(LibraryError):
                self.lib.instantiate('poch_zero',dict(a=bad,q=v('q')))


if __name__=='__main__':unittest.main()
