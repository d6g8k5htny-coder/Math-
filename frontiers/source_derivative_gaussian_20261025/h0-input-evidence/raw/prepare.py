import datetime
import difflib
import hashlib
import json
import os
import pathlib
import platform
import subprocess

REPO = pathlib.Path('/workspace/Math-curvature-20261026')
PACKET = REPO / 'frontiers/source_derivative_gaussian_20261025'
SCRATCH = pathlib.Path('/workspace/scratch/actual-h0-support-inputs')
ORIGIN = 'af17e8d1aaf3a3f47d9763485337a6c0c57b9b99'
PRECODE = '143f845b33cbdb407accc78405f124671ed051c5'
LAKE = '/home/agent/.elan/bin/lake'
MODULES = {
    'ClosedSuperlevel': ('companions/torus_filtration_20261011/ClosedSuperlevel.lean',
        'import Mathlib\n',
        'import Mathlib.AlgebraicTopology.SingularHomology.HomologyZero\n'
        'import Mathlib.Topology.Instances.Real.Lemmas\n'
        'import Mathlib.Tactic.Linarith\n'
        'import Mathlib.Tactic.NormNum\n'),
    'OrdinaryH0': ('companions/torus_filtration_20261011/OrdinaryH0.lean',
        'import Mathlib\nimport ClosedSuperlevel\n',
        'import Mathlib.AlgebraicTopology.SingularHomology.HomologyZero\n'
        'import ClosedSuperlevel\n'),
    'ElderInterval': ('frontiers/asymmetric_elder_bridge_20261017/ElderInterval.lean',
        'import OrdinaryH0\n',
        'import OrdinaryH0\n'
        'import Mathlib.Algebra.Category.ModuleCat.Biproducts\n'
        'import Mathlib.CategoryTheory.Abelian.FunctorCategory\n'
        'import Mathlib.Tactic.Abel\n'),
    'ElderBridge': ('frontiers/asymmetric_elder_bridge_20261017/ElderBridge.lean',
        'import ElderClearance\nimport ElderInterval\n',
        'import ElderClearance\nimport ElderInterval\n'),
}

def identity(path):
    path = pathlib.Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    (SCRATCH / 'build').mkdir(exist_ok=True)
    (SCRATCH / 'origins').mkdir(exist_ok=True)
    (SCRATCH / 'evidence').mkdir(exist_ok=True)
    bindings = {'schema': 1, 'origin_repository': str(REPO), 'origin_published_commit': ORIGIN,
        'precode_commit': PRECODE, 'observed_head_at_preparation': git('rev-parse', 'HEAD').decode().strip(),
        'prepared_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'body_boundary_policy': 'Every byte after the leading contiguous import lines is preserved, including blank lines and comments.',
        'new_research_target_credit': 0, 'modules': []}
    diff = []
    for module, (origin_path, old_header, new_header) in MODULES.items():
        original = git('show', f'{ORIGIN}:{origin_path}')
        assert original.startswith(old_header.encode())
        last_change = git('log', '-1', '--format=%H', ORIGIN, '--', origin_path).decode().strip()
        last_blob = git('show', f'{last_change}:{origin_path}')
        assert last_blob == original
        target = PACKET / 'inputs/elder' / f'{module}.lean'
        assert not target.exists(), str(target)
        saved = SCRATCH / 'origins' / f'{module}.lean'
        saved.write_bytes(original)
        successor = new_header.encode() + original[len(old_header.encode()):]
        target.write_bytes(successor)
        origin_body = original[len(old_header.encode()):]
        successor_body = successor[len(new_header.encode()):]
        assert origin_body == successor_body
        module_diff = ''.join(difflib.unified_diff(original.decode().splitlines(True),
            successor.decode().splitlines(True), fromfile=f'{ORIGIN}/{origin_path}',
            tofile=str(target)))
        diff.append(module_diff)
        (SCRATCH / f'{module}.diff').write_text(module_diff)
        bindings['modules'].append({'module': module, 'origin_path': origin_path,
            'origin_git_blob': git('rev-parse', f'{ORIGIN}:{origin_path}').decode().strip(),
            'last_change_commit': last_change, 'last_change_blob_matches_published': last_blob == original,
            'origin': identity(saved), 'successor': identity(target),
            'origin_header': old_header, 'successor_header': new_header,
            'origin_body_byte_offset': len(old_header.encode()),
            'successor_body_byte_offset': len(new_header.encode()),
            'origin_body_first_line': old_header.count('\n') + 1,
            'successor_body_first_line': new_header.count('\n') + 1,
            'body_bytes': len(origin_body), 'body_sha256': hashlib.sha256(origin_body).hexdigest(),
            'literal_body_equal': True, 'whole_file_equal': original == successor,
            'import_only_diff': str(SCRATCH / f'{module}.diff')})
    (SCRATCH / 'IMPORT_ONLY.diff').write_text(''.join(diff))
    for name in ['SOURCE_ACTUAL_FOLD_H0.md', 'SOURCE_ACTUAL_FOLD_H0_PLAN.md']:
        relative = f'frontiers/source_derivative_gaussian_20261025/{name}'
        frozen = git('show', f'{PRECODE}:{relative}')
        (SCRATCH / 'evidence' / name).write_bytes(frozen)
    for relative in [
        'frontiers/asymmetric_elder_bridge_20261017/historical-results/LOCAL_FORMAL_EXECUTION_REPORT.md',
        'frontiers/asymmetric_elder_bridge_20261017/historical-results/LOCAL_FORMAL_EXECUTION_RESULT.json',
        'frontiers/asymmetric_elder_bridge_20261017/review/NONAUTHOR_ELDER_BRIDGE_REVIEW.json']:
        (SCRATCH / 'evidence' / pathlib.Path(relative).name).write_bytes(git('show', f'{ORIGIN}:{relative}'))
    (SCRATCH / 'BINDINGS.json').write_text(json.dumps(bindings, indent=2) + '\n')
    env = {'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'platform': platform.platform(), 'python': platform.python_version(), 'cwd': str(PACKET),
        'lake': identity(LAKE), 'lean_version_command': [LAKE, 'env', 'lean', '--version'],
        'lean_version': subprocess.check_output([LAKE, 'env', 'lean', '--version'], cwd=PACKET, text=True).strip(),
        'mathlib_head_command': ['git', '-C', str(PACKET / '.lake/packages/mathlib'), 'rev-parse', 'HEAD'],
        'mathlib_head': subprocess.check_output(['git', '-C', str(PACKET / '.lake/packages/mathlib'), 'rev-parse', 'HEAD'], text=True).strip(),
        'lean_path_command': [LAKE, 'env', 'printenv', 'LEAN_PATH'],
        'base_lean_path': subprocess.check_output([LAKE, 'env', 'printenv', 'LEAN_PATH'], cwd=PACKET, text=True).strip()}
    (SCRATCH / 'environment.json').write_text(json.dumps(env, indent=2) + '\n')
    print(json.dumps({'bindings': str(SCRATCH / 'BINDINGS.json'), 'modules': [m['module'] for m in bindings['modules']],
        'all_body_literal_comparisons': True, 'environment': str(SCRATCH / 'environment.json')}, indent=2))

if __name__ == '__main__':
    main()
