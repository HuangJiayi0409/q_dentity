"""Reproduce the optional project-local PARI/GP build (no system installation)."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import urllib.request

VERSION='2.19.0'
URL='https://pari.math.u-bordeaux.fr/pub/pari/unix/pari-'+VERSION+'.tar.gz'
SHA256='f317b9722eb5d9094a60303774f066f3a83e3ec1f170be8546c44d7583f30b6d'
ROOT=Path(__file__).resolve().parent.parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,help='already downloaded, checksum-verified source archive')
    parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args()
    if args.jobs<1:parser.error('jobs must be positive')
    target=ROOT/'.tools';target.mkdir(exist_ok=True)
    archive=args.archive or target/('pari-'+VERSION+'.tar.gz')
    if args.archive is None and not archive.exists():
        with urllib.request.urlopen(URL,timeout=60) as response:archive.write_bytes(response.read())
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=SHA256:raise ValueError('official PARI source checksum mismatch')
    source=target/('pari-'+VERSION)
    if not source.exists():
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                if member.name.startswith('/') or '..' in Path(member.name).parts or member.issym() or member.islnk():
                    raise ValueError('unsafe source archive member')
            tar.extractall(target)
    prefix=target/'pari'
    with (target/'pari_build.log').open('w') as log:
        for command in (['./Configure','--prefix='+str(prefix),'--without-readline'],
                        ['make','-j'+str(args.jobs),'gp'],['make','install-bin']):
            subprocess.run(command,cwd=source,stdout=log,stderr=subprocess.STDOUT,check=True)
    info=dict(name='PARI/GP',version=VERSION,source=URL,source_sha256=SHA256,
              binary_sha256=hashlib.sha256((prefix/'bin/gp').read_bytes()).hexdigest(),
              license='GPL-2.0-or-later; see downloaded source COPYING',prefix=str(prefix))
    (target/'pari_build.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info,indent=2))


if __name__=='__main__':main()
