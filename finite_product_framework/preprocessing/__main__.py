"""CLI. Explicit `run` is required to execute Lean; `prepare` only snapshots."""
import argparse
import json
from pathlib import Path

from .pipeline import prepare, run


def main():
    parser = argparse.ArgumentParser(description='Method-independent finite-q preprocessing')
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('prepare', 'run'):
        command = commands.add_parser(name)
        command.add_argument('--view', choices=('structured','expanded'), default='structured')
        command.add_argument('--identity', required=True, help='Exact ID in current Train')
        command.add_argument('--output', required=True, type=Path, help='New output directory')
        if name == 'run':
            command.add_argument('--timeout', type=float, default=600,
                                 help='Total wall-clock seconds including compilation')
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            result = prepare(args.identity, args.output, view=args.view)
            summary = dict(status=result['status'], identity=args.identity, lean_executed=False)
        else:
            summary = run(args.identity, args.output, timeout=args.timeout, view=args.view)
    except Exception as exc:
        print(json.dumps(dict(status='failed', error_type=type(exc).__name__, reason=str(exc)), ensure_ascii=False))
        raise SystemExit(1)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
