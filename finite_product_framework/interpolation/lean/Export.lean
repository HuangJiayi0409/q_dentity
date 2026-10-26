import Lean
import Mathlib.Tactic
import Benchmark.InterpolationAtoms
open Lean Meta Elab Tactic
namespace FiniteQInterpolation

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
  let mut semantic := Json.null
  if e.getAppFn.isConstOf ``FiniteQBenchmark.poch then
    semantic := Json.mkObj [("kind", toJson "q_pochhammer"),
      ("parameter", toJson (← ppExpr args[args.size-3]!).pretty),
      ("base", toJson (← ppExpr args[args.size-2]!).pretty),
      ("length", toJson (← ppExpr args.back!).pretty),
      ("parameter_degree", toJson "requires certified source bridge; not atom degree")]
  else if e.getAppFn.isConstOf ``FiniteQBenchmark.phi then
    semantic := Json.mkObj [("kind", toJson "finite_hypergeometric_sum"),
      ("obligation", toJson "parameter representation and weight conversion")]
  return Json.mkObj [("semantic", semantic), ("op", toJson "atom"), ("key", toJson index),
    ("display", toJson (← ppExpr e).pretty)]

elab "interpolation_export" label:str : tactic => do
  let mut values : Array Json := #[]
  for goal in ← getGoals do
    let value ← goal.withContext do
      let target ← instantiateMVars (← goal.getType)
      let some (ty, lhs, rhs) := target.eq? | throwError "INTERPOLATION_EXPECTED_EQUALITY: {target}"
      let charZero ← synthInstance? (← mkAppOptM ``CharZero #[some ty, none])
      let mut geometric : Array Json := #[]
      for decl in ← getLCtx do
        if !decl.isImplementationDetail then
          let ht ← instantiateMVars decl.type
          if ht.getAppFn.isConstOf ``FiniteQBenchmark.regular then
            geometric := geometric.push (Json.mkObj [
              ("base", toJson (← ppExpr ht.getAppArgs.back!).pretty),
              ("hypothesis", toJson (← ppExpr decl.toExpr).pretty)])
      let (pair, _) ← (do
        let left ← algebraJSON lhs
        let right ← algebraJSON rhs
        pure (Json.mkObj [("lhs", left), ("rhs", right),
          ("char_zero", toJson charZero.isSome), ("geometric_nodes", toJson geometric),
          ("type", toJson (← ppExpr ty).pretty),
          ("lhs_display", toJson (← ppExpr lhs).pretty),
          ("rhs_display", toJson (← ppExpr rhs).pretty)])).run #[]
      pure pair
    values := values.push value
  logInfo m!"INTERPOLATION_JSON:{(Json.mkObj [("label", toJson label.getString), ("goals", toJson values)]).compress}"
  throwError "INTERPOLATION_EXPORT_ONLY"

end FiniteQInterpolation
