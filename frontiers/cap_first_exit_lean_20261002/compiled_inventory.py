"""Cap-only compiled admission. Protocol primitives adapted from RF-GATE-01.

Supplied text is not execution authentication. The gate must run the pinned Lean
exporter and preserve its actual exit, streams, program/source/object identities.
"""
import hashlib
import re

MODULE_NAME = ('CapFirstExit',)
ALLOWED = frozenset({'propext', 'Classical.choice', 'Quot.sound'})
KINDS = {'theorem', 'def', 'axiom', 'opaque', 'inductive', 'ctor', 'rec', 'quot'}
COMPONENT = r'(?:s(?:[0-9a-f]{2})*|n(?:0|[1-9][0-9]*))'
ENC = re.compile(COMPONENT + r'(?:/' + COMPONENT + r')*')
AUX_SUFFIX = re.compile(r'_proof_[0-9]+|_simp_[0-9]+_[0-9]+|_abel_[0-9]+_[0-9]+|eq_[0-9]+|eq_def|match_[0-9]+')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def decode(encoded):
    require(isinstance(encoded, str) and ENC.fullmatch(encoded), 'protocol: malformed encoded name')
    result = []
    for part in encoded.split('/'):
        if part[0] == 'n':
            result.append(int(part[1:]))
        else:
            try:
                result.append(bytes.fromhex(part[1:]).decode('utf-8'))
            except (ValueError, UnicodeDecodeError):
                raise ValueError('protocol: invalid UTF8 name') from None
    return tuple(result)


def encode(name):
    require(isinstance(name, tuple) and name, 'protocol: empty name')
    require(all(isinstance(x, str) or (type(x) is int and x >= 0) for x in name), 'protocol: invalid name component')
    return '/'.join('n' + str(x) if type(x) is int else 's' + x.encode('utf-8').hex() for x in name)


def dotted(name):
    require(isinstance(name, str) and name and all(p and not any(c.isspace() or c in '«»/|' for c in p)
            for p in name.split('.')), 'unsupported visible name')
    return tuple(name.split('.'))


def render(name):
    return '.'.join(str(x) if type(x) is int else x for x in name)


def parse_inventory(text):
    require(isinstance(text, str), 'protocol: transcript is not text')
    modules, constants, relations, axioms, closures, extras = [], [], [], [], [], []
    lines = []
    for line in text.splitlines():
        if not line:
            continue
        lines.append(line)
        fields = line.split('|')
        tag = fields[0]
        if tag == 'MODULE':
            require(len(fields) == 5 and fields[2] in ('true', 'false')
                    and all(re.fullmatch(r'0|[1-9][0-9]*', n) for n in fields[3:]), 'protocol: invalid MODULE')
            modules.append((decode(fields[1]), fields[2] == 'true', int(fields[3]), int(fields[4])))
        elif tag == 'INV':
            require(len(fields) == 6 and fields[1] in KINDS and fields[2] in ('user', 'aux')
                    and fields[5] in ('safe', 'unsafe', 'partial'), 'protocol: invalid INV')
            constants.append((fields[1], fields[2], decode(fields[3]), decode(fields[4]), fields[5]))
        elif tag == 'REL':
            require(len(fields) == 4 and fields[1] in ('projection','constructor','recursor','no_confusion','aux_recursor'),
                    'protocol: invalid REL')
            relations.append((fields[1], decode(fields[2]), decode(fields[3])))
        elif tag == 'EXTRA':
            require(len(fields) == 3, 'protocol: invalid EXTRA')
            extras.append((decode(fields[1]),decode(fields[2])))
        elif tag == 'AXIOMS':
            require(len(fields) == 2, 'protocol: invalid AXIOMS')
            axioms.append([] if fields[1] == '' else [decode(x) for x in fields[1].split(',')])
        elif tag == 'CLOSURE':
            require(len(fields) == 2 and re.fullmatch(r'0|[1-9][0-9]*', fields[1]), 'protocol: invalid CLOSURE')
            closures.append(int(fields[1]))
        else:
            raise ValueError('protocol: unrecognized output: ' + line)
    require(len(axioms) == 1 and len(closures) == 1, 'protocol: one AXIOMS and CLOSURE required')
    require(constants, 'protocol: empty constant census')
    return dict(modules=modules, constants=constants, relations=relations, extras=extras,
                axioms=axioms[0], closure=closures[0], lines=lines)


def parse_binding(records, visible):
    require(isinstance(records, list), 'compiled binding absent; actual pinned census required')
    result, names = set(), set()
    for row in records:
        require(isinstance(row, list) and len(row) == 5 and all(isinstance(x, str) for x in row), 'invalid binding record')
        kind, origin, module, name, safety = row
        require(kind in KINDS and origin in ('user', 'aux') and safety in ('safe','unsafe','partial'), 'invalid binding kind')
        try:
            item = kind, origin, decode(module), decode(name), safety
        except ValueError as exc:
            raise ValueError('binding: ' + str(exc)) from None
        require(item[2] == MODULE_NAME, 'binding outside module')
        require(item[3] not in visible, 'target_shadowing in binding')
        require(item[3] not in names, 'duplicate_binding')
        names.add(item[3]); result.add(item)
    return frozenset(result)


