#!/usr/bin/env python3
"""Independent recurrence proof pipeline; no cross-method fallback."""
from prove import main

if __name__ == '__main__':
    raise SystemExit(main('recurrence'))
