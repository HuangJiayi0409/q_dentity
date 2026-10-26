import Lean
import Mathlib.Tactic
open Lean Meta Elab Tactic
namespace FiniteQP2

/-- Syntactic polynomial reification. Unknown variable-dependent functions and
variable-dependent denominators are rejected, never interpreted as coefficients. -/
partial def liftPolynomial (e x : Expr) : MetaM Expr := do
  let e := e.consumeMData
  if e == x then
    return ← mkAppOptM ``Polynomial.X #[some (← inferType x), none]
  if !e.containsFVar x.fvarId! then
    let c ← mkAppOptM ``Polynomial.C #[some (← inferType e), none]
    return ← mkAppM ``DFunLike.coe #[c, e]
  let args := e.getAppArgs
  let name := e.getAppFn.constName!
  if [``HAdd.hAdd, ``HSub.hSub, ``HMul.hMul].contains name then
    return ← mkAppM name #[← liftPolynomial args[args.size-2]! x,
                          ← liftPolynomial args.back! x]
  if name == ``Neg.neg then
    return ← mkAppM name #[← liftPolynomial args.back! x]
  if name == ``HPow.hPow && !(args.back!.containsFVar x.fvarId!) then
    unless ← isDefEq (← inferType args.back!) (mkConst ``Nat) do
      throwError "P2_POLYNOMIAL_DOMAIN: only natural polynomial exponents"
    return ← mkAppM name #[← liftPolynomial args[args.size-2]! x, args.back!]
  if name == ``FiniteQBenchmark.rogersSzego then
    let q := args[args.size-2]!
    let n := args.back!
    if q.containsFVar x.fvarId! || n.containsFVar x.fvarId! then
      throwError "P2_POLYNOMIAL_DOMAIN: coefficient parameter depends on variable"
    return ← mkAppM ``Polynomial.comp #[← mkAppM ``FiniteQP2.gaussianPoly #[q,n],
                                        ← liftPolynomial args[args.size-3]! x]
  if name == ``Finset.sum then
    let domain := args[args.size-2]!
    if domain.containsFVar x.fvarId! then
      throwError "P2_POLYNOMIAL_DOMAIN: variable-dependent support"
    let fn ← whnf args.back!
    if let .lam nm ty body bi := fn then
      return ← withLocalDecl nm bi ty fun k => do
        let term ← liftPolynomial (body.instantiate1 k) x
        mkAppM ``Finset.sum #[domain, ← mkLambdaFVars #[k] term]
  throwError "P2_POLYNOMIAL_DOMAIN: unsupported variable-dependent atom {e}"

/-- Reification is followed by a kernel-checked evaluation bridge. No assumed
polynomial identity or sample-point interpolation is used. -/
elab "p2_lift_polynomial" : tactic => withMainContext do
  let target ← getMainTarget
  let some (ty,lhs,rhs) := target.eq? | throwError "P2_POLYNOMIAL_DOMAIN: equality required"
  let initial ← saveState
  let mut tried := 0
  let mut failures : Array String := #[]
  for decl in ← getLCtx do
    if decl.isImplementationDetail then continue
    let x := decl.toExpr
    if !(target.containsFVar decl.fvarId) then continue
    if !(← isDefEq decl.type ty) then continue
    if tried >= 8 then break
    tried := tried + 1
    try
      let lp ← liftPolynomial lhs x
      let rp ← liftPolynomial rhs x
      let a ← Term.exprToSyntax lp
      let b ← Term.exprToSyntax rp
      let v ← Term.exprToSyntax x
      evalTactic (← `(tactic|
        suffices p2_polynomial_identity : $a = $b by
          have p2_eval_identity := FiniteQP2.eval_of_poly_eq $v $a $b p2_polynomial_identity
          simpa only [Polynomial.eval_add, Polynomial.eval_sub, Polynomial.eval_mul,
            Polynomial.eval_neg, Polynomial.eval_pow, Polynomial.eval_C, Polynomial.eval_X,
            Polynomial.eval_comp, Polynomial.eval_finsetSum, FiniteQP2.eval_gaussianPoly]
            using p2_eval_identity))
      logInfo m!"P2_POLYNOMIAL_VARIABLE:{← ppExpr x}"
      return
    catch ex =>
      let detail ← ex.toMessageData.toString
      initial.restore
      failures := failures.push s!"{decl.userName}: {detail}"
  for detail in failures do logInfo m!"P2_POLYNOMIAL_REJECTION:{detail}"
  throwError "P2_POLYNOMIAL_DOMAIN: no certified single-variable representation"

end FiniteQP2