def parse_codegen(records):
    require(isinstance(records,list), 'codegen binding absent')
    result=set()
    for row in records:
        require(isinstance(row,list) and len(row)==2, 'invalid codegen binding')
        item=decode(row[0]),decode(row[1])
        require(item[0]==MODULE_NAME and item not in result, 'invalid or duplicate codegen binding')
        result.add(item)
    return result


def inventory_violations(inventory, visible_kinds, bound_records, reported_axioms=None, codegen_records=None):
    require(isinstance(visible_kinds, dict) and visible_kinds, 'empty visible declaration map')
    visible = {dotted(name): kind for name, kind in visible_kinds.items()}
    require(all(kind in ('theorem','def','inductive') for kind in visible.values()), 'invalid visible kind')
    bound = parse_binding(bound_records, visible)
    codegen = parse_codegen([] if codegen_records is None else codegen_records)
    findings = set()
    def flag(code, name=(), note=''):
        findings.add((code, encode(name) if name else '', note))
    module_counts = {}
    for module, is_module, count, extra in inventory['modules']:
        if module in module_counts:
            flag('duplicate_module', module)
        module_counts[module] = count
        if module != MODULE_NAME:
            flag('unregistered_module', module)
        if is_module:
            flag('module_system', module)
        if extra != sum(owner==module for owner,name in inventory['extras']):
            flag('codegen_extra', module)
    if MODULE_NAME not in module_counts:
        flag('missing_module', MODULE_NAME)
    if len(set(inventory['extras'])) != len(inventory['extras']):
        flag('duplicate_codegen',MODULE_NAME)
    for module,name in set(inventory['extras']) ^ codegen:
        flag('codegen_binding',name)
    for module,name in inventory['extras']:
        if module != MODULE_NAME:
            flag('codegen_outside_module',name)
    constants, observed = {}, set()
    for row in inventory['constants']:
        kind, origin, module, name, safety = row
        if name in constants:
            flag('duplicate_name', name)
        constants[name] = row
        if module != MODULE_NAME:
            flag('outside_module', name)
        if kind == 'axiom':
            flag('package_axiom', name)
        if kind in ('opaque','quot'):
            flag('unsupported_owned_kind', name)
        if safety != 'safe':
            flag('unsafe_or_partial', name)
        if name in visible:
            if kind != visible[name] or origin != 'user':
                flag('visible_kind', name)
        else:
            observed.add(row)
            if row not in bound:
                flag('unregistered_constant', name)
    actual_count = sum(row[2] == MODULE_NAME for row in inventory['constants'])
    if MODULE_NAME in module_counts and actual_count != module_counts[MODULE_NAME]:
        flag('count_mismatch', MODULE_NAME)
    for name in visible.keys() - constants.keys():
        flag('missing_visible', name)
    for row in bound - observed:
        flag('missing_constant', row[3])
    relation_map = {}
    expected_relation_kinds = {'projection': {'def','theorem'}, 'constructor': {'ctor'}, 'recursor': {'rec'},
                               'no_confusion': {'def'}, 'aux_recursor': {'def'}}
    for relation, name, parent in inventory['relations']:
        valid = (name not in relation_map and parent in visible and visible[parent] == 'inductive'
                 and name in constants and constants[name][0] in expected_relation_kinds[relation])
        if not valid:
            flag('invalid_structural_relation', name)
        relation_map[name] = relation, parent
    user_names = {name for name, row in constants.items() if row[1] == 'user'}
    for name, row in constants.items():
        kind, origin, module, _, safety = row
        if name in visible:
            continue
        if origin == 'user' and kind == 'theorem' and relation_map.get(name, (None,))[0] != 'projection':
            flag('extra_user_theorem', name)
        if origin == 'user' and kind in ('def','inductive','opaque') and name not in relation_map:
            flag('extra_user_definition', name)
        if kind in ('ctor','rec') and name not in relation_map:
            flag('invalid_structural_relation', name)
        if origin == 'aux' and kind == 'theorem':
            parents = [name[:i] for i in range(len(name)-1, 0, -1) if name[:i] in user_names]
            if not parents or not all(isinstance(c, str) and AUX_SUFFIX.fullmatch(c) for c in name[len(parents[0]):]):
                flag('unbound_auxiliary', name)
    axioms = set(inventory['axioms'])
    if len(axioms) != len(inventory['axioms']):
        flag('duplicate_axiom')
    for axiom in axioms - {dotted(a) for a in ALLOWED}:
        flag('forbidden_axiom', axiom)
    if reported_axioms is not None:
        reported = {dotted(a) for values in reported_axioms.values() for a in values}
        for axiom in reported - axioms:
            flag('reported_axiom_omitted', axiom)
    if inventory['closure'] < len(inventory['constants']):
        flag('impossible_closure')
    return sorted(findings)


