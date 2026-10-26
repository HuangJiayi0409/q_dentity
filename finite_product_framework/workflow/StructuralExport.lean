import Lean
open Lean Meta Elab Tactic
namespace StructuralExport
def constants (e : Expr) : Array String := e.getUsedConstants.map Name.toString
elab "structural_export" : tactic => withMainContext do
  let target ← getMainTarget
  let mut hs : Array Json := #[]
  for d in ← getLCtx do
    if !d.isImplementationDetail && (← isProp d.type) then
      hs := hs.push (Json.mkObj [("name",toJson d.userName.toString),
        ("type",toJson (← ppExpr d.type).pretty),("constants",toJson (constants d.type))])
  logInfo m!"STRUCTURAL_JSON:{(Json.mkObj [("target",toJson (← ppExpr target).pretty), ("constants",toJson (constants target)), ("hypotheses",toJson hs)]).compress}"
  throwError "STRUCTURAL_EXPORT_ONLY"
end StructuralExport
