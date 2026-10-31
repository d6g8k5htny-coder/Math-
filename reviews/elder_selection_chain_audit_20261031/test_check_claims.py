import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_claims  # noqa: E402

REPOS = {'Math-': os.path.abspath(os.path.join(HERE, '..', '..'))}


def load():
    with open(os.path.join(HERE, 'CLAIMS.json'), encoding='utf-8') as fh:
        return json.load(fh)


def run_doc(doc):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'CLAIMS.json')
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(doc, fh)
        return check_claims.run(path, REPOS)


class CheckClaimsTests(unittest.TestCase):
    def test_committed_register_passes(self):
        ok, out = run_doc(load())
        self.assertTrue(ok, '\n'.join(out))
        self.assertTrue(out[-1].startswith('RESULT PASS'))
        self.assertFalse(any(line.startswith('FAIL') for line in out))

    def test_tampered_sha256_fails(self):
        doc = load()
        key = sorted(k for k, s in doc['sources'].items() if s['repo'] == 'Math-')[0]
        doc['sources'][key]['sha256'] = '0' * 64
        ok, out = run_doc(doc)
        self.assertFalse(ok)
        self.assertTrue(any(line.startswith('FAIL %s: sha256' % key) for line in out), '\n'.join(out))

    def test_wrong_byte_count_fails(self):
        doc = load()
        key = sorted(k for k, s in doc['sources'].items() if s['repo'] == 'Math-')[0]
        doc['sources'][key]['bytes'] += 1
        ok, out = run_doc(doc)
        self.assertFalse(ok)
        self.assertTrue(any(line.startswith('FAIL %s:' % key) and 'bytes' in line for line in out))

    def test_status_outside_taxonomy_fails(self):
        doc = load()
        doc['claims'][0]['status'] = 'Accepted'
        ok, out = run_doc(doc)
        self.assertFalse(ok)
        self.assertTrue(any('not in taxonomy' in line for line in out))

    def test_dangling_dependency_fails(self):
        doc = load()
        doc['claims'][0].setdefault('depends_on', []).append('NO-SUCH-CLAIM')
        ok, out = run_doc(doc)
        self.assertFalse(ok)
        self.assertTrue(any('depends_on unknown claim NO-SUCH-CLAIM' in line for line in out))

    def test_proved_without_review_fails(self):
        doc = load()
        target = next(c for c in doc['claims'] if c['status'] == 'Proved')
        target['reviews'] = []
        target.pop('kernel_checked', None)
        ok, out = run_doc(doc)
        self.assertFalse(ok)
        self.assertTrue(any('Proved without a nonauthor review' in line for line in out))

    def test_other_repository_sources_are_skipped_not_failed(self):
        doc = load()
        doc['sources'] = {k: v for k, v in doc['sources'].items() if v['repo'] != 'Math-'}
        for c in doc['claims']:
            c['sources'] = [s for s in c['sources'] if s in doc['sources']] or [next(iter(doc['sources']))]
        ok, out = run_doc(doc)
        self.assertTrue(ok, '\n'.join(out))
        self.assertTrue(all(line.startswith(('SKIPPED', 'RESULT')) for line in out), '\n'.join(out))

    def test_cli_modes_agree(self):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        a = subprocess.run([sys.executable, '-B', '-S', os.path.join(HERE, 'check_claims.py')],
                           capture_output=True, env=env)
        b = subprocess.run([sys.executable, '-B', '-O', '-S', os.path.join(HERE, 'check_claims.py')],
                           capture_output=True, env=env)
        self.assertEqual(a.returncode, 0, a.stdout.decode() + a.stderr.decode())
        self.assertEqual(a.stdout, b.stdout)
        self.assertEqual(a.returncode, b.returncode)


if __name__ == '__main__':
    unittest.main()
