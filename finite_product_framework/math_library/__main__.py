"""Query without Lean, or explicitly build the checked Lean library.

python -m finite_product_framework.math_library lookup poch --purpose length_shift
python -m finite_product_framework.math_library export
python -m finite_product_framework.math_library instantiate request.json
python -m finite_product_framework.math_library build --output /tmp/fqi-library-build
"""
import argparse
import json
from pathlib import Path

from .registry import Library
from .catalog import SCHEMA


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    query=sub.add_parser('lookup');query.add_argument('symbol');query.add_argument('--purpose')
    sub.add_parser('export')
    build=sub.add_parser('build');build.add_argument('--output',type=Path,required=True)
    instance=sub.add_parser('instantiate');instance.add_argument('request',type=Path)
    args=p.parse_args();lib=Library()
    if args.command=='lookup':result=lib.lookup(args.symbol,args.purpose)
    elif args.command=='export':result=dict(schema=SCHEMA,objects=lib.objects,rules=list(lib.rules.values()),sha256=lib.sha256)
    elif args.command=='build':
        from .build import prepare
        result=prepare(args.output)
    else:
        if args.request.stat().st_size>1024*1024:raise ValueError('request_size_limit')
        req=json.loads(args.request.read_text())
        result=lib.instantiate(req['rule'],req['bindings'],facts=req.get('facts',[]))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
