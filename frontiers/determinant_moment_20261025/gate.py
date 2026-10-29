#!/usr/bin/env python3
"""Source-bound Lean evidence, not a scientific acceptance engine (stdlib only)."""
import argparse
import hashlib
import importlib.util
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
REPO = ROOT.parents[1]
_LOADED_SOURCE_PATH = Path(__file__).resolve()
_LOADED_SOURCE_BYTES = _LOADED_SOURCE_PATH.read_bytes()
_LOADED_CODE = sys._getframe().f_code


# Load only after CLI invalidation and bound-file checks, so a missing or invalid
# bound helper cannot bypass active-receipt invalidation during import.
_compiled = None
_determinant = None
CORE_SHA256 = 'ff8a5374597772b2d37054fd722c2243c4b552a63802c69f7c605519832be6c4'


def verified_implementation(name, path, expected_sha256, message):
    """Execute the single authenticated read; timestamp-valid pyc files are ignored."""
    path = Path(path)
    require(all(not p.is_symlink() for p in (path, *path.parents)), 'symlink inventory implementation')
    require(path.is_file(), 'missing inventory implementation')
    raw = path.read_bytes()
    require(isinstance(expected_sha256, str) and SHA256.fullmatch(expected_sha256)
            and sha(raw) == expected_sha256, message)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, 'cannot load inventory implementation')
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def compiled_implementation():
    global _compiled
    _compiled = verified_implementation('determinant_compiled_inventory',
        ROOT / 'compiled_inventory.py', CORE_SHA256, 'source-preserved core helper hash mismatch')
    return _compiled


def determinant_implementation(m):
    global _determinant
    files = m.get('files')
    require(isinstance(files, dict), 'missing bound determinant adapter identity')
    _determinant = verified_implementation('determinant_specific_inventory',
        ROOT / 'determinant_inventory.py', files.get('determinant_inventory.py'),
        'determinant adapter source hash mismatch')
    return _determinant


def compiled_contract(m):
    """Require a bound non-target inventory; never infer one from source regexes."""
    require(isinstance(m.get('compiled_inventory'), list),
            'CBZ_COMPILED_INVENTORY_UNQUALIFIED: exact non-target compiled constants '
            'have not been inventoried for this determinant package; pinned Lean '
            'census, binding and full execution are required')
    compiled_implementation()
    require(_compiled.ALLOWED == ALLOWED, 'compiled inventory axiom policy mismatch')
    targets = m.get('targets')
    require(isinstance(targets, list) and targets and
            all(isinstance(t, str) for t in targets) and len(set(targets)) == len(targets),
            'empty or duplicate target list')
    paths = m.get('source_modules')
    require(isinstance(paths, list) and paths and all(isinstance(p, str) for p in paths)
            and len(set(paths)) == len(paths), 'invalid source module registry')
    require(all(re.fullmatch(r'ResearchFormalCoreR1/[A-Za-z_][A-Za-z0-9_]*\.lean', p)
                for p in paths), 'noncanonical source module path')
    modules = {p[:-5].replace('/', '.') for p in paths}
    version = m.get('compiled_inventory_version')
    require(version is None or type(version) is int and version == 2,
            'unsupported compiled inventory version')
    if version == 2:
        policy = determinant_implementation(m)
        return modules, policy.bound_contract(m, _compiled)
    bound = _compiled.bound_inventory(m['compiled_inventory'], targets, modules)
    return modules, bound


def audit_compiled(text, m, reported_axioms):
    """Validate the actual compiled package census and all-constant axiom closure."""
    modules, bound = compiled_contract(m)
    if m.get('compiled_inventory_version') == 2:
        return _determinant.audit_inventory(text, m, reported_axioms=reported_axioms)
    return _compiled.audit_inventory(text, m['targets'], modules,
                                     reported_axioms=reported_axioms, bound=bound)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)


def invalidate_active_receipt():
    """Invalidate only the active receipt; historical evidence remains immutable."""
    out = ROOT / '.lake' / 'formal-evidence'
    require(not (ROOT / '.lake').is_symlink() and not (ROOT / '.lake/build').is_symlink()
            and not out.is_symlink(), 'symlink build directory')
    (out / 'receipt.json').unlink(missing_ok=True)

def check_lean_version(text):
    version = text.strip()
    require(re.fullmatch(r'Lean \(version 4\.34\.1, [^()\r\n]+, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release\)', version) is not None,
            'unexpected running Lean version: ' + repr(version))
    return version

def check_worktree_clean(name, status):
    """`git status --porcelain` output of a dependency: staged, unstaged or untracked changes fail."""
    require(status.strip() == '', 'dependency worktree is not clean: ' + name + ': ' + status.strip()[:200])

def _git_bytes(repo, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_NO_REPLACE_OBJECTS='1', GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0')
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)

