"""Solver-readable mathematical rules with separately checked Lean evidence.

Importing this package performs no proof search, Lean compilation or network IO.
Python transformations are proposals; original-statement Lean acceptance remains
the trust boundary.
"""

from .registry import Library, LibraryError

__all__ = ['Library', 'LibraryError']
