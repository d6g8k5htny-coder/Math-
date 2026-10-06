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
