# Defined-sequence recurrence exit

This is an extension of the existing recurrence pipeline's `ore_closure` entry,
not a thirteenth method or a stored identity proof. Implementation:
`defined_relation.py`, selected by expression structure in `ore_pipeline.py`.

## Executable mechanism

1. Read a complete equality involving one supported defined sequence and fixed
   integer index shifts; preserve the original theorem and its hypotheses.
2. Export the actual `rogersSzego` finite-sum definition through Lean, in a
   separate extraction context. Do not apply the original theorem's preprocessing
   bridge to this auxiliary, different declaration.
3. Call the existing q-Zeilberger symbolic constructor on this definition only.
   The statement being proved is **not** a search input. The output is an
   order-two monic recurrence and a rational telescoping certificate.
4. Independently reconstruct the local certificate, finite support and boundary
   proof using the native recurrence-only emitter. Check symbolically that the
   proposed target is a scalar multiple of that computed recurrence.
5. Prove the necessary natural-index reindexing from the original hypotheses,
   then close the unchanged original statement with a checked linear combination.
   The shared workflow performs the original-proof dependency audit.

## Supported input and obligations

Currently one `rogersSzego` sequence with common variable parameters, a single
natural index, fixed index offsets and a homogeneous linear relation. The target
must lie in the computed three-term window after a nonnegative reindexing. Nat
subtraction is never silently interpreted as unrestricted integer subtraction:
the final Lean `omega` obligation must establish the selected offset.

The symbolic search supports the existing q-Zeilberger domain, but this new exit
accepts only its supported monic order-two certificate and polynomial scalar
multiple. Both the coefficient comparison and the local-certificate verifier
reject tampering. There is no ID/name-to-proof dispatch.

CAS work uses existing exact SymPy/q-Gosper infrastructure. Lean reconstruction
checks the generic Gaussian local relation, summation boundary and original
statement. This path does not appeal to an existing Rogers–Szegő recurrence
identity or a historical `Batch*Proofs` theorem.

## Evidence and remaining gaps

`../generated/preprocessing_v3_recovery_20261019/` records original Train runs,
cache/request provenance and the new successful `FQI-ROGERS-SZEGO-RECURRENCE`.
`test_defined_relation.py` exercises wrong targets, altered certificates and
coefficients, variable renaming, scalar multiplication and a missing reindexing
hypothesis. The latter is an explicit rejection of the current exit's domain,
not a claim that the weakened mathematical statement is false.

Before the parameter extension below, `FQI-ROGERS-SZEGO-SQRT` and
`FQI-SRC-FINE-20.64b` were unsupported by this exit:
they require parameter substitutions/shifts rather than one common variable
parameter pair. General closed-form target verification, nonlinear observables,
higher-order reconstruction and arbitrary defined-sequence discovery are not
implemented here. Existing separate Ore closure functionality remains intact.

## Parameter specialization and parameter-instance closure (2026-10-19)

The restriction above describes the original linear-recurrence exit. The existing
`ore_closure` entry now additionally dispatches by expression structure to
`parameter_relation.py`:

- **Closed form:** one unshifted Rogers–Szegő object and one Pochhammer target,
  with parameters independent of the natural sequence index. Export a generic
  definition with fresh independent parameters, construct its monic order-two
  recurrence, and reconstruct the universal polynomial certificate in Lean.
  Instantiate the verified theorem at the actual parameter expressions. Strong
  induction checks both initial values and the actual target's recurrence using
  Pochhammer successor and power/ring normalization. A parameter substitution
  never substitutes into an unchecked rational certificate or assumes a nonzero
  base. The target is not used for recurrence search.
- **Parameter relations:** two to four parameter instances sharing one variable
  base, homogeneous linear combinations of the two-entry sequence states after
  a fixed reindexing. Build a block-diagonal companion system from the computed
  generic recurrence, then use exact Ore row elimination to construct an
  annihilator of the target observable. The observable participates in this
  closure calculation; the definition recurrence is still target-independent.
  Reconstruct an exact polynomial linear combination of shifted base recurrences.
  Lean verifies these combinations, the observable's initial values, induction,
  and the original natural subtraction/reindexing hypotheses.

Both paths use the same existing recurrence method. No identity-ID dispatch,
preproved Rogers–Szegő identity, classifier or additional preprocessing rule is
introduced. Existing single-parameter linear relations and the separate older
nonlinear Ore exit retain their routes.

### Explicit limits

The generic definition reconstruction still supports only the current monic
order-two Gaussian/geometric certificate. Only Rogers–Szegő is recognized as a
named sequence. Closed-form normalization is limited to the specified
Pochhammer target and the implemented polynomial/power simplifier; admitting a
shape does not guarantee success. Parameter closure currently accepts order
one through four with **polynomial** coefficients and reconstruction multipliers;
rational expressions requiring nonzero side conditions are rejected. It does
not implement arbitrary parameter-shift telescoping or general holonomic
conversion. All initial values and original hypotheses remain Lean obligations.

Focused evidence is recorded in `../generated/recurrence_parameters_20261019/`.
The runtime and adversarial checks must finish before its report claims success;
this extension alone does not determine the full Train proof rate.
