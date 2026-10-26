"""Replay local source encoding, every Omega branch, and coefficient GF output."""
from pathlib import Path
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'p1'))
from core import CoreBudget,compute
from check_omega_core import replay
from macmahon.adapter import source_sums,encode,reconstruct


def check(source,binding,requests,responses,value):
    candidates,_=source_sums(source)
    candidate=next((c for c in candidates if c['source_span']==binding['source_span']),None)
    assert candidate is not None,'source span not found'
    expected_requests,expected_binding=encode(candidate)
    assert requests==expected_requests,'encoding no longer matches source constraints/weights'
    assert binding==expected_binding,'source binding altered'
    assert len(responses)==len(requests),'missing branch'
    for req,response in zip(requests,responses):replay(req,response)
    assert str(reconstruct(responses,binding))==value,'wrong reconstructed coefficient GF'
    return len(requests)


def audit_train_sources(root,out):
    import copy
    from collections import Counter
    rows=[json.loads(line) for line in (root/'benchmark/splits/train.jsonl').read_text().splitlines()]
    records=[];encoding_rejections=Counter();source_rejections=Counter()
    for row in rows:
        path=root/'benchmark'/row['lean_path'];source=path.read_text()
        assert hashlib.sha256(source.encode()).hexdigest()==row['lean_sha256']
        candidates,rejected=source_sums(source)
        for r in rejected:source_rejections[r['reason']]+=1
        for index,candidate in enumerate(candidates):
            try:requests,binding=encode(candidate)
            except ValueError as exc:encoding_rejections[str(exc)]+=1;continue
            responses=[compute(req,CoreBudget()) for req in requests]
            value=str(reconstruct(responses,binding))
            check(source,binding,requests,responses,value)
            directory=out/row['id']/str(index);directory.mkdir(parents=True,exist_ok=True)
            artifact=dict(identity=row['id'],source_sha256=row['lean_sha256'],binding=binding,
                requests=requests,responses=responses,value=value,original_identity_proved=False)
            (directory/'audit.json').write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n')
            records.append(dict(identity=row['id'],candidate=index,value=value,path=str((directory/'audit.json').relative_to(out))))
    assert records,'no actual Train input reached Omega'
    first=json.loads((out/records[0]['path']).read_text())
    row=next(r for r in rows if r['id']==first['identity']);source=(root/'benchmark'/row['lean_path']).read_text()
    rejections=[]
    changes=[('source_span',lambda a:a['binding'].update(source_span=[0,1])),
             ('weight',lambda a:a['requests'][0]['input'].update(numerator=2)),
             ('missing_constraint',lambda a:a['requests'][0]['input']['eliminate'].clear()),
             ('missing_branch',lambda a:a['responses'].clear()),
             ('result',lambda a:a.update(value='0'))]
    for name,change in changes:
        bad=copy.deepcopy(first);change(bad)
        try:check(source,bad['binding'],bad['requests'],bad['responses'],bad['value'])
        except (AssertionError,ValueError):rejections.append(name)
        else:raise AssertionError('accepted tampering '+name)
    result=dict(train_sources_scanned=len(rows),actual_core_inputs=len(records),
        identities_with_inputs=len({r['identity'] for r in records}),records=records,
        source_rejections=dict(source_rejections),encoding_rejections=dict(encoding_rejections),
        tampering_rejected=rejections,test_split_read=False,lean_run=False,original_identity_proofs_added=0,
        scope='adapter audit, not five-system full Train batch')
    (out/'source_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['train_sources_scanned','actual_core_inputs','identities_with_inputs','tampering_rejected']},ensure_ascii=False))


if __name__=='__main__':
    root=Path(__file__).resolve().parents[2]
    audit_train_sources(root,root/'finite_product_framework/generated/omega_adapter_20261014')
