"""Execute the workflow's real shell pipeline against synthetic gate output.

These controls test log transport and failure propagation, never Lean results.
The historical broken placement is replayed without altering tracked source.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT.parents[1] / '.github/workflows/determinant-moment-lean.yml'
GATE_LOGS = 'frontiers/determinant_moment_20261025/.lake/formal-evidence'


def execution_script(text):
    marker = '      - name: Fresh build, kernel recheck, complete inventory and seven real controls\n'
    if text.count(marker) != 1:
        raise ValueError('expected exactly one authoritative gate step')
    block = text.split(marker, 1)[1].split('      - ', 1)[0]
    if not block.startswith('        run: |\n'):
        raise ValueError('authoritative gate must remain an explicit shell block')
    lines = block.splitlines()[1:]
    if not lines or any(not line.startswith('          ') for line in lines if line):
        raise ValueError('unexpected gate shell indentation')
    return '\n'.join(line[10:] for line in lines) + '\n'


def exercise_pipeline(text, exit_code=0):
    """Synthetic child creates stable logs, hashes them, then prints its receipt."""
    with tempfile.TemporaryDirectory(prefix='determinant-transport-') as temporary:
        work = Path(temporary)
        evidence = work / GATE_LOGS
        evidence.mkdir(parents=True)
        runner_temp = work / 'runner-temp'
        runner_temp.mkdir()
        fake = work / 'synthetic_gate.py'
        fake.write_text(
            "import hashlib,json,os,sys\n"
            "from pathlib import Path\n"
            "out=Path(" + repr(GATE_LOGS) + ")\n"
            "(out/'kernel.log').write_bytes(b'SYNTHETIC transport fixture; NO LEAN EXECUTED\\n')\n"
            "receipt={'synthetic_transport_fixture':True,'logs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*.log'))}}\n"
            "(out/'receipt.json').write_text(json.dumps(receipt))\n"
            "print(json.dumps(receipt),flush=True)\n"
            "sys.exit(int(os.environ['SYNTHETIC_GATE_EXIT']))\n"
        )
        bindir = work / 'bin'
        bindir.mkdir()
        wrapper = bindir / 'python'
        wrapper.write_text('#!/bin/sh\nexec ' + shlex.quote(sys.executable) +
                           ' ' + shlex.quote(str(fake)) + ' "$@"\n')
        wrapper.chmod(0o700)
        env = dict(os.environ, PATH=str(bindir) + os.pathsep + os.environ['PATH'],
                   RUNNER_TEMP=str(runner_temp), SYNTHETIC_GATE_EXIT=str(exit_code))
        result = subprocess.run(['bash', '-c', execution_script(text)], cwd=work,
                                env=env, capture_output=True, text=True, timeout=30)
        receipt = json.loads((evidence / 'receipt.json').read_text())
        mismatches = [name for name, digest in receipt['logs'].items()
                      if hashlib.sha256((evidence / name).read_bytes()).hexdigest() != digest]
        consoles = list(runner_temp.glob('*.log'))
        return result, receipt, mismatches, [p.read_text() for p in consoles]


class WorkflowReceiptTransportTests(unittest.TestCase):
    def test_actual_workflow_leaves_every_receipt_log_hash_stable(self):
        result, receipt, mismatches, consoles = exercise_pipeline(WORKFLOW.read_text())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(receipt['synthetic_transport_fixture'])
        self.assertEqual(mismatches, [], 'workflow appended to a receipt-hashed gate log')
        self.assertEqual(len(consoles), 1, 'aggregate console must be retained separately')
        self.assertEqual(json.loads(consoles[0]), receipt)

    def test_original_in_gate_tee_reproduces_the_self_hash_failure(self):
        text = WORKFLOW.read_text()
        mutant, count = re.subn(r'tee "\$RUNNER_TEMP/determinant-authoritative-gate\.log"',
                               'tee ' + GATE_LOGS + '/authoritative-gate.log', text)
        self.assertEqual(count, 1, 'exactly one aggregate pipeline is required')
        result, _, mismatches, _ = exercise_pipeline(mutant)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(mismatches, ['authoritative-gate.log'])

    def test_actual_pipeline_preserves_nonzero_gate_exit_and_console(self):
        result, _, mismatches, consoles = exercise_pipeline(WORKFLOW.read_text(), exit_code=17)
        self.assertEqual(result.returncode, 17, 'tee swallowed a gate failure')
        self.assertEqual(mismatches, [])
        self.assertEqual(len(consoles), 1)

    def test_both_gate_evidence_and_separate_console_are_uploaded(self):
        text = WORKFLOW.read_text()
        self.assertIn('          path: |', text)
        self.assertIn('            ' + GATE_LOGS + '/', text)
        for disposable in ('source', 'work', 'repo'):
            self.assertIn('            !' + GATE_LOGS + '/**/' + disposable + '/**', text)
        self.assertIn('          path: $' + '{{ runner.temp }}/determinant-authoritative-gate.log', text)
        self.assertEqual(text.count('          if-no-files-found: error'), 2)


if __name__ == '__main__':
    unittest.main()
