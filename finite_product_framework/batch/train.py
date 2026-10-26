"""Train-only process-pool runner; never edits or selects across method pipelines."""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from dataclasses import asdict
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE, ROOT, FAMILIES, save, sha
from workflow.engine import Budget, prove


def now():
    return datetime.now(timezone.utc).isoformat()


def frozen_files(rows):
    files = set()
    for p in HERE.rglob('*'):
        if p.suffix in ('.py', '.lean') and not set(p.relative_to(HERE).parts) & {
                'generated', '__pycache__', 'archive'}:
            files.add(p)
    files.update((ROOT/'benchmark/lean/Benchmark').glob('*.lean'))
    files.update(ROOT/'benchmark'/r['lean_path'] for r in rows)
    files.update([ROOT/'benchmark/splits/train.jsonl',
                  HERE/'research/train_a_methods/plans.json',
                  ROOT/'project/lean-toolchain', ROOT/'project/lake-manifest.json'])
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(files)}


def verify(files):
    changed = [p for p, digest in files.items() if not (ROOT/p).is_file() or sha(ROOT/p) != digest]
    if changed:
        raise RuntimeError('frozen inputs changed: '+', '.join(changed[:10]))


def classify(report):
    if report['status'] == 'proved':
        return 'proved', []
    if report['status'] == 'preprocessing_failed':
        return 'preprocessing_failed', [report.get('preprocessing',{}),report.get('error','')]
    error = report.get('error', '')
    if 'only current P1/P2 train scope' in error:
        return 'scope_blocked', [error]
    if report['status'] in ('integrity_error', 'invalid_input'):
        return 'engineering_or_integrity_error', [error]
    diagnostics = []
    for stage in report.get('analysis', [])+report.get('attempts', []):
        p = Path(stage['result'])
        if p.exists():
            diagnostics.append(json.loads(p.read_text()))
    statuses = {d.get('status') for d in diagnostics}
    if report['status'] == 'resource_exhausted' or statuses & {'timeout', 'resource_exhausted'}:
        return 'resource_exhausted', diagnostics
    if statuses & {'adapter_failed', 'worker_failed'}:
        return 'adapter_error_needs_review', diagnostics
    if not report.get('plan'):
        return 'representation_or_applicability_unresolved', diagnostics
    if any(d.get('construction', {}).get('status') == 'constructed' for d in diagnostics):
        return 'constructed_but_original_unproved', diagnostics
    # Do not infer mathematical inapplicability from a search failure.
    return 'unproved_needs_review', diagnostics


def task(item):
    identity, method, directory, budget, preprocess = item
    directory = Path(directory)
    started = now()
    try:
        result = prove(identity, output_root=directory/'attempts', method=method,
                       budget=Budget(**budget),preprocess=preprocess)
        label, diagnostics = classify(result)
        record = dict(identity=identity, method=method, label=label,
            pipeline_status=result['status'], started_at=started, finished_at=now(),
            elapsed_seconds=result['elapsed_seconds'], report=str(Path(result['work_directory'])/'report.json'),
            diagnostics=diagnostics, test_files_read=0)
    except Exception as exc:
        record = dict(identity=identity, method=method, label='runner_error',
                      error=repr(exc), started_at=started, finished_at=now(), test_files_read=0)
    save(directory/'result.json', record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=24)
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--preprocess', action='store_true', help='Use verified shared preprocessing before each method')
    args = parser.parse_args()
    if not 1 <= args.workers <= 64:
        parser.error('workers must be 1..64')
    work = args.run_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    lock = (work/'runner.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    manifest_path = work/'manifest.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if manifest['workers'] != args.workers:
            raise ValueError('resume must preserve worker count')
        if manifest.get('preprocess',False) != args.preprocess:
            raise ValueError('resume must preserve preprocessing mode')
        verify(manifest['frozen_files'])
    else:
        rows = [json.loads(s) for s in (ROOT/'benchmark/splits/train.jsonl').read_text().splitlines()]
        assert len({r['id'] for r in rows}) == len(rows)
        for row in rows:
            path = (ROOT/'benchmark'/row['lean_path']).resolve()
            assert path.is_relative_to(ROOT/'benchmark/lean/Benchmark/Statements/Train')
            assert sha(path) == row['lean_sha256'], row['id']
        manifest = dict(created_at=now(), workers=args.workers, methods=list(FAMILIES),preprocess=args.preprocess,
            identities=[r['id'] for r in rows], budget=asdict(Budget()),
            frozen_files=frozen_files(rows), total_tasks=len(rows)*len(FAMILIES),
            test_files_read=0, failure_policy='labels only; pipelines unchanged',
            python=sys.version, logical_cpus=os.cpu_count(),
            dependency_policy='existing project lake manifest; isolated per-task compiled dependencies')
        save(manifest_path, manifest)
    if args.prepare_only:
        print(json.dumps(dict(status='prepared', tasks=manifest['total_tasks'], workers=args.workers)))
        return
    save(work/'runner.json', dict(pid=os.getpid(), started_at=now(), workers=args.workers))
    done = {}
    pending = []
    for identity in manifest['identities']:
        for method in manifest['methods']:
            directory = work/'tasks'/identity/method
            file = directory/'result.json'
            if file.exists():
                row = json.loads(file.read_text())
                assert (row['identity'], row['method']) == (identity, method)
                done[(identity, method)] = row
            else:
                pending.append((identity, method, str(directory), manifest['budget'], manifest.get('preprocess',False)))

    def summary(state, active=()):
        successes = {r['identity'] for r in done.values() if r['label'] == 'proved'}
        result = dict(status=state, updated_at=now(), pid=os.getpid(), workers=args.workers,
            total_tasks=manifest['total_tasks'], completed=len(done),preprocess=manifest.get('preprocess',False),
            remaining=manifest['total_tasks']-len(done), unique_proved=len(successes),
            proved_identities=sorted(successes), labels=dict(Counter(r['label'] for r in done.values())),
            per_method={m: dict(Counter(r['label'] for r in done.values() if r['method']==m))
                        for m in manifest['methods']},
            active=[dict(identity=t[0], method=t[1]) for t in active], test_files_read=0)
        save(work/'summary.json', result)
        return result

    summary('running')
    queue = iter(pending)
    checked = time.monotonic()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        active = {}
        def fill():
            while len(active) < args.workers:
                item = next(queue, None)
                if item is None:
                    break
                active[pool.submit(task, item)] = item
        fill()
        while active:
            finished, _ = wait(active, timeout=10, return_when=FIRST_COMPLETED)
            for future in finished:
                item = active.pop(future)
                row = future.result()
                done[(item[0], item[1])] = row
                print(json.dumps(dict(completed=len(done), identity=item[0], method=item[1],
                                      label=row['label']), ensure_ascii=False), flush=True)
            if time.monotonic()-checked > 60:
                verify(manifest['frozen_files'])
                checked = time.monotonic()
            fill()
            summary('running', active.values())
    verify(manifest['frozen_files'])
    summary('completed')


if __name__ == '__main__':
    main()
