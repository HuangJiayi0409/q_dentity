import Lean.Elab.Command
import Lean.Elab.ElabRules
import Lean.Util.CollectAxioms

/- Trusted driver. Candidate text is separately restricted to a pure Init term
   language before it reaches this file. No project modules are imported. -/
open Lean Elab Command Meta

set_option autoImplicit false

elab "agent_v2_audit " target:ident " against " expected:ident " nonce " nonce:str : command => do
  liftTermElabM do
    let targetName ← realizeGlobalConstNoOverloadWithInfo target
    let expectedName ← realizeGlobalConstNoOverloadWithInfo expected
    let targetInfo ← getConstInfo targetName
    let expectedInfo ← getConstInfo expectedName
    let proofInfo ← match targetInfo with
      | .thmInfo info => pure info
      | _ => throwError "candidate must be a theorem"
    let expectedType ← match expectedInfo with
      | .defnInfo info => pure info.value
      | _ => throwError "expected proposition is not a definition"
    unless proofInfo.levelParams.isEmpty do
      throwError "universe parameters are not supported"
    if proofInfo.type.hasMVar || proofInfo.type.hasFVar || expectedType.hasMVar || expectedType.hasFVar then
      throwError "the proposition must be closed"
    unless ← isProp proofInfo.type do
      throwError "candidate type is not Prop"
    unless ← isDefEq proofInfo.type expectedType do
      throwError "candidate type differs from expected proposition"
    let axioms ← Lean.collectAxioms targetName
    for axiomName in axioms do
      unless axiomName == ``propext || axiomName == ``Classical.choice || axiomName == ``Quot.sound do
        throwError "unapproved axiom: {axiomName}"
    let record := Json.mkObj [
      ("agent_v2_audit_v1", toJson nonce.getString),
      ("theorem", toJson targetName.toString),
      ("axioms", toJson (axioms.map Name.toString)),
      ("modules", toJson ((← getEnv).header.moduleNames.map Name.toString))]
    logInfo record.compress
