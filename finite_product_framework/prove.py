#!/usr/bin/env python3
"""Compatibility dispatcher: explicitly select one independent proof pipeline."""
import argparse
import json
from workflow.contracts import FAMILIES
from workflow.engine import Budget,prove

def main(method=None,select_only=False):
    description=('Preprocess and select one method using AHP/TOPSIS; do not run a proof method.' if select_only else
                 'Preprocess once, select one method using AHP/TOPSIS, and prove under one deadline.' if method=='auto' else
                 f"Independent {method} proof pipeline (class-local analysis and verification)." if method else __doc__)
    p=argparse.ArgumentParser(description=description)
    p.add_argument('--identity',required=True)
    if method is None:p.add_argument('--method',choices=(*FAMILIES,'auto'),required=True)
    else:p.set_defaults(method=method)
    p.add_argument('--output-root')
    p.add_argument('--preprocessing-view',choices=('structured','expanded'),default='structured')
    p.add_argument('--preprocess',action='store_true',help='Verify and consume the shared normalized target before this method')
    p.add_argument('--unknown-policy',choices=('mark','all'),default='mark',
                   help='Auto only: mark all-unknown ties, or explore all 12 methods with a separate --seconds budget per method')
    p.add_argument('--unknown-workers',type=int,choices=range(1,5),default=4,
                   help='Concurrent methods in an explicitly enabled all-unknown exploration (default: 4)')
    for name,default in [('seconds',900),('attempt-seconds',600),('analysis-seconds',120),('symbolic-seconds',240),('preprocessing-seconds',600),('selection-seconds',10)]:
        p.add_argument('--'+name,type=float,default=default)
    p.add_argument('--max-order',type=int,default=4)
    p.add_argument('--max-unknowns',type=int,default=10000)
    p.add_argument('--max-degree',type=int,default=5)
    p.add_argument('--laurent-floor',type=int,default=-1)
    a=p.parse_args()
    budget=Budget(**{name:getattr(a,name) for name in Budget.__dataclass_fields__})
    try:budget.validate()
    except ValueError as exc:p.error(str(exc))
    if a.unknown_policy=='all' and a.method!='auto':p.error('--unknown-policy all requires --method auto')
    r=prove(a.identity,a.output_root,a.method,budget,preprocess=a.preprocess,preprocessing_view=a.preprocessing_view,select_only=select_only,
            unknown_policy=a.unknown_policy,unknown_workers=a.unknown_workers)
    print(json.dumps({k:r[k] for k in ('status','identity','work_directory','classification_status','unclassified_reason','selected_method','selected_route','selection','successful_methods','automatic_train_proofs','remaining_obligations') if k in r},ensure_ascii=False,indent=2))
    return 0 if r['status']=='proved' or select_only and r['status'] in ('selected','unclassified') else 2
if __name__=='__main__':raise SystemExit(main())
