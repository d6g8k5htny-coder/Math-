"""Fresh standalone build of the complete P15 completion proof chain and kernel audit."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

from support.process import run_recorded

ROOT = Path(__file__).resolve().parent
LEAN_SHA = 'e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550'
MATHLIB_COMMIT = 'd13f23b723b8a846827a245b89c10fc7d3f11612'
SPEC_SHA = 'a30d9e6938b64d4e2728c5380d41b3a627cde42448df254069293e3839a41ca6'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
AUDIT_NAMES = json.loads((ROOT/'audit_targets.json').read_text())['names']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strip_noncode(text):
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i+2]
        if depth:
            if pair == '/-': depth += 1; i += 2
            elif pair == '-/': depth -= 1; i += 2
            else: out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif string:
            if text[i] == '\\': out.extend('  '); i += 2
            elif text[i] == '"': string = False; out.append(' '); i += 1
            else: out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif pair == '/-': depth = 1; i += 2
        elif pair == '--':
            end = text.find('\n', i)
            i = len(text) if end == -1 else end
        elif text[i] == '"': string = True; out.append(' '); i += 1
        else: out.append(text[i]); i += 1
    require(depth == 0 and not string, 'unterminated Lean comment/string')
    return ''.join(out)


def source_order():
    files = {p.relative_to(ROOT/'formal').with_suffix('').as_posix().replace('/', '.'): p
             for p in (ROOT/'formal').rglob('*.lean')}
    order, visiting = [], set()
    def visit(module):
        if module in order: return
        require(module not in visiting, 'circular proof imports')
        visiting.add(module)
        for line in re.findall(r'^import\s+([^\n]+)', files[module].read_text(), re.M):
            for imported in line.split():
                if imported in files: visit(imported)
                elif imported.startswith(('Closure.', 'Completion.', 'General.', 'Integration.', 'Specifications.', 'SpecificationProofs.')):
                    raise ValueError('missing project import: '+imported)
        visiting.remove(module)
        order.append(module)
    visit('General.FinalAudit')
    return files, order


def run(lean, mathlib, build, output):
    output.mkdir(parents=True, exist_ok=False)
    require(not build.exists() or not any(build.iterdir()), 'refuse nonempty build directory')
    build.mkdir(parents=True, exist_ok=True)
    files, order = source_order()
    freeze = {str(files[name].relative_to(ROOT)): sha(files[name]) for name in order}
    result = {'schema': 'ul-project-closure-fresh-build-v1', 'status': 'RUNNING', 'order': order,
              'sources': freeze, 'records': [], 'cache_was_fresh': True,
              'old_project_cache_on_lean_path': False}
    start = time.monotonic()
    try:
        require(sha(lean) == LEAN_SHA, 'Lean executable mismatch')
        commit = subprocess.check_output(['git', '-C', str(mathlib), 'rev-parse', 'HEAD'], text=True).strip()
        require(commit == MATHLIB_COMMIT, 'Mathlib commit mismatch')
        require((mathlib/'lean-toolchain').read_text().strip() == 'leanprover/lean4:v4.34.1', 'toolchain mismatch')
        require(sha(files['Specifications.P15']) == SPEC_SHA, 'original statement source mismatch')
        result['runtime'] = {'lean_executable_sha256': LEAN_SHA, 'mathlib_commit': commit,
                             'trust': 'Pinned external Lean/shared libraries and precompiled Mathlib cache; no full Mathlib source rebuild.'}
        frozen = output/'frozen_sources'
        for module in order:
            original = files[module]
            clean = strip_noncode(original.read_text())
            require(not re.search(r'\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by|extern)\b|skipKernel', clean),
                    'proof escape token in '+module)
            target = frozen/original.relative_to(ROOT/'formal')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, target)
        paths = [build, mathlib/'.lake/build/lib/lean']
        packages = mathlib/'.lake/packages'
        if packages.is_dir():
            paths += [p/'.lake/build/lib/lean' for p in sorted(packages.iterdir())
                      if (p/'.lake/build/lib/lean').is_dir()]
        paths.append(lean.parent.parent/'lib/lean')
        env = os.environ.copy()
        env['LEAN_PATH'] = os.pathsep.join(map(str, paths))
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        result['lean_path'] = list(map(str, paths))
        for number, module in enumerate(order):
            source = frozen/files[module].relative_to(ROOT/'formal')
            target = build/Path(*module.split('.')).with_suffix('.olean')
            target.parent.mkdir(parents=True, exist_ok=True)
            command = [str(lean), '-j1', '-M11000', '-DElab.async=false',
                       '-DautoImplicit=false', '--root='+str(frozen), '-o', str(target), str(source)]
            attempt = output/f'{number:02d}-{module}'
            try:
                receipt = run_recorded(command, attempt, timeout=120, cwd=ROOT, env=env)
            except BaseException:
                # run_recorded retains/reaps an interrupted or failed-to-start
                # child before raising. Keep that terminal receipt in the
                # campaign too; failed work must not disappear from accounting.
                retained = attempt/'receipt.json'
                if retained.is_file():
                    receipt = json.loads(retained.read_text())
                    result['records'].append({'module': module, 'source_sha256': sha(source),
                                              'receipt': retained.relative_to(output).as_posix(),
                                              **receipt})
                raise
            result['records'].append({'module': module, 'source_sha256': sha(source),
                                      'receipt': attempt.relative_to(output).as_posix()+'/receipt.json',
                                      **receipt})
            require(receipt['succeeded'], 'fresh proof compile failed: '+module)
            require(sha(source) == freeze[str(files[module].relative_to(ROOT))], 'frozen source drift')
        require(freeze == {str(files[name].relative_to(ROOT)): sha(files[name]) for name in order}, 'production proof source drift')
        stdout = (output/f'{len(order)-1:02d}-General.FinalAudit/stdout.txt').read_text()
        rows = []
        for line in stdout.splitlines():
            if line.startswith('P15_AUDIT|'):
                parts = line.split('|')
                require(len(parts) == 6 and parts[2:5] == ['closed','kernel','declaration'], 'malformed audit row')
                axioms = set(filter(None, parts[5].split(',')))
                require(axioms <= ALLOWED, 'unapproved axiom in final audit')
                rows.append({'name': parts[1], 'axioms': sorted(axioms)})
        require([x['name'] for x in rows] == AUDIT_NAMES and len(set(AUDIT_NAMES)) == len(AUDIT_NAMES), 'incomplete/duplicate kernel audit')
        require('P15_AUDIT_COMPLETE|'+str(len(AUDIT_NAMES)) in stdout.splitlines(), 'kernel audit did not finish')
        require(any(x['name'] == 'UniversalLaw.P15Closure.fullTransformedPriceBudget' for x in rows), 'headline not audited')
        result['audited_theorems'] = rows
        result['outputs'] = {p.relative_to(build).as_posix(): sha(p) for p in sorted(build.rglob('*')) if p.is_file()}
        result['status'] = 'PASS'
        return result
    except BaseException as exc:
        result.update(status='FAILED', failure={'type':type(exc).__name__, 'message':str(exc)})
        raise
    finally:
        result['campaign_wall_seconds'] = time.monotonic()-start
        result['cost_boundary'] = 'Sequential fresh Lean children plus orchestration; individual wait4 CPU/RSS in receipts. Wall and CPU separate, nested child times not added twice.'
        (output/'results.json').write_text(json.dumps(result, indent=2)+'\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lean', type=Path, default=Path('/workspace/scratch/universal-law-toolchains/lean-4.34.1-linux/bin/lean'))
    p.add_argument('--mathlib-root', type=Path, default=Path('/workspace/scratch/universal-law-toolchains/mathlib-d13f23b7'))
    p.add_argument('--build-dir', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    with (ROOT/'.native.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        result = run(args.lean.resolve(), args.mathlib_root.resolve(),
                     args.build_dir.resolve(), args.output.resolve())
    print(json.dumps({'status':result['status'], 'modules':len(result['order']),
                      'audited_theorems':len(result.get('audited_theorems', [])),
                      'result':str(args.output.resolve()/'results.json')}))


if __name__ == '__main__':
    main()
