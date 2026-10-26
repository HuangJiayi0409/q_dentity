import Lean
open Lean Meta Elab Tactic
namespace FiniteQDifferenceStructure
partial def tree (e : Expr) : MetaM Json := do
  let e := e.consumeMData
  if let some n := e.nat? then
    return Json.mkObj [("op",toJson "nat"),("value",toJson n)]
  if let .fvar id := e then
    return Json.mkObj [("op",toJson "var"),("name",toJson (← id.getDecl).userName.toString)]
  if let .lam name ty body _ := e then
    return ← withLocalDeclD name ty fun v => do
      return Json.mkObj [("op",toJson "lambda"),("name",toJson name.toString),
        ("body",← tree (body.instantiate1 v))]
  let args := e.getAppArgs
  let name := e.getAppFn.constName?.getD Name.anonymous
  let count := if [``Eq, ``HAdd.hAdd, ``HSub.hSub, ``HMul.hMul, ``HDiv.hDiv,
      ``HPow.hPow, ``Finset.sum, ``Finset.prod, ``Finset.Icc,
      ``Finset.powersetCard].contains name then 2
    else if [``Neg.neg, ``Inv.inv, ``Nat.cast, ``Int.ofNat,
      ``Finset.range, ``Finset.powerset, ``Finset.card].contains name then 1
    else if name.toString == "FiniteQBenchmark.poch" then 3
    else 0
  return Json.mkObj [("op",toJson name.toString),
    ("args",toJson (← (args.extract (args.size-count) args.size).mapM tree)),
    ("type",toJson (← ppExpr (← inferType e)).pretty),("text",toJson (← ppExpr e).pretty)]
elab "dr_structure" : tactic => withMainContext do
  let target ← getMainTarget
  unless target.isAppOfArity ``Eq 3 do throwError "difference ring requires an equality"
  let mut indices : Array String := #[]
  for decl in ← getLCtx do
    unless decl.isImplementationDetail do
      if ← isDefEq decl.type (mkConst ``Nat) then
        indices := indices.push decl.userName.toString
  logInfo m!"DIFFERENCE_STRUCTURE:{(Json.mkObj [("target",← tree target),("indices",toJson indices)]).compress}"
  throwError "DIFFERENCE_STRUCTURE_ONLY"
end FiniteQDifferenceStructure
