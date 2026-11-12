"""Record a fresh full discovery run; this script makes no capability claims."""
import argparse
import json
from pathlib import Path
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))


def identifiers(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from identifiers(item)
        else:
            yield item.id()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', required=True)
    args = parser.parse_args()
    output = Path(args.output_root).absolute()
    output.mkdir(parents=True, exist_ok=False)
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'agent_v2/tests'))
    ids = list(identifiers(suite))
    (output / 'discovered_tests.json').write_text(json.dumps(ids, indent=2) + '\n')
    started = time.monotonic()
    with (output / 'unittest.log').open('w') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    report = {
        'passed': result.wasSuccessful(),
        'scope': 'fresh full discovery: contracts, unit fixtures and real Lean regression; not Train performance',
        'tests_run': result.testsRun,
        'failures': [{'test': test.id(), 'traceback': trace} for test, trace in result.failures],
        'errors': [{'test': test.id(), 'traceback': trace} for test, trace in result.errors],
        'skipped': [{'test': test.id(), 'reason': reason} for test, reason in result.skipped],
        'expected_failures': [{'test': test.id(), 'traceback': trace} for test, trace in result.expectedFailures],
        'unexpected_successes': [test.id() for test in result.unexpectedSuccesses],
        'wall_seconds': time.monotonic() - started,
        'command': [sys.executable, *sys.argv],
        'discovered_tests': len(ids),
        'model_calls': 0,
        'benchmark_Test_read': False,
    }
    (output / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('passed', 'tests_run', 'wall_seconds')}), flush=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
