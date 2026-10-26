"""Explicit all-method exploration for a selector's all-unknown tie.

Each method keeps its own deadline and original-proof audit. The preprocessor
runs once, all twelve methods finish even after a success, and the classifier's
unclassified label is never replaced with an empirical winner.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .contracts import FAMILIES, check_source, save


def explore(identity, source, work, budget, *, runner, workers, on_result, preprocessing_view):
    from .engine import prove
    check_source(source)
    work = Path(work)
    rows = {}

    def one(method):
        return prove(identity, work/method, method, budget, runner=runner,
                     preprocess=True, preprocessing_descriptor=source['preprocessing'],
                     preprocessing_view=preprocessing_view)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        active = {pool.submit(one, method): method for method in FAMILIES}
        for future in as_completed(active):
            method = active[future]
            result = future.result()
            row = dict(method=method, status=result['status'],
                       report=str(Path(result['work_directory'])/'report.json'),
                       elapsed_seconds=result['elapsed_seconds'],
                       automatic_train_proofs=result['automatic_train_proofs'])
            if result['status'] == 'proved':
                row['proof'] = result['proof']
            rows[method] = row
            save(work/'results.json', [rows[m] for m in FAMILIES if m in rows])
            on_result(row)
    check_source(source)
    return [rows[m] for m in FAMILIES]
