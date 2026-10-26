import Lean
import Lean.Util.CollectAxioms
import Lean.Util.CollectLevelParams
import FiniteQPreprocess.Rules
import FiniteQPreprocess.Wire

open Lean Meta Elab Tactic
namespace FiniteQPreprocess

private def obj (tag : String) (xs : List (String × Json) := []) : Json :=
  Json.mkObj (("tag", toJson tag) :: xs)

private partial def encName : Name → Json
  | .anonymous => obj "anonymous"
  | .str p s => obj "str" [("prefix", encName p), ("value", toJson s)]
  | .num p n => obj "num" [("prefix", encName p), ("value", toJson n)]

private partial def encLevel : Level → MetaM Json
  | .zero => pure (obj "zero")
  | .succ u => return obj "succ" [("of", ← encLevel u)]
  | .max u v => return obj "max" [("left", ← encLevel u), ("right", ← encLevel v)]
  | .imax u v => return obj "imax" [("left", ← encLevel u), ("right", ← encLevel v)]
  | .param n => pure (obj "param" [("name", encName n)])
  | .mvar _ => throwError "PREPROCESS_UNRESOLVED_UNIVERSE"

private def encBinder : BinderInfo → String
  | .default => "explicit"
  | .implicit => "implicit"
  | .strictImplicit => "strict_implicit"
  | .instImplicit => "instance"

/-- Closed kernel syntax: all arguments and universe levels are retained. -/
private partial def encode (e : Expr) : MetaM Json := do
  match e with
  | .bvar i => return obj "bvar" [("index", toJson i)]
  | .fvar _ => throwError "PREPROCESS_UNCLOSED_VARIABLE"
  | .mvar _ => throwError "PREPROCESS_UNRESOLVED_METAVARIABLE"
  | .sort u => return obj "sort" [("level", ← encLevel u)]
  | .const n us => return obj "const" [("name", encName n), ("levels", toJson (← us.toArray.mapM encLevel))]
  | .app f a => return obj "app" [("fn", ← encode f), ("arg", ← encode a)]
  | .lam n t b bi => return obj "lam" [("display_name", toJson n.toString),
      ("type", ← encode t), ("body", ← encode b), ("binder_info", toJson (encBinder bi))]
  | .forallE n t b bi => return obj "forall" [("display_name", toJson n.toString),
      ("type", ← encode t), ("body", ← encode b), ("binder_info", toJson (encBinder bi))]
  | .letE n t v b nd => return obj "let" [("display_name", toJson n.toString),
      ("type", ← encode t), ("value", ← encode v), ("body", ← encode b), ("nondependent", toJson nd)]
  | .lit (.natVal n) => return obj "nat" [("value", toJson n)]
  | .lit (.strVal s) => return obj "string" [("value", toJson s)]
  | .mdata _ b => encode b
  | .proj n i b => return obj "proj" [("structure", encName n), ("index", toJson i), ("body", ← encode b)]

private def get (j : Json) (k : String) : MetaM Json :=
  match j.getObjVal? k with
  | .ok v => pure v
  | .error e => throwError "PREPROCESS_WIRE: {e}"
private def str (j : Json) : MetaM String :=
  match j.getStr? with
  | .ok v => pure v
  | .error e => throwError "PREPROCESS_WIRE: {e}"
private def nat (j : Json) : MetaM Nat :=
  match j.getNat? with
  | .ok v => pure v
  | .error e => throwError "PREPROCESS_WIRE: {e}"
private def arr (j : Json) : MetaM (Array Json) :=
  match j.getArr? with
  | .ok v => pure v
  | .error e => throwError "PREPROCESS_WIRE: {e}"

private partial def decName (j : Json) : MetaM Name := do
  match ← str (← get j "tag") with
  | "anonymous" => return .anonymous
  | "str" => return .str (← decName (← get j "prefix")) (← str (← get j "value"))
  | "num" => return .num (← decName (← get j "prefix")) (← nat (← get j "value"))
  | _ => throwError "PREPROCESS_WIRE_NAME"

