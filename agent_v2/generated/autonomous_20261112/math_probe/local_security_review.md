# Independent generated-local-proof boundary review

Read-only review of local_tasks.py, local_proof_checker.py, LocalProofCheck.lean
and their owning source/receipt/rendering helpers. No production file was edited
by this review. No network or model call was made; neither Train theorem was
proved or submitted as a generated-model result.

## Concrete issue found, and independently rechecked after root's repair

The Lean syntax allowlist initially used a few names that differed from the
actual pinned toolchain parser kinds. Standard rfl was tacticRfl, `%` used
«term_%_», if-then-else used termIfThenElse, and unary negation used «term-_».
This rejected the alternating-Gaussian original proposition before a generated
proof could be checked. Root updated the allowlist and added its own regression.
The final independent driver probe now accepts natural-modulo reflexivity,
if-expression reflexivity and generic field ring commutativity. Both chosen
Train original propositions pass the syntax boundary and reach ordinary
unproved-goal checking. Their deliberately inadequate assumption proofs fail;
no original proof is supplied here.

## Fresh verification evidence

```text
python3 -B agent_v2/generated/autonomous_20261112/math_probe/local_boundary_probe.py
python3 -B -m unittest agent_v2.tests.test_local_tasks -v
```

The driver probe made eleven bounded, single-thread Lean compilations against
the copied fixed mathematical foundations and current trusted driver. Each
file embeds the actual driver used, so the evidence does not depend on a future
version of the production driver. `local_boundary/results.json` records all
commands, exit statuses and errors; adjacent files retain complete output.
The four LocalTask tests passed, exit 0.

| Independent sample | Actual result |
|---|---|
| Closed True proof | exit 0, audited |
| Generic field ring commutativity | exit 0, audited |
| Natural-modulo reflexivity | exit 0, audited |
| If-expression reflexivity | exit 0, audited |
| Valid term followed by an axiom command | rejected: expected end of input |
| True proof audited against False | rejected: exact target type differs |
| Added False premise | rejected: exact target type differs |
| Extra q≠0 assumption over the same universal field | rejected: exact target type differs |
| Direct sorryAx application proving False | rejected: unapproved axiom sorryAx |
| Hockey-stick original type with intentionally inadequate proof | proposition parsed; ordinary open-goal failure and axiom rejection |
| Alternating-Gaussian original type with intentionally inadequate proof | proposition parsed; ordinary open-goal failure and axiom rejection |

The q≠0 negative uses a direct Eq.refl term, so its rejection comes from the
actual extra premise, not a tactic-allowlist error. The direct sorryAx negative
also matters: merely omitting the literal word `sorry` is insufficient; the
Lean axiom audit independently rejects the direct constant application.

## Source, target and dependency reasoning

- The model proposal boundary supplies propositions and proof text only. Task
  creation takes the complete Source and current parent from validated state.
  A changed Source, target type, theorem name or dependency set cannot match the
  registered task/candidate contract. LocalTask content hashes include Source,
  parent, children, representation and exact dependency bindings.
- An independent lemma that changes the original assumptions remains an
  independent theorem in C. It changes O only if its checked proposition is the
  exact children -> actual parent connection. Final acceptance reconstructs
  that proof tree and recompiles the unchanged original declaration.
- Each untrusted proposition/proof string is parsed as one complete term.
  Generated declarations additionally traverse the restricted syntax tree.
  Candidate text cannot append a command, choose imports, or mutate the trusted
  expected declaration. Trusted CAS/assembled terms still receive complete-term
  parsing and the final kernel/axiom audit.
- The expected target is reconstructed independently from the registered task
  or frozen original Source. Lean checks that both sides are closed Prop values,
  matches universe arity, instantiates level-parameter names, and requires
  definitional equality. Logical equivalence or an extra assumption is not
  enough; the negative samples exercise that distinction.
- Dependency bindings include certificate identity, proposition, proof body,
  original source hash and dependency identifiers. Refreshed receipts may change
  without silently changing a theorem's mathematical identity. Before reuse,
  production receipt validation checks the retained transaction, file hashes,
  profile/environment and predecessor bindings. Rendering re-elaborates the
  actual dependency proof terms under stable hashed aliases; resume freshly
  rechecks all C in topological order. A missing task registry entry cannot
  convert an arbitrary old generated proof into a trusted CAS template.
- The original renderer replaces only the unique parsed proof placeholder and
  removes source import commands while retaining the exact original declaration
  body. Its compiled environment supplies fixed foundations and general rules,
  not benchmark statement/proof cache modules. Final acceptance checks actual
  original type and allowed axioms again.

No additional concrete soundness bypass was found in these reviewed paths and
bounded samples. This is scoped evidence, not an exhaustive security proof or a
claim of a completed live Train solution.
