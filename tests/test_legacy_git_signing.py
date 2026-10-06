"""Real-Git signing controls for the disposable legacy workflow fixture.

Only the fixture's exact three-command setup loop is executed here, not its
scientific/checker shell. The original workflow suite covers the latter.
All configuration and signer files belong to TemporaryDirectory; no user Git
configuration, key, agent, network, or subprocess mock is used.
"""
import ast
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/test_legacy_json_workflows.py'


def setup_code():
    """Compile the actual fixture setup statements rather than a copied command."""
    tree = ast.parse(FIXTURE.read_text(encoding='utf-8'), filename=str(FIXTURE))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef)
               and n.name == 'LegacyWorkflowTests')
    case = next(n for n in cls.body if isinstance(n, ast.FunctionDef)
                and n.name == 'case')
    loops = [n for n in ast.walk(case) if isinstance(n, ast.For)
             and isinstance(n.target, ast.Name) and n.target.id == 'cmd']
    if len(loops) != 1:
        raise ValueError('expected one actual fixture Git setup loop')
    commands = ast.literal_eval(loops[0].iter)
    if (len(commands) != 3 or commands[0] != ['git', 'init', '-q']
            or commands[1] != ['git', 'add', '.']
            or commands[2][-3:] != ['commit', '-qm', 'synthetic fixture']):
        raise ValueError('fixture setup command inventory changed')
    return compile(ast.Module(body=[loops[0]], type_ignores=[]), str(FIXTURE), 'exec')


@unittest.skipUnless(os.name == 'posix', 'controlled signer executable needs POSIX')
class LegacyGitSigningTests(unittest.TestCase):
    def configuration(self, directory, fmt, scope='global'):
        env = {key: value for key, value in os.environ.items()
               if not key.startswith('GIT_')}
        env.update(HOME=str(directory), XDG_CONFIG_HOME=str(directory / 'xdg'),
                   GIT_CONFIG_NOSYSTEM='1',
                   GIT_CONFIG_GLOBAL=str(directory / 'private.gitconfig'),
                   SIGNER_TRACE=str(directory / 'signer.trace'))
        signer = directory / 'failing-signer'
        signer.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$SIGNER_TRACE"\n'
                          'exit 86\n', encoding='utf-8')
        signer.chmod(0o700)
        key = directory / 'dummy-key'
        key.write_text('synthetic test key; never used by a real signer\n')
        def configure(name, value):
            self.git(directory, env, 'config', '--global', name, str(value))
        configure('user.name', 'Signing fixture')
        configure('user.email', 'fixture@example.invalid')
        configure('user.signingkey', key)
        configure('commit.gpgsign', 'true')
        configure('gpg.format', fmt)
        configure('gpg.' + fmt + '.program', signer)
        configure('maintenance.auto', 'false')
        configure('core.hooksPath', directory / 'no-hooks')
        if scope == 'environment':
            env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='commit.gpgsign',
                       GIT_CONFIG_VALUE_0='true')
        return env

    def git(self, cwd, env, *args, check=True):
        return subprocess.run(['git', *args], cwd=cwd, env=env,
                              capture_output=True, check=check, timeout=15)

    def test_fixture_commit_ignores_signing_without_changing_configuration(self):
        for fmt in ('openpgp', 'ssh'):
            for scope in ('global', 'environment'):
                with self.subTest(format=fmt, scope=scope), tempfile.TemporaryDirectory() as td:
                    root = Path(td)
                    env = self.configuration(root, fmt, scope)
                    config = root / 'private.gitconfig'
                    original = config.read_bytes()
                    repo = root / 'repo'
                    repo.mkdir()
                    (repo / 'source.txt').write_text('synthetic fixture bytes\n')
                    problem = None
                    try:
                        exec(setup_code(), {'subprocess': subprocess, 'repo': repo, 'env': env})
                    except subprocess.CalledProcessError as exc:
                        problem = exc
                    self.assertEqual(config.read_bytes(), original)
                    self.assertEqual(self.git(repo, env, 'config', '--get', 'commit.gpgsign').stdout, b'true\n')
                    trace = root / 'signer.trace'
                    self.assertFalse(trace.exists(), 'fixture launched inherited %s signer; stderr=%r' %
                                     (fmt, problem.stderr if problem else b''))
                    self.assertIsNone(problem, 'fixture failed without a signer invocation')
                    self.assertEqual(self.git(repo, env, 'rev-list', '--count', 'HEAD').stdout, b'1\n')
                    self.assertEqual(self.git(repo, env, 'log', '-1', '--format=%s').stdout, b'synthetic fixture\n')
                    self.assertEqual(self.git(repo, env, 'show', 'HEAD:source.txt').stdout, b'synthetic fixture bytes\n')
                    raw = self.git(repo, env, 'cat-file', 'commit', 'HEAD').stdout
                    self.assertNotIn(b'\ngpgsig ', raw)
                    self.assertEqual(self.git(repo, env, 'status', '--porcelain').stdout, b'')
                    # A subsequent ordinary commit still signs: no persistent override leaked.
                    (repo / 'source.txt').write_text('second synthetic value\n')
                    self.git(repo, env, 'add', '.')
                    ordinary = self.git(repo, env, 'commit', '-qm', 'must request signature', check=False)
                    self.assertNotEqual(ordinary.returncode, 0)
                    self.assertTrue(trace.exists(), 'ordinary commit lost its configured signer')
                    self.assertEqual(len(trace.read_text().splitlines()), 1)
                    self.assertEqual(config.read_bytes(), original)
                    self.assertEqual(self.git(repo, env, 'config', '--get', 'commit.gpgsign').stdout, b'true\n')

    def test_positive_signer_control_is_not_vacuous(self):
        for fmt in ('openpgp', 'ssh'):
            with self.subTest(format=fmt), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                env = self.configuration(root, fmt)
                self.git(root, env, 'init', '-q')
                (root / 'probe.txt').write_text('synthetic signing probe\n')
                self.git(root, env, 'add', 'probe.txt')
                result = self.git(root, env, 'commit', '-qm', 'ordinary control', check=False)
                self.assertNotEqual(result.returncode, 0)
                trace = root / 'signer.trace'
                self.assertTrue(trace.exists(), 'configured signer was not exercised')
                self.assertEqual(len(trace.read_text().splitlines()), 1)
                self.assertEqual(self.git(root, env, 'config', '--get', 'commit.gpgsign').stdout, b'true\n')


if __name__ == '__main__':
    unittest.main(verbosity=2)
