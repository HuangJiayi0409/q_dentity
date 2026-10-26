#!/usr/bin/env python3
"""Preprocess and select one of twelve methods, without running a proof method."""
from prove import main

if __name__ == '__main__':
    raise SystemExit(main('auto',select_only=True))
