"""Load the current Train statement without historical method/family admission lists."""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[2]
IMPORT = re.compile(r"^import\s+([A-Za-z0-9_.]+)\s*$", re.M)


def imports(masked: str):
    """Fail closed on import syntax outside the reviewed statement format."""
    result = []
    for line in masked.splitlines():
        if re.match(r'\s*(?:public\s+|private\s+)?import\b', line):
            match = IMPORT.fullmatch(line)
            if match is None:
                raise ValueError('unsupported_import_syntax: ' + line.strip())
            result.append(match.group(1))
    return result


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def uncomment(text: str) -> str:
    """Mask nested Lean comments, keeping offsets/newlines for declaration matching."""
    out, i, depth, quoted = list(text), 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                out[i:i+2] = "  "; depth += 1; i += 2; continue
            if text.startswith("-/", i):
                out[i:i+2] = "  "; depth -= 1; i += 2; continue
            if text[i] != "\n": out[i] = " "
        elif quoted:
            if text[i] == "\\": i += 2; continue
            if text[i] == '"': quoted = False
        elif text.startswith("/-", i):
            out[i:i+2] = "  "; depth = 1; i += 2; continue
        elif text.startswith("--", i):
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out[i:end] = " " * (end-i); i = end; continue
        elif text[i] == '"': quoted = True
        i += 1
    if depth or quoted:
        raise ValueError("source_syntax: unterminated comment or string")
    return "".join(out)


@dataclass(frozen=True)
class Source:
    identity: str
    path: Path
    text: str
    sha256: str
    train_sha256: str
    dependencies: tuple
    theorem: str
    support_modules: tuple = ()

    def evidence(self):
        return dict(identity=self.identity, path=str(self.path.relative_to(REPO)),
                    sha256=self.sha256, train_sha256=self.train_sha256,
                    theorem=self.theorem, dependencies=list(self.dependencies),
                    support_modules=list(self.support_modules),
                    permission="current_train_only", family_gate=False)


def probe_text(text: str, tactic: str) -> str:
    """Preserve the target/context; never import or accept the deferred target proof."""
    masked = uncomment(text)
    matches = list(re.finditer(r"(?m)^  sorry\s*$", masked))
    if len(matches) != 1 or len(re.findall(r"\bsorry\b", masked)) != 1:
        raise ValueError("source_shape: expected exactly one deferred proof")
    if len(re.findall(r"(?m)^theorem\s+", masked)) != 1:
        raise ValueError("source_shape: expected exactly one theorem")
    declarations = re.findall(r"(?m)^(?:axiom|def|opaque|unsafe|example|instance|abbrev)\b", masked)
    if declarations:
        raise ValueError("source_shape: extra local declarations need explicit review")
    m = matches[0]
    return "import FiniteQPreprocess.Export\n" + text[:m.start()] + "  " + tactic + "\n" + text[m.end():]


def load(identity: str, support_modules=()) -> Source:
    manifest = REPO / "benchmark/splits/train.jsonl"
    raw = manifest.read_bytes()
    rows = [json.loads(line) for line in raw.decode().splitlines()]
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError("manifest_duplicate_identity")
    row = next((r for r in rows if r['id'] == identity), None)
    if row is None:
        raise ValueError("permission_denied: identity is not in current Train")
    path = (REPO / "benchmark" / row['lean_path']).resolve()
    if not path.is_relative_to((REPO / "benchmark/lean/Benchmark/Statements/Train").resolve()):
        raise ValueError("permission_denied: source outside Train")
    data = path.read_bytes()
    if digest(data) != row['lean_sha256']:
        raise ValueError("source_hash_mismatch")
    text = data.decode()
    probe_text(text, 'preprocess_export')  # Structural check only; no Lean execution.
    masked = uncomment(text)
    theorem = re.findall(r"(?m)^theorem\s+([\w.]+)", masked)[0]
    namespaces = re.findall(r"(?m)^namespace\s+([\w.]+)", masked)
    dependencies, seen, active = [], set(), set()

    def visit(module):
        if module in seen: return
        if module in active: raise ValueError("dependency_cycle: " + module)
        if not module.startswith("Benchmark."):
            if module == "Mathlib" or module.startswith("Mathlib.") or module == "Lean" or module.startswith("Lean."):
                return
            raise ValueError("dependency_not_allowed: " + module)
        if module in ('Benchmark.Train', 'Benchmark.Test') or module.startswith('Benchmark.Statements.'):
            raise ValueError("target_dependency_forbidden: " + module)
        active.add(module)
        dep = REPO / 'benchmark/lean' / (module.replace('.', '/') + '.lean')
        content = dep.read_bytes()
        clean = uncomment(content.decode())
        if re.search(r'\b(sorry|sorryAx|axiom|admit)\b', clean):
            raise ValueError("untrusted_dependency: " + module)
        for child in imports(clean): visit(child)
        dependencies.append(dict(module=module, path=str(dep.relative_to(REPO)), sha256=digest(content)))
        seen.add(module); active.remove(module)

    for module in imports(masked): visit(module)
    # Small generic normalization lemmas need the finite q definitions too.
    visit('Benchmark.Definitions')
    for module in support_modules:
        visit(module)
    return Source(identity, path, text, digest(data), digest(raw), tuple(dependencies),
                  '.'.join(namespaces + [theorem]), tuple(support_modules))
