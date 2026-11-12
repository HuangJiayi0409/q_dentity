"""Generated invocation recorder; does not alter any production/test source."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('label', choices=('recurrence', 'telescoping', 'init'))
    args = parser.parse_args()
    commands = {
        'recurrence': [sys.executable, '-m', 'agent_v2.tests.recurrence_closure_smoke',
            '--output-root', str(OUT / 'recurrence'), '--seconds', '4000'],
        'telescoping': [sys.executable, '-m', 'agent_v2.tests.closure_smoke',
            '--output-root', str(OUT / 'telescoping'), '--seconds', '2400'],
        'init': [sys.executable, str(OUT / 'invoke_init_smoke.py')],
    }
    folder = OUT / 'driver_logs' / args.label
    folder.mkdir(parents=True, exist_ok=False)
    record = {'schema_version': 1, 'label': args.label,
        'command': commands[args.label], 'cwd': str(ROOT),
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'synthetic_test_only' if args.label == 'init' else 'real_single_Train_full_closure',
        'stdout': str(folder / 'stdout.log'), 'stderr': str(folder / 'stderr.log')}
    save(folder / 'command.json', record)
    start = time.monotonic()
    with (folder / 'stdout.log').open('w') as stdout, (folder / 'stderr.log').open('w') as stderr:
        process = subprocess.Popen(commands[args.label], cwd=ROOT, stdout=stdout, stderr=stderr)
        save(folder / 'running.json', dict(record, pid=process.pid))
        returncode = process.wait()
    record.update(returncode=returncode, wall_seconds=time.monotonic() - start,
                  ended_utc=datetime.now(timezone.utc).isoformat())
    save(folder / 'result.json', record)
    print(json.dumps(record, ensure_ascii=False), flush=True)
    return returncode

if __name__ == '__main__':
    raise SystemExit(main())
