"""Retained source-adapter regressions; no five-system dispatcher."""
import unittest
import sympy as s
from source_ir import node, var, nat, candidates, InputGap, Converter, exact_tree
from expressions import expression, shift_ratio, rationalize, k, q, X

class Adapters(unittest.TestCase):

    def test_phi_definition_expansion(self):
        aa = node('List.cons', var('a'), node('List.nil'))
        bb = node('List.nil')
        raw = node('Eq', node('FiniteQBenchmark.phi', aa, bb, var('q'), var('z'), var('n')), nat(0))
        candidate = candidates(raw)[0]
        conv = Converter([candidate['body'], candidate['domain']], 'n', candidate['binder'])
        F = expression(conv.read(candidate['body']))
        V = rationalize(shift_ratio(F, k))
        a = s.Symbol(conv.names['a'])
        z = s.Symbol(conv.names['z'])
        self.assertEqual(s.cancel(V - z * (1 - a * X) / (1 - q * X)), 0)

    def test_opaque_and_truncation_rejected(self):
        conv = Converter([node('HPow.hPow',var('q'),var('n'))], 'n')
        for a in [dict(op='FiniteQBenchmark.gaussian', args=[], text='gaussian q n k'), node('Int.toNat', var('n')), dict(op='sorryAx', args=[])]:
            with self.subTest(node=a), self.assertRaises(InputGap):
                conv.read(a)

    def test_exact_tree_rejects_nonrational_powers(self):
        with self.assertRaises(InputGap):
            exact_tree(q ** s.Symbol('p'))

if __name__ == "__main__":
    unittest.main()
