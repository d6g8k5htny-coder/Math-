#!/usr/bin/env python3
"""Source and execution gate for the CapFirstExit Lean packet. Standard library only.

    python3 gate.py              source identity, main pins, toolchain pins, forbidden tokens,
                                 declared targets
    python3 gate.py --execute    the same, then a fresh `lake build`, a `leanchecker` replay, the
                                 per-declaration axiom audit against MANIFEST.json, and three
                                 negative controls (injected sorry, custom axiom, native_decide)
                                 that the audit must reject

Scientific effect: NONE. A green gate is kernel evidence for the displayed Lean statements only.
It is not an alignment review and not an acceptance of any parent theorem.
"""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[1]
MODULE = 'CapFirstExit'
NAME = r"[A-Za-z_][A-Za-z0-9_'.₀-₉]*"
AXIOM_LINE = re.compile(r"'(" + NAME + r")' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
DECL = re.compile(r'^(?:noncomputable )?(theorem|def|structure) (' + NAME + r')')
FORBIDDEN = ('sorry', 'admit', 'axiom', 'native_decide', 'implemented_by', 'extern', 'unsafe',
             'opaque', 'set_option', 'macro', 'elab', 'syntax', 'run_cmd', 'run_tac', 'decreasing_by',
             'partial', 'debug', 'ofReduceBool', 'trustCompiler')
SKIP_DIRS = {'.lake', '__pycache__'}


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


def declarations(text):
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
            names.append('.'.join([n for k, n in stack if k == 'namespace'] + [m.group(2)]))
    require(not stack, 'unclosed namespace or section')
    return names


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


def source_check(root=ROOT, repo=REPO):
    m = load_json((root / 'MANIFEST.json').read_text())
    present = sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                     if p.is_file() and not SKIP_DIRS & set(p.relative_to(root).parts))
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
    lean_files = sorted(p.relative_to(root).as_posix() for p in root.rglob('*.lean')
                        if not SKIP_DIRS & set(p.relative_to(root).parts))
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
    return m


def run(command, label, out, expect_success=True):
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=1800)
    log = proc.stdout + proc.stderr
    (out / (label + '.log')).write_text(log)
    if expect_success:
        require(proc.returncode == 0, label + ' failed:\n' + log[-4000:])
    return log


def execute(m):
    out = ROOT / '.lake' / 'evidence'
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
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
    controls = {
        'sorry': 'theorem injected : False := by sorry\n',
        'custom_axiom': 'axiom hiddenPremise : False\ntheorem injected : False := hiddenPremise\n',
        'native_decide': 'theorem injected : (2 : Nat) + 2 = 4 := by native_decide\n'}
    outcomes = {}
    for label, body in controls.items():
        path = out / ('Control_' + label + '.lean')
        path.write_text('import ' + MODULE + '\n' + body + '#print axioms injected\n')
        clog = run(['lake', 'env', 'lean', str(path)], 'control_' + label, out, expect_success=False)
        try:
            audit_axioms(clog, ['injected'], m['allowed_axioms'])
        except ValueError as exc:
            require('forbidden transitive axiom' in str(exc), 'control ' + label + ' failed for the wrong reason: ' + str(exc))
            outcomes[label] = 'REJECTED'
            continue
        raise ValueError('negative control escaped the audit: ' + label)
    version = run(['lake', 'env', 'lean', '--version'], 'version', out).strip()
    actual = {name: subprocess.check_output(['git', '-C', str(ROOT / '.lake' / 'packages' / name), 'rev-parse', 'HEAD'],
                                            text=True).strip() for name in m['dependency_revisions']}
    require(actual == m['dependency_revisions'], 'checked-out dependency revisions differ from MANIFEST.json')
    receipt = {
        'scientific_effect': 'NONE',
        'module': MODULE,
        'lean_version': version,
        'toolchain': m['toolchain'],
        'dependency_revisions': actual,
        'source_sha256': {e['path']: e['sha256'] for e in m['files']},
        'build': 'PASS', 'leanchecker': 'PASS',
        'axioms': axioms,
        'negative_controls': outcomes,
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