def verify_committed_files(repo, head, paths=None, allow_symlinks=False):
    """Compare HEAD, stage-zero index and actual file bytes, ignoring no index flags.

    SHA-1 here is Git's exact blob object identity, not a mathematical bound.
    Manifest file identities separately use SHA-256. Owned symlinks, all gitlinks
    and non-stage-zero entries are refused. Dependency file symlinks additionally
    bind their literal link bytes and resolved tracked regular-file targets.
    """
    repo = Path(repo).resolve()
    selected = [] if paths is None else sorted(set(paths))
    require(paths is None or selected, 'empty committed source domain')
    args = ['ls-tree', '-rz', head]
    if paths is not None:
        args += ['--', *selected]
    tree = {}
    for row in _git_bytes(repo, *args).split(b'\0'):
        if not row:
            continue
        fields, separator, encoded = row.partition(b'\t')
        require(separator, 'malformed committed source inventory')
        mode, kind, oid = fields.decode('ascii').split()
        name = encoded.decode('utf-8')
        require(name not in tree and kind == 'blob' and mode in (('100644', '100755', '120000') if allow_symlinks else ('100644', '100755')),
                'unsupported or symlink committed source: ' + name)
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,
                'unsafe committed source path')
        tree[name] = (mode, oid)
    require(bool(tree), 'empty committed source tree')
    if paths is not None:
        require(set(tree) == set(selected), 'uncommitted source domain entry')
    index = {}
    index_args = ['ls-files', '--stage', '-z']
    if paths is not None:
        index_args += ['--', *selected]
    for row in _git_bytes(repo, *index_args).split(b'\0'):
        if not row:
            continue
        fields, separator, encoded = row.partition(b'\t')
        require(separator, 'malformed source index')
        mode, oid, stage = fields.decode('ascii').split()
        name = encoded.decode('utf-8')
        require(stage == '0' and name not in index, 'unmerged or duplicate source index')
        index[name] = (mode, oid)
    require(index == tree, 'source index differs from committed source')
    for name, (mode, oid) in tree.items():
        path = repo / name
        if mode == '120000':
            require(allow_symlinks and path.is_symlink() and path.parent.resolve() == path.parent,
                    'missing or substituted committed source symlink: ' + name)
            target = path.resolve()
            require(target.is_relative_to(repo) and
                    target.relative_to(repo).as_posix() in tree and
                    tree[target.relative_to(repo).as_posix()][0] in ('100644', '100755') and target.is_file(),
                    'unbound symlink target in committed source: ' + name)
            data = os.fsencode(os.readlink(path))
        else:
            require(not path.is_symlink() and path.resolve() == path and path.is_file(),
                    'missing or symlink committed source: ' + name)
            data = path.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
        require(actual == oid, 'working bytes differ from committed source: ' + name)
        require(mode == '120000' or bool(path.stat().st_mode & 0o111) == (mode == '100755'),
                'working mode differs from committed source: ' + name)
    return set(tree)


