#!/usr/bin/env python3
"""Standalone symbolic computation entry; does not run any benchmark or Lean."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent/'p1'))
from core import main

if __name__ == '__main__':
    raise SystemExit(main())
