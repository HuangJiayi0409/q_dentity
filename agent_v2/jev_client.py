"""Typed TypeSafe Choice selector; legality and execution remain in code."""
from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import uuid

from .model_client import _RecordedHTTP
from .models import thaw

_ROUTE_QUESTION = ('Which candidate has a mathematical operation directly matching the current '
                   'open obligations and the available verified certificates?')


@dataclass(frozen=True)
class JevConfig:
    endpoint: str = 'https://api.typesafe.ai/v1/systemone'
    model: str = 'jev-latest'
    credential_path: str | None = None
    credential_env: str | None = None
    max_calls: int = 8

    def __post_init__(self):
        if type(self.max_calls) is not int or not 0 <= self.max_calls <= 1000:
            raise ValueError('invalid_call_limit')
        if not isinstance(self.model, str) or not self.model or len(self.model) > 200:
            raise ValueError('invalid_model')


class JevUnavailable(RuntimeError):
    """Contains only a local category; never a remote exception message."""


class JevSelector(_RecordedHTTP):
    def __init__(self, config: JevConfig | dict, *, attempt_root, seconds=30.0, transport=None, calls_used=0):
        super().__init__(JevConfig(**config) if isinstance(config, dict) else config,
                         transport=transport, calls_used=calls_used)
        self.attempt_root = Path(attempt_root)
        self.seconds = seconds

    def __call__(self, state, legal_candidates):
        candidates = tuple(legal_candidates)
        ids = [candidate.id for candidate in candidates]
        if not 1 <= len(ids) <= 255 or len(set(ids)) != len(ids) or any(not isinstance(i, str) or not i for i in ids):
            self.last_result = {'status': 'unavailable', 'content': None, 'usage': None,
                                'wall_seconds': 0.0, 'error_code': 'invalid_candidates',
                                'model_calls': 0, 'calls_used': self.calls_used, 'artifacts': []}
            raise JevUnavailable('invalid_candidates')
        residual = {
            'G': {'identity': state.G.identity, 'sha256': state.G.sha256,
                  'proposition': state.G.proposition},
            'r': state.r,
            'O': [{'id': obligation.id, 'proposition': obligation.proposition,
                   'dependencies': list(obligation.dependencies)} for obligation in state.O],
            'C': [{'id': certificate.id, 'proposition': certificate.proposition,
                   'dependencies': list(certificate.dependencies)} for certificate in state.C],
            'b': thaw(state.b),
            'recent_failures': [{'action_id': attempt.action_id, 'code': attempt.code,
                                 'round': attempt.round} for attempt in state.attempts[-5:]],
            'round_index': state.round_index,
        }
        payload = {'model': self.config.model,
                   'state': {'residual': residual, 'legal_candidates': [thaw(c) for c in candidates]},
                   'questions': {'compatible_route': {'type': 'choice', 'instructions': _ROUTE_QUESTION,
                       'criteria': {candidate.id: {'method': candidate.M, 'backend': candidate.backend,
                           'transformation': candidate.T, 'source': candidate.source, 'target': candidate.target,
                           'parameters': thaw(candidate.theta)} for candidate in candidates}}}}
        directory = self.attempt_root / f'jev-{self.calls_used + 1:04d}-{uuid.uuid4().hex}'
        result = self._request(payload, endpoint_suffix='systemone', default_endpoint='https://api.typesafe.ai',
                               seconds=self.seconds, attempt_dir=directory,
                               parse=lambda response: self._parse(response, frozenset(ids)))
        if result['status'] != 'ok':
            raise JevUnavailable(result['error_code'])
        return result['content']

    @staticmethod
    def _parse(response, ids):
        answers = response.get('answers')
        if not isinstance(answers, dict) or set(answers) != {'compatible_route'}:
            raise ValueError('invalid_selection')
        answer = answers['compatible_route']
        if not isinstance(answer, dict) or answer.get('type') != 'choice':
            raise ValueError('invalid_selection')
        choice, confidence, probabilities = answer.get('choice'), answer.get('confidence'), answer.get('probabilities')
        if not isinstance(choice, str) or choice not in ids:
            raise ValueError('unregistered_route_id')
        if type(confidence) not in (int, float) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise ValueError('invalid_selection')
        if not isinstance(probabilities, dict) or set(probabilities) != ids:
            raise ValueError('invalid_selection')
        if any(type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1
               for value in probabilities.values()):
            raise ValueError('invalid_selection')
        if abs(sum(probabilities.values()) - 1) > 0.01 or probabilities[choice] < max(probabilities.values()):
            raise ValueError('invalid_selection')
        # Choice returns no natural-language rationale. An empty string records
        # that absence while satisfying the existing Selector wire contract.
        return {'route_id': choice, 'confidence': confidence, 'rationale': ''}
