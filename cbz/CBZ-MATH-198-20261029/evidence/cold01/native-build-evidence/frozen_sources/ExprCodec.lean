import Lean
open Lean
namespace ClosedProof.ExprCodec
/- Adapted from Lean/Elab/Idbg.lean lines 29–157, Lean FRO LLC, Apache-2.0; see LICENSE. -/
/-- Custom `Name` serialization that preserves the exact structure.
The standard `ToJson`/`FromJson Name` uses `toString`/`toName` which doesn't
round-trip for hygienic names (e.g., names containing `@`). -/
def nameToJson : Name → Json
  | .anonymous => Json.null
  | .str p s   => Json.mkObj [("str", Json.arr #[nameToJson p, toJson s])]
  | .num p n   => Json.mkObj [("num", Json.arr #[nameToJson p, n])]

/-- Inverse of `nameToJson`. -/
partial def nameFromJson? (j : Json) : Except String Name := do
  if j.isNull then return .anonymous
  if let some arr := (j.getObjVal? "str").toOption then
    let #[p, s] := (← fromJson? arr : Array Json) | .error "str expects 2 elements"
    return .str (← nameFromJson? p) (← fromJson? s)
  if let some arr := (j.getObjVal? "num").toOption then
    let #[p, n] := (← fromJson? arr : Array Json) | .error "num expects 2 elements"
    return .num (← nameFromJson? p) (← fromJson? n)
  .error s!"expected Name, got {j}"

/-- Serialize `BinderInfo` to JSON. -/
def binderInfoToJson : BinderInfo → Json
  | .default        => "default"
  | .implicit       => "implicit"
  | .strictImplicit => "strictImplicit"
  | .instImplicit   => "instImplicit"

/-- Deserialize `BinderInfo` from JSON. -/
def binderInfoFromJson? : Json → Except String BinderInfo
  | .str "default"        => .ok .default
  | .str "implicit"       => .ok .implicit
  | .str "strictImplicit" => .ok .strictImplicit
  | .str "instImplicit"   => .ok .instImplicit
  | j => .error s!"expected BinderInfo, got {j}"

/-- Serialize `Literal` to JSON. -/
def literalToJson : Literal → Json
  | .natVal n => Json.mkObj [("natVal", n)]
  | .strVal s => Json.mkObj [("strVal", s)]

/-- Deserialize `Literal` from JSON. -/
def literalFromJson? (j : Json) : Except String Literal := do
  if let some n := (j.getObjVal? "natVal").toOption then
    return .natVal (← fromJson? n)
  if let some s := (j.getObjVal? "strVal").toOption then
    return .strVal (← fromJson? s)
  .error s!"expected Literal, got {j}"

/-- Serialize `Level` to JSON. -/
partial def levelToJson : Level → Json
  | .zero     => Json.mkObj [("zero", Json.null)]
  | .succ l   => Json.mkObj [("succ", levelToJson l)]
  | .max a b  => Json.mkObj [("max", Json.arr #[levelToJson a, levelToJson b])]
  | .imax a b => Json.mkObj [("imax", Json.arr #[levelToJson a, levelToJson b])]
  | .param n  => Json.mkObj [("param", nameToJson n)]
  | .mvar id  => Json.mkObj [("mvar", nameToJson id.name)]

/-- Deserialize `Level` from JSON. -/
partial def levelFromJson? (j : Json) : Except String Level := do
  if (j.getObjVal? "zero").toOption.isSome then
    return .zero
  if let some l := (j.getObjVal? "succ").toOption then
    return .succ (← levelFromJson? l)
  if let some arr := (j.getObjVal? "max").toOption then
    let #[a, b] := (← fromJson? arr : Array Json) | .error "max expects 2 elements"
    return .max (← levelFromJson? a) (← levelFromJson? b)
  if let some arr := (j.getObjVal? "imax").toOption then
    let #[a, b] := (← fromJson? arr : Array Json) | .error "imax expects 2 elements"
    return .imax (← levelFromJson? a) (← levelFromJson? b)
  if let some n := (j.getObjVal? "param").toOption then
    return .param (← nameFromJson? n)
  if let some n := (j.getObjVal? "mvar").toOption then
    return .mvar ⟨← nameFromJson? n⟩
  .error s!"expected Level, got {j}"

/-- Serialize `Expr` to JSON. Metadata is stripped; free variables are preserved. -/
partial def exprToJson : Expr → Json
  | .bvar i          => Json.mkObj [("bvar", i)]
  | .fvar id         => Json.mkObj [("fvar", nameToJson id.name)]
  | .mvar id         => Json.mkObj [("mvar", nameToJson id.name)]
  | .sort l          => Json.mkObj [("sort", levelToJson l)]
  | .const n ls      => Json.mkObj [("const", nameToJson n), ("levels", Json.arr (ls.toArray.map levelToJson))]
  | .app fn arg      => Json.mkObj [("app", Json.arr #[exprToJson fn, exprToJson arg])]
  | .lam n ty b bi   => Json.mkObj [("lam", Json.mkObj [("name", nameToJson n), ("type", exprToJson ty), ("body", exprToJson b), ("bi", binderInfoToJson bi)])]
  | .forallE n ty b bi => Json.mkObj [("forallE", Json.mkObj [("name", nameToJson n), ("type", exprToJson ty), ("body", exprToJson b), ("bi", binderInfoToJson bi)])]
  | .letE n ty v b nd => Json.mkObj [("letE", Json.mkObj [("name", nameToJson n), ("type", exprToJson ty), ("value", exprToJson v), ("body", exprToJson b), ("nondep", nd)])]
  | .lit l           => Json.mkObj [("lit", literalToJson l)]
  | .mdata _ e       => exprToJson e  -- strip metadata
  | .proj tn i s     => Json.mkObj [("proj", Json.mkObj [("typeName", nameToJson tn), ("idx", i), ("struct", exprToJson s)])]

/-- Deserialize `Expr` from JSON. -/
partial def exprFromJson? (j : Json) : Except String Expr := do
  if let some i := (j.getObjVal? "bvar").toOption then
    return .bvar (← fromJson? i)
  if let some id := (j.getObjVal? "fvar").toOption then
    return .fvar ⟨← nameFromJson? id⟩
  if let some id := (j.getObjVal? "mvar").toOption then
    return .mvar ⟨← nameFromJson? id⟩
  if let some l := (j.getObjVal? "sort").toOption then
    return .sort (← levelFromJson? l)
  if (j.getObjVal? "const").toOption.isSome then
    let n ← nameFromJson? (← j.getObjVal? "const")
    let ls : Array Json ← fromJson? (← j.getObjVal? "levels")
    return .const n (← ls.toList.mapM levelFromJson?)
  if let some arr := (j.getObjVal? "app").toOption then
    let #[fn, arg] := (← fromJson? arr : Array Json) | .error "app expects 2 elements"
    return .app (← exprFromJson? fn) (← exprFromJson? arg)
  if let some obj := (j.getObjVal? "lam").toOption then
    return .lam (← nameFromJson? (← obj.getObjVal? "name"))
      (← exprFromJson? (← obj.getObjVal? "type"))
      (← exprFromJson? (← obj.getObjVal? "body"))
      (← binderInfoFromJson? (← obj.getObjVal? "bi"))
  if let some obj := (j.getObjVal? "forallE").toOption then
    return .forallE (← nameFromJson? (← obj.getObjVal? "name"))
      (← exprFromJson? (← obj.getObjVal? "type"))
      (← exprFromJson? (← obj.getObjVal? "body"))
      (← binderInfoFromJson? (← obj.getObjVal? "bi"))
  if let some obj := (j.getObjVal? "letE").toOption then
    return .letE (← nameFromJson? (← obj.getObjVal? "name"))
      (← exprFromJson? (← obj.getObjVal? "type"))
      (← exprFromJson? (← obj.getObjVal? "value"))
      (← exprFromJson? (← obj.getObjVal? "body"))
      (← fromJson? (← obj.getObjVal? "nondep"))
  if let some l := (j.getObjVal? "lit").toOption then
    return .lit (← literalFromJson? l)
  if let some obj := (j.getObjVal? "proj").toOption then
    return .proj (← nameFromJson? (← obj.getObjVal? "typeName"))
      (← fromJson? (← obj.getObjVal? "idx"))
      (← exprFromJson? (← obj.getObjVal? "struct"))
  .error s!"expected Expr, got {j}"
end ClosedProof.ExprCodec
