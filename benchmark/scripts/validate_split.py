#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

if __name__ == '__main__':
    subprocess.run([sys.executable, str(Path(__file__).with_name('build_split.py')), '--check'], check=True)
