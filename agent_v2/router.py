"""Deterministic default routing and a validated, optional Jev protocol boundary."""
import math
from typing import Protocol


class Selector(Protocol):
    def __call__(self, state, legal_candidates) -> dict: ...


class RuleBasedRouter:
    def choose(self, state, legal_candidates):
        if not legal_candidates:
            return None
        # The graph has already enforced hard contracts, applicability and
        # failed-attempt suppression. CAS is a soft ordering preference only.
        def rank(action):
            seconds = action.theta.get('seconds', float('inf'))
            if type(seconds) not in (int, float) or not math.isfinite(seconds):
                seconds = float('inf')
            return (action.source != state.r, action.M != 'CAS', seconds, action.id)
        return min(legal_candidates, key=rank)


class JevRouter:
    """No network client. A caller may later supply a typed external selector."""
    def __init__(self, selector: Selector, min_confidence=0.5, fallback=None):
        if type(min_confidence) not in (int, float) or not 0 <= min_confidence <= 1:
            raise ValueError('invalid confidence threshold')
        self.selector = selector
        self.min_confidence = min_confidence
        self.fallback = fallback or RuleBasedRouter()
        self.last_diagnostic = None

    def choose(self, state, legal_candidates):
        self.last_diagnostic = None
        if not legal_candidates:
            self.last_diagnostic = {'code': 'no_legal_candidates'}
            return None
        # Freeze the list passed to a selector so it cannot append a new route
        # and make that route appear in the subsequently validated ID set.
        candidates = tuple(legal_candidates)
        by_id = {candidate.id: candidate for candidate in candidates}
        try:
            result = self.selector(state, candidates)
            if not isinstance(result, dict) or set(result) != {'route_id', 'confidence', 'rationale'}:
                raise ValueError('invalid_response_schema')
            confidence = result['confidence']
            if type(confidence) not in (int, float) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
                raise ValueError('invalid_confidence')
            if not isinstance(result['rationale'], str) or not isinstance(result['route_id'], str):
                raise ValueError('invalid_response_schema')
            if result['route_id'] not in by_id:
                raise ValueError('unregistered_route_id')
            if confidence < self.min_confidence:
                raise ValueError('low_confidence')
            return by_id[result['route_id']]
        except Exception as error:
            # Exception details may include remote input or secrets; retain only
            # a small local category, never a caller's arbitrary error string.
            code = str(error) if isinstance(error, ValueError) and str(error) in {
                'invalid_response_schema', 'invalid_confidence', 'unregistered_route_id', 'low_confidence'
            } else 'selector_exception'
            self.last_diagnostic = {'code': code, 'fallback': 'rule'}
            return self.fallback.choose(state, candidates)
