import Lean.Elab.Command
import Lean.Elab.ElabRules
import Lean.Util.CollectAxioms

/- Fixed audit for a Source whose actual theorem has no universe parameters.
   The separate polymorphic drivers retain their strict original contract. -/
open Lean Elab Command Meta
set_option autoImplicit false

elab "agent_v2_monomorphic_audit " target:ident " against " expected:ident " nonce " nonce:str : command => do
  liftTermElabM do
    let targetName ← realizeGlobalConstNoOverloadWithInfo target
    let expectedName ← realizeGlobalConstNoOverloadWithInfo expected
    let proofInfo ← match ← getConstInfo targetName with
      | .thmInfo info => pure info
      | _ => throwError "candidate must be a theorem"
    let expectedInfo ← match ← getConstInfo expectedName with
      | .defnInfo info => pure info
      | _ => throwError "expected proposition is not a definition"
    unless proofInfo.levelParams.isEmpty && expectedInfo.levelParams.isEmpty do
      throwError "candidate and expected proposition must retain their monomorphic Source type"
    if proofInfo.type.hasMVar || proofInfo.type.hasFVar || expectedInfo.value.hasMVar || expectedInfo.value.hasFVar then
      throwError "the proposition must be closed"
    unless ← isProp proofInfo.type do
      throwError "candidate type is not Prop"
    unless ← isDefEq proofInfo.type expectedInfo.value do
      throwError "candidate type differs from independently reconstructed proposition"
    let axioms ← Lean.collectAxioms targetName
    for axiomName in axioms do
      unless axiomName == ``propext || axiomName == ``Classical.choice || axiomName == ``Quot.sound do
        throwError "unapproved axiom: {axiomName}"
    let record := Json.mkObj [
      ("agent_v2_audit_v1", toJson nonce.getString),
      ("theorem", toJson targetName.toString),
      ("axioms", toJson (axioms.map Name.toString)),
      ("universe_parameters", toJson (proofInfo.levelParams.map Name.toString)),
      ("universe_parameter_count", toJson proofInfo.levelParams.length),
      ("modules", toJson ((← getEnv).header.moduleNames.map Name.toString))]
    logInfo record.compress
