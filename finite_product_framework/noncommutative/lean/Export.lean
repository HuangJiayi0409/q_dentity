import Lean
open Lean Meta Elab Tactic
namespace FiniteQOperator
partial def tree (e : Expr) : MetaM Json := do
  let e := e.consumeMData
  if let some n := e.nat? then
    return Json.mkObj [("op", toJson "nat"), ("value", toJson n)]
  if let .fvar id := e then
    return Json.mkObj [("op", toJson "var"), ("name", toJson (← id.getDecl).userName.toString)]
  let args := e.getAppArgs
  let name := e.getAppFn.constName?.getD Name.anonymous
  let count := if [``Eq, ``HAdd.hAdd, ``HSub.hSub, ``HMul.hMul,
      ``HPow.hPow, ``HSMul.hSMul].contains name then 2
    else if name.toString == "FiniteQBenchmark.kacM" then 2
    else if name == ``Neg.neg || name.toString == "FiniteQBenchmark.kacX" then 1
    else 0
  let children ← (args.extract (args.size-count) args.size).mapM tree
  return Json.mkObj [("op", toJson name.toString), ("args", toJson children),
    ("text", toJson (← ppExpr e).pretty)]
elab "operator_export" : tactic => withMainContext do
  let target ← getMainTarget
  unless target.isAppOfArity ``Eq 3 do throwError "operator equality required"
  let mut hypotheses : Array Json := #[]
  for decl in ← getLCtx do
    unless decl.isImplementationDetail do
      if decl.type.isAppOfArity ``Eq 3 then
        hypotheses := hypotheses.push (Json.mkObj [
          ("name", toJson decl.userName.toString), ("type", ← tree decl.type)])
  logInfo m!"OPERATOR_JSON:{(Json.mkObj [("target", ← tree target),
    ("relations", toJson hypotheses)]).compress}"
  throwError "OPERATOR_EXPORT_ONLY"
end FiniteQOperator
