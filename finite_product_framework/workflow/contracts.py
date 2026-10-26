"""Shared source snapshots and kernel-proof acceptance contract."""
from pathlib import Path
import hashlib
import json
import re

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parent
FAMILIES=('telescoping','recurrence','coefficient','product','interpolation','noncommutative','combinatorial','difference_ring','kernel_transform','spectral','determinant','macmahon')
BACKENDS={
 'direct_q_gosper':'telescoping', 'bibasic_gosper':'telescoping',
 'target_first_order':'recurrence','general_q_zeilberger':'recurrence',
 'ore_closure':'recurrence','multisum':'recurrence',
 'cauchy_coefficient':'coefficient', 'finite_product_indices':'product',
 'polynomial_interpolation':'interpolation','rational_principal_parts':'interpolation','operator_word_normalization':'noncommutative',
 'weighted_bijection':'combinatorial','sign_reversing_involution':'combinatorial','triangular_difference_ring':'difference_ring','finite_kernel_certificate':'kernel_transform','finite_spectral_certificate':'spectral','determinant_certificate':'determinant','finite_omega_elimination':'macmahon'}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    temporary.replace(path)

def snapshot(identity,work,method=None,*,preprocess=False):
    rows={r['id']:r for r in map(json.loads,(ROOT/'benchmark/splits/train.jsonl').read_text().splitlines())}
    if preprocess or method in ('product','interpolation','noncommutative','combinatorial','difference_ring','kernel_transform','spectral','determinant','macmahon'):
        if identity not in rows:raise ValueError('unsupported_input: train membership required')
    else:
        plans=json.loads((HERE/'research/train_a_methods/plans.json').read_text())
        admitted={r['id'] for r in plans['entries'] if r['primary_mechanism'] in ('P1','P2')}
        if identity not in admitted or identity not in rows or rows[identity]['family_id']!='A':
            raise ValueError('unsupported_input: only current P1/P2 train scope is admitted')
    row=rows[identity];path=ROOT/'benchmark'/row['lean_path']
    if sha(path)!=row['lean_sha256']:raise ValueError('source_changed: frozen train hash mismatch')
    source=path.read_text();names=re.findall(r'^theorem\s+(\S+)',source,re.M)
    namespaces=re.findall(r'^namespace\s+(\S+)',source,re.M)
    if len(names)!=1:raise ValueError('unsupported_declaration: one theorem required')
    target=Path(work)/'source.lean';target.write_text(source)
    return {'identity':identity,'path':str(path.relative_to(ROOT)),'sha256':sha(path),
            'snapshot':str(target),'theorem':'.'.join(namespaces+names),
            'scope':('current Train; verified shared preprocessing' if preprocess else 'train only; structural '+method+' frontend' if method in ('product','interpolation','noncommutative','combinatorial','difference_ring','kernel_transform','spectral','determinant','macmahon') else
                     'P1/P2 train only; membership is not backend selection')}

def check_source(source):
    for path in (ROOT/source['path'],Path(source['snapshot'])):
        if sha(path)!=source['sha256']:raise ValueError('source_changed: input changed during run')
    if source.get('preprocessing'):
        from .preprocessed import check
        check(source['preprocessing'],source)

def accept_proof(report,source,attempt_dir):
    """Never trust a backend's success flag without current proof/audit evidence."""
    check_source(source)
    if report.get('status')!='proved' or report.get('remaining_obligations')!=[]:
        raise ValueError('unclosed proof obligations')
    v=report.get('verification',{})
    proof=Path(v.get('proof_file','')).resolve();attempt_dir=Path(attempt_dir).resolve()
    if not proof.is_relative_to(attempt_dir) or not proof.is_file():
        raise ValueError('proof artifact outside this attempt')
    if sha(proof)!=v.get('proof_sha256'):raise ValueError('proof hash mismatch')
    if source.get('preprocessing'):
        audit=report.get('preprocessing_acceptance',{})
        file=Path(audit.get('file','')).resolve()
        if (not file.is_relative_to(attempt_dir) or not file.is_file() or sha(file)!=audit.get('sha256') or
            audit.get('source_sha256')!=source['sha256'] or audit.get('proof_sha256')!=sha(proof) or
            audit.get('bundle_sha256')!=sha(Path(source['preprocessing']['directory'])/'bundle.json') or
            audit.get('lean',{}).get('exit_code')!=0 or
            'PREPROCESS_ORIGINAL_PROOF_AUDIT_OK' not in audit.get('lean',{}).get('output','')):
            raise ValueError('missing or invalid preprocessing original-proof audit')
    lean=v.get('lean',{});output=lean.get('output','')
    if lean.get('exit_code')!=0 or 'sorryAx' in output:raise ValueError('Lean check failed')
    theorem=source['theorem']
    match=re.search(re.escape("'"+theorem+"' depends on axioms: [")+r'([^\]]*)\]',output)
    if match:axioms={a.strip() for a in match[1].split(',') if a.strip()}
    elif "'"+theorem+"' does not depend on any axioms" in output:axioms=set()
    else:raise ValueError('missing exact original-theorem axiom audit')
    if not axioms<={'propext','Classical.choice','Quot.sound'}:raise ValueError('unexpected axioms')
    # The frozen declaration/context must occur verbatim, except dependency imports.
    original=Path(source['snapshot']).read_text()
    body=re.sub(r'^import[^\n]*\n','',original,flags=re.M)
    pieces=re.split(r'(?m)^  sorry\s*$',body)
    if len(pieces)!=2 or pieces[0].strip() not in proof.read_text():
        raise ValueError('original declaration/context not preserved')
    for dep in report.get('dependencies',[]):
        if sha(ROOT/dep['path'])!=dep['sha256']:raise ValueError('dependency source changed')
    if report.get('backend') in ('finite_product_indices','polynomial_interpolation','rational_principal_parts','operator_word_normalization','weighted_bijection','sign_reversing_involution','triangular_difference_ring','finite_kernel_certificate','finite_spectral_certificate','determinant_certificate','finite_omega_elimination'):
        certificate=report.get('certificate',{})
        path=Path(certificate.get('path','')).resolve()
        if not path.is_relative_to(attempt_dir) or not path.is_file() or sha(path)!=certificate.get('sha256'):
            raise ValueError('certificate missing or changed')
        data=json.loads(path.read_text())
        if data.get('proof_sha256')!=sha(proof) or data.get('source_sha256')!=source['sha256']:
            raise ValueError('certificate not bound to source and proof')
    return {'proof_file':str(proof),'proof_sha256':sha(proof),'theorem':theorem,
            'axioms':sorted(axioms),'original_declaration_preserved':True}
