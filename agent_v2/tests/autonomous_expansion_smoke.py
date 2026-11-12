"""Controlled expansion -> real CAS smoke, opt-in live and never a strategy score.

Only the first expansion/repair selection and its proposal shape are controlled.
ModelClient, LocalLibrary, Source freezing, Lean, residual updates, accounting,
checkpoints and the subsequent rule loop are production components. No proof
text is supplied by this driver. Run as ``python3 -m ... --execute`` only after
authorization; the default only prepares and persists the actual initialization.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path
import time
from unittest.mock import patch

from agent_v2.autonomous_adapter import AutonomousExecutor, outcome
from agent_v2.cli import positive_float, positive_int
from agent_v2.models import ContractError, thaw
from agent_v2.storage import IntegrityError, RunStore, sha256_file


IDENTITY = 'FQI-SRC-AP-3.3.9'
METHOD = 'telescoping'


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument('--execute', action='store_true', help='make at most two real model calls')
    result.add_argument('--seconds', type=positive_float, default=1200.0)
    result.add_argument('--action-seconds', type=positive_float, default=480.0)
    result.add_argument('--max-steps', type=positive_int, default=4)
    result.add_argument('--output-root', default='agent_v2/generated/autonomous_20261112/controlled_expansion')
    result.add_argument('--model', default='gpt-6-astra')
    result.add_argument('--model-endpoint', default=None)
    result.add_argument('--model-credential', default=None)
    result.add_argument('--jev-credential', default=None)
    return result


def autonomous_args(args):
    if args.max_steps < 3:
        raise ContractError('controlled expansion needs up to two model actions and one CAS action')
    return argparse.Namespace(identity=IDENTITY, methods=METHOD, selector='rule',
        seconds=args.seconds, action_seconds=args.action_seconds, max_steps=args.max_steps,
        max_model_calls=2, max_expansions=1, max_repairs=1, model=args.model,
        model_endpoint=args.model_endpoint, model_credential=args.model_credential,
        jev_credential=args.jev_credential, pause_after=None)


def matches_protocol(content, child):
    return (isinstance(content, dict) and set(content) == {'kind', 'children', 'proof_term'}
            and content['kind'] == 'decompose' and content['children'] == [child]
            and isinstance(content['proof_term'], str) and bool(content['proof_term'].strip()))


def format_repairable(raw):
    return raw.get('error_code') == 'invalid_json_content' and raw.get('model_calls') == 1


def expansion_payload(payload, child):
    """Constrain only the requested contract; never supply or edit a proof."""
    return dict(payload, purpose='expansion' if payload.get('purpose') != 'repair' else 'repair',
        instructions=payload['instructions'] + (
            ' This is an explicitly controlled graph-to-CAS integration test. Return ONLY the decompose '
            'form with exactly the one required_children proposition, copied exactly. Generate your own '
            'Lean proof of (that child) → (the selected original goal), using only the supplied declarations '
            'and current diagnostics. Do not prove the child in this action: the actual CAS backend will '
            'attempt it after this bridge is checked. Do not return prove or lemma forms.'),
        output_schema={'decompose': payload['output_schema']['decompose']},
        required_children=[child],
        controlled_test={'controlled_first_action': True, 'model_proof_supplied': False,
                         'autonomous_strategy_evaluation': False})


class _ExpansionModel:
    """A payload decorator around the real configured ModelClient."""
    def __init__(self, model, child):
        self.model, self.child = model, child

    def generate(self, kind, payload, *, seconds, attempt_dir):
        if kind != 'residual_action':
            raise ContractError('unexpected model task in controlled expansion')
        return self.model.generate(kind, expansion_payload(payload, self.child),
                                   seconds=seconds, attempt_dir=attempt_dir)


class _ExpansionExecutor(AutonomousExecutor):
    def __init__(self, base, child):
        super().__init__(_ExpansionModel(base.model, child), base.checker, base.capabilities,
                         library=base.library, method_adapter=base.method_adapter, feedback=base.feedback)
        self.child = child

    def execute(self, state, action, graph, attempt_dir):
        if action.M != 'LLM':
            raise ContractError('controlled first phase must select its registered LLM action')
        started = time.monotonic()
        result = super().execute(state, action, graph, attempt_dir)
        if format_repairable(result.raw_result):
            return outcome(started, 'incomplete', 'controlled_model_json_repair_required',
                raw=thaw(result.raw_result), diagnostics=({'format_error': 'invalid_json_content',
                    'required_kind': 'decompose', 'required_children': [self.child]},))
        if result.raw_result.get('status') == 'ok' and not matches_protocol(
                thaw(result.raw_result.get('content')), self.child):
            # The original request, response and content remain untouched. No
            # candidate is passed to verify_and_update for the wrong contract.
            return outcome(started, 'incomplete', 'controlled_expansion_contract_rejected',
                raw=thaw(result.raw_result), diagnostics=({'required_kind': 'decompose',
                    'required_children': [self.child], 'model_proof_supplied': False},))
        return result


def _controlled_action(state, graph, runtime, number):
    from agent_v2.graph import Outlet
    from agent_v2.autonomous import _legal
    purpose = 'expansion' if number == 1 else 'repair'
    graph.add_outlet(Outlet('controlled-expansion-' + str(number), state.root.id, 'LLM', 'llm',
        {'autonomous': True, 'goal_id': state.root.id, 'seconds': runtime.config['action_seconds'],
         'purpose': purpose, 'controlled_expansion_attempt': number}, ('closed_prop',),
        estimated_seconds=0.01, handles=(state.root.id,), provenance=('controlled_integration_first_action',)))
    legal, _ = _legal(state, graph, runtime)
    actions = [a for a in legal if a.M == 'LLM' and a.theta.get('controlled_expansion_attempt') == number]
    if len(actions) != 1:
        raise ContractError('controlled expansion action must be uniquely legal')
    return actions[0]


def _bridge_child(state, child_proposition):
    matches = [link.children[0] for link in state.links if link.parent == state.root
               and len(link.children) == 1 and link.children[0].proposition == child_proposition]
    return matches[0] if len(matches) == 1 else None


def _write_report(store, state, protocol, *, prepared=False, successor=None):
    if sha256_file(Path(__file__).absolute()) != protocol['driver_sha256']:
        raise IntegrityError('controlled driver changed during this run')
    cas_rounds = []
    child = _bridge_child(state, protocol['required_child'])
    if child:
        for number in range(1, state.round_index + 1):
            relative = f'rounds/{number}'
            if not store.path(relative + '/action.json').is_file():
                continue
            action = store.read_json(relative + '/action.json')
            if action.get('M') == 'CAS' and action.get('target') == child.id:
                verification = store.read_json(relative + '/verification.json')
                cas_rounds.append({'round': number, 'action': action,
                    'certificates_added': verification['certificates_added'],
                    'child_closed': child.id not in verification['open_obligations']})
    report = dict(protocol, prepared_only=prepared, status=state.status,
        original_identity_proved=state.status == 'original_theorem_proved',
        model_calls=store.runtime.model.calls_used, jev_calls=0,
        rounds=state.round_index, remaining_budget=state.b.to_dict(),
        bridge_verified=child is not None, child_id=child.id if child else None,
        rule_successor=successor, actual_child_cas_rounds=cas_rounds,
        expansion_to_cas_verified=any(r['certificates_added'] > 0 and r['child_closed'] for r in cas_rounds),
        proof_text_origin='actual ModelClient response only',
        benchmark_split='Train', test_data_read=False)
    store.write_json('controlled_expansion_report.json', report)
    return report


def controlled_entry(state, graph, store, *, execute=False):
    started = time.monotonic()
    from agent_v2 import autonomous
    from agent_v2.graph_builder import sync_residual_graph
    from agent_v2.loop import finish
    from agent_v2.router import RuleBasedRouter
    runtime = store.runtime
    if state.G.identity != IDENTITY or state.C or state.links or state.round_index != 0:
        raise ContractError('controlled expansion requires the unchanged preselected initial Source')
    child = runtime.capabilities.get(METHOD, {}).get('local_proposition')
    if not isinstance(child, str) or not child or child == state.G.proposition:
        raise ContractError('preselected Source lacks its distinct exact CAS local target')
    if runtime.config['selector'] != 'rule' or runtime.config['max_model_calls'] != 2:
        raise ContractError('controlled integration requires rule continuation and at most two calls')
    protocol = {'schema_version': 1, 'controlled_first_action': True, 'model_proof_supplied': False,
        'autonomous_strategy_evaluation': False, 'identity': state.G.identity,
        'source_sha256': state.G.sha256, 'required_child': child, 'method': METHOD,
        'max_model_calls': 2, 'driver_path': str(Path(__file__).absolute()),
        'driver_sha256': sha256_file(Path(__file__).absolute())}
    store.write_json('controlled_expansion_protocol.json', protocol)
    deadline = started + state.b.seconds
    if not execute:
        state = replace(state, b=replace(state.b, seconds=max(0., deadline-time.monotonic())))
        state = finish(store, replace(state, status='incomplete'), graph, 'controlled_expansion_prepared_no_api')
        _write_report(store, state, protocol, prepared=True)
        return state
    base_executor = runtime.executor
    runtime.executor = _ExpansionExecutor(base_executor, child)
    try:
        for number in (1, 2):
            state = replace(state, status='running', b=replace(state.b, seconds=max(0., deadline-time.monotonic())))
            if state.b.seconds <= 0 or state.b.actions <= 0:
                state = finish(store, replace(state, status='budget_exhausted'), graph, 'controlled_expansion_budget_exhausted')
                break
            action = _controlled_action(state, graph, runtime, number)
            if number == 1:
                runtime.expansions += 1
            else:
                runtime.repairs += 1
            first_round = state.round_index + 1
            class ForcedFirstRouter:
                def choose(self, current, legal):
                    if action not in legal:
                        raise ContractError('controlled action is no longer legal')
                    return action
            # One production action; this scoped patch changes only selection.
            with patch('agent_v2.autonomous.RuleBasedRouter', ForcedFirstRouter):
                state = _PRODUCTION_RUN(state, graph, store, pause_after=1)
            selection_path = f'rounds/{first_round}/selection.json'
            if store.path(selection_path).exists():
                selection = store.read_json(selection_path)
                store.write_json(selection_path, dict(selection, selector='controlled_expansion',
                    configured_continuation_selector='rule', controlled_first_action=True,
                    controlled_attempt=number, model_proof_supplied=False))
            _write_report(store, state, protocol)
            if _bridge_child(state, child) or state.status in ('environment_blocked', 'integrity_error', 'budget_exhausted'):
                break
    finally:
        base_executor.feedback = runtime.executor.feedback
        runtime.executor = base_executor
    approved_child = _bridge_child(state, child)
    if approved_child is None or state.status in ('environment_blocked', 'integrity_error', 'budget_exhausted'):
        if state.status == 'incomplete':
            state = finish(store, state, graph, 'controlled_expansion_not_verified')
        _write_report(store, state, protocol)
        return state
    state = replace(state, status='running', b=replace(state.b, seconds=max(0., deadline-time.monotonic())))
    sync_residual_graph(state, graph, runtime.capabilities, seconds=runtime.config['action_seconds'])
    legal, reasons = autonomous._legal(state, graph, runtime)
    chosen = RuleBasedRouter().choose(state, legal)
    edge = graph.edges.get(chosen.T) if chosen else None
    if (chosen is None or chosen.M != 'CAS' or chosen.target != approved_child.id
            or chosen.theta.get('method') != METHOD or edge is None or edge.mode != 'decomposition'):
        store.write_json('controlled_rule_handoff.json', {'legal': [a.to_dict() for a in legal], 'filtered': reasons})
        state = finish(store, replace(state, status='incomplete'), graph, 'controlled_child_cas_route_unavailable')
        _write_report(store, state, protocol)
        return state
    successor = {'action': chosen.to_dict(), 'edge': edge.to_dict()}
    store.write_json('controlled_rule_handoff.json', successor)
    # Ordinary production rule routing, CAS verification, and exact final check.
    state = _PRODUCTION_RUN(state, graph, store)
    _write_report(store, state, protocol, successor=successor)
    return state


# Capture before the train_run entrypoint injection; no recursion/production edit.
from agent_v2.autonomous import run as _PRODUCTION_RUN


def main(argv=None):
    from agent_v2.autonomous_cli import train_run
    from agent_v2.cli import _explicit_directory
    args = parser().parse_args(argv)
    auto = autonomous_args(args)
    store = RunStore.create(_explicit_directory(args.output_root))
    def entry(state, graph, initialized_store, **kwargs):
        return controlled_entry(state, graph, initialized_store, execute=args.execute)
    with patch('agent_v2.autonomous.run', entry):
        status = train_run(auto, store)
    report_path = store.path('controlled_expansion_report.json')
    report = store.read_json('controlled_expansion_report.json') if report_path.exists() else {}
    print(json.dumps({'status': status, 'run_dir': str(store.root), 'controlled_first_action': True,
        'model_proof_supplied': False, 'prepared_only': not args.execute,
        'model_calls': report.get('model_calls', 0), 'original_identity_proved': status == 'original_theorem_proved'},
        ensure_ascii=False))
    if not args.execute and report.get('prepared_only') and report.get('model_calls') == 0:
        return 0
    return 0 if status == 'original_theorem_proved' and report.get('expansion_to_cas_verified') else 2


if __name__ == '__main__':
    raise SystemExit(main())
