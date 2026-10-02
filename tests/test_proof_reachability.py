"""Tests for tools/check_proof_reachability.py: the real document passes, and adverse edits fail."""
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check_proof_reachability as cpr  # noqa: E402

DOC = ROOT / 'docs' / 'integration' / '2026-10-02-proof-reachability.md'


class RealDocument(unittest.TestCase):
    def setUp(self):
        self.text = DOC.read_text(encoding='utf-8')

    def test_document_passes(self):
        self.assertEqual(cpr.check(self.text), [])

    def test_every_row_parses(self):
        cut, rows, lines = cpr.parse(self.text)
        self.assertIsNotNone(cut)
        self.assertTrue(rows)
        self.assertFalse([r for r in rows if 'malformed' in r])


class AdverseEdits(unittest.TestCase):
    def setUp(self):
        self.text = DOC.read_text(encoding='utf-8')
        self.cut, self.rows, self.lines = cpr.parse(self.text)
        self.first = self.lines[0]

    def _fails(self, text):
        return cpr.check(text)

    def test_wrong_blob_fails(self):
        r = self.rows[0]
        bad = self.first.replace(r['blob'], ('0' if r['blob'][0] != '0' else '1') + r['blob'][1:])
        self.assertTrue(self._fails(self.text.replace(self.first, bad)))

    def test_dropped_row_fails(self):
        self.assertTrue(self._fails(self.text.replace(self.first + '\n', '')))

    def test_duplicated_row_fails(self):
        self.assertTrue(self._fails(self.text.replace(self.first + '\n', self.first + '\n' + self.first + '\n')))

    def test_wrong_integration_commit_fails(self):
        r = self.rows[0]
        other = self.rows[-1]['commit']
        self.assertNotEqual(other, r['commit'])
        self.assertTrue(self._fails(self.text.replace(self.first, self.first.replace(r['commit'], other))))

    def test_flipped_index_column_fails(self):
        r = self.rows[0]
        flipped = self.first[: -len('| %s |' % r['linked'])] + '| %s |' % ('no' if r['linked'] == 'yes' else 'yes')
        self.assertTrue(self._fails(self.text.replace(self.first, flipped)))

    def test_verdict_word_fails(self):
        self.assertTrue(cpr.verdict_words([self.first + ' ACCEPT']))
        self.assertEqual(cpr.verdict_words([self.first]), [])

    def test_missing_cut_fails(self):
        self.assertEqual(cpr.check(self.text.replace('Cut: `', 'Cutoff: `')), ['no cut commit line'])


if __name__ == '__main__':
    unittest.main()
