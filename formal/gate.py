#!/usr/bin/env python3
"""RF-GATE-01 compatibility entrypoint.

The reviewed compiled-environment gate remains byte-identical in ``gate_helper.py``.
This module re-exports its public API, binds a constrained manifest overlay, and
retains the later exact-runtime/dependency observation contract from current main.
Scientific effect: NONE.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

_WRAPPER_SOURCE_PATH = Path(__file__).resolve()
_WRAPPER_SOURCE_BYTES = _WRAPPER_SOURCE_PATH.read_bytes()
_WRAPPER_CODE = sys._getframe().f_code
_HELPER_SOURCE_BYTES = None

if 'gate_helper' in sys.modules:
    _core = sys.modules['gate_helper']
else:
    _helper_path = Path(__file__).resolve().with_name('gate_helper.py')
    _helper_spec = importlib.util.spec_from_file_location('rf312_gate_helper', _helper_path)
    if _helper_spec is None or _helper_spec.loader is None:
        raise ImportError('cannot load reviewed RF312 helper: ' + str(_helper_path))
    _core = importlib.util.module_from_spec(_helper_spec)
    # Compile the bytes we retain; do not admit an unrelated cached bytecode file.
    _HELPER_SOURCE_BYTES = _helper_path.read_bytes()
    exec(compile(_HELPER_SOURCE_BYTES, str(_helper_path), 'exec', dont_inherit=True), _core.__dict__)

# Re-export the reviewed helper API. Tests and callers continue importing `gate`.
for _name in dir(_core):
    if not _name.startswith('_'):
        globals()[_name] = getattr(_core, _name)

ROOT = Path(__file__).resolve().parent
OVERLAY = ROOT / 'manifest.overlay.json'
_HELPER_LOAD_JSON = _core.load_json
_HELPER_SOURCE_CHECK = _core.source_check
_HELPER_EXECUTE = _core.execute
_HELPER_RUN = _core.run
_ALLOWED_OVERLAY_KEYS = frozenset({'schema_version', 'files'})


def _sync_root():
    """Propagate this module's effective ``ROOT`` to the reviewed helper at every call boundary.

    The helper reads its own module global ``ROOT`` (and this module derives the overlay path
    from ``ROOT``) at call time, so a caller that rebinds ``gate.ROOT`` -- the fixtures of the
    runtime tests do -- must be observed by every source, overlay and execution read, not only
    by this wrapper. Import-time constants would silently keep reading the original tree.
    """
    global OVERLAY
    root = Path(ROOT)
    _core.ROOT = root
    OVERLAY = root / 'manifest.overlay.json'
    return root


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_lean_version(text):
    version = text.strip()
    require(re.fullmatch(
        r'Lean \(version 4\.34\.1, [^()\r\n]+, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release\)',
        version) is not None, 'unexpected running Lean version: ' + repr(version))
    return version


def check_worktree_clean(name, status):
    require(status.strip() == '',
            'dependency worktree is not clean: ' + name + ': ' + status.strip()[:200])



def run(command, label, out, expect_success=True, cwd=None):
    """The effective root is observed at call time, including compiled-admission copies."""
    return _HELPER_RUN(command, label, out, expect_success,
                       cwd=_sync_root() if cwd is None else cwd)


_GIT_ENV_OVERRIDES = {
    'GIT_CONFIG_NOSYSTEM': '1',
    'GIT_CONFIG_GLOBAL': os.devnull,
    'GIT_NO_REPLACE_OBJECTS': '1',
    'GIT_TERMINAL_PROMPT': '0',
    'GIT_OPTIONAL_LOCKS': '0',
}
_UNTRUSTED_LEAN_ENV = frozenset({'LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT'})


def _sanitized_tool_environment():
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_') and key not in _UNTRUSTED_LEAN_ENV}
    environment.update(_GIT_ENV_OVERRIDES)
    return environment


@contextlib.contextmanager
def _helper_execution_environment():
    affected = {key for key in os.environ if key.startswith('GIT_') or key in _UNTRUSTED_LEAN_ENV}
    affected.update(_GIT_ENV_OVERRIDES)
    previous = {key: os.environ[key] for key in affected if key in os.environ}
    for key in affected:
        os.environ.pop(key, None)
    os.environ.update(_GIT_ENV_OVERRIDES)
    try:
        yield
    finally:
        for key in list(os.environ):
            if key.startswith('GIT_') or key in _UNTRUSTED_LEAN_ENV:
                os.environ.pop(key, None)
        os.environ.update(previous)


def _git_bytes(repo, *args):
    return subprocess.check_output(
        ['git', '-C', str(repo), *args], env=_sanitized_tool_environment())


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


def checked_source_commit(m, digest, expected_head=None):
    """Bind this execution to one immutable Git source/manifest and loaded program."""
    root = _sync_root().resolve()
    repo = Path(_git_bytes(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    prefix = root.relative_to(repo).as_posix()
    prefix = '' if prefix == '.' else prefix + '/'
    head = _git_bytes(repo, 'rev-parse', 'HEAD').decode().strip()
    require(COMMIT.fullmatch(head), 'missing exact checked commit')
    require(expected_head is None or head == expected_head, 'HEAD changed during execution')
    require(isinstance(m.get('files'), dict) and {'gate.py', 'gate_helper.py'} <= set(m['files']),
            'unbound loaded program')
    names = set(m['files']) | {'manifest.json', 'manifest.overlay.json'}
    require(all(isinstance(name, str) and not Path(name).is_absolute() and
                '..' not in Path(name).parts for name in names), 'unsafe bound source path')
    verify_committed_files(repo, head, [prefix + name for name in names])
    raw = (root / 'manifest.json').read_bytes()
    overlay = _overlay_bytes()
    require(sha(raw + b'\0RF312-OVERLAY\0' + overlay) == digest,
            'composite manifest identity differs from execution')
    require(_effective_manifest(raw.decode()) == m, 'effective manifest differs from execution')
    for name, expected in m['files'].items():
        require(sha((root / name).read_bytes()) == expected, 'bound source identity differs: ' + name)
    require((root / 'gate.py').read_bytes() == _WRAPPER_SOURCE_BYTES and
            _WRAPPER_CODE == compile(_WRAPPER_SOURCE_BYTES, str(_WRAPPER_SOURCE_PATH),
                                     'exec', dont_inherit=True, optimize=sys.flags.optimize),
            'loaded wrapper differs from committed source')
    require(_HELPER_SOURCE_BYTES is not None and
            (root / 'gate_helper.py').read_bytes() == _HELPER_SOURCE_BYTES,
            'loaded helper differs from committed source')
    require(_git_bytes(repo, 'rev-parse', 'HEAD').decode().strip() == head,
            'HEAD changed during source observation')
    return head


def _checked_dependency_path(root, name):
    require(isinstance(name, str) and name not in ('', '.', '..') and
            len(Path(name).parts) == 1 and name == Path(name).name and not Path(name).is_absolute(),
            'invalid dependency name')
    path = root / '.lake' / 'packages' / name
    for part in (root / '.lake', root / '.lake' / 'packages', path):
        require(not part.is_symlink() and part.is_dir(), 'symlink dependency path: ' + name)
    return path


def dependency_state(m):
    root = _sync_root().resolve()
    actual = {}
    for name in m['dependency_revisions']:
        repo = str(_checked_dependency_path(root, name))
        actual[name] = _git_bytes(repo, 'rev-parse', 'HEAD').decode('utf-8').strip()
        check_worktree_clean(name, _git_bytes(
            repo, 'status', '--porcelain', '--untracked-files=normal').decode('utf-8'))
    require(actual == m['dependency_revisions'], 'installed dependency HEAD differs from lock')
    for name, head in actual.items():
        repo = _checked_dependency_path(root, name)
        tracked = verify_committed_files(repo, head, allow_symlinks=True)
        # Lake caches are an explicit excluded output domain. An ignored Lean input
        # elsewhere can shadow a registered import and is not a clean dependency.
        for directory, folders, files in os.walk(repo, followlinks=False):
            folders[:] = [part for part in folders if part not in ('.git', '.lake')]
            for part in folders:
                require(not (Path(directory) / part).is_symlink(),
                        'unexpected symlink dependency source directory: ' + name)
            for filename in files:
                path = Path(directory) / filename
                relative = path.relative_to(repo).as_posix()
                if filename.endswith(('.lean', '.olean', '.ilean')):
                    require(relative in tracked, 'unexpected Lean source in dependency: ' + name + '/' + relative)
        require(_git_bytes(repo, 'rev-parse', 'HEAD').decode().strip() == head,
                'dependency HEAD changed during source observation: ' + name)
    return actual


def observation(version, dependencies, digest):
    return {'lean_version': version, 'dependency_revisions': dependencies,
            'dependency_worktrees': 'CLEAN', 'manifest_sha256': digest}


def _overlay_bytes():
    overlay = _sync_root() / 'manifest.overlay.json'
    require(overlay.is_file() and not overlay.is_symlink(), 'missing or symlink manifest overlay')
    return overlay.read_bytes()


def _effective_manifest(text):
    base = _HELPER_LOAD_JSON(text)
    # Only the formal manifest has this shape; lake/alignment JSON passes through unchanged.
    if not (isinstance(base, dict) and 'source_modules' in base and 'targets' in base and 'files' in base):
        return base
    overlay = _HELPER_LOAD_JSON(_overlay_bytes().decode())
    require(isinstance(overlay, dict) and set(overlay) == _ALLOWED_OVERLAY_KEYS,
            'invalid manifest overlay keys')
    require(overlay.get('schema_version') == 1 and isinstance(overlay.get('files'), dict),
            'invalid manifest overlay schema')
    require(all(isinstance(k, str) and isinstance(v, str) and re.fullmatch(r'[0-9a-f]{64}', v)
                for k, v in overlay['files'].items()), 'invalid manifest overlay file binding')
    merged = dict(base)
    merged['files'] = dict(base['files'])
    merged['files'].update(overlay['files'])
    return merged


def source_check():
    root = _sync_root()
    raw = (root / 'manifest.json').read_bytes()
    original = _core.load_json
    try:
        _core.load_json = _effective_manifest
        m, _ = _HELPER_SOURCE_CHECK()
    finally:
        _core.load_json = original
    # The overlay is read after the helper's own contract has passed: a manifest that fails its
    # required-file inventory is refused for that reason, whether or not an overlay exists.
    return m, sha(raw + b'\0RF312-OVERLAY\0' + _overlay_bytes())


def _safe_evidence_path(root):
    lake = Path(root) / '.lake'
    out = lake / 'formal-evidence'
    require(not lake.is_symlink(), 'symlink evidence or build directory')
    require(not out.is_symlink(), 'symlink evidence or build directory')
    require(not (lake / 'build').is_symlink(), 'symlink evidence or build directory')
    if out.exists():
        require(out.is_dir(), 'nonregular evidence directory')
        for member in out.iterdir():
            require(not member.is_symlink() and member.is_file(),
                    'symlink or nonregular evidence member')
    return out


def execute(m, digest):
    root = _sync_root()
    out = _safe_evidence_path(root)
    out.mkdir(parents=True, exist_ok=True)
    # A refused attempt must never leave a stale success-shaped receipt.
    (out / 'receipt.json').unlink(missing_ok=True)
    # Keep test monkeypatches visible to the reviewed helper execution.
    _core.run = globals()['run']
    _core.source_check = source_check
    checked_head = checked_source_commit(m, digest)
    preflight_version = check_lean_version(run(
        ['lake', 'env', 'lean', '--version'], 'version-preflight', out))
    preflight = observation(preflight_version, dependency_state(m), digest)
    try:
        with _helper_execution_environment():
            receipt = _HELPER_EXECUTE(m, digest)
        checked_source_commit(m, digest, checked_head)
        require(receipt.get('checked_commit') == checked_head, 'helper checked commit differs from execution')
        _, after = source_check()
        require(after == digest, 'manifest or overlay changed during execution')
        version = check_lean_version(run(['lake', 'env', 'lean', '--version'], 'version-final', out))
        final = observation(version, dependency_state(m), after)
        require(final == preflight, 'runtime, dependencies or sources changed during execution')
    except BaseException:
        # The reviewed helper has already written its own receipt. A run whose final observation
        # is refused must leave no receipt behind (the logs stay as evidence of the refusal).
        (out / 'receipt.json').unlink(missing_ok=True)
        raise
    receipt = dict(receipt)
    receipt.update(
        checked_commit=checked_head,
        lean_version=version,
        dependency_revisions=m['dependency_revisions'],
        dependency_worktrees='CLEAN',
        workflow_run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),
        observations={'preflight': preflight, 'final': final},
        manifest_sha256=digest,
    )
    receipt['logs'] = {p.name: sha(p.read_bytes()) for p in sorted(out.glob('*.log'))}
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute', action='store_true',
                   help='run build, compiled inventory, transitive axiom audit and controls')
    p.add_argument('--alignment', type=Path,
                   help='validate a separately authenticated alignment record; never promotes science')
    args = p.parse_args()
    try:
        if args.execute:
            (_safe_evidence_path(Path(ROOT)) / 'receipt.json').unlink(missing_ok=True)
        m, digest = source_check()
        if args.alignment:
            check_alignment(load_json(args.alignment.read_text()), digest,
                            m['targets'], m['files']['SCOPE.md'])
        if args.execute:
            execute(m, digest)
        else:
            print('SOURCE_IDENTITY_PASS (not a Lean build or scientific acceptance): ' + digest)
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as e:
        print('FORMAL_GATE_FAIL: ' + str(e), file=sys.stderr)
        return 1
    return 0


# The helper must see the effective source check even when it calls back internally.
_core.source_check = source_check

if __name__ == '__main__':
    sys.exit(main())
