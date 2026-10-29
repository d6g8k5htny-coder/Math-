"""Execute this workflow's bounded gate pipeline with a SYNTHETIC gate only."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

REPO = Path(__file__).resolve().parents[3]
WORKFLOW = REPO / '.github/workflows/determinant-moment-lean.yml'
PACKAGE = Path('frontiers/determinant_moment_20261025')
OUTPUT = PACKAGE / '.lake/formal-evidence'
START = '      - name: Fresh build, kernel recheck, complete inventory and seven real controls\n'
END = '      - name: Tracked tree unchanged\n'
CAPTURE = str(OUTPUT / 'authoritative-gate')

SYNTHETIC_GATE = r'''
"""SYNTHETIC file-custody fixture: no Lean, theorem or native gate execution."""
import hashlib
import json
from pathlib import Path
import time

output = Path(__file__).resolve().parent / '.lake/formal-evidence'
# tee and Python are concurrent. Wait only for tee to open its known capture
# file, so the old .log fixture is deterministically included in glob('*.log').
deadline = time.monotonic() + 5
while not any((output / name).exists() for name in
              ('authoritative-gate.log', 'authoritative-gate.console.txt')):
    if time.monotonic() >= deadline:
        raise SystemExit('SYNTHETIC fixture capture file was not opened')
    time.sleep(0.001)
(output / 'process.log').write_text('SYNTHETIC owned process output; no Lean executed\n')
receipt = dict(scope='SYNTHETIC_CONSOLE_CAPTURE_ONLY_NO_LEAN', logs={
    path.name: hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(output.glob('*.log'))})
raw = json.dumps(receipt, indent=2, sort_keys=True) + '\n'
(output / 'receipt.json').write_text(raw)
print(raw, end='', flush=True)
'''


def final_gate_block():
    """Extract only the known final gate run block, not arbitrary YAML jobs."""
    source = WORKFLOW.read_text()
    if source.count(START) != 1:
        raise ValueError('expected one determinant final gate step')
    step = source.split(START, 1)[1]
    if step.count('        run: |\n', 0, step.index(END)) != 1:
        raise ValueError('expected one literal determinant gate run block')
    block = textwrap.dedent(step.split('        run: |\n', 1)[1].split(END, 1)[0])
    lines = block.strip().splitlines()
    prefix = 'python -B -S ' + str(PACKAGE / 'gate.py') + ' --execute 2>&1 | tee '
    if len(lines) != 2 or lines[0] != 'set -euo pipefail' or not lines[1].startswith(prefix):
        raise ValueError('unsupported determinant gate block layout')
    if lines[1][len(prefix):] not in (CAPTURE + '.log', CAPTURE + '.console.txt'):
        raise ValueError('unsupported determinant console capture path')
    return block


class DeterminantConsoleCaptureTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='determinant-console-capture-')
        self.addCleanup(temporary.cleanup)
        self.fixture = Path(temporary.name)
        (self.fixture / OUTPUT).mkdir(parents=True)
        (self.fixture / PACKAGE / 'gate.py').write_text(SYNTHETIC_GATE)

    def run_synthetic_gate(self, block):
        result = subprocess.run(['bash', '-c', block], cwd=self.fixture,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
            capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = self.fixture / OUTPUT
        receipt = json.loads((output / 'receipt.json').read_text())
        observed = {name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                    for name in receipt['logs']}
        mismatches = {name: dict(expected=digest, actual=observed[name])
                      for name, digest in receipt['logs'].items() if observed[name] != digest}
        # Local evidence collection can retain this pure synthetic observation
        # without changing where production tests write their temporary files.
        self.observation = dict(scope=receipt['scope'], block=block,
            command=['bash', '-c', block], returncode=result.returncode,
            stdout=result.stdout, stderr=result.stderr, receipt=receipt,
            actual_sha256=observed, mismatches=mismatches,
            retained_files={path.name: path.read_text() for path in output.iterdir() if path.is_file()})
        return receipt, mismatches

    def test_actual_gate_pipeline_preserves_final_receipt_log_hashes(self):
        receipt, mismatches = self.run_synthetic_gate(final_gate_block())
        self.assertEqual(receipt['scope'], 'SYNTHETIC_CONSOLE_CAPTURE_ONLY_NO_LEAN')
        self.assertIn('process.log', receipt['logs'])
        self.assertEqual(mismatches, {}, 'receipt hashes must match final retained files: ' + repr(mismatches))

    def test_old_log_pipeline_is_detected_as_a_growing_log_hash_mismatch(self):
        block = final_gate_block()
        old = block.replace(CAPTURE + '.console.txt', CAPTURE + '.log')
        receipt, mismatches = self.run_synthetic_gate(old)
        self.assertEqual(set(mismatches), {'authoritative-gate.log'})
        self.assertEqual(receipt['logs']['process.log'], self.observation['actual_sha256']['process.log'])
        self.assertEqual(self.observation['retained_files']['authoritative-gate.log'],
                         self.observation['retained_files']['receipt.json'])


if __name__ == '__main__':
    unittest.main()
