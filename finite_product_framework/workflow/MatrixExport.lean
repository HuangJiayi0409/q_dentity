import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

open Lean Meta Elab Tactic
namespace MatrixSynthesisExport

private def numeral (e : Expr) : Option Nat :=
  match e.consumeMData with
  | .lit (.natVal n) => some n
  | e => if e.isAppOf ``OfNat.ofNat then
      match e.getAppArgs[1]! with
      | .lit (.natVal n) => some n
      | _ => none
    else none

private def size (ty : Expr) : MetaM Nat := do
  let ty ← whnf ty
  unless ty.isAppOf ``Fin do throwError "SYNTHESIS_UNSUPPORTED: Fin index required"
  let some n := numeral (← whnf ty.getAppArgs.back!) |
    throwError "SYNTHESIS_UNSUPPORTED: symbolic dimension is not implemented"
  unless 0 < n && n ≤ 5 do throwError "SYNTHESIS_UNSUPPORTED: dimension must be 1..5"
  return n

private def index (n i : Nat) : MetaM Expr := do
  let h ← mkDecideProof (← mkAppM ``LT.lt #[mkNatLit i, mkNatLit n])
  return mkApp3 (mkConst ``Fin.mk) (mkNatLit n) (mkNatLit i) h

/-- Only exact scalar arithmetic is interpreted. Other scalar terms are atoms. -/
partial def algebra (e : Expr) : StateT (Array Expr) MetaM Json := do
  let e := e.consumeMData.headBeta
  let args := e.getAppArgs
  if let some n := numeral e then
    return Json.mkObj [("op", toJson "integer"), ("value", toJson n)]
  if let .const name _ := e.getAppFn then
    if [``HAdd.hAdd, ``HSub.hSub, ``HMul.hMul, ``HDiv.hDiv].contains name then
      return Json.mkObj [("op", toJson name.toString),
        ("args", toJson #[← algebra args[args.size-2]!, ← algebra args.back!])]
    if name == ``Neg.neg || name == ``Inv.inv then
      return Json.mkObj [("op", toJson (if name == ``Neg.neg then "neg" else "inv")),
        ("arg", ← algebra args.back!)]
    if name == ``HPow.hPow then
      if let some n := numeral args.back! then
        if n ≤ 64 then
          return Json.mkObj [("op", toJson "pow"), ("exponent", toJson n),
            ("arg", ← algebra args[args.size-2]!)]
  let atoms ← get
  let mut key := atoms.size
  for i in [:atoms.size] do
    if ← isDefEq e atoms[i]! then key := i; break
  if key == atoms.size then set (atoms.push e)
  return Json.mkObj [("op", toJson "atom"), ("key", toJson key),
    ("display", toJson (← ppExpr e).pretty)]

private def simplifyEntry (e : Expr) : MetaM Expr := do
  let ctx ← Simp.mkContext (simpTheorems := #[← getSimpTheorems])
  let (result, _) ← simp e ctx
  return result.expr

private def matrix (a : Expr) (n : Nat) : StateT (Array Expr) MetaM Json := do
  let mut rows : Array (Array Json) := #[]
  for i in [:n] do
    let mut row := #[]
    for j in [:n] do
      row := row.push (← algebra (← simplifyEntry (mkApp2 a (← index n i) (← index n j))))
    rows := rows.push row
  return Json.mkObj [("display", toJson (← ppExpr a).pretty), ("entries", toJson rows)]

private def vector (a : Expr) (n : Nat) : StateT (Array Expr) MetaM Json := do
  let mut values := #[]
  for i in [:n] do values := values.push (← algebra (← simplifyEntry (mkApp a (← index n i))))
  return Json.mkObj [("display", toJson (← ppExpr a).pretty), ("entries", toJson values)]

private def factors (e : Expr) : MetaM (Expr × Expr) := do
  let e := e.consumeMData.headBeta
  unless e.isAppOf ``HMul.hMul do throwError "SYNTHESIS_UNSUPPORTED: product required"
  let args := e.getAppArgs
  return (args[args.size-2]!, args.back!)

private def sumBinder (e : Expr) : MetaM Expr := do
  let e := e.consumeMData.headBeta
  unless e.isAppOf ``Finset.sum do throwError "SYNTHESIS_UNSUPPORTED: finite sum required"
  let args := e.getAppArgs
  unless args[args.size-2]!.isAppOf ``Finset.univ do
    throwError "SYNTHESIS_UNSUPPORTED: full finite support required"
  return args.back!

private def determinant (lhs rhs : Expr) : MetaM Json := do
  let (a, reverse) ← if lhs.isAppOf ``Matrix.det then pure (lhs.getAppArgs.back!, false)
    else if rhs.isAppOf ``Matrix.det then pure (rhs.getAppArgs.back!, true)
    else throwError "SYNTHESIS_UNSUPPORTED: determinant side required"
  forallTelescopeReducing (← inferType a) fun xs ty => do
    unless xs.size == 2 do throwError "SYNTHESIS_UNSUPPORTED: matrix type required"
    let n ← size (← inferType xs[0]!)
    unless ← isDefEq (← inferType xs[0]!) (← inferType xs[1]!) do
      throwError "SYNTHESIS_UNSUPPORTED: square matrix required"
    let (value, _) ← (do
      return Json.mkObj [("matrix", ← matrix a n), ("size", toJson n),
        ("type", toJson (← ppExpr ty).pretty), ("reverse", toJson reverse)]).run #[]
    return value

private def kernel (lhs rhs : Expr) : MetaM Json := do
  lambdaTelescope lhs fun is body => do
    unless is.size == 1 do throwError "SYNTHESIS_UNSUPPORTED: kernel action lambda required"
    let i := is[0]!
    let n ← size (← inferType i)
    lambdaTelescope (← sumBinder body) fun ks term => do
      unless ks.size == 1 do throwError "SYNTHESIS_UNSUPPORTED: one kernel index required"
      let k := ks[0]!
      unless ← isDefEq (← inferType i) (← inferType k) do throwError "SYNTHESIS_UNSUPPORTED: square kernel required"
      let (aik, inner) ← factors term
      lambdaTelescope (← sumBinder inner) fun js term => do
        unless js.size == 1 do throwError "SYNTHESIS_UNSUPPORTED: one vector index required"
        let j := js[0]!
        unless ← isDefEq (← inferType i) (← inferType j) do throwError "SYNTHESIS_UNSUPPORTED: square kernel required"
        let (bkj, vj) ← factors term
        let a ← mkLambdaFVars #[i,k] aik
        let b ← mkLambdaFVars #[k,j] bkj
        let v ← mkLambdaFVars #[j] vj
        let c ← if ← isDefEq v rhs then pure none else
          lambdaTelescope rhs fun ris rbody => do
            unless ris.size == 1 do throwError "SYNTHESIS_UNSUPPORTED: action target required"
            unless ← isDefEq (← inferType ris[0]!) (← inferType i) do throwError "SYNTHESIS_UNSUPPORTED: target index mismatch"
            lambdaTelescope (← sumBinder rbody) fun rjs rterm => do
              unless rjs.size == 1 do throwError "SYNTHESIS_UNSUPPORTED: target vector index required"
              let (cij, rvj) ← factors rterm
              let rv ← mkLambdaFVars rjs rvj
              unless ← isDefEq rv v do throwError "SYNTHESIS_UNSUPPORTED: target vector mismatch"
              return some (← mkLambdaFVars #[ris[0]!, rjs[0]!] cij)
        let ty ← inferType aik
        let (value, _) ← (do
          return Json.mkObj [("matrix", ← matrix a n), ("proposed_inverse", ← matrix b n),
            ("operation", toJson (if c.isSome then "composition" else "inverse")),
            ("target_kernel", ← match c with | some c => matrix c n | none => pure Json.null),
            ("vector", toJson (← ppExpr v).pretty), ("size", toJson n),
            ("type", toJson (← ppExpr ty).pretty)]).run #[]
        return value

private def spectral (lhs rhs : Expr) : MetaM Json := do
  unless numeral rhs == some 0 do throwError "SYNTHESIS_UNSUPPORTED: zero pairing target required"
  lambdaTelescope (← sumBinder lhs) fun xs term => do
    unless xs.size == 1 do throwError "SYNTHESIS_UNSUPPORTED: one pairing index required"
    let i := xs[0]!
    let n ← size (← inferType i)
    let (wf, gi) ← factors term
    let (wi, fi) ← factors wf
    let w ← mkLambdaFVars #[i] wi
    let f ← mkLambdaFVars #[i] fi
    let g ← mkLambdaFVars #[i] gi
    let ty ← inferType wi
    let (value, _) ← (do
      return Json.mkObj [("weight", ← vector w n), ("left", ← vector f n),
        ("right", ← vector g n), ("size", toJson n), ("type", toJson (← ppExpr ty).pretty)]).run #[]
    return value

elab "matrix_synthesis_export" kind:str : tactic => withMainContext do
  let target ← instantiateMVars (← getMainTarget)
  let some (_, lhs, rhs) := target.eq? | throwError "SYNTHESIS_UNSUPPORTED: equality required"
  let result ← match kind.getString with
    | "determinant" => determinant lhs rhs
    | "kernel_transform" => kernel lhs rhs
    | "spectral" => spectral lhs rhs
    | _ => throwError "unknown synthesis method"
  logInfo m!"MATRIX_SYNTHESIS_JSON:{result.compress}"
  throwError "MATRIX_SYNTHESIS_EXPORT_ONLY"
end MatrixSynthesisExport
