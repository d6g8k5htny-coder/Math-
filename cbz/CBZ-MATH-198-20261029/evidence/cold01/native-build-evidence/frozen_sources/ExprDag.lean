import ExprCodec
open Lean
namespace ClosedProof.ExprDag

structure Encoder where
  memo : ExprStructMap Nat := {}
  nodes : Array Json := #[]

partial def intern (e : Expr) : StateM Encoder Nat := do
  if let .mdata _ body := e then return ← intern body
  if let some index := (← get).memo[(⟨e⟩ : ExprStructEq)]? then return index
  let node ← match e with
    | .bvar i => pure <| Json.mkObj [("bvar", toJson i)]
    | .fvar id => pure <| Json.mkObj [("fvar", ExprCodec.nameToJson id.name)]
    | .mvar id => pure <| Json.mkObj [("mvar", ExprCodec.nameToJson id.name)]
    | .sort l => pure <| Json.mkObj [("sort", ExprCodec.levelToJson l)]
    | .const n ls => pure <| Json.mkObj [("const", ExprCodec.nameToJson n), ("levels", toJson (ls.toArray.map ExprCodec.levelToJson))]
    | .app f a =>
      let fi ← intern f
      let ai ← intern a
      pure <| Json.mkObj [("app", toJson #[fi, ai])]
    | .lam n ty body bi =>
      let ti ← intern ty
      let b ← intern body
      pure <| Json.mkObj [("lam", Json.mkObj [("name", ExprCodec.nameToJson n), ("type", toJson ti), ("body", toJson b), ("bi", ExprCodec.binderInfoToJson bi)])]
    | .forallE n ty body bi =>
      let ti ← intern ty
      let b ← intern body
      pure <| Json.mkObj [("forallE", Json.mkObj [("name", ExprCodec.nameToJson n), ("type", toJson ti), ("body", toJson b), ("bi", ExprCodec.binderInfoToJson bi)])]
    | .letE n ty value body nd =>
      let ti ← intern ty
      let vi ← intern value
      let b ← intern body
      pure <| Json.mkObj [("letE", Json.mkObj [("name", ExprCodec.nameToJson n), ("type", toJson ti), ("value", toJson vi), ("body", toJson b), ("nondep", toJson nd)])]
    | .lit l => pure <| Json.mkObj [("lit", ExprCodec.literalToJson l)]
    | .proj n i s =>
      let si ← intern s
      pure <| Json.mkObj [("proj", Json.mkObj [("typeName", ExprCodec.nameToJson n), ("idx", toJson i), ("struct", toJson si)])]
    | .mdata _ _ => unreachable!
  let state ← get
  let index := state.nodes.size
  set ({ memo := state.memo.insert ⟨e⟩ index, nodes := state.nodes.push node } : Encoder)
  return index

def encode (e : Expr) : Json :=
  let (root, state) := (intern e).run {}
  Json.mkObj [("schema", toJson "ul-expr-dag-v1"), ("nodes", Json.arr state.nodes), ("root", toJson root)]

def decodeNode (row : Json) (expressions : Array Expr) : Except String Expr := do
  let ref (j : Json) : Except String Expr := do
    let index ← j.getNat?
    match expressions[index]? with
    | some e => return e
    | none => throw "DAG reference must point to an earlier node"
  if let .ok i := row.getObjVal? "bvar" then return Expr.bvar (← i.getNat?)
  if let .ok id := row.getObjVal? "fvar" then return .fvar ⟨← ExprCodec.nameFromJson? id⟩
  if let .ok id := row.getObjVal? "mvar" then return .mvar ⟨← ExprCodec.nameFromJson? id⟩
  if let .ok l := row.getObjVal? "sort" then return .sort (← ExprCodec.levelFromJson? l)
  if let .ok n := row.getObjVal? "const" then
    let ls : Array Json ← fromJson? (← row.getObjVal? "levels")
    return .const (← ExprCodec.nameFromJson? n) (← ls.toList.mapM ExprCodec.levelFromJson?)
  if let .ok app := row.getObjVal? "app" then
    let #[f, a] := (← fromJson? app : Array Json) | throw "app requires two refs"
    return .app (← ref f) (← ref a)
  if let .ok o := row.getObjVal? "lam" then
    return .lam (← ExprCodec.nameFromJson? (← o.getObjVal? "name"))
      (← ref (← o.getObjVal? "type")) (← ref (← o.getObjVal? "body"))
      (← ExprCodec.binderInfoFromJson? (← o.getObjVal? "bi"))
  if let .ok o := row.getObjVal? "forallE" then
    return .forallE (← ExprCodec.nameFromJson? (← o.getObjVal? "name"))
      (← ref (← o.getObjVal? "type")) (← ref (← o.getObjVal? "body"))
      (← ExprCodec.binderInfoFromJson? (← o.getObjVal? "bi"))
  if let .ok o := row.getObjVal? "letE" then
    return .letE (← ExprCodec.nameFromJson? (← o.getObjVal? "name"))
      (← ref (← o.getObjVal? "type")) (← ref (← o.getObjVal? "value"))
      (← ref (← o.getObjVal? "body")) (← fromJson? (← o.getObjVal? "nondep"))
  if let .ok l := row.getObjVal? "lit" then return .lit (← ExprCodec.literalFromJson? l)
  if let .ok o := row.getObjVal? "proj" then
    return .proj (← ExprCodec.nameFromJson? (← o.getObjVal? "typeName"))
      (← o.getObjVal? "idx" >>= Json.getNat?) (← ref (← o.getObjVal? "struct"))
  throw "unknown expression DAG node"

def decode (wire : Json) : Except String Expr := do
  unless (← wire.getObjVal? "schema" >>= Json.getStr?) == "ul-expr-dag-v1" do
    throw "unknown expression DAG schema"
  let rows : Array Json ← fromJson? (← wire.getObjVal? "nodes")
  let mut expressions : Array Expr := #[]
  for row in rows do
    let node ← decodeNode row expressions
    expressions := expressions.push node
  match expressions[← wire.getObjVal? "root" >>= Json.getNat?]? with
  | some e => return e
  | none => throw "expression DAG root is missing"

end ClosedProof.ExprDag
