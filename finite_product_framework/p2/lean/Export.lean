import Lean
import Mathlib.Tactic
open Lean Meta Elab Tactic
namespace FiniteQP2

private def naturalValue (e : Expr) : Option Nat :=
  match e.consumeMData with
  | .lit (.natVal n) => some n
  | e =>
    if e.getAppFn.isConstOf ``OfNat.ofNat then
      match e.getAppArgs[1]! with
      | .lit (.natVal n) => some n
      | _ => none
    else none

/-- Exact ring syntax; every non-ring subexpression is an independent atom.
No inversion cancellation, q-shift law or equality of different atoms is assumed. -/
partial def ringJSON (e : Expr) : StateT (Array Expr) MetaM Json := do
  let e := e.consumeMData
  let args := e.getAppArgs
  if let .const name _ := e.getAppFn then
    if name == ``OfNat.ofNat then
      if let some n := naturalValue args[1]! then
        return Json.mkObj [("op", toJson "integer"), ("value", toJson n)]
    if [``HAdd.hAdd, ``HSub.hSub, ``HMul.hMul].contains name then
      return Json.mkObj [("op", toJson name.toString),
        ("args", toJson #[← ringJSON args[args.size-2]!, ← ringJSON args[args.size-1]!])]
    if name == ``Neg.neg then
      return Json.mkObj [("op", toJson "neg"), ("arg", ← ringJSON args.back!)]
    if name == ``HPow.hPow then
      if let some n := naturalValue args.back! then
        if n ≤ 100 then
          return Json.mkObj [("op", toJson "pow"), ("exponent", toJson n),
            ("arg", ← ringJSON args[args.size-2]!)]
  let atoms ← get
  let mut index := atoms.size
  for i in [:atoms.size] do
    if ← isDefEq e atoms[i]! then
      index := i
      break
  if index == atoms.size then
    set (atoms.push e)
  return Json.mkObj [("op", toJson "atom"), ("key", toJson index),
    ("display", toJson (← ppExpr e).pretty)]

elab "p2_export" : tactic => do
  if (← getGoals).isEmpty then
    logInfo "P2_JSON:{\"closed_by_preparation\":true}"
    throwError "P2_EXPORT_ONLY"
  let goals ← getGoals
  if goals.length > 128 then throwError "P2_GOAL_LIMIT"
  let mut entries : Array Json := #[]
  for goal in goals do
    let entry ← goal.withContext do
      let target ← instantiateMVars (← goal.getType)
      if let some (_, lhs, rhs) := target.eq? then
        let (data, _) ← (do
          let left ← ringJSON lhs
          let right ← ringJSON rhs
          pure (Json.mkObj [("lhs", left), ("rhs", right)])).run #[]
        pure data
      else
        pure (Json.mkObj [("unsupported_goal", toJson (← ppExpr target).pretty)])
    entries := entries.push entry
  let data := Json.mkObj [("goals", toJson entries)]
  logInfo m!"P2_JSON:{data.compress}"
  throwError "P2_EXPORT_ONLY"

end FiniteQP2
