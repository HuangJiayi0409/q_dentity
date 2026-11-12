"""One fixed pure weighted-choice constructor in a supervised process."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
from .models import digest
from .storage import sha256_file

ROOT=Path(__file__).resolve().parents[1]
CORE=ROOT/'finite_product_framework/combinatorial/choice_construct.py'


def core_inventory():
    return {str(path.relative_to(ROOT)):sha256_file(path)
            for path in (Path(__file__).resolve(),CORE)}


def load_core():
    spec=importlib.util.spec_from_file_location('agent_v2_pure_combinatorial_indices',CORE)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve()!=CORE.resolve():raise ValueError('pure combinatorial constructor path differs')
    return module


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();request=json.loads(Path(args.input).read_text())
    core=load_core();core.validate_request(request)
    raw={'schema_version':1,'method':'combinatorial','request_sha256':digest(request),
         'original_identity_proved':False,'python_version':sys.version.split()[0],
         'source_before':core_inventory()}
    try:
        construction=core.construct(request['input'])
        raw.update(status=construction['status'],construction=construction)
    except ValueError as error:
        status='budget_exhausted' if 'budget' in str(error) or 'resource' in str(error) else 'search_exhausted'
        raw.update(status=status,construction={'status':status,'reason':str(error)})
    except Exception as error:
        raw.update(status='environment_blocked',error={'type':type(error).__name__,'message':str(error)})
    raw['source_after']=core_inventory()
    Path(args.output).write_text(json.dumps(raw,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    return 1 if raw['status']=='environment_blocked' else 0


if __name__=='__main__':raise SystemExit(main())
