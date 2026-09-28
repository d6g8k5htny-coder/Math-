"""Source-bound finite replay. Standard library only; no network or repository writes."""
import argparse
import hashlib
import importlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

MUTANTS = {
    'allow-odd-capacity': (
        'if any(a % 2 for a in capacities):', 'if False:',
        'test_even_capacity_requires_even'),
    'wrong-even-splitting': (
        'half_capacity = capacity // 2', 'half_capacity = capacity',
        'test_even_triangle_same_palette'),
    'floor-instead-of-ceiling': (
        '(len(vertices & b) + a - 1) // a', 'len(vertices & b) // a',
        'test_exact_coloring_against_partition_oracle'),
    'ignore-bipartition': (
        'if sides[i] == sides[j] and b & blocks[j]:', 'if False:',
        'test_bipartition_validation'),
    'false-overlap-independence': (
        'return joint**2 <= left*right', 'return joint <= left*right',
        'test_overlap_destroys_local_independence'),
    'lose-cauchy-schwarz-factor': (
        'return 2/hhi, 2/hlo', 'return 1/hhi, 1/hlo',
        'test_overlap_constant'),
    'charge-inactive-blocks': (
        'if d == k and b not in answer:', 'if d <= k and b not in answer:',
        'test_inactive_demand_one_is_not_a_generator'),
    'drop-active-generators': (
        'if d == k and b not in answer:', 'if d < k and b not in answer:',
        'test_complete_active_block_needs_extra_color'),
    'omit-exponential-tail': (
        'return lo, lo+tail', 'return lo, lo',
        'test_exp_rational_enclosure'),
    'strict-capacity-event': (
        'if not all(len(selected & b) <= a for b, a in zip(blocks, capacities)):',
        'if not all(len(selected & b) < a for b, a in zip(blocks, capacities)):',
        'test_binomial_five_tail_identity'),
}


def decode_unique(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: '+key)
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=pairs)


def child(root):
    sys.path.insert(0, str(root))
    tests = importlib.import_module('test_overlap')
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(
        unittest.defaultTestLoader.loadTestsFromModule(tests))
    output = {
        'tests': result.testsRun,
        'failures': sorted(t.id().rsplit('.', 1)[-1] for t, _ in result.failures),
        'errors': sorted(t.id().rsplit('.', 1)[-1] for t, _ in result.errors),
        'passed': result.wasSuccessful(),
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


def source_check(root):
    manifest = decode_unique((root/'SOURCE_FILES.json').read_text())
    entries = manifest['files']
    names = [entry['path'] for entry in entries]
    if len(names) != len(set(names)) or any(Path(p).name != p for p in names):
        raise ValueError('unique flat manifest paths required')
    present = sorted(p.name for p in root.iterdir())
    if present != sorted(names+['SOURCE_FILES.json']):
        raise ValueError('source membership mismatch')
    for entry in entries:
        p = root/entry['path']
        if p.is_symlink() or not p.is_file():
            raise ValueError('regular source required')
        data = p.read_bytes()
        if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError('source identity mismatch: '+p.name)


def replay(root):
    source_check(root)
    original = (root/'overlap.py').read_text()
    expected = decode_unique((root/'RESULTS.json').read_text())
    records = []
    for name in ['baseline', *MUTANTS]:
        with tempfile.TemporaryDirectory(prefix='p15-overlap-replay-') as tmp:
            copy = Path(tmp)
            shutil.copyfile(root/'overlap.py', copy/'overlap.py')
            shutil.copyfile(root/'test_overlap.py', copy/'test_overlap.py')
            if name != 'baseline':
                old, new, _ = MUTANTS[name]
                if original.count(old) != 1:
                    raise ValueError('mutation anchor is not unique: '+name)
                (copy/'overlap.py').write_text(original.replace(old, new))
            outputs = []
            for flags in (['-B', '-S'], ['-B', '-O', '-S']):
                process = subprocess.run([sys.executable, *flags, str(root/'run_validation.py'),
                                          '--child', str(copy)], capture_output=True, timeout=45)
                result = decode_unique(process.stdout.decode())
                if process.stderr or result['errors']:
                    raise ValueError('execution error, not a valid predicate test: '+name)
                if name == 'baseline':
                    if process.returncode != 0 or result != expected['baseline']:
                        raise ValueError('baseline differs from frozen summary')
                else:
                    if process.returncode != 1 or result['passed'] or MUTANTS[name][2] not in result['failures']:
                        raise ValueError('expected semantic assertion did not reject: '+name)
                outputs.append(process.stdout)
            if outputs[0] != outputs[1]:
                raise ValueError('normal and optimized outputs differ: '+name)
            records.append({'case': name, **decode_unique(outputs[0].decode())})
    source_check(root)
    summary = {'scientific_effect':'NONE', 'nonauthor_acceptance':False,
               'tests_per_mode': expected['baseline']['tests'],
               'mutants_per_mode': len(MUTANTS), 'all_output_pairs_identical':True,
               'source_membership_and_hashes':'PASS', 'cases':records}
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--child', type=Path)
    options = parser.parse_args()
    if options.child is not None:
        sys.exit(child(options.child.resolve()))
    sys.exit(replay(Path(__file__).resolve().parent))
