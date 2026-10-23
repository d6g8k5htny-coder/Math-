"""Run the actual C7 workflow shell against real committed synthetic packets.

These tests validate the wrapper protocol, not the Gaussian theorem. The expected
mutant messages were independently measured from checker blob 0f9d4cf4.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/c7-total-bounded.yml'
PACKET = Path('frontiers/c7_total_bounded_20260929')
STAGES = ('baseline', 'M1', 'M2', 'M3')
ORDER = [[mode, label] for mode in (0, 1) for label in STAGES]
FAILURES = {
    'M1': b'FAIL T_pieceB1_7_12\n',
    'M2': b'FAIL T_threshold_is_r_equals_k\n',
    'M3': b'FAIL K_62prime_layer_integral_exact\n',
}
BASELINE = b'{"synthetic": true, "passed": true}\n'


def workflow_shell():
    """Extract the complete verification step; do not replace its source guards."""
    text = WORKFLOW.read_text()
    marker = '      - name: Verify sources, replay both modes, reject mutants\n'
    if text.count(marker) != 1:
        raise ValueError('unique verification step required')
    tail = text.split(marker, 1)[1].split('        run: |\n', 1)[1]
    lines = []
    for line in tail.splitlines():
        if line and not line.startswith('          '):
            break
        lines.append(line[10:] if line else '')
    shell = '\n'.join(lines) + '\n'
    if not shell.startswith('set -euo pipefail\n') or not shell.endswith('git diff --exit-code\n'):
        raise ValueError('complete strict shell/postflight required')
    return shell


def synthetic_checker():
    return 'FAILURES = ' + repr(FAILURES) + '\nBASELINE = ' + repr(BASELINE) + r'''
import json, os, signal, sys
from pathlib import Path
args = sys.argv[1:]
label = 'baseline' if not args else args[1] if len(args) == 2 and args[0] == '--mutant' else 'INVALID'
if label not in ('baseline', 'M1', 'M2', 'M3'):
    raise RuntimeError('unexpected invocation')
with open(os.environ['C7_TRACE'], 'a') as stream:
    stream.write(json.dumps([sys.flags.optimize, label]) + '\n')
code = 0 if label == 'baseline' else 1
out = BASELINE if label == 'baseline' else FAILURES[label]
err = b''
case = os.environ['C7_CASE']
if case == 'dirty':
    Path(os.environ['C7_RESULTS']).write_bytes(b'changed after preflight\n')
if label == os.environ['C7_STAGE'] and sys.flags.optimize == int(os.environ['C7_MODE']):
    if case == 'crash': raise RuntimeError('unrelated synthetic crash')
    if case == 'signal': os.kill(os.getpid(), signal.SIGTERM)
    if case == 'silent': out = b''
    elif case == 'stderr': err = b'unexpected stderr\n'
    elif case == 'wrong-reason': out = b'FAIL an_unrelated_check\n'
    elif case == 'other-mutant': out = FAILURES['M2' if label != 'M2' else 'M3']
    elif case == 'prefix': out = b'prefix ' + out
    elif case == 'suffix': out += b'additional report\n'
    elif case == 'no-newline': out = out.rstrip(b'\n')
    elif case == 'crlf': out = out.replace(b'\n', b'\r\n')
    elif case == 'json': out = b'{"passed": false}\n'
    elif case == 'bad-utf8': out = b'\xff' + out
    elif case == 'extra-newline': out += b'\n'
    elif case == 'wrong-exit': code = 1 if label == 'baseline' else 0
    elif case == 'exit-two': code = 2
sys.stdout.buffer.write(out)
sys.stderr.buffer.write(err)
sys.exit(code)
'''


@unittest.skipUnless(os.name == 'posix', 'workflow requires Bash and POSIX processes')
class C7TotalWorkflowTests(unittest.TestCase):
    def fixture(self, case='valid', stage='baseline', mode=0, guard=None):
        with tempfile.TemporaryDirectory(prefix='c7-protocol-') as temp:
            home = Path(temp)
            repo = home / 'repo'
            packet = repo / PACKET
            packet.mkdir(parents=True)
            trace = home / 'calls.jsonl'
            (packet / 'exponent_check.py').write_text(synthetic_checker())
            (packet / 'RESULTS.json').write_bytes(BASELINE)
            files = []
            for path in sorted(packet.iterdir()):
                data = path.read_bytes()
                files.append({'path': path.name, 'bytes': len(data),
                              'sha256': hashlib.sha256(data).hexdigest()})
            manifest = packet / 'SOURCE_FILES.json'
            manifest.write_text(json.dumps({'files': files}))
            env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            env.update(HOME=str(home), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_AUTHOR_NAME='Synthetic fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                       GIT_COMMITTER_NAME='Synthetic fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid',
                       PYTHONDONTWRITEBYTECODE='1', C7_TRACE=str(trace), C7_CASE=case,
                       C7_STAGE=stage, C7_MODE=str(mode), C7_RESULTS=str(packet / 'RESULTS.json'))
            env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
            for args in (['init', '-q'], ['add', '.'],
                         ['-c', 'commit.gpgsign=false', '-c', 'maintenance.auto=false',
                          '-c', 'core.hooksPath=' + os.devnull, 'commit', '-qm', 'synthetic C7 packet']):
                subprocess.run(['git', *args], cwd=repo, env=env, check=True,
                               capture_output=True, timeout=15)
            if guard == 'hash':
                (packet / 'RESULTS.json').write_bytes(b'X' + BASELINE[1:])
            elif guard == 'size':
                files[0]['bytes'] += 1
                manifest.write_text(json.dumps({'files': files}))
            elif guard == 'extra':
                (packet / 'unexpected').write_bytes(b'extra')
            elif guard == 'missing':
                (packet / 'RESULTS.json').unlink()
            elif guard == 'symlink':
                (home / 'target').write_bytes(BASELINE)
                (packet / 'RESULTS.json').unlink()
                (packet / 'RESULTS.json').symlink_to(home / 'target')
            result = subprocess.run(['bash', '--noprofile', '--norc', '-c', workflow_shell()],
                                    cwd=repo, env=env, capture_output=True, timeout=20)
            calls = [json.loads(row) for row in trace.read_text().splitlines()] if trace.exists() else []
            if saved := os.environ.get('C7_EVIDENCE'):
                dest = Path(saved)
                dest.mkdir(parents=True, exist_ok=True)
                key = '-'.join((case, stage, str(mode), str(guard)))
                record = {'case': case, 'stage': stage, 'mode': mode, 'guard': guard,
                          'returncode': result.returncode, 'calls': calls,
                          'stdout_base64': base64.b64encode(result.stdout).decode(),
                          'stderr_base64': base64.b64encode(result.stderr).decode()}
                target = dest / (key + '.json')
                with target.open('x') as stream:
                    json.dump(record, stream, sort_keys=True)
                    stream.write('\n')
            return result, calls

    def rejected_at(self, case, stage, mode):
        result, calls = self.fixture(case, stage, mode)
        target = ORDER.index([mode, stage]) + 1
        self.assertIn([mode, stage], calls, 'target must actually execute')
        self.assertNotEqual(result.returncode, 0, 'invalid admission: ' + repr((case, stage, mode)))
        self.assertEqual(calls, ORDER[:target], 'reject at intended stage, before later children')

    def test_valid_complete_inventory(self):
        result, calls = self.fixture()
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
        self.assertEqual(calls, ORDER)
        self.assertEqual(result.stderr, b'')

    def test_each_mutant_requires_exact_reason_and_clean_stderr(self):
        for case in ('crash', 'silent', 'stderr', 'wrong-reason', 'other-mutant', 'prefix',
                     'suffix', 'no-newline', 'crlf', 'json', 'bad-utf8', 'extra-newline'):
            for mode in (0, 1):
                for stage in STAGES[1:]:
                    with self.subTest(case=case, mode=mode, stage=stage):
                        self.rejected_at(case, stage, mode)

    def test_mutant_wrong_exit_and_signal(self):
        for case in ('wrong-exit', 'exit-two', 'signal'):
            for mode in (0, 1):
                for stage in STAGES[1:]:
                    with self.subTest(case=case, mode=mode, stage=stage):
                        self.rejected_at(case, stage, mode)

    def test_baseline_bytes_exit_and_stderr(self):
        for case in ('silent', 'stderr', 'wrong-exit', 'suffix', 'no-newline'):
            for mode in (0, 1):
                with self.subTest(case=case, mode=mode):
                    self.rejected_at(case, 'baseline', mode)

    def test_source_guards_precede_children(self):
        for guard in ('hash', 'size', 'extra', 'missing', 'symlink'):
            with self.subTest(guard=guard):
                result, calls = self.fixture(guard=guard)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, [])
                expected = (b'source identity mismatch' if guard in ('hash', 'size') else
                            b'flat regular source required' if guard == 'symlink' else
                            b'packet tree differs from manifest')
                self.assertIn(expected, result.stderr)

    def test_tracked_mutation_rejected_after_full_replay(self):
        result, calls = self.fixture('dirty')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, ORDER)
        self.assertIn(b'changed after preflight', result.stdout)

    def test_regression_wiring(self):
        text = WORKFLOW.read_text()
        self.assertIn("- 'tests/test_c7_total_workflow.py'", text)
        for flags in ('-B -S', '-B -O -S'):
            self.assertIn('python ' + flags + ' -m unittest discover -s tests -p test_c7_total_workflow.py -v', text)


if __name__ == '__main__':
    unittest.main()
