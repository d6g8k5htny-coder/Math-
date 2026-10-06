"""Behavior of tools/retrofit_record_check.py against reviews/retrofit_20261006/CONTRACT.md v0.1."""
import copy
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOL = ROOT / 'tools' / 'retrofit_record_check.py'
EXAMPLE = ROOT / 'reviews' / 'retrofit_20261006' / 'CONTRACT_EXAMPLE.json'
SPEC = importlib.util.spec_from_file_location('retrofit_record_check', TOOL)
rc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rc)


def example():
    return rc.load_strict(EXAMPLE.read_text(encoding='utf-8'))


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True, check=True).stdout.strip()


class Shape(unittest.TestCase):
    def test_example_is_valid(self):
        self.assertEqual(rc.validate(example()), [])

    def mutated(self, change):
        data = example()
        change(data)
        return rc.validate(data)

    def test_closed_vocabulary_and_keys(self):
        cases = {
            'status word as state': lambda d: d['records'][0].update(state='PROVED_REVIEWED'),
            'CLOSED as state': lambda d: d['records'][0].update(state='CLOSED'),
            'unknown axis': lambda d: d['records'][0].update(axis='closure'),
            'extra status field': lambda d: d['records'][0].update(status='ACCEPT'),
            'extra top-level field': lambda d: d.update(classification='PROVED_REVIEWED'),
            'missing exposure': lambda d: d['records'][0].pop('exposure'),
            'status authority true': lambda d: d.update(status_authority=True),
            'status authority zero': lambda d: d.update(status_authority=0),
            'scientific effect': lambda d: d.update(scientific_effect='ACCEPT'),
            'other baseline': lambda d: d['baseline'].update(main='0' * 40),
            'independence one': lambda d: d['records'][0].update(independence_credit=1),
            'independence boolean': lambda d: d['records'][0].update(independence_credit=False),
            'recorded without evidence': lambda d: d['records'][0].update(evidence=[]),
            'not_recorded with evidence': lambda d: d['records'][0].update(state='not_recorded'),
            'non-baseline without delta': lambda d: d['records'][0]['subject'].update(commit='a' * 40),
            'delta not boolean': lambda d: d['records'][0].update(delta=0),
            'path traversal': lambda d: d['records'][0]['subject'].update(path='../STATUS.md'),
            'absolute path': lambda d: d['records'][0]['subject'].update(path='/etc/passwd'),
            'uppercase blob': lambda d: d['records'][0]['subject'].update(blob='A' * 40),
            'duplicate id': lambda d: d['records'][1].update(id='EX-001'),
            'dangling alias': lambda d: d['records'][1].update(alias_of='EX-999'),
            'self alias': lambda d: d['records'][1].update(alias_of='EX-002'),
            'performer as Human': lambda d: d['records'][0].update(performer={'provider': 'Human'}),
            'empty performer field': lambda d: d['records'][0]['performer'].update(session=''),
            'comment ref not numeric': lambda d: d['records'][0]['evidence'].append(
                {'kind': 'github_comment', 'repository': 'main', 'ref': 'latest'}),
            'unknown evidence kind': lambda d: d['records'][0]['evidence'].append(
                {'kind': 'chat', 'repository': 'main', 'ref': '1'}),
            'unknown repository': lambda d: d['records'][0]['subject'].update(repository='elsewhere'),
            'empty records': lambda d: d.update(records=[]),
        }
        for name, change in cases.items():
            with self.subTest(case=name):
                self.assertNotEqual(self.mutated(change), [])

    def test_alias_and_delta_are_accepted_when_well_formed(self):
        def change(d):
            d['records'][1].update(alias_of='EX-001')
            d['records'][0].update(delta=True)
            d['records'][0]['subject'].update(commit='b' * 40)
        self.assertEqual(self.mutated(change), [])

    def test_shard_must_match_directory(self):
        self.assertEqual(rc.validate(example(), shard_dir='EXAMPLE'), [])
        self.assertNotEqual(rc.validate(example(), shard_dir='B1_side24'), [])

    def test_strict_parsing(self):
        text = EXAMPLE.read_text(encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
            rc.load_strict(text.replace('"shard": "EXAMPLE",', '"shard": "EXAMPLE", "shard": "OTHER",', 1))
        with self.assertRaisesRegex(ValueError, 'non-finite'):
            rc.load_strict(text.replace('"independence_credit": 0', '"independence_credit": NaN', 1))


def run_item(ref, job, tested, conclusion, purpose='check', expected='success', attempt=1):
    return {'kind': 'workflow_run', 'repository': 'Math-', 'ref': ref, 'attempt': attempt, 'job': job,
            'tested_commit': tested, 'purpose': purpose, 'conclusion': conclusion, 'expected_conclusion': expected}


# Native objects read from the GitHub API on 2026-10-06. The two #343 runs (D2 square/Schur companion) are the
# failed and successful executions named in main#275 6019011163; the custody chain is the six records of
# main#275 6019173460 plus the landing push run of Math-#250.
FAILED_RUN = run_item('37414215874', '112109136502', '3479b6e127b05e953f84feef3f3fb7e88de625ac', 'failure')
PASSED_RUN = run_item('37416061763', '112114814333', 'cc8b2d5bd7505b7f185607880bc0aa1403c8c148', 'success')
CUSTODY_CHAIN = [
    {'kind': 'github_review', 'repository': 'Math-', 'ref': '5365065925',
     'commit': '4e25b9159b7711f4625ec2f6b34b00f819fa29a6'},
    {'kind': 'github_review', 'repository': 'Math-', 'ref': '5401199597',
     'commit': '0efd00e64446f1859cd2c6bb1833068bb16e03a3'},
    {'kind': 'github_review', 'repository': 'Math-', 'ref': '5401287158',
     'commit': '5634edade1db84ddefa25f2cbf92e79da6cce7eb'},
    {'kind': 'github_comment', 'repository': 'Math-', 'ref': '5970327030'},
    {'kind': 'github_comment', 'repository': 'Math-', 'ref': '5970508391'},
    run_item('37131496772', None, '7858329974e28be79f29b22644370084ff43da4f', 'success'),
    {'kind': 'github_comment', 'repository': 'Math-', 'ref': '5972612166'},
]


class EvidenceBindings(unittest.TestCase):
    """State records availability; each event keeps its own binding and outcome."""

    def with_evidence(self, items):
        data = example()
        data['records'][0]['evidence'] = copy.deepcopy(items)
        return data

    def test_failed_and_successful_runs_are_both_recorded(self):
        data = self.with_evidence([FAILED_RUN, PASSED_RUN])
        self.assertEqual(rc.validate(data), [])
        self.assertEqual(data['records'][0]['state'], 'recorded')
        self.assertEqual([e['conclusion'] for e in data['records'][0]['evidence']], ['failure', 'success'])
        self.assertEqual(rc.aggregate([data])['counts']['evidence_items_non_alias'], 2)

    def test_expected_failure_of_a_negative_control_is_well_formed(self):
        control = dict(FAILED_RUN, purpose='negative_control', expected_conclusion='failure')
        self.assertEqual(rc.validate(self.with_evidence([control])), [])

    def test_run_binding_is_closed(self):
        cases = {
            'attempt zero': dict(FAILED_RUN, attempt=0),
            'attempt boolean': dict(FAILED_RUN, attempt=True),
            'attempt string': dict(FAILED_RUN, attempt='1'),
            'job integer': dict(FAILED_RUN, job=112109136502),
            'job text': dict(FAILED_RUN, job='d2-square-schur'),
            'tested commit short': dict(FAILED_RUN, tested_commit='3479b6e1'),
            'purpose build': dict(FAILED_RUN, purpose='build'),
            'verdict as conclusion': dict(FAILED_RUN, conclusion='PASS'),
            'expected cancelled': dict(FAILED_RUN, expected_conclusion='cancelled'),
            'missing purpose': {k: v for k, v in FAILED_RUN.items() if k != 'purpose'},
            'extra verdict': dict(FAILED_RUN, verdict='success'),
        }
        for name, item in cases.items():
            with self.subTest(case=name):
                self.assertNotEqual(rc.validate(self.with_evidence([item])), [])

    def test_review_commit_is_native_and_comments_carry_none(self):
        data = self.with_evidence(CUSTODY_CHAIN)
        self.assertEqual(rc.validate(data), [])
        self.assertEqual(rc.aggregate([data])['counts']['evidence_items_non_alias'], 7)
        cases = {
            'review without commit': (0, lambda e: e.pop('commit')),
            'review commit short': (0, lambda e: e.update(commit='4e25b915')),
            'comment with a commit': (3, lambda e: e.update(commit='5634edade1db84ddefa25f2cbf92e79da6cce7eb')),
            'comment with a verdict': (4, lambda e: e.update(verdict='PASS')),
        }
        for name, (index, change) in cases.items():
            with self.subTest(case=name):
                items = copy.deepcopy(CUSTODY_CHAIN)
                change(items[index])
                self.assertNotEqual(rc.validate(self.with_evidence(items)), [])


class GitVerification(unittest.TestCase):
    def test_subject_and_file_blobs_are_checked_against_git(self):
        head = git('rev-parse', 'HEAD')
        path = 'tools/check_proof_reachability.py'
        blob = git('rev-parse', 'HEAD:' + path)
        data = example()
        record = data['records'][0]
        record.update(delta=True)
        record['subject'].update(commit=head, path=path, blob=blob)
        record['evidence'] = [{'kind': 'file', 'repository': 'Math-', 'commit': head, 'path': path, 'blob': blob}]
        data['records'] = [record]
        repos = {'Math-': ROOT}
        self.assertEqual(rc.validate(data, repos=repos), [])
        wrong = copy.deepcopy(data)
        wrong['records'][0]['subject']['blob'] = 'f' * 40
        self.assertTrue(any('does not match git' in e for e in rc.validate(wrong, repos=repos)))
        wrong = copy.deepcopy(data)
        wrong['records'][0]['evidence'][0]['blob'] = 'f' * 40
        self.assertTrue(any('file evidence blob' in e for e in rc.validate(wrong, repos=repos)))
        wrong = copy.deepcopy(data)
        wrong['records'][0]['subject']['path'] = 'tools/absent_file.py'
        self.assertTrue(any('does not match git' in e for e in rc.validate(wrong, repos=repos)))


class CommandLine(unittest.TestCase):
    def run_tool(self, *args):
        flags = ['-O'] if sys.flags.optimize else []
        return subprocess.run([sys.executable, '-B', *flags, '-S', str(TOOL), *args],
                              capture_output=True, text=True, timeout=60)

    def test_valid_file_aggregates_and_invalid_file_fails(self):
        run = self.run_tool('--aggregate', str(EXAMPLE))
        self.assertEqual((run.returncode, run.stderr), (0, ''))
        report = json.loads(run.stdout)
        self.assertTrue(report['passed'])
        self.assertIs(report['aggregate']['status_authority'], False)
        self.assertEqual(report['aggregate']['counts']['records'], 2)
        with tempfile.TemporaryDirectory() as tmp:
            shard = pathlib.Path(tmp) / 'B1_side24'
            shard.mkdir()
            bad = shard / 'RECORDS.json'
            bad.write_text(EXAMPLE.read_text(encoding='utf-8'))
            before = bad.read_bytes()
            run = self.run_tool(str(bad))
            self.assertEqual(run.returncode, 1)
            report = json.loads(run.stdout)
            self.assertFalse(report['passed'])
            self.assertTrue(any('does not match its directory' in e for e in report['files'][str(bad)]['errors']))
            self.assertEqual(bad.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
