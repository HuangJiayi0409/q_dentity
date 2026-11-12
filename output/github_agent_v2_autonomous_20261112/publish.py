"""Publish the reviewed autonomous changes with a non-forced GitHub update."""
import base64
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
TRANSPORT=OUT/'transport_xz'
EVIDENCE=ROOT/'agent_v2/generated/autonomous_20261112'
REPO='repos/HuangJiayi0409/q_dentity'
GH=ROOT/'.tools/github-cli/bin/gh'
ENV=dict(os.environ,GH_CONFIG_DIR=str(ROOT/'.tools/github-cli/auth'))

def sha(data):return hashlib.sha256(data).hexdigest()
def blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def read(name):return json.loads((OUT/name).read_text())
def save(name,data):
    file=OUT/name;file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def api(endpoint,body=None,method=None):
    cmd=[str(GH),'api',REPO+('/'+endpoint if endpoint else '')]
    payload=None
    if body is not None:
        cmd+=['--method',method or 'POST','--input','-'];payload=json.dumps(body,ensure_ascii=False)
    result=subprocess.run(cmd,cwd=ROOT,env=ENV,input=payload,capture_output=True,text=True,timeout=300)
    if result.returncode:raise RuntimeError('GitHub request failed: '+result.stderr.strip()[:2000])
    return json.loads(result.stdout)

def tree(identity):
    result=api('git/trees/'+identity+'?recursive=1')
    if result.get('truncated'):raise RuntimeError('truncated remote tree')
    return {row['path']:row for row in result['tree'] if row['type']!='tree'}

def inspect_remote():
    info=api('');head=api('git/ref/heads/main')['object']['sha']
    commit=api('git/commits/'+head);branch=api('branches/main')
    files=tree(commit['tree']['sha'])
    if branch['commit']['sha']!=head or api('git/ref/heads/main')['object']['sha']!=head:
        raise RuntimeError('remote moved during inspection')
    save('remote_inspection.json',{'head':head,'tree':commit['tree']['sha'],
        'branch_protected':branch['protected'],'default_branch':info['default_branch'],
        'permissions':info.get('permissions'), 'files':files})
    print(json.dumps({'head':head,'protected':branch['protected'],'files':len(files),
                      'default_branch':info['default_branch']}),flush=True)

def frozen_check():
    final=json.loads((EVIDENCE/'final_validation.json').read_text())
    if final['status']!='validated' or not final['final_runtime_hashes_match']:
        raise RuntimeError('final validation is not successful')
    manifest=json.loads((EVIDENCE/'final_revision_02/source_manifest.json').read_text())
    for item in manifest['files']:
        data=(ROOT/item['path']).read_bytes()
        if sha(data)!=item['sha256'] or data!=(EVIDENCE/'final_revision_02/frozen'/item['path']).read_bytes():
            raise RuntimeError('runtime freeze differs: '+item['path'])
    changed=json.loads((EVIDENCE/'changed_files.json').read_text())
    for item in changed['files']:
        if sha((ROOT/item['path']).read_bytes())!=item['sha256']:
            raise RuntimeError('accepted change differs: '+item['path'])
    return manifest,changed

def baseline_for(name,expected):
    for path in [EVIDENCE/'before'/name,OUT/'before'/name,
                 ROOT/'output/github_agent_v2_phase3_20261112/staging'/name]:
        if path.is_file() and blob(path.read_bytes())==expected:return str(path.relative_to(ROOT))
    raise RuntimeError('remote file has no matching reviewed baseline: '+name)

def safe_path(name):
    path=ROOT/name
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(ROOT):
        raise RuntimeError('unsafe upload source: '+name)
    if any(part in {'Test','__pycache__','.git','.tools','.env','.lake'} or part.startswith('API_')
           for part in path.relative_to(ROOT).parts):
        raise RuntimeError('excluded upload source: '+name)
    return path

