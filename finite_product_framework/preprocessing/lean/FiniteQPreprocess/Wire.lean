import Lean
open Lean
namespace FiniteQPreprocess

private structure WireState where
  nodes : Array Json := #[]
  index : Std.HashMap Json Nat := {}

private partial def intern (j : Json) : StateM WireState Json := do
  match j with
  | .arr _ | .obj _ => pure ()
  | _ => return j
  let node ← match j with
    | .arr a => pure <| Json.arr (← a.mapM intern)
    | .obj o => pure <| Json.mkObj (← o.toArray.toList.mapM fun (k, v) => do
        return (k, ← intern v))
    | _ => pure j
  let s ← get
  let n ← match s.index[node]? with
    | some n => pure n
    | none => do
      let n := s.nodes.size
      set ({ nodes := s.nodes.push node, index := s.index.insert node n } : WireState)
      pure n
  return Json.mkObj [("$ref", toJson n)]

def packWire (j : Json) : Json :=
  let (root, s) := (intern j).run {}
  Json.mkObj [("packet_version", toJson (2 : Nat)), ("nodes", toJson s.nodes), ("root", root)]

private def unref (values : Array Json) (j : Json) : Except String Json := do
  match j with
  | .obj o =>
    unless o.size == 1 do throw "wire_expected_reference"
    let n ← (← j.getObjVal? "$ref").getNat?
    match values[n]? with
    | some v => return v
    | none => throw "wire_forward_or_invalid_reference"
  | .arr _ => throw "wire_uninterned_array"
  | _ => return j

def unpackWire (j : Json) : Except String Json := do
  if !(j.getObjVal? "packet_version").isOk then return j
  unless (← (← j.getObjVal? "packet_version").getNat?) == 2 do
    throw "unsupported_wire_packet"
  let nodes ← (← j.getObjVal? "nodes").getArr?
  if nodes.size > 1000000 then throw "wire_node_budget"
  let mut values := #[]
  for node in nodes do
    let value ← match node with
      | .obj o => pure <| Json.mkObj (← o.toArray.toList.mapM fun (k, v) => do
          return (k, ← unref values v))
      | .arr a => pure <| Json.arr (← a.mapM (unref values))
      | _ => throw "wire_expected_container"
    values := values.push value
  unref values (← j.getObjVal? "root")
end FiniteQPreprocess
