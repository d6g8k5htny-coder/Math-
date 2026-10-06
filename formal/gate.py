#!/usr/bin/env python3
"""Source-bound Lean evidence, not a scientific acceptance engine (stdlib only)."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys

ALLOWED = frozenset({'propext', 'Classical.choice', 'Quot.sound'})
NAME = r'[A-Za-z_][A-Za-z0-9_.]*'
AXIOM = re.compile(r"'(" + NAME + r")' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
SHA256 = re.compile(r'[0-9a-f]{64}')
COMMIT = re.compile(r'[0-9a-f]{40}')
ROOT = Path(__file__).resolve().parent
PACKAGE = 'ResearchFormalCoreR1'
# Environment-bound inventory lines emitted by the generated Lean audit (RF-GATE-01).
INV = re.compile(r'^INV\|(theorem|def|axiom|opaque|inductive|ctor|rec|quot)\|(' + NAME + r')\|(' + NAME + r')$')
MODULE = re.compile(r'^MODULE\|(' + NAME + r')\|(true|false)\|([0-9]+)\|([0-9]+)$')
AXIOMS = re.compile(r'^AXIOMS\|\[([^\]]*)\]$')
CLOSURE = re.compile(r'^CLOSURE\|([0-9]+)$')
AUX = re.compile(r'(^|\.)(_[A-Za-z0-9_]*|proof_[0-9]+|match_[0-9]+|eq_[0-9]+|aux_[0-9]+|instance_[0-9]+)(\.|$)')
# Conservative declaration grammar the source scanner understands: public theorems
# start at column 0 as `theorem NAME` or `lemma NAME`; every other spelling of a
# theorem (indented, private, protected, attributed on the same line) is refused.
DECL_KEYWORD = re.compile(r'(?<![A-Za-z0-9_.])(?:theorem|lemma)(?![A-Za-z0-9_])')
CANONICAL = re.compile(r'^(?:theorem|lemma) (' + NAME + r')(?=\s|$)')
FORBIDDEN_TOKENS = re.compile(r'(?<![A-Za-z0-9_.])(?:sorry|axiom|native_decide|implemented_by|extern|unsafe)(?![A-Za-z0-9_])')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def audit_axioms(text, targets):
    require(isinstance(targets, list) and targets and len(set(targets)) == len(targets), 'empty or duplicate target list')
    records = {}
    for match in AXIOM.finditer(text):
        name, raw = match.groups()
        require(name in targets and name not in records, 'unexpected or duplicate axiom target: ' + name)
        axioms = [] if raw is None or not raw.strip() else [a.strip() for a in raw.split(',')]
        require(all(re.fullmatch(NAME, a) for a in axioms), 'malformed axiom name')
        require(set(axioms) <= ALLOWED, 'forbidden transitive axiom: ' + repr(set(axioms) - ALLOWED))
        records[name] = sorted(set(axioms))
    require(not AXIOM.sub('', text).strip(), 'unrecognized audit output')
    require(set(records) == set(targets), 'missing target axiom report')
    return records

def check_files(root, files):
    require(isinstance(files, dict) and files, 'empty file manifest')
    root = root.resolve()
    for name, digest in files.items():
        p = PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts and str(p) == name and '\\' not in name, 'unsafe manifest path')
        require(isinstance(digest, str) and SHA256.fullmatch(digest), 'invalid source hash')
        target = root / p
        require(all(not (root.joinpath(*p.parts[:i])).is_symlink() for i in range(1, len(p.parts) + 1)), 'symlink source')
        require(target.is_file() and target.resolve().is_relative_to(root), 'missing or escaping source: ' + name)
        require(sha(target.read_bytes()) == digest, 'source hash mismatch: ' + name)

def check_blueprint(text, targets):
    links = re.findall(r'\\lean\{([^}]+)\}', text)
    require(links and all(n in targets for n in links), 'missing or unresolved Blueprint declaration')
    require('\\leanok' not in text, 'unreviewed Blueprint completion label')
    return links

def strip_lean_comments(text):
    """Remove `--` line comments and `/- ... -/` block comments (nesting-aware) before scanning.

    Newlines are kept, so line numbers in refusals refer to the original file. String literals
    are not parsed: a comment marker inside a string is treated as a comment, which can only
    make the pre-check stricter, never admit anything.
    """
    out, i, depth = [], 0, 0
    while i < len(text):
        two = text[i:i + 2]
        if depth == 0 and two == '--':
            j = text.find('\n', i)
            i = len(text) if j < 0 else j
            continue
        if two == '/-':
            depth += 1; i += 2; continue
        if depth and two == '-/':
            depth -= 1; i += 2; continue
        if depth == 0 or text[i] == '\n':
            out.append(text[i])
        i += 1
    require(depth == 0, 'unterminated block comment')
    return ''.join(out)

def grammar_check(text, path):
    """Refuse theorem spellings the column-0 scanner cannot inventory, and admission tokens.

    The source scanner is only a pre-check (see GATE_HARDENING.md); the authoritative
    package-wide admission check is `audit_inventory` on the compiled environment.
    """
    code = strip_lean_comments(text)
    require(not FORBIDDEN_TOKENS.search(code), 'forbidden token in source module: ' + path)
    names = []
    for number, line in enumerate(code.splitlines(), 1):
        if not DECL_KEYWORD.search(line):
            continue
        canonical = CANONICAL.match(line)
        require(canonical, 'unsupported theorem spelling (indented, private, protected or attributed on the same line) at ' + path + ':' + str(number))
        names.append(canonical.group(1))
    return names

def inventory_source(include_local=False):
    """Lean program that enumerates every constant of every package module from the compiled
    environment's module tables, then axiom-closes all of them in one shared traversal.

    The enumeration reads `env.header.moduleData[idx].constNames` for the modules under the
    package prefix (the whole-environment scan `env.constants.map\u2081` takes minutes in the
    interpreter; the module tables are the same data indexed by module). The closure replicates
    the kernel-side rules of `Lean.CollectAxioms.collect` (axiom: record and visit its type;
    def/theorem/opaque: type and value; quot: nothing; ctor/rec: type; inductive: type and
    constructors) with one visited set, so the printed AXIOMS line is the union over every
    package constant, and the gate accepts only when that union is inside ALLOWED.
    """
    local = ('  if includeLocal then\n'
             '    for (c, ci) in env.constants.map\u2082.toList do\n'
             '      unless (`_inv).isPrefixOf c do\n'
             '        consts := consts.push (c, ci, `_local)\n')
    return ('import ' + PACKAGE + '\nimport Lean\nopen Lean\n\n'
            'def _inv.kind : ConstantInfo \u2192 String\n'
            '  | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque"\n'
            '  | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec" | .quotInfo _ => "quot"\n\n'
            'structure _inv.St where\n'
            '  visited : NameSet := {}\n'
            '  axioms : NameSet := {}\n\n'
            'partial def _inv.collect (env : Environment) (c : Name) : StateM _inv.St Unit := do\n'
            '  unless (\u2190 get).visited.contains c do\n'
            '    modify fun s => { s with visited := s.visited.insert c }\n'
            '    let collectExpr (e : Expr) : StateM _inv.St Unit := e.getUsedConstants.forM (_inv.collect env)\n'
            '    match env.find? c with\n'
            '    | some (.axiomInfo v)  => modify (fun s => { s with axioms := s.axioms.insert c }) *> collectExpr v.type\n'
            '    | some (.defnInfo v)   => collectExpr v.type *> collectExpr v.value\n'
            '    | some (.thmInfo v)    => collectExpr v.type *> collectExpr v.value\n'
            '    | some (.opaqueInfo v) => collectExpr v.type *> collectExpr v.value\n'
            '    | some (.quotInfo _)   => pure ()\n'
            '    | some (.ctorInfo v)   => collectExpr v.type\n'
            '    | some (.recInfo v)    => collectExpr v.type\n'
            '    | some (.inductInfo v) => collectExpr v.type *> v.ctors.forM (_inv.collect env)\n'
            '    | none                 => pure ()\n\n'
            'def _inv.main (env : Environment) (pkg : Name) (includeLocal : Bool) : IO Unit := do\n'
            '  let header := env.header\n'
            '  let names := header.moduleNames\n'
            '  let mut consts : Array (Name \u00d7 ConstantInfo \u00d7 Name) := #[]\n'
            '  for h : idx in [0:names.size] do\n'
            '    let m := names[idx]\n'
            '    if pkg.isPrefixOf m then\n'
            '      let data := header.moduleData[idx]!\n'
            '      IO.println s!"MODULE|{m}|{data.isModule}|{data.constNames.size}|{data.extraConstNames.size}"\n'
            '      for c in data.constNames do\n'
            '        match env.find? c with\n'
            '        | some ci => consts := consts.push (c, ci, m)\n'
            '        | none => throw (IO.userError s!"constant {c} of module {m} is missing from the environment")\n'
            + local +
            '  let sorted := consts.qsort (fun a b => a.1.toString < b.1.toString)\n'
            '  for (c, ci, m) in sorted do\n'
            '    IO.println s!"INV|{_inv.kind ci}|{m}|{c}"\n'
            '  let (_, s) := (sorted.forM (fun x => _inv.collect env x.1)).run {}\n'
            '  let axs := (s.axioms.toArray.qsort (fun a b => a.toString < b.toString)).toList.map toString\n'
            '  IO.println s!"AXIOMS|[{", ".intercalate axs}]"\n'
            '  IO.println s!"CLOSURE|{s.visited.size}"\n\n'
            '#eval show CoreM Unit from do _inv.main (\u2190 getEnv) `' + PACKAGE + ' ' + ('true' if include_local else 'false') + '\n')

def audit_inventory(text, targets, modules, allow_local=False, reported_axioms=None):
    """Package-wide admission check on the compiled environment, not on source text.

    Every constant of every registered module (public, private or auxiliary, used or unused)
    is enumerated by Lean from the module tables; the axiom closure of all of them together
    must be inside ALLOWED; no constant may itself be an axiom; the public theorem-kind
    declarations must equal the manifest targets exactly; and the module table must be
    exactly the registered modules plus the empty root module.
    """
    require(isinstance(targets, list) and targets and len(set(targets)) == len(targets), 'empty or duplicate target list')
    require(isinstance(modules, (list, set, frozenset)) and modules, 'empty module registry')
    modules = set(modules)
    lines = [line for line in text.splitlines() if line.startswith(('INV|', 'MODULE|', 'AXIOMS|', 'CLOSURE|'))]
    inv = [line for line in lines if line.startswith('INV|')]
    table = [line for line in lines if line.startswith('MODULE|')]
    axiom_lines = [line for line in lines if line.startswith('AXIOMS|')]
    closure_lines = [line for line in lines if line.startswith('CLOSURE|')]
    require(inv and table, 'empty environment inventory')
    require(len(axiom_lines) == 1 and len(closure_lines) == 1, 'inventory must report exactly one axiom closure')
    counts, seen_modules = {}, set()
    for line in table:
        match = MODULE.fullmatch(line)
        require(match, 'malformed module line: ' + line)
        name, is_module, constants, extra = match.groups()
        require(name not in seen_modules, 'duplicate module table entry: ' + name)
        seen_modules.add(name)
        require(is_module == 'false', 'package module compiled under the module system: ' + name)
        if name == PACKAGE:
            require(constants == '0' and extra == '0', 'root module must declare nothing')
        else:
            require(name in modules, 'compiled module not registered in the manifest: ' + name)
            require(extra == '0', 'code generator added auxiliary constants in ' + name)
            counts[name] = int(constants)
    require(seen_modules == modules | {PACKAGE}, 'module table differs from registered modules: ' + repr(sorted(seen_modules ^ (modules | {PACKAGE}))))
    seen, public, per_module = set(), [], {name: 0 for name in modules}
    for line in inv:
        match = INV.fullmatch(line)
        require(match, 'malformed inventory line: ' + line)
        kind, module, name = match.groups()
        require(name not in seen, 'duplicate inventory name: ' + name)
        seen.add(name)
        require(module in modules or (allow_local and module == '_local'), 'declaration outside registered modules: ' + name + ' in ' + module)
        require(kind != 'axiom', 'axiom declared inside package: ' + name)
        if module in per_module:
            per_module[module] += 1
        if kind == 'theorem' and not AUX.search(name):
            public.append(name)
    require(per_module == counts, 'inventory count differs from module table: ' + repr((per_module, counts)))
    raw = AXIOMS.fullmatch(axiom_lines[0])
    require(raw, 'malformed axiom closure line')
    axioms = [] if not raw.group(1).strip() else [a.strip() for a in raw.group(1).split(',')]
    require(all(re.fullmatch(NAME, a) for a in axioms) and len(set(axioms)) == len(axioms), 'malformed axiom closure')
    require(set(axioms) <= ALLOWED, 'forbidden transitive axiom in package closure: ' + repr(sorted(set(axioms) - ALLOWED)))
    if reported_axioms is not None:
        reported = set().union(*[set(v) for v in reported_axioms.values()]) if reported_axioms else set()
        require(reported <= set(axioms), 'per-target axiom audit reports axioms the package closure omits: ' + repr(sorted(reported - set(axioms))))
    closure = CLOSURE.fullmatch(closure_lines[0])
    require(closure and int(closure.group(1)) >= len(inv), 'malformed or impossible closure size')
    extra, missing = sorted(set(public) - set(targets)), sorted(set(targets) - set(public))
    require(not extra and not missing, 'environment theorem inventory differs from manifest targets: extra=' + repr(extra) + ' missing=' + repr(missing))
    return dict(declarations=len(inv), public_theorems=sorted(public), axioms=sorted(axioms), closure=int(closure.group(1)),
                sha256=sha('\n'.join(lines).encode()))

def lineage_identity(party, role):
    """Validate declared identity text, not the truth or completeness of authorship."""
    require(isinstance(party, dict), 'malformed review lineage: ' + role)
    placeholders = {'unknown', 'unverified', 'unspecified', 'tbd', 'n/a',
                    'none', 'null', '?', 'not known', 'not available'}
    result = {}
    for key in ('provider', 'family', 'agent'):
        value = party.get(key)
        require(isinstance(value, str) and value.strip(), 'missing review lineage: ' + role + '.' + key)
        normalized = ' '.join(value.split()).casefold()
        require(normalized not in placeholders, 'ambiguous review lineage: ' + role + '.' + key)
        result[key] = normalized
    return result

def check_alignment(review, manifest_digest, targets, scope_digest):
    require(isinstance(review, dict), 'review must be object')
    require(review.get('disposition') == 'ACCEPTED', 'alignment not accepted')
    require(review.get('manifest_sha256') == manifest_digest, 'stale alignment manifest')
    require(review.get('scope_sha256') == scope_digest, 'stale alignment scope')
    covered = review.get('targets', [])
    require(isinstance(covered, list) and len(covered) == len(set(covered)) and set(covered) == set(targets), 'partial or ambiguous review')
    r = lineage_identity(review.get('reviewer'), 'reviewer')
    authors = [('author', lineage_identity(review.get('author'), 'author'))]
    # Absence preserves the historical single-author schema. Declared proposers
    # are additional authors, never ignored metadata or a substitute for author.
    proposers = review.get('proposal_authors', [])
    require(isinstance(proposers, list), 'malformed review lineage: proposal_authors')
    for index, proposer in enumerate(proposers):
        role = 'proposal_authors[' + str(index) + ']'
        identity = lineage_identity(proposer, role)
        if 'targets' in proposer:
            scope = proposer['targets']
            require(isinstance(scope, list) and scope and
                    all(isinstance(name, str) and name in targets for name in scope) and
                    len(scope) == len(set(scope)), 'invalid proposal target scope: ' + role)
        authors.append((role, identity))
    for role, author in authors:
        for key in ('provider', 'family', 'agent'):
            require(author[key] != r[key], 'lineage not independent: ' + role + '.' + key)
    e = review.get('evidence', {})
    require(isinstance(e.get('repository'), str) and re.fullmatch(r'[^/\s]+/[^/\s]+', e['repository']), 'missing evidence repo')
    require(isinstance(e.get('commit'), str) and COMMIT.fullmatch(e['commit']), 'mutable review ref')
    require(isinstance(e.get('sha256'), str) and SHA256.fullmatch(e['sha256']), 'missing review hash')
    require(isinstance(e.get('path'), str) and e['path'] and not PurePosixPath(e['path']).is_absolute() and '..' not in PurePosixPath(e['path']).parts, 'missing or unsafe review path')
    # This checks structure, identity and scope. A controller must retrieve and
    # authenticate the review evidence; strings do not prove a review happened.

def load_json(text):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            require(key not in obj, 'duplicate JSON key: ' + key)
            obj[key] = value
        return obj
    return json.loads(text, object_pairs_hook=unique)

def source_check():
    raw = (ROOT / 'manifest.json').read_bytes()
    m = load_json(raw)
    require(m.get('schema_version') == 1 and m.get('scientific_effect') == 'NONE', 'invalid evidence schema')
    require(m.get('formalization_status') == 'proved' and m.get('alignment_status') == 'PENDING_INDEPENDENT_REVIEW', 'source metadata cannot self-award execution or review')
    required = {'gate.py', 'tests/test_gate.py', 'lean-toolchain', 'lakefile.toml', 'lake-manifest.json', 'ResearchFormalCoreR1.lean', 'SCOPE.md', 'GLOSSARY.md', 'README.md', 'blueprint/src/content.tex', 'tests/test_alignment_lineage.py', 'LINEAGE_VALIDATION.md', 'tests/test_inventory_gate.py', 'GATE_HARDENING.md'}
    require(required <= set(m['files']), 'unbound control or scope file')
    originals = {'originals/Algebra.lean.txt': '4c196820c4db8fafc288dd35642828ba577e3544d60aba7d1d6d24f14ad1e8ae', 'originals/ProbabilityCompanions.lean.txt': '4ace6600a476859982c8851ae9097c89b082d3c96291b3c8330bd4cc00bae65d'}
    require(all(m['files'].get(path) == value for path, value in originals.items()), 'original source identity changed or omitted')
    require('COMPATIBILITY.md' in m['files'], 'unbound successor rationale')
    check_files(ROOT, m['files'])
    require((ROOT / 'lean-toolchain').read_text().strip() == 'leanprover/lean4:v4.34.1', 'wrong Lean toolchain')
    lock = load_json((ROOT / 'lake-manifest.json').read_text())
    packages = lock['packages']
    require(len(packages) == len({p['name'] for p in packages}), 'duplicate dependency')
    actual = {p['name']: p['rev'] for p in packages}
    require(actual == m['dependency_revisions'], 'dependency lock mismatch')
    require(all(COMMIT.fullmatch(v) for v in actual.values()), 'unpinned dependency')
    expected_root = ''.join('import ' + path[:-5].replace('/', '.') + '\n' for path in m['source_modules'])
    require((ROOT / 'ResearchFormalCoreR1.lean').read_text() == expected_root, 'root must only import registered modules')
    names = []
    for path in m['source_modules']:
        require(path in m['files'], 'unbound source module')
        require(path.startswith(PACKAGE + '/') and path.endswith('.lean') and path.count('/') == 1, 'source module outside the package directory: ' + path)
        text = (ROOT / path).read_text()
        # Pre-check only: the scanner refuses any theorem spelling it cannot count, and the
        # compiled environment is audited package-wide in execute() (RF-GATE-01).
        names.extend(PACKAGE + '.' + n for n in grammar_check(text, path))
    require(names == m['targets'], 'target inventory differs from source declarations')
    check_blueprint((ROOT / 'blueprint/src/content.tex').read_text(), names)
    lean_files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*.lean') if '.lake' not in p.relative_to(ROOT).parts}
    require(lean_files == set(m['source_modules']) | {'ResearchFormalCoreR1.lean'}, 'unregistered Lean module')
    return m, sha(raw)

def run(command, label, out, expect_success=True):
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
    (out / (label + '.log')).write_text(result.stdout)
    print(label + ': exit ' + str(result.returncode), flush=True)
    require((result.returncode == 0) == expect_success, 'unexpected process outcome: ' + label + '\n' + result.stdout[-6000:])
    return result.stdout

def execute(m, digest):
    out = ROOT / '.lake' / 'formal-evidence'
    out.mkdir(parents=True, exist_ok=True)
    require(not (ROOT / '.lake').is_symlink() and not (ROOT / '.lake/build').is_symlink(), 'symlink build directory')
    if (ROOT / '.lake/build').exists():
        shutil.rmtree(ROOT / '.lake/build')  # fresh local-package build; dependency cache is untouched
    run(['lake', 'build'], 'build', out)
    run(['lake', 'env', 'leanchecker', 'ResearchFormalCoreR1'], 'leanchecker', out)
    audit = out / 'Audit.lean'
    audit.write_text('import ResearchFormalCoreR1\n' + '\n'.join('#print axioms ' + n for n in m['targets']) + '\n')
    text = run(['lake', 'env', 'lean', str(audit)], 'axioms', out)
    axioms = audit_axioms(text, m['targets'])
    types = out / 'Types.lean'
    types.write_text('import ResearchFormalCoreR1\nset_option pp.explicit true\n' + '\n'.join('#check ' + n for n in m['targets']) + '\n')
    run(['lake', 'env', 'lean', str(types)], 'elaborated-types', out)
    # Package-wide admission check bound to the compiled environment, not to source text:
    # every constant in a registered module is enumerated by Lean itself and axiom-audited,
    # and the public theorems must be exactly the manifest targets (RF-GATE-01).
    modules = {PACKAGE + '.' + path[len(PACKAGE) + 1:-5] for path in m['source_modules']}
    inventory = out / 'Inventory.lean'
    inventory.write_text(inventory_source())
    inventory_report = audit_inventory(run(['lake', 'env', 'lean', str(inventory)], 'inventory', out), m['targets'], modules, reported_axioms=axioms)
    # Admission controls: declarations the source scanner could never see, or would
    # mis-prefix, must be caught by the environment inventory. Each compiles (sorry only
    # warns) and must be rejected.
    admissions = {
        'hidden_sorry': 'namespace ' + PACKAGE + '\n  private theorem hiddenAdmission : (1 : Nat) = 1 := by sorry\nend ' + PACKAGE + '\n',
        'hidden_theorem': 'namespace ' + PACKAGE + '\n  @[simp] theorem indentedAdmission : (1 : Nat) = 1 := rfl\nend ' + PACKAGE + '\n',
        'hidden_def': 'namespace ' + PACKAGE + '\n  noncomputable def unusedAdmission : Nat := by sorry\nend ' + PACKAGE + '\n',
        'outside_namespace': 'theorem outsideNamespaceAdmission : (1 : Nat) = 1 := rfl\n'}
    admission_outcomes = {}
    for label, declaration in admissions.items():
        path = out / (label + '.lean')
        path.write_text(inventory_source(include_local=True).replace('import Lean\n', 'import Lean\n' + declaration, 1))
        log = run(['lake', 'env', 'lean', str(path)], label, out)
        try:
            audit_inventory(log, m['targets'], modules, allow_local=True)
        except ValueError:
            admission_outcomes[label] = 'REJECTED_BY_INVENTORY_GATE'
        else:
            raise ValueError('admission control escaped the environment inventory: ' + label)
    # Real counterexample/mutation controls, not comparisons of fixed labels.
    cases = {
        'false_fold': ('import ResearchFormalCoreR1\nexample : ResearchFormalCoreR1.foldPotential 1 1 - ResearchFormalCoreR1.foldPotential 1 (-1) = (2 : Real)^3 / 7 := by\n  norm_num [ResearchFormalCoreR1.foldPotential]\n', False, None),
        'false_power': ('import ResearchFormalCoreR1\nexample : (2 : Real)^4 <= (2 : Real)^3 := by\n  norm_num\n', False, None),
        'sorry': ('import ResearchFormalCoreR1\ntheorem injected : False := by sorry\n#print axioms injected\n', True, 'injected'),
        'custom_imported': ('import ResearchFormalCoreR1\naxiom hiddenPremise : False\ntheorem middle : False := hiddenPremise\ntheorem injected : False := middle\n#print axioms injected\n', True, 'injected'),
        'native': ('import ResearchFormalCoreR1\ntheorem injected : (2 : Nat) + 2 = 4 := by native_decide\n#print axioms injected\n', True, 'injected')}
    outcomes = {}
    for label, (source, succeeds, target) in cases.items():
        path = out / (label + '.lean'); path.write_text(source)
        log = run(['lake', 'env', 'lean', str(path)], label, out, succeeds)
        if target:
            # Remove compiler diagnostics only by selecting the axiom line onward;
            # absence remains an error, never an empty allowlist.
            matches = list(AXIOM.finditer(log))
            require(matches, 'negative control missing axiom report: ' + label)
            payload = '\n'.join(x.group() for x in matches)
            try:
                audit_axioms(payload, [target])
            except ValueError:
                outcomes[label] = 'REJECTED_BY_AXIOM_GATE'
            else:
                raise ValueError('negative control escaped: ' + label)
        else:
            require('unsolved goals' in log or 'norm_num' in log and 'failed' in log, 'negative control did not fail on its proof goal')
            outcomes[label] = 'REJECTED_BY_LEAN'
    # Recheck after compilation: a build hook must not rewrite bound sources/lock.
    _, after = source_check(); require(after == digest, 'manifest changed during execution')
    version = run(['lake', 'env', 'lean', '--version'], 'version', out).strip()
    require('version 4.34.1' in version, 'unexpected running Lean version')
    actual_dependencies = {name: subprocess.check_output(['git', '-C', str(ROOT / '.lake/packages' / name), 'rev-parse', 'HEAD'], text=True).strip() for name in m['dependency_revisions']}
    require(actual_dependencies == m['dependency_revisions'], 'installed dependency HEAD differs from lock')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    require(COMMIT.fullmatch(head), 'missing exact checked commit')
    receipt = dict(schema_version=1, scientific_effect='NONE', formalization_status='kernel-checked',
                   alignment_status='PENDING_INDEPENDENT_REVIEW', manifest_sha256=digest,
                   checked_commit=head, repository=os.environ.get('GITHUB_REPOSITORY'),
                   workflow_run_id=os.environ.get('GITHUB_RUN_ID'), lean_version=version,
                   dependency_revisions=m['dependency_revisions'], axioms=axioms, negative_controls=outcomes,
                   inventory=dict(declarations=inventory_report['declarations'], public_theorems=len(inventory_report['public_theorems']),
                                  axioms=inventory_report['axioms'], closure=inventory_report['closure'],
                                  sha256=inventory_report['sha256'], admission_controls=admission_outcomes))
    receipt['logs'] = {p.name: sha(p.read_bytes()) for p in sorted(out.glob('*.log'))}
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute', action='store_true', help='run build, transitive axiom audit and negative controls')
    p.add_argument('--alignment', type=Path, help='validate a separately authenticated alignment record; never promotes science')
    args = p.parse_args()
    try:
        m, digest = source_check()
        if args.alignment:
            check_alignment(load_json(args.alignment.read_text()), digest, m['targets'], m['files']['SCOPE.md'])
        if args.execute:
            execute(m, digest)
        else:
            print('SOURCE_IDENTITY_PASS (not a Lean build or scientific acceptance): ' + digest)
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as e:
        print('FORMAL_GATE_FAIL: ' + str(e), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
