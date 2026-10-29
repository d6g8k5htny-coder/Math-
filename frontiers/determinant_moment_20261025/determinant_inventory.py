#!/usr/bin/env python3
"""Strict determinant-specific admission policy around an unchanged source-preserved core.

Policy acceptance is not Lean execution, scientific acceptance, or a kernel/CBZ receipt.
"""
from collections import Counter, defaultdict
import copy
import hashlib
from pathlib import Path
import re
import shutil
from types import ModuleType

CORE_SHA256 = 'ff8a5374597772b2d37054fd722c2243c4b552a63802c69f7c605519832be6c4'
PACKAGE = 'ResearchFormalCoreR1'
SCOPE = 'DETERMINANT_ADMISSION_POLICY_ONLY_NOT_KERNEL_OR_CBZ_SUCCESS'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_core(path=None):
    path = Path(path) if path is not None else Path(__file__).with_name('compiled_inventory.py')
    require(not path.is_symlink(), 'symlink core helper refused')
    require(path.is_file(), 'source-preserved core helper hash mismatch')
    source = path.read_bytes()
    require(hashlib.sha256(source).hexdigest() == CORE_SHA256, 'source-preserved core helper hash mismatch')
    core = ModuleType('pinned_determinant_inventory_core')
    core.__file__ = str(path)
    exec(compile(source, str(path), 'exec'), core.__dict__)
    return core


def typed_name(value):
    """Decode explicit string/numeric tags without dotted-name or bool/int coercion."""
    require(type(value) is list and bool(value), 'invalid typed name component array')
    result = []
    for component in value:
        require(type(component) is list and len(component) == 2, 'invalid typed name component')
        tag, payload = component
        require((tag == 's' and type(payload) is str) or
                (tag == 'n' and type(payload) is int and payload >= 0), 'invalid typed name component')
        if tag == 's':
            payload.encode('utf-8')
        result.append(payload)
    return tuple(result)


def typed_record(row, core):
    require(type(row) is list and len(row) == 4, 'malformed typed compiled inventory record')
    kind, origin, module_raw, name_raw = row
    require(type(kind) is str and kind in core.KINDS and kind != 'axiom', 'invalid bound kind or bound axiom')
    require(type(origin) is str and origin in ('user', 'aux'), 'invalid bound provenance')
    return kind, origin, typed_name(module_raw), typed_name(name_raw)


def bound_contract(manifest, core):
    require(type(manifest) is dict and manifest.get('compiled_inventory_version') == 2,
            'compiled inventory version2 required')
    targets = manifest.get('targets')
    require(type(targets) is list and bool(targets) and all(type(t) is str for t in targets)
            and len(set(targets)) == len(targets), 'empty or duplicate public targets')
    wanted = {core.simple_name(t) for t in targets}
    require(all(len(t) >= 2 and t[0] == PACKAGE for t in wanted), 'public target outside package')
    paths = manifest.get('source_modules')
    require(type(paths) is list and bool(paths) and all(type(p) is str and re.fullmatch(
        PACKAGE + r'/[A-Za-z_][A-Za-z0-9_]*\.lean', p) for p in paths)
        and len(set(paths)) == len(paths), 'invalid source module registry')
    modules = {core.simple_name(p[:-5].replace('/', '.')) for p in paths}
    records = manifest.get('compiled_inventory')
    require(type(records) is list, 'missing typed compiled inventory')
    bound, internal, seen_names = set(), set(), set()
    for row in records:
        kind, origin, module, name = typed_record(row, core)
        require(module in modules, 'bound constant outside registered module')
        require(name not in wanted, 'bound record shadows a public target')
        require(name not in seen_names, 'duplicate bound constant name')
        seen_names.add(name)
        record = (kind, origin, module, name)
        (internal if kind == 'theorem' and origin == 'user' else bound).add(record)
    extras_raw = manifest.get('ir_extra_counts')
    require(type(extras_raw) is list, 'missing IR module-count binding')
    extras = {}
    for row in extras_raw:
        require(type(row) is list and len(row) == 2, 'invalid IR module-count record')
        module = typed_name(row[0]);count = row[1]
        require(type(count) is int and count >= 0, 'invalid IR count')
        require(module not in extras, 'duplicate IR module binding')
        extras[module] = count
    root = (PACKAGE,)
    require(set(extras) == modules | {root}, 'IR module binding differs from exact module registry')
    require(extras[root] == 0, 'root IR extras must remain empty')
    compatibility = manifest.get('auxiliary_compatibility')
    require(type(compatibility) is list and len(compatibility) == 4,
            'exact four auxiliary compatibility records required')
    compatible = {}
    for entry in compatibility:
        require(type(entry) is dict and set(entry) == {'record','parent','reason'}, 'invalid auxiliary compatibility entry')
        record = typed_record(entry['record'], core)
        parent = typed_record(entry['parent'], core)
        require(record in bound and record[:2] == ('theorem','aux'), 'compatibility record must already be frozen bound theorem/aux')
        require(record[3] not in compatible, 'duplicate auxiliary compatibility entry')
        require(parent[2] in modules and parent[1] == 'user', 'invalid compatibility parent owner/provenance')
        require(record[3][:-1] == parent[3], 'compatibility parent name differs from exact prefix')
        if entry['reason'] == 'deferred_equation':
            require(parent[:2] == ('def','user') and parent in bound, 'compatibility parent must already be a bound user definition')
            require(record[3][-1] == 'eq_1', 'unapproved deferred-equation compatibility name')
        elif entry['reason'] == 'abel_proof':
            require(parent[:2] == ('theorem','user') and (parent in internal or parent[3] in wanted),
                    'compatibility parent is not a registered user proof')
            require(record[2] == parent[2] and record[3][-1] == '_abel_1_1', 'unapproved abel compatibility owner/name')
        else:
            raise ValueError('unapproved auxiliary compatibility reason')
        compatible[record[3]] = (record, parent)
    return dict(targets=targets, wanted=wanted, modules=modules, bound=frozenset(bound),
                internal=frozenset(internal), extras=extras, compatible=compatible)