private partial def decLevel (j : Json) : MetaM Level := do
  match ← str (← get j "tag") with
  | "zero" => return .zero
  | "succ" => return .succ (← decLevel (← get j "of"))
  | "max" => return .max (← decLevel (← get j "left")) (← decLevel (← get j "right"))
  | "imax" => return .imax (← decLevel (← get j "left")) (← decLevel (← get j "right"))
  | "param" => return .param (← decName (← get j "name"))
  | _ => throwError "PREPROCESS_WIRE_LEVEL"

private def decBinder (j : Json) : MetaM BinderInfo := do
  match ← str j with
  | "explicit" => return .default
  | "implicit" => return .implicit
  | "strict_implicit" => return .strictImplicit
  | "instance" => return .instImplicit
  | _ => throwError "PREPROCESS_WIRE_BINDER"

private partial def decode (j : Json) : MetaM Expr := do
  match ← str (← get j "tag") with
  | "bvar" => return .bvar (← nat (← get j "index"))
  | "sort" => return .sort (← decLevel (← get j "level"))
  | "const" => return .const (← decName (← get j "name")) (← (← arr (← get j "levels")).toList.mapM decLevel)
  | "app" => return .app (← decode (← get j "fn")) (← decode (← get j "arg"))
  | "lam" => return .lam (Name.mkSimple (← str (← get j "display_name"))) (← decode (← get j "type")) (← decode (← get j "body")) (← decBinder (← get j "binder_info"))
  | "forall" => return .forallE (Name.mkSimple (← str (← get j "display_name"))) (← decode (← get j "type")) (← decode (← get j "body")) (← decBinder (← get j "binder_info"))
  | "let" =>
      let nd ← match (← get j "nondependent").getBool? with
        | .ok b => pure b
        | .error _ => throwError "PREPROCESS_WIRE_BOOL"
      return .letE (Name.mkSimple (← str (← get j "display_name")))
        (← decode (← get j "type")) (← decode (← get j "value")) (← decode (← get j "body")) nd
  | "nat" => return .lit (.natVal (← nat (← get j "value")))
  | "string" => return .lit (.strVal (← str (← get j "value")))
  | "proj" => return .proj (← decName (← get j "structure")) (← nat (← get j "index")) (← decode (← get j "body"))
  | _ => throwError "PREPROCESS_WIRE_EXPRESSION"

private def closeType (xs : Array Expr) (e : Expr) : MetaM Expr :=
  mkForallFVars xs e (usedLetOnly := false) (generalizeNondepLet := false)
private def closeProof (xs : Array Expr) (e : Expr) : MetaM Expr :=
  mkLambdaFVars xs e (usedLetOnly := false) (generalizeNondepLet := false)

private def contextVars : MetaM (Array Expr) := do
  let mut xs := #[]
  for d in ← getLCtx do
    -- Elaborator recursive-declaration placeholders are not user hypotheses.
    unless d.isImplementationDetail do xs := xs.push (mkFVar d.fvarId)
  return xs

private def audit (e : Expr) : MetaM Unit := do
  for c in e.getUsedConstants do
    if c.toString.startsWith "FiniteQBenchmark.Identity" then
      throwError "PREPROCESS_TARGET_THEOREM_DEPENDENCY: {c}"
    for a in ← Lean.collectAxioms c do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "PREPROCESS_UNTRUSTED_AXIOM: {c}: {a}"

