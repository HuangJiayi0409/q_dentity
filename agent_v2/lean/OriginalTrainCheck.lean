import Lean.Elab.Command
import Lean.Elab.ElabRules
import Lean.Util.CollectAxioms

/- Audit the exact original declaration, whose `Type*` universe name is chosen
   by Lean. Renaming its single universe to the independent template's `u`
   preserves universe generality; no specialization to Type 0 is allowed. -/
open Lean Elab Command Meta
set_option autoImplicit false

elab "agent_v2_original_train_audit " target:ident " against " expected:ident " nonce " nonce:str : command => do
  liftTermElabM do
    let targetName ← realizeGlobalConstNoOverloadWithInfo target
    let expectedName ← realizeGlobalConstNoOverloadWithInfo expected
    let proofInfo ← match ← getConstInfo targetName with
      | .thmInfo info => pure info
      | _ => throwError "original declaration must be a theorem"
    let expectedInfo ← match ← getConstInfo expectedName with
      | .defnInfo info => pure info
      | _ => throwError "expected proposition is not a definition"
    unless proofInfo.levelParams.length == 1 && expectedInfo.levelParams == [`u] do
      throwError "original declaration must retain exactly its one polymorphic universe"
    let originalType := proofInfo.type.instantiateLevelParams proofInfo.levelParams [mkLevelParam `u]
    if originalType.hasMVar || originalType.hasFVar || expectedInfo.value.hasMVar || expectedInfo.value.hasFVar then
      throwError "the original proposition must be closed"
    unless ← isProp originalType do
      throwError "original type is not Prop"
    unless ← isDefEq originalType expectedInfo.value do
      throwError "original type differs from independently reconstructed frozen proposition"
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