def _violations(inventory, contract, core, reported_axioms):
    modules = {'.'.join(m) for m in contract['modules']}
    base = core.inventory_violations(inventory, contract['targets'], modules,
        reported_axioms=reported_axioms, bound=contract['bound'])
    observed = Counter(tuple(row) for row in inventory['constants'])
    by_name = defaultdict(list)
    for row in inventory['constants']:
        by_name[row[3]].append(tuple(row))
    table = defaultdict(list)
    for module, system, count, extra in inventory['modules']:
        table[module].append((system, count, extra))
    result = []
    for code, name, note in base:
        known_internal = (code == 'extra_theorem' and note == '' and len(by_name[name]) == 1
                          and by_name[name][0] in contract['internal'])
        known_IR_count = (code == 'codegen_extra' and name in contract['extras']
                          and len(table[name]) == 1 and table[name][0][2] == contract['extras'][name]
                          and note == str(contract['extras'][name]))
        compatibility = contract['compatible'].get(name)
        known_compat_aux = (code == 'unbound_auxiliary' and note == '' and compatibility is not None
                           and by_name[name] == [compatibility[0]]
                           and by_name[compatibility[1][3]] == [compatibility[1]])
        if known_internal or known_IR_count or known_compat_aux:
            continue
        result.append((code, name, note))
    for record in contract['internal']:
        if observed[record] != 1:
            result.append(('missing_internal_proof', record[3], core.render(record[2])))
    for module, expected in contract['extras'].items():
        for system, count, actual in table.get(module, []):
            if actual != expected:
                result.append(('ir_extra_count_mismatch', module, str(actual) + '/' + str(expected)))
    for name, (record, parent) in contract['compatible'].items():
        if observed[record] != 1:
            result.append(('auxiliary_compatibility_record_mismatch', name, core.render(record[2])))
        if by_name[parent[3]] != [parent]:
            result.append(('auxiliary_compatibility_parent_mismatch', name, core.render(parent[2])))
    return sorted(set(result), key=lambda v: (v[0], core.encode(v[1]), v[2]))


class InventoryRejected(ValueError):
    def __init__(self, violations, inventory, core):
        self.violations, self.inventory = violations, inventory
        super().__init__('determinant inventory rejected: ' + '; '.join(
            code + ' ' + core.render(name) + (' ' + note if note else '') for code, name, note in violations))


def audit_inventory(text, manifest, reported_axioms=None, *, core_path=None):
    core = load_core(core_path)
    contract = bound_contract(manifest, core)
    inventory = core.parse_inventory(text)
    violations = _violations(inventory, contract, core, reported_axioms)
    if violations:
        raise InventoryRejected(violations, inventory, core)
    return dict(scope=SCOPE, declarations=len(inventory['constants']),
        public_theorems=sorted(manifest['targets']), internal_user_proofs=len(contract['internal']),
        auxiliary_theorems=sum(k == 'theorem' and o == 'aux' for k,o,m,n in inventory['constants']),
        axioms=sorted(core.render(a) for a in inventory['axioms']), closure=inventory['closure'],
        sha256=hashlib.sha256('\n'.join(inventory['lines']).encode()).hexdigest(),
        ir_extra_total=sum(extra for module,system,count,extra in inventory['modules']),
        exact_auxiliary_compatibility_records=len(contract['compatible']),
        IR_scope='Exact module counts only; IR names/payloads are not authenticated',
        kernel_or_cbz_status='NOT_AWARDED')


