"""Explicit synthetic two-action integration fixture, with the REAL Lean checker.

The handwritten candidate provider is test-only: this is neither a model call
nor a Train proof result. Unlike ordinary temporary unit tests, evidence is kept.
"""
import json
from pathlib import Path

from agent_v2.cli import GENERATED
from agent_v2.executor import Executor
from agent_v2.graph import Graph, Outlet
from agent_v2.lean_checker import LeanChecker, init_original_template
from agent_v2.loop import run
from agent_v2.models import (Budget, Candidate, Cost, ExecutionResult, FailureSignature,
                             Obligation, initial_state)
from agent_v2.storage import RunStore, freeze_source


class HandwrittenCandidates:
    def __init__(self, source):
        self.source = source
        self.index = 0

    def execute(self, identity, method, source, attempt_dir, seconds):
        if self.index == 0:
            leaf = Obligation('leaf', 'subgoal', 'True', 'True', self.source.sha256, 'fixture_bridge')
            candidate = Candidate('bridge', '(True) → (True)', 'fun h => h',
                'AgentV2Candidate.proof', self.source.sha256, (), 'original', (leaf,))
            remaining = (leaf,)
        elif self.index == 1:
            candidate = Candidate('leaf_proof', 'True', 'True.intro',
                'AgentV2Candidate.proof', self.source.sha256, (), 'leaf')
            remaining = ()
        else:
            raise AssertionError('fixture must not execute an old route tail')
        self.index += 1
        return ExecutionResult('incomplete', (candidate,), remaining,
            FailureSignature('fixture', 'candidate_generated', 'Handwritten synthetic test candidate', None),
            Cost(0.0, 1), {'provider': 'test_only_handwritten', 'candidate': candidate.to_dict()},
            (), ('No model or mathematical discovery is claimed.',), False).to_dict()


def main():
    store = RunStore.create(GENERATED)
    source_path = store.write_bytes('input/Original.lean',
        init_original_template('Synthetic.statement', 'True').encode())
    source = freeze_source(source_path, 'synthetic-real-lean-smoke', 'Synthetic.statement', store,
                           proposition='True')
    state, representation = initial_state(source, Budget(90, 2))
    graph = Graph(source.sha256); graph.add_node(representation)
    graph.add_outlet(Outlet('fixture', 'original', 'CAS', 'method',
        {'method': 'synthetic_fixture', 'seconds': 30.0}, ('closed_prop',)))
    final = run(state, graph, store, Executor({'method': HandwrittenCandidates(source)}), LeanChecker())
    store.write_json('fixture_scope.json', {'schema_version': 1, 'candidate_provider': 'test_only_handwritten',
        'checker': 'real_Lean', 'Train_result': False, 'expected_actions': 2,
        'observed_actions': final.round_index, 'verified_certificates': len(final.C),
        'status': final.status})
    print(json.dumps({'run_dir': str(store.root), 'status': final.status,
                      'scope': 'synthetic_test_only', 'rounds': final.round_index}))
    return 0 if final.status == 'original_theorem_proved' and final.round_index == 2 else 3


if __name__ == '__main__':
    raise SystemExit(main())
