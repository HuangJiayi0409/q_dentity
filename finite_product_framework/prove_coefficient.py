#!/usr/bin/env python3
"""Independent coefficient proof pipeline; no cross-method fallback."""
from prove import main

if __name__ == '__main__':
    raise SystemExit(main('coefficient'))