def audit_inventory(text, visible_kinds, bound_records, reported_axioms=None, codegen_records=None):
    inventory = parse_inventory(text)
    findings = inventory_violations(inventory, visible_kinds, bound_records, reported_axioms, codegen_records)
    require(not findings, 'compiled inventory rejected: ' + '; '.join(code+' '+name for code,name,note in findings))
    return dict(declarations=len(inventory['constants']), visible_declarations=len(visible_kinds),codegen_entries=len(inventory['extras']),
                axioms=sorted(render(a) for a in inventory['axioms']), closure=inventory['closure'],
                sha256=hashlib.sha256('\n'.join(inventory['lines']).encode()).hexdigest())


def inventory_source():
    """Pinned Lean module-table exporter; structure relations come from environment metadata."""
    return r'''import CapFirstExit
import Lean
open Lean

def _cap.kind : ConstantInfo → String
  | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec" | .quotInfo _ => "quot"
def _cap.safety (ci : ConstantInfo) : String :=
  if ci.isUnsafe then "unsafe" else
    match ci with
    | .defnInfo v => match v.safety with
      | .safe => "safe" | .unsafe => "unsafe" | .partial => "partial"
    | _ => "safe"
def _cap.hex (s : String) : String :=
  s.toUTF8.foldl (fun acc b => acc ++ (if b.toNat < 16 then "0" else "") ++ String.ofList (Nat.toDigits 16 b.toNat)) ""
def _cap.join (a b : String) : String := if a.isEmpty then b else a ++ "/" ++ b
def _cap.enc : Name → String
  | .anonymous => ""
  | .str p s => _cap.join (_cap.enc p) ("s" ++ _cap.hex s)
  | .num p k => _cap.join (_cap.enc p) ("n" ++ toString k)
structure _cap.St where
  visited : NameSet := {}
  axioms : NameSet := {}
  missing : NameSet := {}
partial def _cap.collect (env : Environment) (c : Name) : StateM _cap.St Unit := do
  unless (← get).visited.contains c do
    modify fun s => { s with visited := s.visited.insert c }
    let expr (e : Expr) : StateM _cap.St Unit := e.getUsedConstants.forM (_cap.collect env)
    match env.find? c with
    | some (.axiomInfo v) => modify (fun s => { s with axioms := s.axioms.insert c }) *> expr v.type
    | some (.defnInfo v) => expr v.type *> expr v.value
    | some (.thmInfo v) => expr v.type *> expr v.value
    | some (.opaqueInfo v) => expr v.type *> expr v.value
    | some (.quotInfo _) => pure ()
    | some (.ctorInfo v) => expr v.type
    | some (.recInfo v) => expr v.type
    | some (.inductInfo v) => expr v.type *> v.ctors.forM (_cap.collect env)
    | none => modify fun s => { s with missing := s.missing.insert c }
def _cap.main : CoreM Unit := do
  let env ← getEnv
  let header := env.header
  let names := header.moduleNames
  let mut owned : Array (Name × ConstantInfo × Name) := #[]
  for h : idx in [0:names.size] do
    let m := names[idx]
    if (`CapFirstExit).isPrefixOf m then
      let data := header.moduleData[idx]!
      IO.println s!"MODULE|{_cap.enc m}|{data.isModule}|{data.constNames.size}|{data.extraConstNames.size}"
      for c in data.extraConstNames do
        IO.println s!"EXTRA|{_cap.enc m}|{_cap.enc c}"
      for c in data.constNames do
        match env.find? c with
        | some ci => owned := owned.push (c, ci, m)
        | none => throwError "module constant missing from environment"
  let sorted := owned.qsort (fun a b => _cap.enc a.1 < _cap.enc b.1)
  for (c, ci, m) in sorted do
    let origin := if (← findDeclarationRanges? c).isSome then "user" else "aux"
    IO.println s!"INV|{_cap.kind ci}|{origin}|{_cap.enc m}|{_cap.enc c}|{_cap.safety ci}"
  let structName := `CapFirstExit.CapHyp
  if let some info := getStructureInfo? env structName then
    let ctor := getStructureCtor env structName
    IO.println s!"REL|constructor|{_cap.enc ctor.name}|{_cap.enc structName}"
    for field in info.fieldInfo do
      IO.println s!"REL|projection|{_cap.enc field.projFn}|{_cap.enc structName}"
    for (c, ci, _) in sorted do
      if c.getPrefix == structName then
        match ci with
        | .recInfo _ => IO.println s!"REL|recursor|{_cap.enc c}|{_cap.enc structName}"
        | _ =>
          if isAuxRecursor env c then
            IO.println s!"REL|aux_recursor|{_cap.enc c}|{_cap.enc structName}"
          else if isNoConfusion env c then
            IO.println s!"REL|no_confusion|{_cap.enc c}|{_cap.enc structName}"
  let (_, state) := (sorted.forM (fun item => _cap.collect env item.1)).run {}
  unless state.missing.isEmpty do throwError "dependency constant missing from environment"
  let axioms := (state.axioms.toArray.map _cap.enc).qsort (· < ·)
  IO.println s!"AXIOMS|{",".intercalate axioms.toList}"
  IO.println s!"CLOSURE|{state.visited.size}"
#eval _cap.main
'''