def secret_scan(names):
    # Credentials are compared in memory only. Never write their values or
    # digests into publication records, diagnostics, or exception messages.
    secrets=[]
    for path in ROOT.glob('API_*'):
        if not path.is_file() or path.stat().st_size>16384:continue
        text=path.read_text().strip()
        if text.startswith('{'):
            obj=json.loads(text)
            secrets.extend(v.encode() for k,v in obj.items() if k.lower() in {'key','api_key','token'} and isinstance(v,str) and len(v)>12)
        elif '\n' not in text and len(text)>12:secrets.append(text.encode())
    for name in names:
        data=safe_path(name).read_bytes()
        if any(value in data for value in secrets):raise RuntimeError('credential content in upload: '+name)
    return {'passed':True,'files':len(names),'secret_values_recorded':False}

def select_names(manifest,changed):
    names={item['path'] for item in manifest['files']}|{item['path'] for item in changed['files']}
    names.update({'agent_v2/PUBLISHING.md','docs/superpowers/plans/2026-11-12-agent-v2-autonomous.md'})
    # Freeze the concrete project-owned input/dependency sources for these
    # demonstrations; installed packages/toolchains and run-local JSON belong
    # to the audited archive/environment, not to production source uploads.
    final=json.loads((EVIDENCE/'final_validation.json').read_text())
    for item in final['runs']:
        run=EVIDENCE/item['path']
        data=json.loads((run/'initial_state.json').read_text())['G']
        paths=[data['path']]+[a['path'] for a in data['dependencies']]
        for value in paths:
            path=Path(value)
            if not path.is_relative_to(ROOT):continue
            rel=path.relative_to(ROOT)
            if '.lake' in rel.parts or 'generated' in rel.parts:continue
            names.add(str(rel))
    direct=['final_validation.json','changed_files.json','baseline.json','train_preregistration.json',
            'math_probe/live_hockey_audit.json','math_probe/live_hockey_audit.md',
            'math_probe/local_security_review.md','math_probe/runtime_review.md',
            'task2_independent_review.md','final_revision_01/unittest.log',
            'final_revision_02/targeted_unittest.log','final_revision_01/source_manifest.json',
            'final_revision_02/source_manifest.json']
    for name in direct:names.add(str((EVIDENCE/name).relative_to(ROOT)))
    for item in final['runs']:
        run=EVIDENCE/item['path']
        for name in ['run.json','controlled_expansion_report.json']:
            if (run/name).is_file():names.add(str((run/name).relative_to(ROOT)))
    transport=json.loads((TRANSPORT/'manifest.json').read_text())
    for name in transport['publication_files']:
        if Path(name).name!=name:raise RuntimeError('unsafe transport publication name')
        names.add(str((TRANSPORT/name).relative_to(ROOT)))
    names.add(str((OUT/'local_audit.json').relative_to(ROOT)))
    names.add(str((OUT/'local_audit.md').relative_to(ROOT)))
    names.add(str(Path(__file__).relative_to(ROOT)))
    return names

