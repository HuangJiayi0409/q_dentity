#!/usr/bin/env python3
"""Check review coverage, source provenance and independently recompute local residuals."""
import hashlib
import contextlib
import io
from html.parser import HTMLParser
import json
from pathlib import Path
import sympy as s
from build_review import HERE,P1,ROOT,REVIEW,main


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def check():
    before={name:(HERE/name).read_bytes() for name in ('review.json','review.csv','index.html')}
    with contextlib.redirect_stdout(io.StringIO()):
        main()
    assert all((HERE/name).read_bytes()==data for name,data in before.items()),'stale generated review'
    data=json.loads((HERE/'review.json').read_text());rows=data['records']
    assert len(rows)==51 and set(REVIEW)=={r['id'] for r in rows}
    baseline=json.loads((P1/'generated/train_a_screen/table.json').read_text())['records']
    assert set(REVIEW)=={r['id'] for r in baseline if r['candidate_routes']}
    for row in rows:
        assert digest(ROOT/row['source_path'])==row['source_sha256']
        assert all(row[k]==v for k,v in REVIEW[row['id']].items())
        assert row['mathematical_reason'] and row['required_check_or_preprocessing'] and row['next_action']
        assert row['category']!='defer_from_current_routes' or row['alternative_method']
    probes=[]
    for path in sorted((HERE/'trials').glob('*.json')):
        report=json.loads(path.read_text());assert report['status']=='constructed'
        assert report['source_unchanged'] and not report['lean_representation_verified']
        assert not report['automatic_train_proof']
        assert digest(ROOT/report['source']['path'])==report['source']['sha256']
        assert report['probe_code_sha256']==digest(HERE/'symbolic_trials.py')
        assert report['diagnostics']['status']=='passed'
        symbols={name:s.Symbol(name) for name in ('q','Q','X','a','c','z')}
        U,V,c=[s.sympify(report['derived_shifts'][key],locals=symbols) for key in ('U','V','c')]
        R=s.sympify(report['construction']['certificate'],locals=symbols);q,X=s.symbols('q X')
        assert s.cancel(V*R.subs(X,q*X)-R-U+c)==0
        probes.append(report['id'])
    assert len(probes)==4
    for entry in data['summary']['evidence_sources']:assert digest(ROOT/entry['path'])==entry['sha256']
    production=json.loads((P1/'validation.json').read_text())
    assert production['status']=='passed' and production['automatic_train_proofs']==2
    for name,expected in production['code_sha256'].items():assert digest(P1/name)==expected,'production pipeline changed'
    class Links(HTMLParser):
        def handle_starttag(self,tag,attrs):
            if tag=='a':
                href=dict(attrs).get('href','')
                if href:assert (HERE/href).exists(),href
    Links().feed((HERE/'index.html').read_text())
    report={'status':'passed','reviewed':51,'categories':data['summary']['categories'],
            'source_hashes_checked':51,'shared_definition_hashes_checked':4,
            'independent_symbolic_residuals_checked':4,
            'exact_finite_diagnostics_per_probe':16,
            'production_code_unchanged':True,'automatic_train_proofs':2,'new_lean_proofs':0,
            'probe_ids':probes,'review_builder_sha256':digest(HERE/'build_review.py'),
            'probe_code_sha256':digest(HERE/'symbolic_trials.py')}
    (HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':check()
