"""Focused integration regressions; synthetic goals only, never Test data."""
import argparse
import copy
import json
import os
from pathlib import Path
import subprocess

from .pipeline import payload, read_messages, write_json
from .source import REPO, probe_text
from .wire import pack


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepared',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    base=args.prepared.resolve(); out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    toolchain=(base/'lean-toolchain').read_text().strip().replace('/','--').replace(':','---')
    exe=Path.home()/'.elan/toolchains'/toolchain/'bin/lean'
    env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,[base/'build',*sorted((REPO/'project/.lake/packages').glob('*/.lake/build/lib/lean'))])))
    results=[]

    def compile(name,text):
        file=out/(name+'.lean');file.write_text(text)
        log=out/(name+'.jsonl')
        with log.open('w') as stream:
            result=subprocess.run([str(exe),'--json','-DmaxRecDepth=8192','-DmaxHeartbeats=2000000',str(file)],
                                  cwd=out,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=60)
        return result.returncode,read_messages(log)

    header='import Benchmark.Batch5Definitions\nimport FiniteQPreprocess.Export\nopen scoped BigOperators\nnamespace ConnectionSynthetic\n'
    def source(statement):
        return header+'theorem statement '+statement+' := by\n  sorry\nend ConnectionSynthetic\n'

    cases={
      'concrete_list_length': '(a b c : ℚ) : ([a,b,c].map (fun x => x+1)).length = 3',
      'closed_interval': '(f : ℕ → ℚ) (a b : ℕ) : (∑ k ∈ Finset.Icc a b, f k) = ∑ j ∈ Finset.range (b+1-a), f (a+j)',
      'empty_closed_interval': '(f : ℕ → ℚ) : (∑ k ∈ Finset.Icc 3 1, f k) = ∑ j ∈ Finset.range (1+1-3), f (3+j)',
      'definition_unfold': '(as bs cs ds : List ℚ) (p q z : ℚ) (n : ℕ) : FiniteQBenchmark.bibasicPhi as bs cs ds p q z n = ∑ k ∈ Finset.range (n+1), FiniteQBenchmark.phiTerm as bs p z k * FiniteQBenchmark.multibaseTerm q cs ds k',
      'interval': '(f : ℕ → ℚ) (a b : ℕ) : (∑ k ∈ Finset.Ico a b, f k) + 0 = ∑ j ∈ Finset.range (b-a), f (a+j)',
      'division_with_hypothesis': '(q : ℚ) (h : q ≠ 0) : q / q = 1',
      'division_without_hypothesis': '(q : ℚ) : q / q = 1',
      'reversed_interval': '(f : ℕ → ℚ) : (∑ k ∈ Finset.Ico 3 1, f k) = ∑ j ∈ Finset.range (1-3), f (3+j)',
    }
    bundles={}
    for name,statement in cases.items():
        original=source(statement)
        code,messages=compile(name+'_export',probe_text(original,'preprocess_export_expanded' if name in ('definition_unfold','closed_interval','empty_closed_interval') else 'preprocess_export'))
        bundle=payload(messages,'PREPROCESS_JSON:','PREPROCESS_EXPORT_ONLY',code)
        assert all(row['original_name']!='statement' for row in bundle['context'])
        path=out/(name+'.json');write_json(path,pack(bundle));bundles[name]=bundle
        code,messages=compile(name+'_replay',probe_text(original,'preprocess_replay '+json.dumps(str(path))))
        payload(messages,'PREPROCESS_REPLAY_JSON:','PREPROCESS_REPLAY_ONLY',code)
        code,messages=compile(name+'_enter',probe_text(original,'preprocess_enter '+json.dumps(str(path))+'\n  first | rfl | trivial'))
        expected=name!='division_without_hypothesis'
        assert (code==0)==expected,(name,code,messages)
        rules=[e['rule'] for e in bundle['transformations']]
        if name=='definition_unfold':assert 'FiniteQBenchmark.bibasicPhi' in rules
        if name=='interval':assert 'FiniteQPreprocess.nat_Ico_sum' in rules
        if name=='division_without_hypothesis':assert 'div_self' not in rules
        if name=='division_with_hypothesis':assert 'div_self' in rules
        results.append(dict(case=name,passed=True,transformations=len(rules),original_proved=code==0))

    original=source(cases['interval']); original_bundle=bundles['interval']
    for name in ('normalized','proof','context','declarations','signatures','relations'):
        changed=copy.deepcopy(original_bundle)
        if name=='normalized':changed['normalized_closed']=changed['original_closed']
        elif name=='proof':changed['bridge_proof']={'tag':'nat','value':0}
        elif name=='context':changed['context']=[]
        elif name=='declarations':changed['declarations']=[{'tampered':True}]
        else:changed[name]=[{'tampered':True}]
        path=out/('tampered_'+name+'.json');write_json(path,pack(changed))
        code,messages=compile('tampered_'+name,probe_text(original,'preprocess_enter '+json.dumps(str(path))+'\n  trivial'))
        assert code!=0,(name,messages)
        results.append(dict(case='tampered_'+name,passed=True,rejected=True))
    changed=original.replace('(a b : ℕ)', '(a b : ℕ) (injected : False)')
    code,messages=compile('changed_assumptions',probe_text(changed,'preprocess_enter '+json.dumps(str(out/'interval.json'))+'\n  trivial'))
    assert code!=0,messages
    results.append(dict(case='changed_assumptions',passed=True,rejected=True))
    write_json(out/'validation.json',dict(status='passed',cases=results,test_files_read=0))
    print(json.dumps(dict(status='passed',cases=len(results),output=str(out))))


if __name__=='__main__':main()
