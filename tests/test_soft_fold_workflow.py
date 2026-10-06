"""Real whole-shell protocol fixtures; synthetic outputs, not a field theorem."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/soft-fold-limit.yml'
PACKET = 'frontiers/soft_fold_limit_20261002'
MUTANTS = tuple('M' + str(i) for i in range(1, 9))
STAGES = ('baseline', *MUTANTS, 'M99')
ORDER = [[mode, stage] for mode in (0, 1) for stage in STAGES]
# Independent reference carriers from original hosted job112272450916.
CONTROLS = ('F1_model_pins_and_weight', 'F2_lemma_FL2_generic',
            'F3_lemma_FL1_window', 'F4_proposition_FL4_certificates',
            'F5_theorem_FL_bookkeeping', 'F6_corollaries',
            'F4_proposition_FL4_certificates', 'F7_proposition_FL7_identification')
EXPECTED_STDERR = {m: ('mutant ' + m + ': failing controls ' + c + '\n').encode()
                   for m, c in zip(MUTANTS, CONTROLS)}
EXPECTED_STDERR.update(baseline=b'', M99=b'unknown mutant label\n')
BASELINE = b'{"synthetic": "soft-fold baseline"}\n'


def verification_shell(text):
    """Extract only the existing named step, without replacing any source guard."""
    marker = '      - name: Verify sources, replay both modes, reject mutants\n'
    if text.count(marker) != 1:
        raise ValueError('one original verification step required')
    tail = text.split(marker, 1)[1].split('        run: |\n', 1)[1]
    lines = []
    for line in tail.splitlines():
        if line and not line.startswith('          '):
            break
        lines.append(line[10:] if line else '')
    if not lines or lines[0] != 'set -euo pipefail':
        raise ValueError('original strict shell missing')
    return '\n'.join(lines) + '\n'


def file_identity(name, data):
    return {'path': name, 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()}


def synthetic_checker():
    return ('import json, os, signal, sys\nfrom pathlib import Path\n'
            + 'messages = ' + repr(EXPECTED_STDERR) + '\n'
            + 'baseline = ' + repr(BASELINE) + '\n' + textwrap.dedent(r'''
        args = sys.argv[1:]
        label = 'baseline' if not args else args[1]
        mode = sys.flags.optimize
        with open(os.environ['SOFT_FOLD_TRACE'], 'a') as stream:
            stream.write(json.dumps([mode, label]) + '\n')
        code = 0 if label == 'baseline' else 2 if label == 'M99' else 1
        out = baseline if label == 'baseline' else b''
        err = messages[label]
        case = os.environ['SOFT_FOLD_CASE']
        if case == 'dirty':
            Path(os.environ['SOFT_FOLD_RESULTS']).write_bytes(b'changed after preflight\n')
        if mode == int(os.environ['SOFT_FOLD_MODE']) and label == os.environ['SOFT_FOLD_STAGE']:
            if case == 'crash':
                raise RuntimeError('unrelated synthetic crash')
            if case == 'silent':
                out = err = b''
            elif case == 'wrong-control':
                err = b'unrelated failure reason\n'
            elif case == 'extra-stdout':
                out += b'unexpected stdout\n'
            elif case == 'prefix':
                err = b'prefix ' + err
            elif case == 'extra-newline':
                err += b'\n'
            elif case == 'stderr':
                err += b'unexpected stderr\n'
            elif case == 'garbage':
                out = b'not the frozen result\n'
            elif case == 'wrong-exit':
                code = 1 if label == 'baseline' else 0
            elif case == 'signal':
                os.kill(os.getpid(), signal.SIGTERM)
        sys.stdout.buffer.write(out)
        sys.stderr.buffer.write(err)
        sys.exit(code)
    '''))


class SoftFoldWorkflowTests(unittest.TestCase):
    def run_case(self, case='valid', stage='baseline', mode=0, guard=None):
        with tempfile.TemporaryDirectory(prefix='soft-fold-fixture-') as tmp:
            home = Path(tmp)
            repo = home / 'repo'
            packet = repo / PACKET
            packet.mkdir(parents=True)
            trace = home / 'trace.jsonl'
            script = packet / 'fold_check.py'
            script.write_text(synthetic_checker(), encoding='utf-8')
            (packet / 'RESULTS.json').write_bytes(BASELINE)
            manifest = {'files': [file_identity(p.name, p.read_bytes()) for p in sorted(packet.iterdir())],
                        'mutants': list(MUTANTS), 'consumed': [], 'cited_only': [],
                        'consumed_unmerged': [], 'cited_unmerged': []}
            for kind in ('consumed', 'cited_only'):
                name = kind + '.txt'
                data = ('nonempty synthetic pinned ' + kind + '\n').encode()
                (repo / name).write_bytes(data)
                manifest[kind] = [file_identity(name, data)]
            manifest_path = packet / 'SOURCES.json'
            manifest_path.write_text(json.dumps(manifest))
            env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            env.update(HOME=str(home), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                       GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid',
                       PYTHONDONTWRITEBYTECODE='1', GH_REPOSITORY='fixture/fixture', GH_TOKEN='unused',
                       SOFT_FOLD_CASE=case, SOFT_FOLD_STAGE=stage, SOFT_FOLD_MODE=str(mode),
                       SOFT_FOLD_TRACE=str(trace), SOFT_FOLD_RESULTS=str(packet / 'RESULTS.json'))
            env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')

            def git(*args):
                return subprocess.run(['git', '-c', 'commit.gpgsign=false', '-c', 'maintenance.auto=false',
                                       '-c', 'core.hooksPath=' + os.devnull, *args],
                                      cwd=repo, env=env, check=True, capture_output=True, timeout=15)

            git('init', '-q')
            git('add', '.')
            git('commit', '-qm', 'synthetic authenticated fixture')
            if guard == 'packet-hash':
                script.write_text(script.read_text() + '\n# changed after manifest\n')
            elif guard == 'missing-packet':
                (packet / 'RESULTS.json').unlink()
            elif guard == 'extra-member':
                (packet / 'extra.txt').write_bytes(b'extra')
            elif guard == 'packet-symlink':
                target = home / 'copy'
                target.write_bytes(BASELINE)
                (packet / 'RESULTS.json').unlink()
                (packet / 'RESULTS.json').symlink_to(target)
            elif guard in ('consumed-hash', 'cited-hash'):
                (repo / ('consumed.txt' if guard == 'consumed-hash' else 'cited_only.txt')).write_bytes(b'tampered\n')
            elif guard == 'consumed-mode':
                git('update-index', '--chmod=+x', 'consumed.txt')
                git('commit', '-qm', 'wrong tracked mode')
            elif guard == 'consumed-missing':
                (repo / 'consumed.txt').unlink()
            elif guard == 'untracked-pin':
                git('rm', '--cached', 'consumed.txt')
                git('commit', '-qm', 'untracked consumed file')
            elif guard and guard.startswith('inventory-'):
                variants = {'inventory-missing': list(MUTANTS[:-1]),
                            'inventory-order': list(reversed(MUTANTS)),
                            'inventory-duplicate': [*MUTANTS, 'M8'],
                            'inventory-object': dict.fromkeys(MUTANTS, 1)}
                manifest['mutants'] = variants[guard]
                manifest_path.write_text(json.dumps(manifest))
                git('add', '.')
                git('commit', '-qm', 'coherent inventory variant')
            result = subprocess.run(['bash', '--noprofile', '--norc', '-c', verification_shell(WORKFLOW.read_text())],
                                    cwd=repo, env=env, capture_output=True, timeout=40)
            calls = [json.loads(line) for line in trace.read_text().splitlines()] if trace.exists() else []
            if destination := os.environ.get('SOFT_FOLD_SAVE'):
                saved = Path(destination) / ('-'.join((case, stage, str(mode), str(guard))))
                saved.mkdir(parents=True, exist_ok=False)
                (saved / 'stdout.bin').write_bytes(result.stdout)
                (saved / 'stderr.bin').write_bytes(result.stderr)
                record = {'case': case, 'stage': stage, 'mode': mode, 'guard': guard,
                          'returncode': result.returncode, 'calls': calls,
                          'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
                          'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()}
                (saved / 'record.json').write_text(json.dumps(record, sort_keys=True) + '\n')
            return result, calls

    def reject_at(self, case, stage, mode):
        result, calls = self.run_case(case, stage, mode)
        prefix = ORDER[:ORDER.index([mode, stage]) + 1]
        self.assertIn([mode, stage], calls, 'targeted command must actually run')
        self.assertNotEqual(result.returncode, 0, 'wrong-result admission: ' + repr((case, stage, mode)))
        self.assertEqual(calls, prefix, 'failure must stop at exactly its intended stage')

    def test_valid_complete_inventory(self):
        result, calls = self.run_case()
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
        self.assertEqual(calls, ORDER)

    def test_every_named_rejection_requires_its_full_carrier(self):
        for case in ('silent', 'crash', 'wrong-control', 'extra-stdout', 'prefix', 'extra-newline'):
            for mode in (0, 1):
                for stage in MUTANTS:
                    with self.subTest(case=case, stage=stage, mode=mode):
                        self.reject_at(case, stage, mode)

    def test_named_wrong_exits(self):
        for mode in (0, 1):
            for stage in MUTANTS:
                with self.subTest(stage=stage, mode=mode):
                    self.reject_at('wrong-exit', stage, mode)

    def test_baseline_exact_output_and_empty_stderr(self):
        for case in ('stderr', 'silent', 'garbage', 'wrong-exit'):
            for mode in (0, 1):
                with self.subTest(case=case, mode=mode):
                    self.reject_at(case, 'baseline', mode)

    def test_unknown_complete_diagnostic(self):
        for case in ('silent', 'wrong-control', 'extra-stdout', 'prefix', 'wrong-exit', 'signal'):
            for mode in (0, 1):
                with self.subTest(case=case, mode=mode):
                    self.reject_at(case, 'M99', mode)

    def test_source_guards_precede_children(self):
        for guard in ('packet-hash', 'missing-packet', 'extra-member', 'packet-symlink',
                      'consumed-hash', 'cited-hash', 'consumed-mode', 'consumed-missing', 'untracked-pin'):
            with self.subTest(guard=guard):
                result, calls = self.run_case(guard=guard)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, [])

    def test_ordered_inventory_before_any_child(self):
        for guard in ('inventory-missing', 'inventory-order', 'inventory-duplicate', 'inventory-object'):
            with self.subTest(guard=guard):
                result, calls = self.run_case(guard=guard)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, [])

    def test_final_git_guard_remains_effective(self):
        result, calls = self.run_case('dirty')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, ORDER)
        self.assertIn(b'changed after preflight', result.stdout)

    def test_focused_suite_is_wired(self):
        text = WORKFLOW.read_text()
        self.assertIn("- 'tests/test_soft_fold_workflow.py'", text)
        for flags in ('-B -S', '-B -O -S'):
            self.assertIn('python ' + flags + ' -m unittest discover -s tests -p test_soft_fold_workflow.py -v', text)


if __name__ == '__main__':
    unittest.main()
