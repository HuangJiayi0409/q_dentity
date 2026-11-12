"""Bounded lookup of a fixed, pure mathematical declaration allowlist.

Types are printed by the installed Lean environment, not reconstructed from
text or invented by a model. Only these mathematical modules are imported;
there is no recursive repository search, benchmark Test or old proof access.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

_BASIC = 'Mathlib/Algebra/BigOperators/Group/Finset/Basic.lean'
_INTERVALS = 'Mathlib/Algebra/BigOperators/Intervals.lean'
_ALLOWLIST = {
    **{name: ('foundation', 'Init/Prelude.lean') for name in
       ('True.intro', 'And.intro', 'And.left', 'And.right', 'Iff.intro', 'Eq.refl', 'Eq.trans', 'Eq.symm')},
    **{name: ('foundation', 'Init/Data/Nat/Basic.lean') for name in
       ('Nat.add_comm', 'Nat.add_assoc', 'Nat.mul_comm', 'Nat.mul_assoc')},
    **{f'Finset.{op}_range_{suffix}': ('mathlib', _BASIC)
       for op in ('sum', 'prod') for suffix in ('succ', 'add')},
    **{f'Finset.{op}_Ico_eq_{op}_range': ('mathlib', _INTERVALS) for op in ('sum', 'prod')},
    **{name: ('mathlib', _BASIC) for name in ('Finset.sum_range_sub', "Finset.sum_range_sub'", 'Finset.sum_congr')},
    **{name: ('mathlib', 'Mathlib/Data/Nat/Init.lean') for name in ('Nat.twoStepInduction', 'Nat.strong_induction_on')},
    **{name: ('mathlib', 'Mathlib/Algebra/Group/Monoid.lean') for name in ('pow_add', 'pow_mul')},
    **{name: ('retained_foundation', 'finite_product_framework/p1/lean/GaussianRules.lean') for name in
       ('FiniteQP1.gaussian_pascal', 'FiniteQP1.gaussian_adjacent')},
    **{name: ('retained_foundation', 'benchmark/lean/Benchmark/Gaussian.lean') for name in
       ('FiniteQBenchmark.gaussian_above', 'FiniteQBenchmark.gaussian_zero_right')},
    'FiniteQBenchmark.poch_succ': ('retained_foundation', 'benchmark/lean/Benchmark/Auxiliary.lean'),
}


_FOUNDATIONS = (
    ('Definitions', 'benchmark/lean/Benchmark/Definitions.lean'),
    ('Auxiliary', 'benchmark/lean/Benchmark/Auxiliary.lean'),
    ('Gaussian', 'benchmark/lean/Benchmark/Gaussian.lean'),
    ('GaussianRules', 'finite_product_framework/p1/lean/GaussianRules.lean'),
)


class LibraryUnavailable(RuntimeError):
    pass


class LocalLibrary:
    def __init__(self, root=None, *, seconds=30.0, lean_binary=None):
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        if type(seconds) not in (int, float) or not math.isfinite(seconds) or not 0 < seconds <= 120:
            raise ValueError('invalid_library_timeout')
        self.seconds = seconds
        toolchain = (self.root/'project/lean-toolchain').read_text().strip()
        if not re.fullmatch(r'[A-Za-z0-9_./:-]+', toolchain):
            raise LibraryUnavailable('invalid_toolchain')
        self.lean = Path(lean_binary or Path.home()/'.elan/toolchains'/toolchain.replace('/', '--').replace(':', '---')/'bin/lean').resolve()
        self._records = None

    def lookup(self, name):
        if not isinstance(name, str) or name not in _ALLOWLIST:
            return None
        return deepcopy(self._load()[name])

    def query(self, text='', *, limit=12):
        if type(limit) is not int or not 1 <= limit <= 32 or not isinstance(text, str) or len(text) > 1000:
            raise ValueError('invalid_library_query')
        terms = text.lower().split()
        records = self._load()
        # Stable names make repeated lookup reproducible. This is exact text
        # filtering, not a claim of semantic retrieval or mathematical fit.
        return [deepcopy(record) for name, record in sorted(records.items())
                if all(term in (name+' '+record['type']).lower() for term in terms)][:limit]

    def _load(self):
        if self._records is not None:
            return self._records
        project = self.root/'project'
        deadline = time.monotonic()+self.seconds
        try:
            manifest = json.loads((project/'lake-manifest.json').read_text())
            if manifest.get('packagesDir') != '.lake/packages':
                raise LibraryUnavailable('unsupported_package_layout')
            directories = []
            for package in manifest['packages']:
                name = package['name']
                if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
                    raise LibraryUnavailable('invalid_package_name')
                directory = project/'.lake/packages'/name/'.lake/build/lib/lean'
                if name == 'mathlib' and not directory.is_dir():
                    raise LibraryUnavailable('package_unavailable')
                directories.append(str(directory.resolve()))
            script = ('import Benchmark.GaussianRules\nimport Mathlib.Algebra.BigOperators.Intervals\nimport Mathlib.Data.Nat.Init\n'
                      'set_option pp.universes true\n' +
                      '\n'.join('#check @'+name for name in _ALLOWLIST)+'\n')
            with tempfile.TemporaryDirectory(prefix='agent-v2-library-') as directory:
                temp = Path(directory); src = temp/'sources'; obj = temp/'objects'
                (src/'Benchmark').mkdir(parents=True); (obj/'Benchmark').mkdir(parents=True)
                environment = dict(os.environ, LEAN_PATH=os.pathsep.join([str(obj), *directories]))
                def compile_file(file, output=None):
                    remaining = deadline-time.monotonic()
                    if remaining <= 0:
                        raise LibraryUnavailable('library_timeout')
                    command = [str(self.lean), '-j', '1', '--json', '-R', str(src)]
                    if output is not None:
                        command += ['-o', str(output)]
                    command.append(str(file))
                    result = subprocess.run(command, cwd=src, env=environment,
                        capture_output=True, text=True, timeout=remaining)
                    if result.returncode:
                        raise LibraryUnavailable('library_lean_failed')
                    return result
                for module, relative in _FOUNDATIONS:
                    source = (self.root/relative).read_bytes()
                    # These exact four pure source modules are the only local
                    # imports. A future source drift cannot import Test/Train.
                    imports = re.findall(r'^import ([^\n]+)', source.decode(), re.M)
                    for names in imports:
                        for name in names.split():
                            if not (name.startswith('Mathlib.') or name in
                                    {'Benchmark.'+m for m, _ in _FOUNDATIONS}):
                                raise LibraryUnavailable('unapproved_foundation_import')
                    file = src/'Benchmark'/(module+'.lean'); file.write_bytes(source)
                    compile_file(file, obj/'Benchmark'/(module+'.olean'))
                file = src/'Lookup.lean'; file.write_text(script)
                run = compile_file(file)
            if run.returncode:
                raise LibraryUnavailable('library_lean_failed')
            records = {}
            for line in run.stdout.splitlines():
                message = json.loads(line)
                if message.get('severity') != 'information':
                    continue
                printed = message.get('data', '')
                for name, (kind, relative) in _ALLOWLIST.items():
                    # pp.universes adds .{u,...} after polymorphic constants.
                    match = re.match(r'@?'+re.escape(name)+r'(?:\.\{[^}]*\})?\s*:\s*([\s\S]+)', printed)
                    if match:
                        origin = (self.lean.parent.parent/'src/lean'/relative if kind == 'foundation' else
                                  self.root/relative if kind == 'retained_foundation' else
                                  project/'.lake/packages/mathlib'/relative)
                        records[name] = {'name': name, 'type': match.group(1),
                            'provenance': {'kind': kind, 'path': str(origin.resolve()),
                                           'sha256': hashlib.sha256(origin.read_bytes()).hexdigest()},
                            'type_source': 'installed_lean_check',
                            'lean_binary': str(self.lean)}
            if set(records) != set(_ALLOWLIST):
                raise LibraryUnavailable('incomplete_library_types')
            self._records = records
            return self._records
        except LibraryUnavailable:
            raise
        except subprocess.TimeoutExpired:
            raise LibraryUnavailable('library_timeout') from None
        except (OSError, ValueError, TypeError, KeyError):
            raise LibraryUnavailable('library_environment_unavailable') from None
