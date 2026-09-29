"""Real local Git fixtures for the prior-credit pin regression; no network."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import verify_packet as v


class SourcePinTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.root = self.repo/'packet'
        self.root.mkdir()
        self.data = b'fixture proof\n'
        (self.repo/'premise.md').write_bytes(self.data)
        (self.repo/'prior.md').write_bytes(b'credited result\n')
        self.git('init', '-q')
        self.git('add', 'premise.md', 'prior.md')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'isolated test fixture')
        self.commit = self.git('rev-parse', 'HEAD').strip().decode()
        self.pins = {'sources': [{
            'commit': self.commit, 'path': 'premise.md', 'bytes': len(self.data),
            'sha256': hashlib.sha256(self.data).hexdigest(),
            'git_blob': self.git('rev-parse', 'HEAD:premise.md').strip().decode()}],
            'prior_in_project_result': {
                'commit': self.commit, 'path': 'prior.md',
                'git_blob': self.git('rev-parse', 'HEAD:prior.md').strip().decode()}}

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.repo, check=True,
                              capture_output=True, timeout=20).stdout

    def write(self, pins):
        (self.root/'SOURCE_PINS.json').write_text(json.dumps(pins), encoding='utf-8')

    def test_valid_all_pins(self):
        self.write(self.pins)
        v.source_identity(self.root)

    def test_prior_wrong_blob(self):
        pins = copy.deepcopy(self.pins)
        pins['prior_in_project_result']['git_blob'] = '0'*40
        self.write(pins)
        with self.assertRaises(ValueError):
            v.source_identity(self.root)

    def test_prior_wrong_path(self):
        pins = copy.deepcopy(self.pins)
        pins['prior_in_project_result']['path'] = 'missing.md'
        self.write(pins)
        with self.assertRaises(subprocess.CalledProcessError):
            v.source_identity(self.root)

    def test_prior_wrong_commit(self):
        pins = copy.deepcopy(self.pins)
        pins['prior_in_project_result']['commit'] = '0'*40
        self.write(pins)
        with self.assertRaises(subprocess.CalledProcessError):
            v.source_identity(self.root)

    def test_prior_unsafe_path(self):
        pins = copy.deepcopy(self.pins)
        pins['prior_in_project_result']['path'] = '../prior.md'
        self.write(pins)
        with self.assertRaises(ValueError):
            v.source_identity(self.root)

    def test_premise_still_checks_sha256(self):
        pins = copy.deepcopy(self.pins)
        pins['sources'][0]['sha256'] = '0'*64
        self.write(pins)
        with self.assertRaises(ValueError):
            v.source_identity(self.root)


if __name__ == '__main__':
    unittest.main()