def source_custody(m, digest, expected_head=None):
    """Bind observed package bytes and code to a commit; not an immutable mount."""
    root = Path(ROOT).resolve()
    repo = Path(_git_bytes(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    prefix = root.relative_to(repo).as_posix() + '/'
    head = _git_bytes(repo, 'rev-parse', 'HEAD').decode().strip()
    require(COMMIT.fullmatch(head), 'missing exact checked commit')
    require(expected_head is None or head == expected_head, 'HEAD changed during execution')
    require(isinstance(m.get('files'), dict) and 'gate.py' in m['files'], 'unbound loaded driver')
    names = set(m['files']) | {'manifest.json'}
    require(all(isinstance(name, str) and not Path(name).is_absolute() and
                '..' not in Path(name).parts for name in names), 'unsafe bound source path')
    owned = [prefix + name for name in names]
    admission = m.get('source_admission')
    if admission is not None:
        require(isinstance(admission, dict) and SHA256.fullmatch(admission.get('helper_sha256', '')),
                'invalid source admission helper binding')
        helper_name = 'tools/lean_packet_admission.py'
        owned.append(helper_name)
    verify_committed_files(repo, head, owned)
    raw = (root / 'manifest.json').read_bytes()
    require(sha(raw) == digest and load_json(raw) == m, 'manifest identity differs from execution')
    for name, expected in m['files'].items():
        require(sha((root / name).read_bytes()) == expected, 'bound source identity differs: ' + name)
    if admission is not None:
        require(sha((repo / helper_name).read_bytes()) == admission['helper_sha256'],
                'source admission helper identity differs')
    require(root / 'gate.py' == _LOADED_SOURCE_PATH and
            (root / 'gate.py').read_bytes() == _LOADED_SOURCE_BYTES and
            _LOADED_CODE == compile(_LOADED_SOURCE_BYTES, _LOADED_CODE.co_filename,
                                    'exec', dont_inherit=True, optimize=sys.flags.optimize),
            'loaded driver differs from committed source')
    require(_git_bytes(repo, 'rev-parse', 'HEAD').decode().strip() == head,
            'HEAD changed during source observation')
    return head

def dependency_state(m):
    """Exact locked revision and a clean worktree for every dependency, read from the checkouts."""
    actual = {}
    for name in m['dependency_revisions']:
        repo = str(ROOT / '.lake' / 'packages' / name)
        actual[name] = _git_bytes(repo, 'rev-parse', 'HEAD').decode().strip()
        check_worktree_clean(name, _git_bytes(
            repo, 'status', '--porcelain', '--untracked-files=normal').decode())
    require(actual == m['dependency_revisions'], 'installed dependency HEAD differs from lock')
    for name, head in actual.items():
        repo = (ROOT / '.lake' / 'packages' / name).resolve()
        try:
            tracked = verify_committed_files(repo, head, allow_symlinks=True)
        except ValueError as exc:
            raise ValueError('dependency ' + name + ' source custody: ' + str(exc)) from exc
        for directory, folders, files in os.walk(repo, followlinks=False):
            folders[:] = [part for part in folders if part not in ('.git', '.lake')]
            for part in folders:
                require(not (Path(directory) / part).is_symlink(),
                        'dependency source directory symlink: ' + name)
            for filename in files:
                path = Path(directory) / filename
                relative = path.relative_to(repo).as_posix()
                if filename.endswith(('.lean', '.olean', '.ilean')):
                    require(relative in tracked, 'dependency untracked Lean source: ' + name + '/' + relative)
        require(_git_bytes(repo, 'rev-parse', 'HEAD').decode().strip() == head,
                'dependency HEAD changed during source observation: ' + name)
    return actual

def observation(version, dependencies, digest):
    return {'lean_version': version, 'dependency_revisions': dependencies, 'dependency_worktrees': 'CLEAN',
            'manifest_sha256': digest}

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

def load_admission(repo, metadata):
    """Verify fixed helper bytes BEFORE executing them; never trust a manifest path."""
    require(isinstance(metadata, dict) and set(metadata) == {'helper_sha256', 'census', 'continuations', 'declarations'},
            'source declaration census metadata malformed')
    digest = metadata['helper_sha256']
    require(isinstance(digest, str) and re.fullmatch(r'[0-9a-f]{64}', digest), 'invalid admission helper hash')
    helper = repo / 'tools' / 'lean_packet_admission.py'
    require(all(not part.is_symlink() for part in (helper, *helper.parents)),
            'symlink admission helper')
    require(helper.is_file(), 'missing admission helper')
    data = helper.read_bytes()
    require(sha(data) == digest, 'admission helper hash mismatch')
    # Execute exactly the verified bytes, without importlib's second read or pyc cache.
    namespace = {'__name__': '_verified_lean_packet_admission', '__file__': str(helper)}
    exec(compile(data, str(helper), 'exec'), namespace)
    return namespace

def source_check():
    raw = (ROOT / 'manifest.json').read_bytes()
    m = load_json(raw)
    require(m.get('schema_version') == 1 and m.get('scientific_effect') == 'NONE', 'invalid evidence schema')
    require(m.get('formalization_status') == 'proved' and m.get('alignment_status') == 'PENDING_INDEPENDENT_REVIEW', 'source metadata cannot self-award execution or review')
    required = {'gate.py', 'tests/test_gate.py', 'lean-toolchain', 'lakefile.toml', 'lake-manifest.json', 'ResearchFormalCoreR1.lean', 'SCOPE.md', 'GLOSSARY.md', 'README.md', 'blueprint/src/content.tex', 'tests/test_alignment_lineage.py', 'LINEAGE_VALIDATION.md', 'compiled_inventory.py', 'tests/test_compiled_admission.py', 'tests/test_cli_receipt_boundary.py', 'tests/run_cbz_mutations.py', 'GOVERNANCE.md', 'TOOLING.md', 'QUARANTINE.json', 'STATUS.md'}
    if m.get('compiled_inventory_version') == 2:
        required |= {'determinant_inventory.py', 'tests/test_determinant_inventory.py',
                     'tests/test_determinant_admission_harness.py', 'tests/run_adapter_mutations.py',
                     'tests/test_adapter_mutation_runner.py', 'tests/test_determinant_execute.py',
                     'tests/test_inventory_loader.py', 'tests/test_determinant_binding.py',
                     'tests/fixtures/actual_inventory_4ccc.log',
                     'tests/fixtures/actual_manifest_v2_fields.json'}
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
    admission = load_admission(REPO, m.get('source_admission'))
    continuation_bindings = m['source_admission']['continuations']
    require(isinstance(continuation_bindings, dict) and set(continuation_bindings) ==
            {path[:-5].replace('/', '.') for path in m['source_modules']}, 'source continuation module inventory mismatch')
    declaration_bindings = m['source_admission']['declarations']
    require(isinstance(declaration_bindings, dict) and set(declaration_bindings) ==
            {path[:-5].replace('/', '.') for path in m['source_modules']}, 'source declaration header module inventory mismatch')
    source_census = []
    for path in m['source_modules']:
        require(path in m['files'], 'unbound source module')
        text = (ROOT / path).read_text()
        module = path[:-5].replace('/', '.')
        require(continuation_bindings[module] is not None, 'unsupported missing source continuation binding')
        require(declaration_bindings[module] is not None, 'unsupported missing source declaration header binding')
        source_census.extend(admission['census'](text, module, continuation_bindings[module], declaration_bindings[module]))
    admission['check_census'](source_census, m['source_admission']['census'])
    names = [d['name'] for d in source_census if d['kind'] in {'theorem', 'lemma'} and d['privacy'] == 'public']
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
    invalidate_active_receipt()
    out = ROOT / '.lake' / 'formal-evidence'
    checked_head = source_custody(m, digest)
    modules, bound = compiled_contract(m)
    out.mkdir(parents=True, exist_ok=True)
    preflight_version = check_lean_version(run(['lake', 'env', 'lean', '--version'], 'version-preflight', out))
    preflight = observation(preflight_version, dependency_state(m), digest)
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
    inventory_source = out / 'Inventory.lean'
    inventory_source.write_text(_compiled.inventory_source())
    inventory = audit_compiled(
        run(['lake', 'env', 'lean', str(inventory_source)], 'inventory', out), m, axioms)
    # Both mutations must build, pass leanchecker and the public-only axiom audit,
    # then fail this package-wide census for exactly their intended admission reason.
    if m.get('compiled_inventory_version') == 2:
        # The unchanged core's injection payloads run through the same exact
        # determinant policy as the positive inventory, with frozen bindings.
        compiled_admission = _determinant.compiled_admission(m, inventory, out, package_root=ROOT)
    else:
        _compiled.ROOT = ROOT
        compiled_admission = _compiled.compiled_admission(m, modules, inventory, bound, out)
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
    source_custody(m, digest, checked_head)
    _, after = source_check(); require(after == digest, 'manifest changed during execution')
    # Final observation after the last Lean execution: the same exact release, the same locked
    # and clean dependencies and the same bound sources as before the first one.
    version = check_lean_version(run(['lake', 'env', 'lean', '--version'], 'version', out))
    final = observation(version, dependency_state(m), after)
    require(final == preflight, 'runtime, dependencies or sources changed during execution')
    head = source_custody(m, digest, checked_head)
    receipt = dict(schema_version=1, scientific_effect='NONE', formalization_status='kernel-checked',
                   alignment_status='PENDING_INDEPENDENT_REVIEW', manifest_sha256=digest,
                   checked_commit=head, repository=os.environ.get('GITHUB_REPOSITORY'),
                   workflow_run_id=os.environ.get('GITHUB_RUN_ID'),
                   workflow_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'), lean_version=version,
                   dependency_revisions=m['dependency_revisions'], dependency_worktrees='CLEAN',
                   observations={'preflight': preflight, 'final': final},
                   axioms=axioms, negative_controls=outcomes,
                   inventory={**inventory, 'compiled_admission': compiled_admission})
    receipt['logs'] = {p.name: sha(p.read_bytes()) for p in sorted(out.glob('*.log'))}
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt

def main():
    try:
        # Every CLI attempt invalidates prior active evidence before argument,
        # source, manifest, helper or qualification failures can short-circuit.
        invalidate_active_receipt()
        p = argparse.ArgumentParser(description=__doc__)
        p.add_argument('--execute', action='store_true', help='run build, transitive axiom audit and negative controls')
        p.add_argument('--alignment', type=Path, help='validate a separately authenticated alignment record; never promotes science')
        args = p.parse_args()
        if args.execute:
            initial_raw = (ROOT / 'manifest.json').read_bytes()
            source_custody(load_json(initial_raw), sha(initial_raw))
        m, digest = source_check()
        if args.alignment:
            check_alignment(load_json(args.alignment.read_text()), digest, m['targets'], m['files']['SCOPE.md'])
        if args.execute:
            execute(m, digest)
        else:
            compiled_contract(m)
            raise ValueError('CBZ_KERNEL_EXECUTION_REQUIRED: source identity and compiled '
                             'bindings alone do not establish kernel evidence; run --execute')
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as e:
        print('FORMAL_GATE_FAIL: ' + str(e), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
