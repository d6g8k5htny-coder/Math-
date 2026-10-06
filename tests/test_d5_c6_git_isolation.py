"""Real-Git lifecycle regression for the disposable D5/C6 protocol fixtures.

The controlled task is eligible after one commit. Foreground maintenance makes
this a deterministic child-launch test, not a probabilistic cleanup-race test.
No real repository configuration, production checker, or subprocess is mocked.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/test_d5_c6_workflows.py'


def trace_environment(trace):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith('GIT_')}
    settings = [
        ('maintenance.auto', 'true'),
        ('maintenance.autoDetach', 'false'),
        ('maintenance.gc.enabled', 'false'),
        ('maintenance.loose-objects.enabled', 'true'),
        ('maintenance.loose-objects.auto', '-1'),
    ]
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TRACE2_EVENT=str(trace.resolve()),
               GIT_CONFIG_COUNT=str(len(settings)))
    for index, (key, value) in enumerate(settings):
        env['GIT_CONFIG_KEY_' + str(index)] = key
        env['GIT_CONFIG_VALUE_' + str(index)] = value
    return env


def read_events(trace):
    return [json.loads(line) for line in trace.read_text().splitlines() if line]


def child_commands(events):
    return [event.get('argv', []) for event in events
            if event.get('event') == 'child_start']


def maintenance_commands(events):
    return [argv for argv in child_commands(events)
            if 'maintenance' in argv and '--auto' in argv]


def trace_fixture(fixture, folder, family, behavior='valid'):
    """Execute the actual fixture function in an isolated child interpreter."""
    trace = folder / 'git-trace.jsonl'
    env = trace_environment(trace)
    env['WORKFLOW_SOURCE_ROOT'] = str(fixture.resolve().parents[1])
    driver = '''import importlib.util,json,subprocess,sys
from pathlib import Path
p=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('fixture_under_test',p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def auto():
    return subprocess.check_output(['git','config','--bool','--get','maintenance.auto'],text=True).strip()
before=auto()
r=m.run_fixture(sys.argv[2],sys.argv[3])
after=auto()
print(json.dumps({'before':before,'after':after,'returncode':r.returncode,
                  'stdout':r.stdout.decode(),'stderr':r.stderr.decode()}))
'''
    flags = ['-B', '-O', '-S'] if sys.flags.optimize else ['-B', '-S']
    result = subprocess.run([sys.executable, *flags, '-c', driver,
                             str(fixture.resolve()), family, behavior],
                            env=env, capture_output=True, timeout=60)
    (folder / 'driver.stdout').write_bytes(result.stdout)
    (folder / 'driver.stderr').write_bytes(result.stderr)
    (folder / 'driver.exit').write_text(str(result.returncode) + '\n')
    return result, read_events(trace)


class GitFixtureIsolationTests(unittest.TestCase):
    def test_actual_fixtures_never_launch_automatic_maintenance(self):
        for family in ('d5', 'palm', 'factorial'):
            with self.subTest(family=family), tempfile.TemporaryDirectory() as td:
                result, events = trace_fixture(FIXTURE, Path(td), family)
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                self.assertEqual(result.stderr, b'')
                report = json.loads(result.stdout)
                self.assertEqual(report['returncode'], 0, report)
                self.assertEqual(report['stderr'], '')
                self.assertEqual((report['before'], report['after']), ('true', 'true'))
                commits = [event for event in events if event.get('event') == 'start'
                           and 'commit' in event.get('argv', [])]
                self.assertEqual(len(commits), 1, 'trace must observe the real fixture commit')
                self.assertEqual(maintenance_commands(events), [],
                                 'fixture commit launched automatic maintenance before cleanup')

    def test_trace_detects_eligible_maintenance_in_positive_control(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            root = folder / 'positive-control'
            root.mkdir()
            trace = folder / 'positive-trace.jsonl'
            env = trace_environment(trace)
            (root / 'payload').write_bytes(b'synthetic positive control\n')
            for command in (['git', 'init', '-q'], ['git', 'add', '.'],
                            ['git', '-c', 'user.name=Protocol Fixture',
                             '-c', 'user.email=fixture@example.invalid',
                             '-c', 'commit.gpgsign=false', 'commit', '-qm', 'positive control']):
                subprocess.run(command, cwd=root, env=env, check=True, capture_output=True, timeout=30)
            events = read_events(trace)
            self.assertEqual(len(maintenance_commands(events)), 1,
                             'positive control must start automatic maintenance')
            self.assertTrue(any('pack-objects' in argv for argv in child_commands(events)),
                            'forced loose-object task must actually run')


if __name__ == '__main__':
    unittest.main()
