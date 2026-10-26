import Lean
import Mathlib.Algebra.BigOperators.Ring.Finset
import Benchmark.P1Atoms

open Lean Meta Elab Tactic
namespace FiniteQP1
private def node (op : String) (args : Array Json) : Json :=
  Json.mkObj [("op", toJson op), ("args", toJson args)]
partial def expressionJSON (e : Expr) : MetaM Json := do
  let e := e.consumeMData
  if let .fvar id := e then
    return Json.mkObj [("op", toJson "var"), ("name", toJson (← id.getDecl).userName.toString)]
  if let .lit (.natVal v) := e then
    return Json.mkObj [("op", toJson "nat"), ("value", toJson v)]
  if let .lam name ty body _ := e then
    return ← withLocalDeclD name ty fun v => do
      return Json.mkObj [("op", toJson "lambda"), ("name", toJson name.toString),
        ("body", ← expressionJSON (body.instantiate1 v))]
  let args := e.getAppArgs
  if let .const name _ := e.getAppFn then
    if name == ``OfNat.ofNat then
      return ← expressionJSON args[1]!
    let binary := [``HAdd.hAdd, ``HSub.hSub, ``HMul.hMul, ``HDiv.hDiv, ``HPow.hPow,
      ``Eq, ``Finset.sum, ``Finset.prod, ``And, ``Finset.Icc]
    if binary.contains name then
      return node name.toString #[← expressionJSON args[args.size-2]!, ← expressionJSON args[args.size-1]!]
    if name == ``Neg.neg || name == ``Finset.range then
      return node name.toString #[← expressionJSON args[args.size-1]!]
    if name == ``Int.ofNat || name == ``Int.toNat || name == ``Nat.cast then
      return node name.toString #[← expressionJSON args[args.size-1]!]
    if name == ``List.nil then
      return node "List.nil" #[]
    if name == ``List.cons then
      return node "List.cons" #[← expressionJSON args[args.size-2]!, ← expressionJSON args[args.size-1]!]
    if name == ``ite then
      return node "ite" #[← expressionJSON args[1]!, ← expressionJSON args[3]!, ← expressionJSON args[4]!]
    if name.toString == "FiniteQBenchmark.phi" || name.toString == "FiniteQBenchmark.sillsAlpha" then
      return node name.toString #[← expressionJSON args[args.size-5]!,
        ← expressionJSON args[args.size-4]!, ← expressionJSON args[args.size-3]!,
        ← expressionJSON args[args.size-2]!, ← expressionJSON args[args.size-1]!]
    if name.toString == "FiniteQBenchmark.kacPowerNat" then
      return node name.toString #[← expressionJSON args[args.size-4]!,
        ← expressionJSON args[args.size-3]!, ← expressionJSON args[args.size-2]!,
        ← expressionJSON args[args.size-1]!]
    if name.toString == "FiniteQBenchmark.gaussian" || name.toString == "FiniteQBenchmark.poch" ||
        name.toString == "FiniteQBenchmark.pochList" || name.toString == "FiniteQBenchmark.gaussianInt" ||
        name.toString == "FiniteQBenchmark.unitBailey" then
      return node name.toString #[← expressionJSON args[args.size-3]!,
        ← expressionJSON args[args.size-2]!, ← expressionJSON args[args.size-1]!]
  throwError "Unsupported expression in P1 frontend: {e}"
elab "p1_export" : tactic => withMainContext do
  let goal ← getMainTarget
  let data ← expressionJSON goal
  logInfo m!"P1_JSON:{data.compress}"
  let mut hypotheses : Array Json := #[]
  for decl in ← getLCtx do
    unless decl.isImplementationDetail do
      if (← isProp decl.type) then
        try
          let value ← expressionJSON decl.type
          hypotheses := hypotheses.push (Json.mkObj [("name", toJson decl.userName.toString), ("type", value)])
        catch _ => pure ()
  logInfo m!"P1_HYPOTHESES_JSON:{(toJson hypotheses).compress}"
  throwError "P1_EXPORT_ONLY"
end FiniteQP1

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-BAILEY-UNIT — 一般参数单位 Bailey 对
Original representative source: AQ-3.48
Frozen statement: formulas/train/FQI-BAILEY-UNIT.md
Source formula:
\sum_{r=0}^n\frac{u_r(a)}{(q;q)_{n-r}(aq;q)_{n+r}}=\delta_{n,0},\quad u_0(a)=1,\quad u_r(a)=\frac{(-1)^rq^{r(r-1)/2}(1-aq^{2r})(aq;q)_{r-1}}{(q;q)_r}\ (r\ge1).
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity020
variable {K : Type*} [Field K]

theorem statement (a q : K) (n : ℕ)
    (hunit : ∀ r ≤ n, poch q q r ≠ 0)
    (hden : ∀ r ≤ n, poch q q (n-r) * poch (a*q) q (n+r) ≠ 0) :
    (∑ r ∈ Finset.range (n+1), unitBailey a q r /
      (poch q q (n-r) * poch (a*q) q (n+r))) = if n = 0 then 1 else 0 := by
  p1_export
end FiniteQBenchmark.Identity020
