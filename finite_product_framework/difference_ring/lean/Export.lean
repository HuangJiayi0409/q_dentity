import Lean
import Mathlib.Tactic
open Lean Meta Elab Tactic
namespace FiniteQDifferenceExport

private def naturalValue (e : Expr) : Option Nat :=
  match e.consumeMData with
  | .lit (.natVal n) => some n
  | e =>
    if e.getAppFn.isConstOf ``OfNat.ofNat then
      match e.getAppArgs[1]! with
      | .lit (.natVal n) => some n
      | _ => none
    else none

/-- Nonalgebraic applications remain exact, independent scalar atoms. -/
partial def algebraJSON (e : Expr) : StateT (Array Expr) MetaM Json := do
  let e := e.consumeMData
  let args := e.getAppArgs
  if let .const name _ := e.getAppFn then
    if name == ``OfNat.ofNat then
      if let some n := naturalValue args[1]! then
        return Json.mkObj [("op", toJson "integer"), ("value", toJson n)]
    if [``HAdd.hAdd, ``HSub.hSub, ``HMul.hMul, ``HDiv.hDiv].contains name then
      return Json.mkObj [("op", toJson name.toString),
        ("args", toJson #[← algebraJSON args[args.size-2]!, ← algebraJSON args.back!])]
    if name == ``Neg.neg || name == ``Inv.inv then
      return Json.mkObj [("op", toJson (if name == ``Neg.neg then "neg" else "inv")),
        ("arg", ← algebraJSON args.back!)]
    if name == ``HPow.hPow then
      if let some n := naturalValue args.back! then
        if n ≤ 64 then
          return Json.mkObj [("op", toJson "pow"), ("exponent", toJson n),
            ("arg", ← algebraJSON args[args.size-2]!)]
  let atoms ← get
  let mut index := atoms.size
  for i in [:atoms.size] do
    if ← isDefEq e atoms[i]! then
      index := i
      break
  if index == atoms.size then set (atoms.push e)
  return Json.mkObj [("op", toJson "atom"), ("key", toJson index),
    ("display", toJson (← ppExpr e).pretty)]

elab "dr_export" : tactic => do
  let mut values : Array Json := #[]
  for goal in ← getGoals do
    let value ← goal.withContext do
      let target ← instantiateMVars (← goal.getType)
      let some (ty, lhs, rhs) := target.eq? | throwError "DIFFERENCE_EXPECTED_EQUALITY: {target}"
      let (pair, _) ← (do
        let left ← algebraJSON lhs
        let right ← algebraJSON rhs
        let mut hypotheses : Array Json := #[]
        for decl in ← getLCtx do
          unless decl.isImplementationDetail do
            if let some (ht, hl, hr) := decl.type.eq? then
              if ← isDefEq ht ty then
                hypotheses := hypotheses.push (Json.mkObj [
                  ("name",toJson decl.userName.toString),
                  ("lhs",← algebraJSON hl),("rhs",← algebraJSON hr)])
        pure (Json.mkObj [("lhs",left),("rhs",right),("hypotheses",toJson hypotheses),
          ("type",toJson (← ppExpr ty).pretty)])).run #[]
      pure pair
    values := values.push value
  logInfo m!"DIFFERENCE_JSON:{(toJson values).compress}"
  throwError "DIFFERENCE_EXPORT_ONLY"
end FiniteQDifferenceExport
