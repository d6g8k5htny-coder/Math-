"""Real-Git lifecycle regression for the downstream-gate disposable fixtures.

The actual fixture tests in frontiers/downstream_gate_20260925/test_transition_contract.py
run in a child interpreter under Trace2. Global and system Git configuration
are emptied and every inherited GIT_* variable is removed, so the effective
maintenance.auto value is Git's default unless the fixture sets it
repository-locally. No maintenance setting is forced at command or environment
scope: the claim is bounded to that effective configuration and says nothing
about runners with higher-priority overrides. No fixture, checker or
subprocess is mocked.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / 'frontiers/downstream_gate_20260925'
FIXTURE_TESTS = (
    'test_git_source_only_change_on_real_commits',
    'test_git_d1_component_change_revalidates_d1_d2_d3',
    'test_git_unrelated_edit_does_not_revalidate_d1',
    'test_git_pre_repair_graph_misses_component_change',
)


def trace_environment(trace):
    env = {key: value for key, value in os.environ.items()
           if not key.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TRACE2_EVENT=str(trace.resolve()))
    return env


def read_events(trace):
    return [json.loads(line) for line in trace.read_text().splitlines() if line]


def maintenance_commands(events):
    return [event.get('argv', []) for event in events
            if event.get('event') == 'child_start'
            and 'maintenance' in event.get('argv', []) and '--auto' in event.get('argv', [])]


def commit_starts(events):
    return [event for event in events if event.get('event') == 'start'
            and 'commit' in event.get('argv', [])]


class DownstreamGateGitIsolationTests(unittest.TestCase):
    def test_actual_gate_fixtures_never_launch_automatic_maintenance(self):
        flags = ['-B', '-O', '-S'] if sys.flags.optimize else ['-B', '-S']
        names = ['test_transition_contract.TransitionContract.' + name for name in FIXTURE_TESTS]
        with tempfile.TemporaryDirectory() as td:
            trace = Path(td) / 'git-trace.jsonl'
            result = subprocess.run([sys.executable, *flags, '-m', 'unittest', *names],
                                    cwd=GATE, env=trace_environment(trace),
                                    capture_output=True, text=True, timeout=120)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f'Ran {len(FIXTURE_TESTS)} tests', result.stderr)
            self.assertNotIn('skipped=', result.stderr)
            self.assertNotIn('\nERROR:', result.stderr)
            events = read_events(trace)
            self.assertGreaterEqual(len(commit_starts(events)), len(FIXTURE_TESTS),
                                    'trace must observe the real fixture commits')
            self.assertEqual(maintenance_commands(events), [],
                             'gate fixture commit launched automatic maintenance before cleanup')

    def test_trace_detects_default_maintenance_in_positive_control(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            root = folder / 'positive-control'
            root.mkdir()
            trace = folder / 'positive-trace.jsonl'
            env = trace_environment(trace)
            unset = subprocess.run(['git', 'config', '--get', 'maintenance.auto'],
                                   cwd=folder, env=env, capture_output=True, timeout=30)
            self.assertEqual(unset.returncode, 1, 'effective maintenance.auto must be Git default here')
            (root / 'payload').write_bytes(b'synthetic positive control\n')
            for command in (['git', 'init', '-q'], ['git', 'add', '.'],
                            ['git', '-c', 'user.name=Gate Fixture',
                             '-c', 'user.email=fixture@example.invalid',
                             '-c', 'commit.gpgsign=false', 'commit', '-qm', 'positive control']):
                subprocess.run(command, cwd=root, env=env, check=True, capture_output=True, timeout=30)
            self.assertEqual(len(maintenance_commands(read_events(trace))), 1,
                             'positive control must start automatic maintenance under the default')


if __name__ == '__main__':
    unittest.main()