private def certify (ty value : Expr) : MetaM (Array String) := do
  let value ← instantiateMVars value
  let ty ← instantiateMVars ty
  if value.hasMVar || ty.hasMVar || value.hasFVar || ty.hasFVar then
    throwError "PREPROCESS_OPEN_CERTIFICATE"
  audit ty
  audit value
  -- Check a typed let with the kernel, without inserting auxiliary theorem
  -- declarations into the target's asynchronous elaboration transaction.
  checkWithKernel (.letE `certificate ty value (.bvar 0) false)
  let mut axioms : NameSet := {}
  for c in ty.getUsedConstants ++ value.getUsedConstants do
    for ax in ← Lean.collectAxioms c do axioms := axioms.insert ax
  return (axioms.toArray.qsort Name.lt).map Name.toString

private def allowedRules : Array Name := #[
  ``FiniteQPreprocess.poch_zero, ``FiniteQPreprocess.pochList_nil,
  ``FiniteQPreprocess.pochList_cons,
  ``FiniteQPreprocess.nat_Ico_sum, ``FiniteQPreprocess.nat_Ico_prod,
  ``FiniteQPreprocess.nat_Icc_sum, ``FiniteQPreprocess.nat_Icc_prod,
  ``FiniteQPreprocess.merge_sum,
  ``FiniteQPreprocess.sum_left_factor, ``FiniteQPreprocess.sum_right_factor,
  ``add_zero, ``zero_add, ``mul_one, ``one_mul, ``mul_zero, ``zero_mul,
  ``sub_zero, ``pow_zero, ``pow_one,
  ``List.map_cons, ``List.map_nil, ``List.length_map,
  ``List.length_cons, ``List.length_nil,
  ``Finset.sum_empty, ``Finset.prod_empty, ``div_self]

/-- Only nonrecursive mathematical wrappers are unfolded. Core products, Gaussian
    coefficients, recursors and arbitrary user definitions retain their identity. -/
private def unfoldNames : Array Name := #[
  `FiniteQBenchmark.wellPoisedRaw, `FiniteQBenchmark.bibasicPhi,
  `FiniteQBenchmark.multibaseTerm, `FiniteQBenchmark.ultraspherical,
  `FiniteQBenchmark.littleJacobi, `FiniteQBenchmark.qRacah,
  `FiniteQBenchmark.askeyWilson, `FiniteQBenchmark.phi,
  `FiniteQBenchmark.phiTerm, `FiniteQBenchmark.fineA]

private def activeRules : MetaM (Array Name) := do
  let env ← getEnv
  return allowedRules ++ unfoldNames.filter (fun name =>
    match env.find? name with | some (.defnInfo _) => true | _ => false)

/-- Conditions can only be discharged from actual hypotheses (up to definitional equality).
    No new assumptions, numerical probing, classifier, or solver is used. -/
private def discharge : Simp.Discharge := fun p => do
  for d in ← getLCtx do
    if d.isImplementationDetail then continue
    if (← isProp d.type) && (← isDefEq d.type p) then return some (mkFVar d.fvarId)
  return none

/-- Preserve definitions separately, without expanding them in the target.
    Library constants retain their qualified identity and pinned environment. -/
private def declarations (root : Expr) : MetaM (Array Json) := do
  let mut pending := root.getUsedConstants
  let mut seen : NameSet := {}
  let mut rows : Array Json := #[]
  while !pending.isEmpty do
    let name := pending.back!
    pending := pending.pop
    if seen.contains name || !name.toString.startsWith "FiniteQBenchmark." then
      continue
    seen := seen.insert name
    if rows.size >= 2048 then throwError "PREPROCESS_DEFINITION_BUDGET"
    let info ← getConstInfo name
    let mut fields := [("name", encName name), ("type", ← encode info.type),
      ("universe_parameters", toJson (info.levelParams.toArray.map encName))]
    pending := pending ++ info.type.getUsedConstants
    match info with
    | .defnInfo d =>
      fields := fields ++ [("kind", toJson "definition"), ("body", ← encode d.value)]
      pending := pending ++ d.value.getUsedConstants
    | .thmInfo _ => fields := fields ++ [("kind", toJson "theorem_reference")]
    | _ => fields := fields ++ [("kind", toJson "environment_declaration")]
    rows := rows.push (Json.mkObj fields)
  return rows

/-- Exact kernel signatures supply operand positions; Python never guesses
    arity from the last few arguments of a partially applied constant. -/
private def signatures (original normalized : Expr) : MetaM (Array Json) := do
  let mut names : NameSet := {}
  for name in original.getUsedConstants ++ normalized.getUsedConstants do
    names := names.insert name
  let mut rows := #[]
  for name in names.toArray.qsort Name.lt do
    let info ← getConstInfo name
    let mut ty := info.type
    let mut binders : Array Json := #[]
    while ty.isForall do
      binders := binders.push (Json.mkObj [
        ("name", toJson ty.bindingName!.toString),
        ("binder_info", toJson (encBinder ty.bindingInfo!))])
      ty := ty.bindingBody!
    rows := rows.push (Json.mkObj [("symbol", toJson name.toString),
      ("type", ← encode info.type), ("binders", toJson binders)])
  return rows

private def relationCatalog : MetaM Json := do
  let name := ``FiniteQPreprocess.poch_shift
  let info ← getConstInfo name
  return toJson (#[Json.mkObj [("kind", toJson "q_pochhammer_successor"),
    ("theorem", toJson name.toString), ("type", ← encode info.type),
    ("application", toJson "available_not_eagerly_rewritten")]])

private def contextRows (xs : Array Expr) : MetaM (Array Json) := do
  let mut context : Array Json := #[]
  for i in [:xs.size] do
    let d ← xs[i]!.fvarId!.getDecl
    let proposition ← isProp d.type
    context := context.push (Json.mkObj [("id", toJson s!"v{i}"),
      ("original_name", toJson d.userName.toString),
      ("role", toJson (if proposition then "assumption" else "parameter")),
      ("type_in_full_context", ← encode (d.type.abstract xs)),
      ("binder_info", toJson (encBinder d.binderInfo))])
  return context

private def exportGoal (expanded : Bool) : TacticM Unit := withMainContext do
  let rules ← if expanded then activeRules else pure (allowedRules.filter fun name =>
    name != ``FiniteQPreprocess.nat_Icc_sum && name != ``FiniteQPreprocess.nat_Icc_prod)
  let original ← instantiateMVars (← getMainTarget)
  let xs ← contextVars
  let originalClosed ← closeType xs original
  audit originalClosed
  let mut current := original
  let mut evidence ← mkEqRefl original
  let mut trace : Array Json := #[]
  let mut exhausted := true
  for round in [:3] do
    let mut changed := false
    for rule in rules do
      let thms ← if unfoldNames.contains rule then
          ({} : SimpTheorems).addDeclToUnfold rule
        else ({} : SimpTheorems).addConst rule
      let ctx ← Simp.mkContext (config := {
          maxSteps := 10000, zeta := false, zetaDelta := false,
          beta := true, iota := false, proj := false, autoUnfold := false, decide := false
        }) (simpTheorems := #[thms])
      let (r, _) ← Meta.simp current ctx (discharge? := some discharge)
      if r.expr != current then
        let step ← match r.proof? with
          | some proof => pure proof
          | none => mkEqRefl current
        let stepTy ← closeType xs (← mkEq current r.expr)
        let stepProof ← closeProof xs step
        let _ ← certify stepTy stepProof
        trace := trace.push (Json.mkObj [
          ("round", toJson round), ("rule", toJson rule.toString),
          ("before", ← encode (← closeType xs current)),
          ("after", ← encode (← closeType xs r.expr)),
          ("bridge_type", ← encode stepTy), ("proof", ← encode stepProof)])
        evidence ← mkEqTrans evidence step
        current := r.expr
        changed := true
    if !changed then
      exhausted := false
      break
  let bridgeTy ← closeType xs (← mkEq original current)
  let bridgeProof ← closeProof xs evidence
  let axioms ← certify bridgeTy bridgeProof
  let context ← contextRows xs
  let bundle := Json.mkObj [("wire_version", toJson (1 : Nat)),
    ("normalization_view", toJson (if expanded then "expanded" else "structured")),
    ("relations", ← relationCatalog),
    ("original_closed", ← encode originalClosed),
    ("normalized_closed", ← encode (← closeType xs current)),
    ("bridge_type", ← encode bridgeTy), ("bridge_proof", ← encode bridgeProof),
    ("signatures", toJson (← signatures originalClosed (← closeType xs current))),
    ("context", toJson context), ("transformations", toJson trace),
    ("declarations", toJson (← declarations originalClosed)),
    ("allowed_rules", toJson ((allowedRules ++ unfoldNames).map Name.toString)),
    ("round_limit_reached", toJson exhausted), ("axioms", toJson axioms)]
  logInfo m!"PREPROCESS_JSON:{(packWire bundle).compress}"
  -- Extraction deliberately leaves the original target unproved.
  throwError "PREPROCESS_EXPORT_ONLY"

elab "preprocess_export" : tactic => exportGoal false
elab "preprocess_export_expanded" : tactic => exportGoal true

/-- Recover the two closed propositions from a pointwise equality certificate. -/
private partial def bridgeSides (e : Expr) : MetaM (Expr × Expr) := do
  match e with
  | .forallE n t b bi =>
      let (l, r) ← bridgeSides b
      return (.forallE n t l bi, .forallE n t r bi)
  | .letE n t v b nd =>
      let (l, r) ← bridgeSides b
      return (.letE n t v l nd, .letE n t v r nd)
  | _ =>
      let args := e.getAppArgs
      unless e.isAppOfArity ``Eq 3 do throwError "PREPROCESS_NOT_EQ_BRIDGE"
      return (args[1]!, args[2]!)

private def replay (file : String) : TacticM (Expr × Array String) := withMainContext do
  let text ← IO.FS.readFile file
  let j ← match Json.parse text with
    | .ok j => pure j
    | .error e => throwError "PREPROCESS_JSON_PARSE: {e}"
  let j ← match unpackWire j with
    | .ok j => pure j
    | .error e => throwError "PREPROCESS_WIRE: {e}"
  if let .ok saved := j.getObjVal? "relations" then
    unless saved == (← relationCatalog) do throwError "PREPROCESS_RELATION_MISMATCH"
  let old ← decode (← get j "original_closed")
  let normalized ← decode (← get j "normalized_closed")
  let ty ← decode (← get j "bridge_type")
  let proof ← decode (← get j "bridge_proof")
  if let .ok saved := j.getObjVal? "signatures" then
    unless saved == toJson (← signatures old normalized) do
      throwError "PREPROCESS_SIGNATURE_MISMATCH"
  let xs ← contextVars
  let target ← closeType xs (← instantiateMVars (← getMainTarget))
  unless ← isDefEq target old do throwError "PREPROCESS_ORIGINAL_MISMATCH"
  unless (← get j "declarations") == toJson (← declarations target) do
    throwError "PREPROCESS_DECLARATIONS_MISMATCH"
  let storedContext ← arr (← get j "context")
  let actualContext ← contextRows xs
  unless storedContext.size == actualContext.size do
    throwError "PREPROCESS_CONTEXT_METADATA_MISMATCH"
  for i in [:storedContext.size] do
    for key in ["id", "role", "binder_info"] do
      unless (← get storedContext[i]! key) == (← get actualContext[i]! key) do
        throwError "PREPROCESS_CONTEXT_METADATA_MISMATCH: {key}"
    let storedType ← decode (← get storedContext[i]! "type_in_full_context")
    let actualType ← decode (← get actualContext[i]! "type_in_full_context")
    unless ← isDefEq (storedType.instantiateRev xs) (actualType.instantiateRev xs) do
      throwError "PREPROCESS_CONTEXT_TYPE_MISMATCH"
  unless (← get j "allowed_rules") == toJson ((allowedRules ++ unfoldNames).map Name.toString) do
    throwError "PREPROCESS_RULE_POLICY_MISMATCH"
  let (l, r) ← bridgeSides ty
  unless (← isDefEq l old) && (← isDefEq r normalized) do
    throwError "PREPROCESS_NORMALIZED_MISMATCH"
  let axioms ← certify ty proof
  let mut previous := old
  for entry in ← arr (← get j "transformations") do
    let before ← decode (← get entry "before")
    let after ← decode (← get entry "after")
    let st ← decode (← get entry "bridge_type")
    let sp ← decode (← get entry "proof")
    let (sl, sr) ← bridgeSides st
    unless (← isDefEq before previous) && (← isDefEq sl before) && (← isDefEq sr after) do
      throwError "PREPROCESS_TRACE_MISMATCH"
    let rule ← str (← get entry "rule")
    unless ((allowedRules ++ unfoldNames).map Name.toString).contains rule do
      throwError "PREPROCESS_UNREGISTERED_RULE"
    let _ ← certify st sp
    previous := after
  unless ← isDefEq previous normalized do throwError "PREPROCESS_TRACE_END_MISMATCH"
  return (proof, axioms)

elab "preprocess_replay " file:str : tactic => withMainContext do
  let (_, axioms) ← replay file.getString
  logInfo m!"PREPROCESS_REPLAY_JSON:{(Json.mkObj [("bridge_kernel_checked", toJson true),
    ("original_context_matched", toJson true), ("axioms", toJson axioms)]).compress}"
  throwError "PREPROCESS_REPLAY_ONLY"

/-- A backend receives precisely the verified normalized goal. Its proof is
    transported back to the unchanged original goal through Eq.mpr. -/
elab "preprocess_enter " file:str : tactic => withMainContext do
  let (closedProof, _) ← replay file.getString
  let xs ← contextVars
  let mut args := #[]
  for x in xs do
    let d ← x.fvarId!.getDecl
    unless d.isLet do args := args.push x
  let proof := mkAppN closedProof args
  let eqType ← whnf (← inferType proof)
  unless eqType.isAppOfArity ``Eq 3 do throwError "PREPROCESS_APPLIED_BRIDGE_TYPE"
  let parts := eqType.getAppArgs
  unless ← isDefEq parts[1]! (← getMainTarget) do throwError "PREPROCESS_APPLIED_ORIGINAL_MISMATCH"
  let newGoal ← mkFreshExprSyntheticOpaqueMVar parts[2]!
  let result ← mkEqMPR proof newGoal
  (← getMainGoal).assign result
  replaceMainGoal [newGoal.mvarId!]

/-- Original imports may contain historical closed identities. They are needed
    to recover definitions, but cannot supply the new backend's proof. -/
def auditCompleted (root : Name) : CoreM Unit := do
  let env ← getEnv
  let mut pending := #[root]
  let mut seen : NameSet := {}
  while !pending.isEmpty do
    let name := pending.back!
    pending := pending.pop
    if seen.contains name then continue
    seen := seen.insert name
    let info ← getConstInfo name
    if let some idx := env.getModuleIdxFor? name then
      let moduleName := env.header.moduleNames[idx]!.toString
      -- External library declarations cannot depend on project modules.
      unless moduleName.startsWith "Benchmark." || moduleName.startsWith "FiniteQPreprocess." do
        continue
      if info.isTheorem && (moduleName.endsWith "Proofs" ||
          ["Benchmark.Representation", "Benchmark.InitialValues", "Benchmark.BatchAuxiliary"].contains moduleName ||
          moduleName.startsWith "Benchmark.Statements.") then
        throwError "PREPROCESS_FORBIDDEN_PROOF_DEPENDENCY: {name} from {moduleName}"
    pending := pending ++ info.type.getUsedConstants
    if let some value := info.value? (allowOpaque := true) then
      pending := pending ++ value.getUsedConstants
  for ax in ← Lean.collectAxioms root do
    unless [``propext, ``Classical.choice, ``Quot.sound].contains ax do
      throwError "PREPROCESS_ORIGINAL_PROOF_AXIOM: {ax}"
  logInfo "PREPROCESS_ORIGINAL_PROOF_AUDIT_OK"

end FiniteQPreprocess
