import Lean
open Lean Meta Elab Tactic
namespace FiniteQCombinatorialExport
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
  let count := if [``Eq, ``And, ``HAdd.hAdd, ``HSub.hSub, ``HMul.hMul, ``HDiv.hDiv,
      ``HPow.hPow, ``Finset.sum, ``Finset.prod, ``Finset.Icc,
      ``Finset.powersetCard, ``Finset.filter, ``Union.union, ``SDiff.sdiff].contains name then 2
    else if [``Neg.neg, ``Finset.range, ``Finset.powerset, ``Finset.card].contains name then 1
    else if ["FiniteQBenchmark.gaussian", "FiniteQBenchmark.poch", "FiniteQBenchmark.rogersSzego"].contains name.toString then 3
    else 0
  return Json.mkObj [("op",toJson name.toString),
    ("args",toJson (← (args.extract (args.size-count) args.size).mapM tree)),
    ("type",toJson (← ppExpr (← inferType e)).pretty),("text",toJson (← ppExpr e).pretty)]
elab "combinatorial_export" : tactic => withMainContext do
  let target ← getMainTarget
  unless target.isAppOfArity ``Eq 3 || target.isAppOfArity ``And 2 do
    throwError "finite weighted equality or conjunction required"
  logInfo m!"COMBINATORIAL_JSON:{(← tree target).compress}"
  throwError "COMBINATORIAL_EXPORT_ONLY"
end FiniteQCombinatorialExport