def check_admission(text, label, injected, expected, manifest, *, core_path=None):
    """Require the actual injected full identity and precisely its expected findings."""
    core = load_core(core_path)
    contract = bound_contract(manifest, core)
    inventory = core.parse_inventory(text)
    kind, origin, short_name, private, module = injected
    hits = [row for row in inventory['constants'] if row[0] == kind and row[1] == origin
            and core.user_name(row[3]) == (short_name, private) and row[2] == module]
    require(len(hits) == 1, 'admission control did not inject exactly one expected full identity: ' + label)
    full = hits[0][3]
    wanted = []
    for code, short, is_private in expected:
        if (short, is_private) == (short_name, private):
            wanted.append((code, core.encode(full)))
        else:
            require(not is_private, 'unidentified unrelated private expected finding')
            wanted.append((code, core.encode(short)))
    findings = _violations(inventory, contract, core, reported_axioms=None)
    got = [(code, core.encode(name)) for code,name,note in findings]
    require(sorted(got) == sorted(wanted), 'admission control rejected for an unexpected reason: ' + label
            + ' expected=' + repr(sorted(wanted)) + ' got=' + repr(sorted(got)))
    return dict(outcome='REJECTED_FOR_EXPECTED_REASON', injected_name_encoded=core.encode(full),
                violations=[dict(code=code, name_encoded=core.encode(name), note=note)
                            for code,name,note in findings])


def compiled_admission(manifest, baseline, output, *, package_root, core_path=None, runner=None):
    """Run both unchanged core payloads through this policy, never through core globals.

    The outer gate owns source/runtime qualification and its five remaining real controls.
    A caller-supplied runner is an external-process seam; unit runners are not Lean evidence.
    """
    core = load_core(core_path)
    frozen = copy.deepcopy(manifest)
    bound_contract(frozen, core)
    digest = baseline.get('sha256') if type(baseline) is dict else None
    require(type(digest) is str and re.fullmatch('[0-9a-f]{64}', digest), 'missing baseline inventory digest')
    package = Path(package_root).absolute()
    output = Path(output).absolute()
    work = package / '.lake/determinant-compiled-admission'
    require(not any(p.is_symlink() for p in (package, package/'.lake', package/'.lake/build', work)),
            'symlink compiled-admission source/build/work path')
    require((package/'.lake/build').is_dir(), 'fresh package build missing before admission controls')
    require(not any(p.is_symlink() for p in (output, *output.parents)),
            'symlink admission output or ancestor refused')
    require(not output.resolve().is_relative_to(work.resolve()),
            'admission evidence must remain outside disposable copy')
    output.mkdir(parents=True, exist_ok=True)
    if work.exists():
        shutil.rmtree(work)
    run = core.run if runner is None else runner
    results = {}
    try:
        clone = work / 'package'
        shutil.copytree(package, clone, ignore=lambda d,names: ['.lake'] if Path(d) == package else [])
        shutil.copytree(package/'.lake/build', clone/'.lake/build')
        (clone/'.lake/packages').symlink_to(package/'.lake/packages', target_is_directory=True)
        program = work/'Inventory.lean';program.write_text(core.inventory_source())
        audit = work/'Audit.lean'
        audit.write_text('import '+PACKAGE+'\n'+'\n'.join('#print axioms '+n for n in frozen['targets'])+'\n')
        text = run(['lake','env','lean',str(program)],'compiled_baseline',output,cwd=clone)
        clean = audit_inventory(text, frozen, core_path=core_path)
        require(clean['sha256'] == digest, 'compiled baseline inventory digest differs from real package')
        source_path = frozen['source_modules'][0]
        module = core.simple_name(source_path[:-5].replace('/','.'))
        original = (clone/source_path).read_text()
        marker = '\nend '+PACKAGE+'\n'
        require(original.count(marker) == 1, 'admission source has no unique namespace end')
        for label,declaration,(kind,origin,name,private),expected in core.COMPILED_INJECTIONS:
            injected = original.replace(marker, '\n'+declaration+marker)
            (clone/source_path).write_text(injected)
            run(['lake','build'],label+'_build',output,cwd=clone)
            run(['lake','env','leanchecker',PACKAGE],label+'_leanchecker',output,cwd=clone)
            public_axioms = run(['lake','env','lean',str(audit)],label+'_axioms',output,cwd=clone)
            core.audit_axioms(public_axioms, frozen['targets'])
            text = run(['lake','env','lean',str(program)],label,output,cwd=clone)
            result = check_admission(text,label,(kind,origin,name,private,module),expected,
                                     frozen,core_path=core_path)
            result.update(module_encoded=core.encode(module),
                          module_sha256=hashlib.sha256(injected.encode()).hexdigest(),
                          stages=['build','leanchecker','public_axioms','inventory'])
            results[label] = result
            (clone/source_path).write_text(original)
    finally:
        if work.exists():
            shutil.rmtree(work)
    return dict(scope=SCOPE,baseline_sha256=clean['sha256'],injections=results,
                kernel_or_cbz_status='NOT_AWARDED')
