"""Synthetic theorem source shared by finite-sum proof regression suites.

The historical namespace is retained to keep fixture declarations unchanged.
"""

def source_for(target):
    return ('import Benchmark.Definitions\nopen scoped BigOperators\nopen FiniteQBenchmark\n'
        'set_option autoImplicit false\nnamespace CoreExitRegression\nvariable {K : Type*} [Field K]\n'
        'theorem statement '+target+' := by\n  sorry\nend CoreExitRegression\n')
