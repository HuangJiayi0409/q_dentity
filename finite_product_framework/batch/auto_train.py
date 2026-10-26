"""Detached, resumable Train evaluation of preprocess -> select -> prove.

One worker owns one identity. Unknown ties explore twelve methods sequentially,
so N identity workers never expand into 4N simultaneous solver processes.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from dataclasses import asdict
from datetime import datetime, timezone
import csv
import fcntl
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from batch.train import frozen_files, verify
from selection.policy import all_unknown_tie, fingerprint
from workflow.contracts import ROOT, HERE, FAMILIES, accept_proof, save, sha
from workflow.engine import Budget, prove


def now():
    return datetime.now(timezone.utc).isoformat()


def load(path):
    return json.loads(Path(path).read_text())


def train_rows():
    rows = [json.loads(s) for s in (ROOT/'benchmark/splits/train.jsonl').read_text().splitlines()]
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('duplicate Train identity')
    for row in rows:
        source = (ROOT/'benchmark'/row['lean_path']).resolve()
        if not source.is_relative_to(ROOT/'benchmark/lean/Benchmark/Statements/Train'):
            raise ValueError('non-Train path')
        if sha(source) != row['lean_sha256']:
            raise ValueError('Train source hash mismatch: '+row['id'])
    return rows


def resources(work):
    mem = {line.split(':', 1)[0]: int(line.split()[1])*1024
           for line in Path('/proc/meminfo').read_text().splitlines() if ':' in line}
    return dict(time=now(), available_memory_gib=mem['MemAvailable']/2**30,
                free_disk_gib=shutil.disk_usage(work).free/2**30)


def inspect_report(report, *, accept=True):
    """Validate the routing contract and reaccept every counted original proof."""
    classification = 'not_reached'
    selection = None
    if report.get('selection'):
        selection = load(report['selection']['result'])
        classification = selection['status']
        if classification in ('selected', 'unclassified', 'unsupported_input'):
            if selection['provenance'] != fingerprint():
                raise ValueError('selector version changed')
            source = report['source']
            standard = Path(source['preprocessing']['directory'])/'standard.json'
            if selection['source_sha256'] != source['sha256'] or selection['standard_sha256'] != sha(standard):
                raise ValueError('selection/input mismatch')
    method_reports = []
    if report.get('exploration'):
        exploration = report['exploration']
        if classification != 'unclassified' or not all_unknown_tie(selection['ranking']):
            raise ValueError('all-method exploration without an all-unknown tie')
        if report.get('selected_method') is not None or exploration['workers'] != 1:
            raise ValueError('batch unknown exploration must be sequential and unclassified')
        if exploration['status'] == 'completed':
            names = [r['method'] for r in exploration['results']]
            if len(names) != 12 or set(names) != set(FAMILIES):
                raise ValueError('incomplete twelve-method exploration')
        for row in exploration['results']:
            child = load(row['report'])
            if child['method_request'] != row['method'] or child['identity'] != report['identity']:
                raise ValueError('child identity/method mismatch')
            if child['source']['preprocessing'] != report['source']['preprocessing']:
                raise ValueError('methods did not consume the same preprocessing')
            if not child['preprocessing']['reused_from_parent'] or 'selection' in child:
                raise ValueError('child reran preprocessing or classification')
            method_reports.append((row['method'], child, row['report'], child['elapsed_seconds']))
    elif classification == 'selected' and report.get('selected_method'):
        method = report['selected_method']
        if method != selection['selected_method']:
            raise ValueError('method differs from selector choice')
        started = next(e['elapsed_seconds'] for e in report['events'] if e['stage'] == 'selection')
        method_reports.append((method, report, str(Path(report['work_directory'])/'report.json'),
                               max(0., report['elapsed_seconds']-started)))
    methods = []; accepted = []
    for method, child, path, seconds in method_reports:
        if any(a['method'] != method for a in child['plan']+child['attempts']):
            raise ValueError('cross-method child attempt')
        methods.append(dict(method=method, status=child['status'], seconds=seconds,
                            report=path, report_sha256=sha(path)))
        if child['status'] == 'proved':
            attempts = [a for a in child['attempts'] if a['status'] == 'proved']
            if len(attempts) != 1 or child['automatic_train_proofs'] != 1:
                raise ValueError('ambiguous success evidence')
            if child['elapsed_seconds'] > child['budget']['seconds']:
                raise ValueError('method proof exceeded its deadline')
            p = Path(attempts[0]['result'])
            artifact = accept_proof(load(p), child['source'], p.parent) if accept else None
            accepted.append(dict(method=method, result=str(p), artifact=artifact))
    if (report['status'] == 'proved') != bool(accepted):
        raise ValueError('parent proof status differs from audited methods')
    if report['automatic_train_proofs'] != int(bool(accepted)):
        raise ValueError('parent proof count mismatch')
    return classification, methods, accepted


def task(identity, directory, budget):
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    start = time.monotonic(); started = now()
    try:
        report = prove(identity, directory/'runs', method='auto', budget=Budget(**budget),
                       unknown_policy='all', unknown_workers=1)
        path = Path(report['work_directory'])/'report.json'
        classification, methods, accepted = inspect_report(report)
        record = dict(identity=identity, status=report['status'], classification=classification,
            selected_method=report.get('selected_method'), successful_methods=[r['method'] for r in accepted],
            proved=bool(accepted), methods=methods, proof_acceptance=accepted,
            report=str(path), report_sha256=sha(path), pipeline_seconds=report['elapsed_seconds'],
            preprocessing_seconds=report.get('preprocessing', {}).get('wall_seconds', 0.),
            selection_seconds=report.get('selection', {}).get('wall_seconds', 0.),
            preprocessing_cache_hit=report.get('preprocessing', {}).get('cache_hit'),
            method_seconds_sum=sum(r['seconds'] for r in methods))
    except Exception as exc:
        record = dict(identity=identity, status='runner_error', classification='incomplete',
                      selected_method=None, successful_methods=[], proved=False, methods=[],
                      error=repr(exc), traceback=traceback.format_exc())
    record.update(started_at=started, finished_at=now(), problem_seconds=time.monotonic()-start,
                  test_files_read=0)
    save(directory/'result.json', record)
    return record


def atomic_csv(path, fields, rows):
    path = Path(path); tmp = path.with_suffix('.csv.tmp')
    with tmp.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader(); writer.writerows(rows)
    tmp.replace(path)


def write_tables(work, records):
    rows = [dict(r, successful_methods=';'.join(r['successful_methods']), method_count=len(r['methods']))
            for r in records]
    atomic_csv(work/'per_identity.csv', ['identity','status','classification','selected_method','successful_methods',
        'proved','problem_seconds','pipeline_seconds','preprocessing_seconds','selection_seconds',
        'method_seconds_sum','method_count','preprocessing_cache_hit','started_at','finished_at','report'], rows)
    methods = [dict(m, identity=r['identity']) for r in records for m in r['methods']]
    atomic_csv(work/'per_method.csv', ['identity','method','status','seconds','report'], methods)


def summarize(manifest, records, *, state, active, first_started, session_started, prior_active):
    proved = sorted(r['identity'] for r in records if r['proved'])
    total = len(manifest['identities'])
    result = dict(status=state, updated_at=now(), pid=os.getpid(), workers=manifest['workers'],
        total=total, completed=len(records), remaining=total-len(records), active=list(active),
        active_count=len(active), proved=len(proved), proved_identities=proved,
        success_rate=len(proved)/total if state == 'completed' else None,
        provisional_proved_fraction_of_all_train=len(proved)/total,
        classification_counts=dict(Counter(r['classification'] for r in records)),
        status_counts=dict(Counter(r['status'] for r in records)),
        wall_seconds=max(0., time.time()-first_started),
        active_wall_seconds=prior_active+time.monotonic()-session_started,
        problem_seconds_sum=sum(r['problem_seconds'] for r in records),
        pipeline_seconds_sum=sum(r.get('pipeline_seconds', 0.) for r in records),
        method_seconds_sum=sum(r.get('method_seconds_sum', 0.) for r in records),
        method_tasks_completed=sum(len(r['methods']) for r in records),
        cache_hits=sum(r.get('preprocessing_cache_hit') is True for r in records),
        cache_misses=sum(r.get('preprocessing_cache_hit') is False for r in records),
        test_files_read=0, success_definition='accepted complete original theorem; deduplicated by Train identity')
    return result


def audit(work, manifest, records):
    verify(manifest['frozen_files'])
    if len(records) != len(manifest['identities']) or {r['identity'] for r in records} != set(manifest['identities']):
        raise ValueError('incomplete Train records')
    proofs = []
    for record in records:
        if not record.get('report'):
            if record['proved']: raise ValueError('proof without a report')
            continue
        if sha(record['report']) != record['report_sha256']:
            raise ValueError('saved report changed')
        classification, methods, accepted = inspect_report(load(record['report']))
        if classification != record['classification'] or methods != record['methods']:
            raise ValueError('saved result differs from original report')
        if bool(accepted) != record['proved']:
            raise ValueError('audited proof count changed')
        proofs.extend(dict(identity=record['identity'], **p) for p in accepted)
    verify(manifest['frozen_files'])
    result = dict(status='passed', identities=len(records), proved=len({p['identity'] for p in proofs}),
                  proofs=proofs, frozen_files=len(manifest['frozen_files']), test_files_read=0)
    save(work/'final_audit.json', result)
    return result


def final_report(work, summary):
    lines = ['Train：预处理 → 分类 → 符号计算 → 完整原题 Lean 验证', '',
        f"状态：{summary['status']}；完成 {summary['completed']}/{summary['total']} 题。",
        f"完整原题证明成功：{summary['proved']}/{summary['total']}（{summary['success_rate']:.2%}）。",
        f"整轮墙钟耗时：{summary['wall_seconds']:.3f} 秒；运行会话墙钟累计：{summary['active_wall_seconds']:.3f} 秒。",
        f"逐题耗时之和：{summary['problem_seconds_sum']:.3f} 秒；各方法阶段耗时之和：{summary['method_seconds_sum']:.3f} 秒。",
        '逐题墙钟从该题开始执行到完成并重新接收证据，不含派发前排队；包含预处理、分类、方法执行和审计。',
        '整轮墙钟包括并发、派发和最终审计；如发生中断续跑，也包括两会话间的间隔。',
        '运行会话墙钟累计排除已记录的会话间隔；突然中断的会话以最后一次心跳为准。',
        '明确首选：原共同900秒预算，只运行首选；全部未知并列：共用预处理，十二方法各900秒，依次尝试且不在首次成功后停止。',
        f"并发上限 {summary['workers']} 道题，未知题内部每次仅一个方法；分类与算法运行期间冻结。",
        f"预处理缓存：命中 {summary['cache_hits']}，未命中 {summary['cache_misses']}；不是统一冷缓存测量。",
        f"全部{summary['total']}题均在成功率分母内，错误/不支持/超时不排除；失败不是数学不可证明。",
        '逐题数据 per_identity.csv；逐方法数据 per_method.csv；完整证明重新接收 final_audit.json。',
        '未读取Test。']
    (work/'REPORT.txt').write_text('\n'.join(lines)+'\n')


def prepare(work, workers):
    path = work/'manifest.json'
    if path.exists():
        manifest = load(path)
        if manifest['workers'] != workers: raise ValueError('resume must preserve concurrency')
        verify(manifest['frozen_files'])
        return manifest
    rows = train_rows()
    manifest = dict(schema_version=1, created_at=now(), workers=workers, identities=[r['id'] for r in rows],
        budget=asdict(Budget()), unknown_policy='all', unknown_workers=1,
        methods=list(FAMILIES), frozen_files=frozen_files(rows), selector=fingerprint(),
        min_available_memory_gib=32, min_free_disk_gib=40,
        preprocessing_view='structured', cache_policy='reuse validated cache; record actual hits and timing',
        total=len(rows), test_files_read=0, failure_policy='record only; no changes to frozen implementations',
        timing='per-identity wall, sum of identity walls, complete batch wall and individual method walls')
    save(path, manifest)
    return manifest


def run(work, manifest):
    done = {}
    for identity in manifest['identities']:
        path = work/'tasks'/identity/'result.json'
        if path.exists():
            record = load(path)
            if record['identity'] != identity: raise ValueError('resume identity mismatch')
            if record.get('report') and sha(record['report']) != record['report_sha256']:
                raise ValueError('resume report changed')
            done[identity] = record
    timing_path = work/'timing.json'
    timing = load(timing_path) if timing_path.exists() else dict(first_started_epoch=time.time(), sessions=[])
    prior_active = sum(s.get('active_seconds', 0.) for s in timing['sessions'])
    session = dict(started_at=now(), pid=os.getpid(), status='running', active_seconds=0.)
    timing['sessions'].append(session);save(timing_path, timing)
    started = time.monotonic(); checked = started; sampled = 0.; stop_reason = None
    pending = iter(i for i in manifest['identities'] if i not in done)
    active = {}; exhaustion = False

    def publish(state):
        records = [done[i] for i in manifest['identities'] if i in done]
        summary = summarize(manifest, records, state=state, active=active.values(),
                            first_started=timing['first_started_epoch'], session_started=started, prior_active=prior_active)
        if stop_reason: summary['stop_reason'] = stop_reason
        save(work/'summary.json', summary);write_tables(work, records)
        session.update(status=state, updated_at=now(), active_seconds=time.monotonic()-started)
        save(timing_path, timing)
        return summary

    def check_resources():
        nonlocal sampled
        row = resources(work)
        if time.monotonic()-sampled >= 30:
            with (work/'resources.jsonl').open('a') as stream:stream.write(json.dumps(row)+'\n')
            sampled = time.monotonic()
        if row['available_memory_gib'] < manifest['min_available_memory_gib'] or row['free_disk_gib'] < manifest['min_free_disk_gib']:
            return row
        return None

    publish('running')
    try:
        with ThreadPoolExecutor(max_workers=manifest['workers']) as pool:
            while True:
                if not stop_reason:
                    low = check_resources()
                    if low: stop_reason = dict(kind='resource_guard', resources=low)
                while not stop_reason and not exhaustion and len(active) < manifest['workers']:
                    identity = next(pending, None)
                    if identity is None: exhaustion = True;break
                    future = pool.submit(task, identity, work/'tasks'/identity, manifest['budget'])
                    active[future] = identity
                publish('draining' if stop_reason else 'running')
                if not active: break
                finished, _ = wait(active, timeout=10, return_when=FIRST_COMPLETED)
                for future in finished:
                    identity = active.pop(future);record = future.result();done[identity] = record
                    print(json.dumps(dict(completed=len(done), total=manifest['total'], identity=identity,
                        status=record['status'], classification=record['classification'],
                        proved=record['proved'], seconds=record['problem_seconds']), ensure_ascii=False), flush=True)
                if time.monotonic()-checked >= 60:
                    try:verify(manifest['frozen_files'])
                    except Exception as exc:stop_reason = dict(kind='integrity_guard', error=repr(exc))
                    checked = time.monotonic()
        if stop_reason:
            return publish('resource_paused' if stop_reason['kind']=='resource_guard' else 'integrity_stopped')
        publish('auditing')
        records = [done[i] for i in manifest['identities']]
        audit(work, manifest, records)
        summary = publish('completed');final_report(work, summary)
        print(json.dumps(dict(status='completed', proved=summary['proved'], total=summary['total'],
                              success_rate=summary['success_rate'],wall_seconds=summary['wall_seconds']),ensure_ascii=False),flush=True)
        return summary
    except BaseException as exc:
        stop_reason = dict(kind='controller_error', error=repr(exc), traceback=traceback.format_exc())
        publish('interrupted')
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=36)
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--audit-only', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.workers <= 64:parser.error('workers must be 1..64')
    work = args.run_dir.resolve();work.mkdir(parents=True, exist_ok=True)
    with (work/'runner.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = prepare(work, args.workers)
        if args.prepare_only:
            print(json.dumps(dict(status='prepared', total=manifest['total'], workers=args.workers,
                                  unknown_workers=1, work=str(work))));return
        if args.audit_only:
            audit(work, manifest, [load(work/'tasks'/i/'result.json') for i in manifest['identities']]);return
        run(work, manifest)


if __name__ == '__main__':main()