def prepare():
    if (OUT/'created_commit.json').exists():raise RuntimeError('commit already created')
    remote=read('remote_inspection.json')
    if remote['branch_protected']:raise RuntimeError('protected main needs a branch/PR publication')
    manifest,changed=frozen_check()
    audit=read('local_audit.json')
    if audit.get('passed') is not True:raise RuntimeError('local publication audit incomplete')
    if not (TRANSPORT/'manifest.json').is_file():raise RuntimeError('curated transport not prepared')
    transport=json.loads((TRANSPORT/'verification.json').read_text())
    scan_report=json.loads((TRANSPORT/'sensitive_scan.json').read_text())
    if (transport.get('status')!='passed' or not transport.get('per_member_sha256_and_size_match')
            or not transport.get('second_build_byte_identical') or transport.get('unresolved_internal_artifact_references')!=0
            or scan_report.get('status')!='passed' or scan_report.get('findings')):
        raise RuntimeError('archive safety/roundtrip audit incomplete')
    for line in (TRANSPORT/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split(maxsplit=1)
        name=name.lstrip('*')
        if Path(name).name!=name or sha((TRANSPORT/name).read_bytes())!=expected:
            raise RuntimeError('transport checksum differs')
    if sha((TRANSPORT/transport['archive']).read_bytes())!=transport['archive_sha256']:
        raise RuntimeError('archive differs from verified extraction')
    names=select_names(manifest,changed)
    scan=secret_scan(names)
    updates=[];unchanged=[]
    for name in sorted(names):
        data=safe_path(name).read_bytes();old=remote['files'].get(name)
        item={'path':name,'sha256':sha(data),'bytes':len(data),'git_blob_sha':blob(data)}
        if old and (old['type']!='blob' or old['mode']!='100644'):
            raise RuntimeError('unexpected remote kind: '+name)
        if old and old['sha']==item['git_blob_sha']:
            unchanged.append(item);continue
        item['baseline_path']=baseline_for(name,old['sha']) if old else None
        item['baseline_blob_sha']=old['sha'] if old else None
        item['binary']=name.endswith(('.tar.gz','.xz'))
        if not item['binary']:data.decode('utf-8')
        target=OUT/'staging'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        updates.append(item)
    available=set(remote['files'])|names;checked_links=[]
    for name in ['agent_v2/README.md','agent_v2/AUTONOMOUS.md','agent_v2/AUTONOMOUS_VALIDATION.md',
                 'agent_v2/PUBLISHING.md',str((TRANSPORT/'README.md').relative_to(ROOT))]:
        for target in re.findall(r'\]\(([^)]+)\)',(ROOT/name).read_text()):
            if '://' in target or target.startswith('#'):continue
            destination=posixpath.normpath(posixpath.join(posixpath.dirname(name),target.split('#')[0]))
            if destination not in available:raise RuntimeError('unpublished documentation target: '+name+' -> '+target)
            checked_links.append({'source':name,'target':destination})
    save('upload_manifest.json',{'schema_version':1,'remote_head':remote['head'],'branch':'main',
        'files':updates,'unchanged_required_files':unchanged,'runtime_files_verified':len(manifest['files']),
        'credential_scan':scan,'documentation_links':checked_links,'deletions':[],
        'scope':'Autonomous Agent v2 source, tests, docs, selected results and audited text evidence archive'})
    print(json.dumps({'prepared':True,'changed_files':len(updates),'required_unchanged':len(unchanged),
        'changed_bytes':sum(x['bytes'] for x in updates),'doc_links':len(checked_links)}),flush=True)

def staged_check():
    frozen_check();manifest=read('upload_manifest.json')
    for item in manifest['files']+manifest['unchanged_required_files']:
        data=safe_path(item['path']).read_bytes()
        if sha(data)!=item['sha256'] or blob(data)!=item['git_blob_sha']:
            raise RuntimeError('publication source changed: '+item['path'])
        if item in manifest['files'] and data!=(OUT/'staging'/item['path']).read_bytes():
            raise RuntimeError('staged bytes differ: '+item['path'])
    return manifest

def check_tree(actual,before,manifest):
    changed={x['path']:x for x in manifest['files']}
    if set(actual)!=set(before['files'])|set(changed):raise RuntimeError('remote file set differs')
    for name,item in changed.items():
        row=actual[name]
        if row['sha']!=item['git_blob_sha'] or row['mode']!='100644' or row['type']!='blob':
            raise RuntimeError('uploaded content differs: '+name)
    for name,old in before['files'].items():
        if name not in changed and any(actual[name][k]!=old[k] for k in ('sha','mode','type')):
            raise RuntimeError('unrelated remote content changed: '+name)
    for item in manifest['unchanged_required_files']:
        if actual[item['path']]['sha']!=item['git_blob_sha']:
            raise RuntimeError('required dependency mismatch: '+item['path'])

def upload():
    if (OUT/'created_commit.json').exists():raise RuntimeError('existing created commit; verify before retry')
    manifest=staged_check();before=read('remote_inspection.json')
    if api('git/ref/heads/main')['object']['sha']!=before['head']:
        raise RuntimeError('remote moved; no upload')
    branch=api('branches/main')
    if branch['protected'] or branch['commit']['sha']!=before['head']:raise RuntimeError('main changed')
    entries=[]
    progress=[]
    for item in manifest['files']:
        data=(OUT/'staging'/item['path']).read_bytes()
        entry={'path':item['path'],'mode':'100644','type':'blob'}
        if item['binary'] or len(data)>700000:
            print(json.dumps({'uploading_blob':item['path'],'bytes':len(data)}),flush=True)
            result=api('git/blobs',{'content':base64.b64encode(data).decode(),'encoding':'base64'})
            if result['sha']!=item['git_blob_sha']:raise RuntimeError('blob upload hash mismatch')
            entry['sha']=result['sha']
            progress.append({'event':'blob_uploaded','path':item['path'],'sha':result['sha']})
            save('upload_progress.json',progress)
            print(json.dumps(progress[-1]),flush=True)
        else:entry['content']=data.decode()
        entries.append(entry)
    current=before['tree'];batch=[];size=0
    for entry in entries+[None]:
        length=len(json.dumps(entry).encode()) if entry else 0
        if batch and (entry is None or size+length>1500000):
            result=api('git/trees',{'base_tree':current,'tree':batch});current=result['sha']
            print(json.dumps({'tree_entries_uploaded':len(batch)}),flush=True)
            batch=[];size=0
        if entry is not None:batch.append(entry);size+=length
    check_tree(tree(current),before,manifest)
    if api('git/ref/heads/main')['object']['sha']!=before['head']:raise RuntimeError('remote moved before commit')
    commit=api('git/commits',{'message':'Add autonomous residual proof loop with checked graph expansion\n\nConnect bounded live model proofs, Jev selection, typed local tasks, library lookup, exact Lean validation and resume. Preserve manual mode. Include two live Train successes, an unfinished multi-method case, controlled Graph-to-CAS validation, and audited text evidence.','tree':current,'parents':[before['head']]})
    save('created_commit.json',{'sha':commit['sha'],'tree':current,'parent':before['head']})
    result=api('git/refs/heads/main',{'sha':commit['sha'],'force':False},'PATCH');save('published_ref.json',result)
    print(json.dumps({'published':True,'branch':'main','commit':commit['sha'],
        'url':'https://github.com/HuangJiayi0409/q_dentity/commit/'+commit['sha']}),flush=True)

def verify():
    before=read('remote_inspection.json');created=read('created_commit.json');manifest=staged_check()
    if api('git/ref/heads/main')['object']['sha']!=created['sha']:raise RuntimeError('main differs from publication')
    commit=api('git/commits/'+created['sha'])
    if [p['sha'] for p in commit['parents']]!=[before['head']] or commit['tree']['sha']!=created['tree']:
        raise RuntimeError('commit ancestry differs')
    actual=tree(created['tree']);check_tree(actual,before,manifest)
    if api('git/ref/heads/main')['object']['sha']!=created['sha']:raise RuntimeError('main moved during verification')
    result={'passed':True,'branch':'main','commit':created['sha'],'parent':before['head'],
        'uploaded_blob_hashes_verified':len(manifest['files']),
        'required_unchanged_hashes_verified':len(manifest['unchanged_required_files']),
        'all_unrelated_remote_files_preserved':True,'runtime_files_verified':81,'remote_total_files':len(actual)}
    save('remote_verification.json',result);print(json.dumps(result),flush=True)

if __name__=='__main__':
    {'inspect':inspect_remote,'prepare':prepare,'upload':upload,'verify':verify}[sys.argv[1]]()
