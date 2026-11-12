import Lean.Elab.Command
import Lean.Elab.ElabRules
import Lean.Util.CollectAxioms

/- The trusted commands parse each untrusted string as ONE complete term.
   No candidate command or import is spliced into the source file. The limited
   tactic syntax below excludes executable elaborator/reflection extensions. -/
open Lean Elab Command Meta
set_option autoImplicit false

private def localParseTerm (text : String) : CommandElabM (TSyntax `term) := do
  match Parser.runParserCategory (← getEnv) `term text with
  | .ok stx => pure ⟨stx⟩
  | .error error => throwError "invalid complete local term: {error}"

private partial def checkLocalSyntax (stx : Syntax) : CommandElabM Unit := do
  match stx with
  | .atom .. | .ident .. | .missing => return
  | _ => pure ()
  let name := stx.getKind.toString
  let allowed := ["Lean.Parser.Tactic.tacticSeq", "Lean.Parser.Tactic.tacticSeq1Indented",
    "Lean.Parser.Tactic.tacticSeqBracketed", "Lean.Parser.Tactic.exact", "Lean.Parser.Tactic.apply",
    "Lean.Parser.Tactic.intro", "Lean.Parser.Tactic.intros", "Lean.Parser.Tactic.assumption",
    "Lean.Parser.Tactic.rfl", "Lean.Parser.Tactic.tacticRfl", "Lean.Parser.Tactic.constructor", "Lean.Parser.Tactic.trivial",
    "Lean.Parser.Tactic.simp", "Lean.Parser.Tactic.simpa", "Lean.Parser.Tactic.simpArgs",
    "Lean.Parser.Tactic.simpaArgsRest", "Lean.Parser.Tactic.optConfig", "Lean.Parser.Tactic.simpLemma",
    "Lean.Parser.Tactic.simpArg", "Lean.Parser.Tactic.simpErase", "Lean.Parser.Tactic.simpStar",
    "Lean.Parser.Tactic.rwSeq", "Lean.Parser.Tactic.rwRule", "Lean.Parser.Tactic.rwRuleSeq",
    "Lean.Parser.Tactic.rewrite", "Lean.Parser.Tactic.change", "Lean.Parser.Tactic.symm",
    "Lean.Parser.Tactic.trans", "Lean.Parser.Tactic.refine", "Lean.Parser.Tactic.left",
    "Lean.Parser.Tactic.right", "Lean.Parser.Tactic.skip", "Lean.Parser.Tactic.done",
    "Lean.Parser.Tactic.tacticHave__", "Lean.Parser.Tactic.omega", "Lean.Parser.Tactic.induction",
    "Lean.Parser.Tactic.elimTarget", "Lean.Parser.Tactic.inductionAlts", "Lean.Parser.Tactic.inductionAlt",
    "Lean.Parser.Tactic.inductionAltLHS", "Lean.Parser.Tactic.tacticTrivial", "Lean.Parser.Tactic.rcases",
    "Lean.Parser.Tactic.rcasesPatLo", "Lean.Parser.Tactic.rcasesPatMed", "Lean.Parser.Tactic.rcasesPat.tuple",
    "Lean.Parser.Tactic.rcasesPat.one", "Lean.Parser.Tactic.allGoals", "Lean.Parser.Tactic.location",
    "Lean.Parser.Tactic.locationHyp", "Lean.Parser.Tactic.locationType", "Lean.Parser.Tactic.«tactic_<;>_»",
    "Lean.Parser.Tactic.congr", "Mathlib.Tactic.RingNF.ring", "Mathlib.Tactic.RingNF.ringNF",
    "Mathlib.Tactic.normNum"]
  if name.startsWith "Lean.Parser.Tactic." && !allowed.contains name then
    throwError "local tactic syntax is not permitted: {name}"
  let terms := ["hygieneInfo", "Lean.Parser.Term.hygienicLParen", "Lean.Parser.Term.app", "Lean.Parser.Term.basicFun", "Lean.Parser.Term.paren", "Lean.Parser.Term.fun",
    "Lean.Parser.Term.forall", "Lean.Parser.Term.arrow", "Lean.Parser.Term.byTactic",
    "Lean.Parser.Term.explicitBinder", "Lean.Parser.Term.implicitBinder", "Lean.Parser.Term.strictImplicitBinder",
    "Lean.Parser.Term.instBinder", "Lean.Parser.Term.typeSpec", "Lean.Parser.Term.binderIdent",
    "Lean.Parser.Term.hole", "Lean.Parser.Term.syntheticHole", "Lean.Parser.Term.type",
    "Lean.Parser.Term.sort", "Lean.Parser.Term.prop", "Lean.Parser.Term.num", "Lean.Parser.Term.cdot",
    "Lean.Parser.Term.proj", "Lean.Parser.Term.ident", "Lean.Parser.Term.typeAscription",
    "Lean.Parser.Term.explicit", "Lean.Parser.Term.let", "Lean.Parser.Term.letIdDecl",
    "Lean.Parser.Term.letDecl", "Lean.Parser.Term.have", "Lean.Parser.Term.show",
    "Lean.Parser.Term.tuple", "Lean.Parser.Term.anonymousCtor", "Lean.Parser.Term.universe",
    "Lean.Parser.Term.level", "Lean.Parser.Term.binderType", "Lean.Parser.Term.binderPred",
    "Lean.Parser.Term.namedArgument", "Lean.Parser.Term.match", "Lean.Parser.Term.matchAlt",
    "Lean.Parser.Term.matchAlts", "Lean.Parser.Term.matchDiscr", "Lean.Parser.Term.matchDiscrs",
    "Lean.Parser.Term.letConfig", "Lean.Parser.Term.letId", "group", "Lean.cdot", "Lean.cdotTk",
    "Lean.calcTactic", "Lean.calcSteps", "Lean.calcFirstStep", "Lean.calcStep", "patternIgnore", "token.«⊢»",
    "termIfThenElse", "termℕ", "termℤ", "termℚ", "termℝ", "termℂ", "BigOperators.bigsum", "BigOperators.bigprod",
    "BigOperators.bigOpBinders", "BigOperators.bigOpBinder", "Lean.«binderPred∈_»", "null", "num"]
  let notations := ["«term_∧_»", "«term_∨_»", "«term_↔_»", "«term¬_»",
    "«term_=_»", "«term_≠_»", "«term_+_»", "«term_-_»", "«term_*_»", "«term_/_»",
    "«term_^_»", "«term_%_»", "«term_≤_»", "«term_<_»", "«term_≥_»", "«term_>_»", "«term-_»"]
  if !(terms.contains name || allowed.contains name || notations.contains name ||
       name.startsWith "Lean.Parser.Level.") then
    throwError "local extension syntax is not permitted: {name}"
  for child in stx.getArgs do
    checkLocalSyntax child

elab "agent_v2_local_declaration " target:ident proposition:str proof:str : command => do
  let proposition ← localParseTerm proposition.getString
  let proof ← localParseTerm proof.getString
  checkLocalSyntax proposition
  checkLocalSyntax proof
  elabCommand (← `(theorem $target : $proposition := $proof))

/- Trusted assembly includes canonical CAS tactics already reconstructed by
   Python. It still uses single-term parsing and a final kernel/axiom audit. -/
elab "agent_v2_local_assembled " target:ident proposition:str proof:str : command => do
  let proposition ← localParseTerm proposition.getString
  let proof ← localParseTerm proof.getString
  elabCommand (← `(theorem $target : $proposition := $proof))

elab "agent_v2_local_expected " proposition:str : command => do
  let proposition ← localParseTerm proposition.getString
  let name := mkIdent `AgentV2Expected
  elabCommand (← `(def $name : Prop := $proposition))

