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


class IntegrationOrder(unittest.TestCase):
    """Finding r4170055081: rows must follow first-parent integration order; any swapped pair fails."""

    def setUp(self):
        self.text = DOC.read_text(encoding='utf-8')
        self.cut, self.rows, self.lines = cpr.parse(self.text)

    def _swap(self, i, j):
        a, b = self.lines[i], self.lines[j]
        return self.text.replace(a + '\n', '\0').replace(b + '\n', a + '\n').replace('\0', b + '\n')

    def test_real_order_has_no_order_failure(self):
        self.assertFalse([f for f in cpr.check(self.text) if f.startswith('row order')])

    def test_swapped_adjacent_rows_with_different_commits_fail(self):
        i = next(k for k in range(len(self.rows) - 1) if self.rows[k]['commit'] != self.rows[k + 1]['commit'])
        failures = cpr.check(self._swap(i, i + 1))
        self.assertTrue([f for f in failures if f.startswith('row order')], failures)

    def test_swapped_rows_sharing_a_commit_fail(self):
        i = next(k for k in range(len(self.rows) - 1) if self.rows[k]['commit'] == self.rows[k + 1]['commit'])
        failures = cpr.check(self._swap(i, i + 1))
        self.assertTrue([f for f in failures if f.startswith('row order')], failures)

    def test_last_four_rows_reversed_fail(self):
        n = len(self.lines)
        text = self._swap(n - 4, n - 1)
        failures = cpr.check(text)
        self.assertTrue([f for f in failures if f.startswith('row order')], failures)


class VerdictWordsBothTables(unittest.TestCase):
    """Finding r4170055086: every row of both tables is scanned; a verdict word in either table fails."""

    def setUp(self):
        self.text = DOC.read_text(encoding='utf-8')
        self.inventory_row = cpr.parse(self.text)[2][0]
        self.chain_row = [l for l in self.text.splitlines() if l.startswith('| `')][0]

    def test_both_tables_are_scanned(self):
        scanned = cpr.all_table_lines(self.text)
        self.assertIn(self.inventory_row, scanned)
        self.assertIn(self.chain_row, scanned)
        self.assertEqual(len(cpr.chain_rows(self.text)), 3)

    def test_each_verdict_word_in_each_table_fails(self):
        for word in cpr.VERDICT_WORDS:
            for row in (self.inventory_row, self.chain_row):
                for variant in (word, word.lower()):
                    bad = row[:-1] + variant + ' |'
                    failures = cpr.check(self.text.replace(row, bad))
                    self.assertTrue([f for f in failures if f.startswith('verdict word')], (word, row[:40]))

    def test_verdict_word_in_a_header_fails(self):
        header = '| Packet | PR | Integration commit | `PROOF.md` blob | Landing receipt on main#229 |'
        self.assertIn(header, self.text)
        failures = cpr.check(self.text.replace(header, header.replace('PR |', 'PR (PASS) |')))
        self.assertTrue([f for f in failures if f.startswith('verdict word')], failures)


class ChainTableIdentities(unittest.TestCase):
    def setUp(self):
        self.text = DOC.read_text(encoding='utf-8')
        self.row = [l for l in self.text.splitlines() if l.startswith('| `')][0]
        self.chain = cpr.chain_rows(self.text)[0]

    def test_wrong_chain_blob_prefix_fails(self):
        b = self.chain['blob']
        bad = self.row.replace(b, ('0' if b[0] != '0' else '1') + b[1:])
        self.assertIn('chain-table identity mismatch: ' + self.chain['folder'], cpr.check(self.text.replace(self.row, bad)))

    def test_wrong_chain_commit_prefix_fails(self):
        c = self.chain['commit']
        bad = self.row.replace(c, ('0' if c[0] != '0' else '1') + c[1:])
        self.assertIn('chain-table identity mismatch: ' + self.chain['folder'], cpr.check(self.text.replace(self.row, bad)))

    def test_wrong_chain_pr_fails(self):
        bad = self.row.replace('| #%s |' % self.chain['pr'], '| #%d |' % (int(self.chain['pr']) + 1))
        self.assertIn('chain-table identity mismatch: ' + self.chain['folder'], cpr.check(self.text.replace(self.row, bad)))


if __name__ == '__main__':
    unittest.main()
