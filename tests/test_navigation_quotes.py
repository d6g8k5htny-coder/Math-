"""Tests for tools/check_doc_quotes.py: verbatim excerpts versus labelled summaries in
navigation tables, checked against the linked local record (offline)."""
import pathlib
import shutil
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check_doc_quotes  # noqa: E402

NAV_DOC = 'docs/integration/2026-09-29-navigation-refresh.md'
HEADER = ('| PR | Records — “verbatim excerpt” or summary: |\n'
          '|---|---|\n')
RECORD = ('# Review\n\nVerdict: **ACCEPT** at the stated `fixed-d` scope. No defect was found.\n\n'
          'Item 4 | pins \\| minors | CONFIRMED.\n')


class NavigationRecordOffline(unittest.TestCase):
    def test_navigation_record_file_sourced_passages_are_verbatim_or_labelled(self):
        report = check_doc_quotes.check_document(str(ROOT / NAV_DOC), str(ROOT))
        self.assertEqual(report['failures'], [])
        self.assertGreater(report['checked'], 0)
        self.assertGreater(report['quotes'], 0)
        self.assertGreater(report['summaries'], 0)

    def test_main_exit_status(self):
        rc = check_doc_quotes.main([str(ROOT / NAV_DOC), '--root', str(ROOT)])
        self.assertEqual(rc, 0)


class QuoteSemantics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='docquotes-')
        self.root = pathlib.Path(self.tmp)
        (self.root / 'reviews').mkdir()
        (self.root / 'reviews' / 'r.md').write_text(RECORD, encoding='utf-8')
        (self.root / 'docs' / 'nested').mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _report(self, row):
        doc = self.root / 'docs' / 'nested' / 'a.md'
        doc.write_text(HEADER + row + '\n', encoding='utf-8')
        return check_doc_quotes.check_document(str(doc), self.tmp)

    def test_verbatim_excerpt_is_accepted(self):
        report = self._report('| #1 | [r](../../reviews/r.md) — “Verdict: ACCEPT at the stated fixed-d scope. No defect was found.” |')
        self.assertEqual(report['failures'], [])
        self.assertEqual((report['checked'], report['quotes']), (1, 1))

    def test_omissions_in_order_are_accepted(self):
        report = self._report('| #1 | [r](../../reviews/r.md) — “Verdict: ACCEPT … No defect was found … CONFIRMED.” |')
        self.assertEqual(report['failures'], [])

    def test_pieces_out_of_order_are_rejected(self):
        report = self._report('| #1 | [r](../../reviews/r.md) — “No defect was found … Verdict: ACCEPT” |')
        self.assertEqual([f[0] for f in report['failures']], ['not-verbatim'])

    def test_paraphrase_in_quotation_marks_is_rejected(self):
        report = self._report('| #1 | [r](../../reviews/r.md) — “Items 1–4: CONFIRMED; verdict ACCEPT at scope.” |')
        self.assertEqual([f[0] for f in report['failures']], ['not-verbatim'])

    def test_escaped_pipe_inside_cell_matches_source(self):
        report = self._report('| #1 | [r](../../reviews/r.md) — “Item 4 \\| pins \\| minors \\| CONFIRMED.” |')
        self.assertEqual(report['failures'], [])

    def test_labelled_summary_with_source_verdict_words_is_accepted(self):
        report = self._report('| #1 | [r](../../reviews/r.md) — summary: items 1–4 CONFIRMED; ACCEPT at the stated scope |')
        self.assertEqual(report['failures'], [])
        self.assertEqual((report['checked'], report['summaries']), (1, 1))

    def test_labelled_summary_with_foreign_verdict_word_is_rejected(self):
        report = self._report('| #1 | [r](../../reviews/r.md) — summary: continuum HOLD; finite ACCEPT |')
        self.assertEqual([f[0] for f in report['failures']], ['verdict-word-not-in-source'])

    def test_passage_without_preceding_link_is_rejected(self):
        report = self._report('| #1 | “Verdict: ACCEPT” — [r](../../reviews/r.md) |')
        self.assertEqual([f[0] for f in report['failures']], ['no-source-link'])

    def test_missing_source_file_is_rejected(self):
        report = self._report('| #1 | [r](../../reviews/none.md) — “Verdict: ACCEPT” |')
        self.assertEqual([f[0] for f in report['failures']], ['source-missing'])

    def test_github_link_is_unchecked_offline_not_failed(self):
        report = self._report('| #1 | [c](https://github.com/o/r/pull/1#issuecomment-2) — “anything at all” |')
        self.assertEqual(report['failures'], [])
        self.assertEqual((report['checked'], report['unchecked_offline']), (0, 1))


    def test_require_online_rejects_unchecked_github_link(self):
        doc = self.root / 'docs' / 'nested' / 'a.md'
        doc.write_text(HEADER + '| #1 | [c](https://github.com/o/r/pull/1#issuecomment-2) — “anything at all” |\n', encoding='utf-8')
        rc = check_doc_quotes.main([str(doc), '--root', self.tmp, '--require-online'])
        self.assertEqual(rc, 1)

    def test_github_transport_failure_is_not_counted_as_offline(self):
        doc = self.root / 'docs' / 'nested' / 'a.md'
        doc.write_text(HEADER + '| #1 | [c](https://github.com/o/r/pull/1#issuecomment-2) — “anything at all” |\n', encoding='utf-8')
        original = check_doc_quotes.Sources._fetch
        try:
            check_doc_quotes.Sources._fetch = lambda self, match: (None, 'unreachable')
            report = check_doc_quotes.check_document(str(doc), self.tmp, github=True, token='x')
        finally:
            check_doc_quotes.Sources._fetch = original
        self.assertEqual(report['unchecked_offline'], 0)
        self.assertEqual([f[0] for f in report['failures']], ['source-unreachable'])

    def test_nearest_preceding_link_governs_each_passage(self):
        (self.root / 'reviews' / 's.md').write_text('Disposition: AMEND the ledger.\n', encoding='utf-8')
        row = ('| #1 | [r](../../reviews/r.md) — “No defect was found.”'
               '<br>[s](../../reviews/s.md) — “Disposition: AMEND the ledger.” |')
        self.assertEqual(self._report(row)['failures'], [])
        row_wrong = ('| #1 | [r](../../reviews/r.md) — “No defect was found.”'
                     '<br>[s](../../reviews/s.md) — “No defect was found.” |')
        self.assertEqual([f[0] for f in self._report(row_wrong)['failures']], ['not-verbatim'])

    def test_header_row_quotation_marks_are_ignored(self):
        report = self._report('| #1 | [r](../../reviews/r.md) — summary: no defect |')
        self.assertEqual((report['quotes'], report['summaries']), (0, 1))


if __name__ == '__main__':
    unittest.main()
