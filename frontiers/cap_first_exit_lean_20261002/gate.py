#!/usr/bin/env python3
"""Source and execution gate for the CapFirstExit Lean packet. Standard library only.

    python3 gate.py              source identity, main pins, toolchain pins, forbidden tokens,
                                 declared targets
    python3 gate.py --execute    the same, then a fresh `lake build`, a `leanchecker` replay, the
                                 per-declaration axiom audit against MANIFEST.json, and three
                                 negative controls (injected sorry, custom axiom, native_decide)
                                 that the audit must reject; the exact Lean release, the dependency
                                 checkouts and the bound source identity are observed before the
                                 first and after the last Lean execution, and must agree

Scientific effect: NONE. A green gate is kernel evidence for the displayed Lean statements only.
It is not an alignment review and not an acceptance of any parent theorem.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import signal
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[1]
MODULE = 'CapFirstExit'
NAME = r"[A-Za-z_][A-Za-z0-9_'.₀-₉]*"
AXIOM_LINE = re.compile(r"'(" + NAME + r")' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
DECL = re.compile(r'^(?:noncomputable )?(theorem|def|structure) (' + NAME + r')')
FORBIDDEN = ('sorry', 'admit', 'axiom', 'native_decide', 'implemented_by', 'extern', 'unsafe',
             'opaque', 'set_option', 'macro', 'elab', 'syntax', 'run_cmd', 'run_tac', 'decreasing_by',
             'partial', 'debug', 'ofReduceBool', 'trustCompiler', 'private', 'protected', 'lemma',
             'class', 'instance', 'inductive', 'mutual', 'run_elab', 'initialize')
SKIP_DIRS = {'.lake', '__pycache__'}
# Official release commit of each Lean version this packet may pin. A pin with no entry fails closed.
LEAN_RELEASE_COMMITS = {'4.34.1': '5045d0056413266e57c625dcd7c365b10e377c52'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_json(text):
    def unique(pairs):
        keys = [k for k, _ in pairs]
        require(len(keys) == len(set(keys)), 'duplicate JSON key')
        return dict(pairs)
    return json.loads(text, object_pairs_hook=unique)


def strip_comments(text):
    """Remove Lean block comments (nested) and line comments; strings are not used in the source."""
    out, depth, i = [], 0, 0
    while i < len(text):
        if text.startswith('/-', i):
            depth += 1
            i += 2
        elif depth and text.startswith('-/', i):
            depth -= 1
            i += 2
        elif depth:
            i += 1
        elif text.startswith('--', i):
            j = text.find('\n', i)
            i = len(text) if j < 0 else j
        else:
            out.append(text[i])
            i += 1
    require(depth == 0, 'unterminated block comment')
    return ''.join(out)


def forbidden_tokens(text):
    code = strip_comments(text)
    words = set(re.findall(r'[A-Za-z_][A-Za-z0-9_]*', code))
    return sorted(set(FORBIDDEN) & words)


def declaration_records(text):
    """Fully qualified names of top-level theorem/def/structure declarations.

    Namespaces prefix names; named sections only scope variables and must close like namespaces."""
    stack, names = [], []
    for line in strip_comments(text).splitlines():
        m = re.match(r'^(namespace|section) (' + NAME + r')\s*$', line)
        if m:
            stack.append((m.group(1), m.group(2)))
            continue
        m = re.match(r'^end (' + NAME + r')\s*$', line)
        if m:
            require(stack and stack[-1][1] == m.group(1), 'unbalanced namespace or section: ' + m.group(1))
            stack.pop()
            continue
        require(re.match(r'^(section|end)\s*$', line) is None, 'anonymous section or end is not supported')
        m = DECL.match(line)
        if m:
            names.append((m.group(1), '.'.join([n for k, n in stack if k == 'namespace'] + [m.group(2)])))
    require(not stack, 'unclosed namespace or section')
    return names


def declarations(text):
    return [name for kind, name in declaration_records(text)]


def audit_axioms(text, targets, allowed):
    records = {}
    for name, raw in AXIOM_LINE.findall(text):
        require(name in targets and name not in records, 'unexpected or duplicate axiom report: ' + name)
        axioms = [] if not raw.strip() else [a.strip() for a in raw.split(',')]
        require(all(re.fullmatch(NAME, a) for a in axioms), 'malformed axiom name')
        require(set(axioms) <= set(allowed), 'forbidden transitive axiom: ' + repr(sorted(set(axioms) - set(allowed))))
        records[name] = sorted(set(axioms))
    require(set(records) == set(targets), 'missing axiom report: ' + repr(sorted(set(targets) - set(records))))
    return records


def packet_files(root):
    """Prune ignored cache trees before traversal, retaining every other source leaf."""
    paths = []
    for directory, directories, filenames in os.walk(root):
        directories[:] = [name for name in directories if name not in SKIP_DIRS]
        for name in directories:
            require(not (pathlib.Path(directory) / name).is_symlink(), 'source directory symlink')
        paths.extend((pathlib.Path(directory) / name).relative_to(root).as_posix() for name in filenames)
    return sorted(paths)


def source_check(root=None, repo=None):
    root = ROOT if root is None else root  # resolved at call time, not bound at import
    repo = REPO if repo is None else repo
    m = load_json((root / 'MANIFEST.json').read_text())
    present = packet_files(root)
    expected = sorted([e['path'] for e in m['files']] + ['MANIFEST.json'])
    require(present == expected, 'packet tree differs from manifest: ' + repr(present))
    for e in m['files']:
        p = root / e['path']
        require(not p.is_symlink() and '/' not in e['path'], 'flat regular file required: ' + e['path'])
        data = p.read_bytes()
        require(len(data) == e['bytes'] and sha(data) == e['sha256'], 'source identity mismatch: ' + e['path'])
    for pin in m['pins_on_main']:
        p = repo / pin['path']
        require(p.is_file() and not p.is_symlink(), 'pinned source missing: ' + pin['path'])
        require(git_blob(p.read_bytes()) == pin['git_blob'], 'pinned source drifted: ' + pin['path'])
    require((root / 'lean-toolchain').read_text().strip() == m['toolchain'], 'toolchain pin mismatch')
    lakefile = (root / 'lakefile.toml').read_text()
    require(re.search(r'^rev = "' + m['mathlib_rev'] + r'"$', lakefile, re.M) is not None, 'lakefile Mathlib rev mismatch')
    lock = load_json((root / 'lake-manifest.json').read_text())
    revs = {pkg['name']: pkg['rev'] for pkg in lock['packages']}
    require(revs.get('mathlib') == m['mathlib_rev'], 'lake-manifest Mathlib rev mismatch')
    require(revs == m['dependency_revisions'], 'dependency revisions differ from MANIFEST.json')
    lean_files = [name for name in present if name.endswith('.lean')]
    require(lean_files == [MODULE + '.lean'], 'unexpected Lean files: ' + repr(lean_files))
    text = (root / (MODULE + '.lean')).read_text()
    code = strip_comments(text)
    imports = re.findall(r'^import\s+(\S+)', code, re.M)
    require(imports == ['Mathlib'], 'imports must be exactly Mathlib: ' + repr(imports))
    bad = forbidden_tokens(text)
    require(not bad, 'forbidden tokens in Lean source: ' + repr(bad))
    decls = declarations(text)
    require(len(decls) == len(set(decls)), 'duplicate declaration names')
    require(decls == m['targets'], 'declared targets differ from MANIFEST.json')
    require(sorted(m['expected_axioms']) == sorted(m['targets']), 'expected_axioms must cover exactly the targets')
    require(set(m['allowed_axioms']) == {'propext', 'Classical.choice', 'Quot.sound'}, 'allowed axiom set changed')
    visible = {name: ('inductive' if kind == 'structure' else kind) for kind, name in declaration_records(text)}
    require(m.get('compiled_visible_kinds') == visible, 'visible declaration kinds differ from source')
    require(len(visible) == 152 and sum(k == 'theorem' for k in visible.values()) == 138
            and sum(k == 'def' for k in visible.values()) == 13
            and sum(k == 'inductive' for k in visible.values()) == 1, 'original visible declaration scope changed')
    return m


def pinned_lean_version(toolchain):
    m = re.fullmatch(r'leanprover/lean4:v(\d+\.\d+\.\d+)', toolchain)
    require(m is not None, 'unrecognized toolchain pin: ' + toolchain)
    return m.group(1)


def check_lean_version(text, toolchain):
    """The running Lean must be exactly the pinned release, not merely a compatible one.

    The last non-empty line of `lake env lean --version` (lake may print `info:` lines first, and
    nothing else) must fully match the pinned version, its official release commit and a Release
    build."""
    version = pinned_lean_version(toolchain)
    require(version in LEAN_RELEASE_COMMITS, 'no official release commit recorded for the pinned ' + version)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    require(lines and all(line.startswith('info:') for line in lines[:-1]),
            'unexpected output around the Lean version: ' + repr(text[:200]))
    line = lines[-1]
    pattern = (r'Lean \(version ' + re.escape(version) + r', [^()\r\n]+, commit '
               + LEAN_RELEASE_COMMITS[version] + r', Release\)')
    require(re.fullmatch(pattern, line) is not None,
            'running Lean is not the pinned release ' + version + ': ' + repr(line[:160]))
    return line


def check_worktree_clean(name, status):
    """`git status --porcelain` output of a dependency: staged, unstaged or untracked changes fail."""
    require(status.strip() == '', 'dependency worktree is not clean: ' + name + ': ' + status.strip()[:200])


def dependency_state(m):
    """Exact pinned revision and a clean worktree for every dependency, read from the checkouts."""
    actual = {}
    for name in m['dependency_revisions']:
        repo = str(ROOT / '.lake' / 'packages' / name)
        actual[name] = subprocess.check_output(['git', '-C', repo, 'rev-parse', 'HEAD'], text=True).strip()
        check_worktree_clean(name, subprocess.check_output(
            ['git', '-C', repo, 'status', '--porcelain', '--untracked-files=normal'], text=True))
    require(actual == m['dependency_revisions'], 'checked-out dependency revisions differ from MANIFEST.json')
    return actual


def source_identity(m, root=None, repo=None):
    """SHA-256 over the source that source_check binds, read afresh from disk: the bytes of
    MANIFEST.json itself, of every manifest file and of every pinned source on main, by name and
    SHA-256 in manifest order. Any byte change to any of them changes the digest."""
    root = ROOT if root is None else root
    repo = REPO if repo is None else repo
    parts = [('MANIFEST.json', root / 'MANIFEST.json')]
    parts += [(e['path'], root / e['path']) for e in m['files']]
    parts += [('main:' + pin['path'], repo / pin['path']) for pin in m['pins_on_main']]
    return sha(''.join(name + '\0' + sha(path.read_bytes()) + '\n' for name, path in parts).encode())


def run_process(command, cwd, timeout=1800):
    """Own one process group, retaining partial streams and reaping it on timeout."""
    process = subprocess.Popen(command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    timed_out = False
    signals = []
    try:
        stdout,stderr=process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out=True
        try:
            os.killpg(process.pid,signal.SIGTERM);signals.append('SIGTERM')
        except ProcessLookupError:
            pass
        try:
            stdout,stderr=process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid,signal.SIGKILL);signals.append('SIGKILL')
            except ProcessLookupError:
                pass
            stdout,stderr=process.communicate()
    result=subprocess.CompletedProcess(command,process.returncode,stdout,stderr)
    result.timed_out=timed_out;result.cleanup_signals=signals
    return result


def run(command, label, out, expect_success=True, cwd=None, pure_stream=False):
    working_directory=ROOT if cwd is None else cwd
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc = run_process(command,cwd=working_directory,timeout=1800)
    log = proc.stdout + proc.stderr
    (out / (label + '.log')).write_text(log)
    (out / (label + '.stdout')).write_text(proc.stdout)
    (out / (label + '.stderr')).write_text(proc.stderr)
    (out / (label + '.exit')).write_text(str(proc.returncode) + '\n')
    (out / (label + '.process.json')).write_text(json.dumps({'command':command,'cwd':str(working_directory),
        'exit':proc.returncode,'timed_out':getattr(proc,'timed_out',False),
        'cleanup_signals':getattr(proc,'cleanup_signals',[]),'started_utc':started,
        'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
    require(not getattr(proc,'timed_out',False), label+' timed out; partial streams and cleanup retained')
    if expect_success:
        require(proc.returncode == 0, label + ' failed:\n' + log[-4000:])
    if pure_stream:
        require(proc.returncode == 0 and proc.stderr == '', label + ' requires successful pure stdout')
    return log


def compiled_implementation():
    path = ROOT / 'compiled_inventory.py'
    spec = importlib.util.spec_from_file_location('cap_compiled_inventory', path)
    require(spec is not None and spec.loader is not None, 'compiled inventory loader unavailable')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compiled_contract(m, implementation):
    require(isinstance(m.get('compiled_inventory'), list),
            'CBZ_CAP_COMPILED_INVENTORY_UNQUALIFIED: actual pinned compiled census binding required')
    require(m.get('compiled_inventory_schema') == 'cap-name-components-v1', 'compiled inventory schema')
    require(implementation.ALLOWED == frozenset(m['allowed_axioms']), 'compiled axiom policy mismatch')
    implementation.parse_binding(m['compiled_inventory'],
                                 {implementation.dotted(n): k for n,k in m['compiled_visible_kinds'].items()})
    require(isinstance(m.get('compiled_codegen_inventory'),list),'actual IR-name binding required')
    implementation.parse_codegen(m['compiled_codegen_inventory'])
    observation=m.get('compiled_inventory_observation')
    require(isinstance(observation,dict) and observation.get('proof_sha256')==sha((ROOT/'CapFirstExit.lean').read_bytes()),
            'compiled binding observation has different proof identity')
    require(observation.get('support_records')==len(m['compiled_inventory'])
            and observation.get('ir_names')==len(m['compiled_codegen_inventory'])
            and observation.get('owned_constants')==len(m['targets'])+len(m['compiled_inventory']),
            'compiled binding differs from observed census size')


def output_objects(packet):
    required=['.lake/build/lib/lean/CapFirstExit.olean','.lake/build/lib/lean/CapFirstExit.ilean',
              '.lake/build/ir/CapFirstExit.c']
    optional=['.lake/build/lib/lean/CapFirstExit.olean.private','.lake/build/lib/lean/CapFirstExit.olean.server',
              '.lake/build/lib/lean/CapFirstExit.ir','.lake/build/lib/lean/CapFirstExit.ir.sig']
    paths=required+[name for name in optional if (packet/name).exists()]
    result={}
    for name in paths:
        path=packet/name
        require(path.is_file() and not path.is_symlink(), 'missing or symlink compiled output: '+name)
        data=path.read_bytes();result[name]={'bytes':len(data),'sha256':sha(data)}
    return result


def audit_compiled(m, out, axioms):
    implementation = compiled_implementation()
    compiled_contract(m, implementation)
    program = out / 'Inventory.lean'
    program.write_text(implementation.inventory_source())
    text = run(['lake', 'env', 'lean', str(program)], 'compiled_inventory', out, pure_stream=True)
    report = implementation.audit_inventory(text, m['compiled_visible_kinds'], m['compiled_inventory'], axioms,
                                            m['compiled_codegen_inventory'])
    report['program_sha256'] = sha(program.read_bytes())
    report['admission_controls'] = compiled_admission(m, implementation, report, out)
    return report


def compiled_admission(m, implementation, baseline, out):
    """Actual disposable package mutations; unrelated build/audit failures are never kills."""
    mutations = {
        'private_theorem': ('\nnamespace CapFirstExit\nprivate theorem cbzUnlisted : True := by trivial\nend CapFirstExit\n',
                            {'extra_user_theorem', 'unregistered_constant'}),
        'private_sorry': ('\nnamespace CapFirstExit\nprivate theorem cbzUnlistedSorry : True := by sorry\nend CapFirstExit\n',
                          {'extra_user_theorem', 'unregistered_constant', 'forbidden_axiom'}),
        'unused_sorry_def': ('\nnamespace CapFirstExit\nnoncomputable def cbzUnused : Nat := by sorry\nend CapFirstExit\n',
                             {'extra_user_definition', 'unregistered_constant', 'forbidden_axiom'}),
        'range_less': ('\nset_option maxRecDepth 1000 in run_elab\n  Lean.addDecl <| .thmDecl {\n'
                       '    name := `CapFirstExit.path_meets_frontier._proof_999\n    levelParams := []\n'
                       '    type := Lean.mkConst ``True\n    value := Lean.mkConst ``True.intro\n  }\n',
                       {'unregistered_constant'})}
    results = {}
    work_parent = ROOT / '.lake' / 'compiled-admission'
    require(not work_parent.is_symlink(), 'symlink compiled admission directory')
    work_parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=work_parent, prefix='run-') as temporary:
        work = pathlib.Path(temporary)
        def one(label, injection, expected):
            packet = work / label
            shutil.copytree(ROOT, packet, ignore=lambda directory, names: ['.lake'] if pathlib.Path(directory) == ROOT else [])
            shutil.copytree(ROOT / '.lake' / 'build', packet / '.lake' / 'build')
            (packet / '.lake' / 'packages').symlink_to(ROOT / '.lake' / 'packages', target_is_directory=True)
            source = packet / (MODULE + '.lean')
            source.write_bytes(source.read_bytes() + injection.encode())
            setup=packet/'.lake/build/ir/CapFirstExit.setup.json'
            require(setup.is_file() and not setup.is_symlink(), 'missing actual Lake compiler setup')
            setup_sha256=sha(setup.read_bytes())
            if label != 'baseline':
                # Exact full source compilation using the successful Lake setup; dependency
                # artifacts are read through its absolute import paths. Every output is local
                # to this copied packet, so concurrent controls cannot rebuild shared packages.
                command=['lake','env','lean',str(source),'-j2',
                         '-o',str(packet/'.lake/build/lib/lean/CapFirstExit.olean'),
                         '-i',str(packet/'.lake/build/lib/lean/CapFirstExit.ilean'),
                         '-c',str(packet/'.lake/build/ir/CapFirstExit.c'),
                         '--setup',str(setup),'--json']
                run(command, 'admission_'+label+'_build', out, cwd=packet)
            objects=output_objects(packet)
            if label != 'baseline':
                run(['lake','env','leanchecker',MODULE], 'admission_'+label+'_kernel', out, cwd=packet)
                public = run(['lake','env','lean',str(out / 'Axioms.lean')], 'admission_'+label+'_axioms', out, cwd=packet)
                audit_axioms(public, m['targets'], m['allowed_axioms'])
            text = run(['lake','env','lean',str(out / 'Inventory.lean')], 'admission_'+label+'_inventory', out,
                       cwd=packet, pure_stream=True)
            inventory = implementation.parse_inventory(text)
            require(output_objects(packet)==objects and sha(setup.read_bytes())==setup_sha256,
                    'compiled outputs or compiler setup changed during control audit: '+label)
            findings = implementation.inventory_violations(inventory, m['compiled_visible_kinds'], m['compiled_inventory'],
                                                            codegen_records=m['compiled_codegen_inventory'])
            if label == 'baseline':
                copied = implementation.audit_inventory(text, m['compiled_visible_kinds'], m['compiled_inventory'],
                                                        codegen_records=m['compiled_codegen_inventory'])
                require(copied['sha256'] == baseline['sha256'], 'copied compiled baseline differs')
                return label, copied
            codes = {code for code, name, note in findings}
            require(codes == expected, 'compiled control '+label+' rejected for unexpected reasons: '+repr(findings))
            injected = [row for row in inventory['constants'] if ('cbzUnlisted' in implementation.render(row[3])
                        or 'cbzUnused' in implementation.render(row[3]) or row[3][-1] == '_proof_999')]
            require(len(injected) == 1, 'compiled control injection missing or ambiguous: '+label)
            full_name = implementation.encode(injected[0][3])
            for code, name, note in findings:
                require(name == full_name or (code == 'forbidden_axiom' and name == implementation.encode(('sorryAx',))),
                        'compiled control wrong full declaration identity: '+label)
            return label, {'outcome':'REJECTED_FOR_EXPECTED_REASON', 'injected_name':full_name,
                           'findings':[list(row) for row in findings], 'mutated_source_sha256':sha(source.read_bytes()),
                           'compiler_setup_sha256':setup_sha256,'output_objects':objects,
                           'compilation':'full unchanged prefix plus injection; exact Lake setup; private outputs; 2 Lean threads'}
        one('baseline','',set())
        # At most two independent package controls, each with two Lean threads.
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures=[executor.submit(one,label,injection,expected) for label,(injection,expected) in mutations.items()]
            try:
                for future in futures:
                    label,result=future.result();results[label]=result
            except BaseException:
                for future in futures:future.cancel()
                raise
    return results


def observe(m, out, label):
    """One observation of what execution runs against, read afresh: the exact Lean release (G1),
    every dependency at its pinned HEAD with a clean worktree, and the source identity re-checked by
    source_check against the manifest bound before execution. The source is read last."""
    version = check_lean_version(run(['lake', 'env', 'lean', '--version'], label, out), m['toolchain'])
    revisions = dependency_state(m)
    require(source_check(ROOT, REPO) == m, 'MANIFEST.json differs from the manifest bound before execution')
    return {'lean_version': version, 'dependency_revisions': revisions, 'dependency_worktrees': 'CLEAN',
            'source_identity_sha256': source_identity(m)}


def execute(m):
    require(ROOT.is_dir() and not ROOT.is_symlink(), 'symlink or absent package root')
    require(not (ROOT/'.lake').is_symlink(), 'symlink .lake ancestor')
    out = ROOT / '.lake' / 'evidence'
    require(not out.is_symlink(), 'symlink evidence directory')
    if out.exists():
        history = ROOT / '.lake' / 'evidence-history'
        require(not history.is_symlink(), 'symlink evidence history')
        history.mkdir(exist_ok=True)
        archive = pathlib.Path(tempfile.mkdtemp(prefix='attempt-', dir=history)) / 'evidence'
        shutil.move(str(out), archive)
    out.mkdir(parents=True)
    preflight = observe(m, out, 'version')  # before the first Lean execution
    compiled_contract(m, compiled_implementation())
    build = ROOT / '.lake' / 'build'
    require(not build.is_symlink(), 'symlink build directory')
    if build.exists():
        shutil.rmtree(build)  # fresh build of this package; the Mathlib cache is untouched
    log = run(['lake', 'build'], 'build', out)
    require('error' not in log.lower(), 'build log reports an error')
    require('declaration uses' not in log, 'build log reports sorry or a similar escape')
    run(['lake', 'env', 'leanchecker', MODULE], 'leanchecker', out)
    audit = out / 'Axioms.lean'
    audit.write_text('import ' + MODULE + '\n' + ''.join('#print axioms ' + n + '\n' for n in m['targets']))
    axioms = audit_axioms(run(['lake', 'env', 'lean', str(audit)], 'axioms', out), m['targets'], m['allowed_axioms'])
    require(axioms == {k: sorted(v) for k, v in m['expected_axioms'].items()}, 'axiom report differs from MANIFEST.json')
    compiled = audit_compiled(m, out, axioms)
    controls = {
        'sorry': 'theorem injected : False := by sorry\n',
        'custom_axiom': 'axiom hiddenPremise : False\ntheorem injected : False := hiddenPremise\n',
        'native_decide': 'theorem injected : (2 : Nat) + 2 = 4 := by native_decide\n'}
    outcomes = {}
    for label, body in controls.items():
        path = out / ('Control_' + label + '.lean')
        path.write_text('import ' + MODULE + '\n' + body + '#print axioms injected\n')
        clog = run(['lake', 'env', 'lean', str(path)], 'control_' + label, out, pure_stream=True)
        try:
            audit_axioms(clog, ['injected'], m['allowed_axioms'])
        except ValueError as exc:
            require('forbidden transitive axiom' in str(exc), 'control ' + label + ' failed for the wrong reason: ' + str(exc))
            outcomes[label] = 'REJECTED'
            continue
        raise ValueError('negative control escaped the audit: ' + label)
    final = observe(m, out, 'version_final')  # after the last Lean execution, before the receipt
    require(final['lean_version'] == preflight['lean_version'],
            'Lean runtime changed during execution: ' + repr((preflight['lean_version'], final['lean_version'])))
    require(final['dependency_revisions'] == preflight['dependency_revisions'], 'dependency revisions changed during execution')
    require(final['source_identity_sha256'] == preflight['source_identity_sha256'], 'bound source changed during execution')
    require(final == preflight, 'execution observations differ')
    receipt = {
        'scientific_effect': 'NONE',
        'module': MODULE,
        'lean_version': final['lean_version'],
        'toolchain': m['toolchain'],
        'dependency_revisions': final['dependency_revisions'],
        'source_sha256': {e['path']: e['sha256'] for e in m['files']},
        'build': 'PASS', 'leanchecker': 'PASS', 'dependency_worktrees': 'CLEAN',
        'axioms': axioms,
        'negative_controls': outcomes,
        'compiled_inventory': compiled,
        'observations': {'preflight': preflight, 'final': final},
        'alignment_review': 'NOT_CLAIMED'}
    text = json.dumps(receipt, indent=2, sort_keys=True) + '\n'
    (out / 'receipt.json').write_text(text)
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--execute', action='store_true', help='build, replay, audit axioms and run negative controls')
    args = p.parse_args()
    m = source_check()
    if args.execute:
        receipt = execute(m)
        print(json.dumps({'passed': True, 'axioms_allowed_only': True,
                          'negative_controls': receipt['negative_controls'], 'targets': len(m['targets'])}, sort_keys=True))
    else:
        print(json.dumps({'passed': True, 'source_check': 'PASS', 'targets': len(m['targets'])}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print('GATE FAILURE: ' + str(exc), file=sys.stderr)
        sys.exit(1)