elab "agent_v2_local_audit " target:ident " against " expected:ident " nonce " auditNonce:str : command => do
  liftTermElabM do
    let targetName ← realizeGlobalConstNoOverloadWithInfo target
    let expectedName ← realizeGlobalConstNoOverloadWithInfo expected
    let proofInfo ← match ← getConstInfo targetName with
      | .thmInfo info => pure info
      | _ => throwError "candidate must be a theorem"
    let expectedInfo ← match ← getConstInfo expectedName with
      | .defnInfo info => pure info
      | _ => throwError "expected proposition must be a definition"
    unless proofInfo.levelParams.length == expectedInfo.levelParams.length do
      throwError "candidate universe generality differs from exact target"
    let actual := proofInfo.type.instantiateLevelParams proofInfo.levelParams
      (expectedInfo.levelParams.map mkLevelParam)
    if actual.hasMVar || actual.hasFVar || expectedInfo.value.hasMVar || expectedInfo.value.hasFVar then
      throwError "local proposition must be closed"
    unless ← isProp actual do throwError "local target must be Prop"
    unless ← isDefEq actual expectedInfo.value do throwError "local type differs from exact target"
    let axioms ← Lean.collectAxioms targetName
    for axiomName in axioms do
      unless axiomName == ``propext || axiomName == ``Classical.choice || axiomName == ``Quot.sound do
        throwError "unapproved axiom: {axiomName}"
    logInfo (Json.mkObj [
      ("agent_v2_audit_v1", toJson auditNonce.getString),
      ("theorem", toJson targetName.toString),
      ("axioms", toJson (axioms.map Name.toString)),
      ("universe_parameters", toJson (proofInfo.levelParams.map Name.toString)),
      ("universe_parameter_count", toJson proofInfo.levelParams.length),
      ("modules", toJson ((← getEnv).header.moduleNames.map Name.toString))]).compress
