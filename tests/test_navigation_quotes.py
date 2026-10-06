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


class VerdictWordStart(unittest.TestCase):
    """Vocabulary membership only: not negation, suffix equality or entailment."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='verdict-boundary-')
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.source = self.root / 'record.md'
        self.doc = self.root / 'navigation.md'

    def _report(self, source, passage):
        self.source.write_text(source, encoding='utf-8')
        self.doc.write_text(HEADER + '| #1 | [r](record.md) — summary: ' + passage + '|\n',
                            encoding='utf-8')
        return check_doc_quotes.check_document(str(self.doc), str(self.root))

    def test_prefixed_source_words_do_not_supply_verdict_roots(self):
        for word in check_doc_quotes.VERDICT:
            for prefix in ('UN', 'NON_', 'x', '_', '0', 'é'):
                with self.subTest(word=word, prefix=prefix):
                    report = self._report(prefix + word, word)
                    self.assertEqual(report['failures'],
                        [['verdict-word-not-in-source', 'record.md', word + ': ' + word]])
                    self.assertEqual((report['checked'], report['unchecked_offline']), (1, 0))

    def test_scoped_summary_cannot_use_a_prefixed_source_word(self):
        report = self._report('UNVERIFIED_SCOPED', 'VERIFIED_SCOPED')
        self.assertEqual(report['failures'],
            [['verdict-word-not-in-source', 'record.md', 'VERIFIED: VERIFIED_SCOPED']])

    def test_existing_word_start_families_and_punctuation_remain_supported(self):
        for word, family in zip(check_doc_quotes.VERDICT,
                ('ACCEPTED', 'AMEND_REQUIRED', 'HOLD_PENDING', 'CONFIRMED_SCOPED',
                 'VERIFIED_SCOPED', 'REJECTED')):
            for source in (word, family, '**' + word + '**.', '`' + family + '`',
                           'Disposition:\n(' + family + ');'):
                with self.subTest(word=word, source=source):
                    self.assertEqual(self._report(source, word)['failures'], [])
                    self.assertEqual(self._report(source, family)['failures'], [])

    def test_missing_roots_and_multiple_failures_keep_exact_diagnostics(self):
        for word in check_doc_quotes.VERDICT:
            with self.subTest(word=word):
                self.assertEqual(self._report('No disposition.', word)['failures'],
                    [['verdict-word-not-in-source', 'record.md', word + ': ' + word]])
        passage = 'ACCEPT HOLD VERIFIED'
        self.assertEqual(self._report('ACCEPT UNVERIFIED', passage)['failures'],
            [['verdict-word-not-in-source', 'record.md', 'HOLD: ' + passage],
             ['verdict-word-not-in-source', 'record.md', 'VERIFIED: ' + passage]])

    def test_embedded_summary_words_are_not_new_verdict_claims(self):
        # Preserve the existing left-boundary policy on the summary side.
        for word in check_doc_quotes.VERDICT:
            with self.subTest(word=word):
                self.assertEqual(self._report('No disposition.', 'UN' + word)['failures'], [])

    def test_case_sensitivity_and_semantic_limits_are_explicit(self):
        self.assertEqual(self._report('verified', 'VERIFIED')['failures'],
            [['verdict-word-not-in-source', 'record.md', 'VERIFIED: VERIFIED']])
        self.assertEqual(self._report('No disposition.', 'verified')['failures'], [])
        # Presence does not establish entailment or equality of scoped verdicts.
        self.assertEqual(self._report('NOT VERIFIED', 'VERIFIED')['failures'], [])
        self.assertEqual(self._report('VERIFIED_A', 'VERIFIED_B')['failures'], [])

    def test_other_source_segments_cannot_supply_the_missing_verdict(self):
        self.source.write_text('UNVERIFIED', encoding='utf-8')
        (self.root / 'other.md').write_text('VERIFIED', encoding='utf-8')
        self.doc.write_text(HEADER + '| #1 | [r](record.md) summary: VERIFIED'
                            '<br>[s](other.md) summary: VERIFIED |\n', encoding='utf-8')
        report = check_doc_quotes.check_document(str(self.doc), str(self.root))
        self.assertEqual(report['failures'],
            [['verdict-word-not-in-source', 'record.md', 'VERIFIED: VERIFIED']])
        self.assertEqual((report['checked'], report['summaries']), (2, 2))

    def test_cli_reports_boundary_failure_and_genuine_success(self):
        import json
        import subprocess
        flags = ['-B', '-S'] if not sys.flags.optimize else ['-B', '-O', '-S']
        for source, expected_exit in (('UNVERIFIED', 1), ('VERIFIED_SCOPED', 0)):
            with self.subTest(source=source):
                self._report(source, 'VERIFIED')
                process = subprocess.run(
                    [sys.executable, *flags, str(ROOT / 'tools/check_doc_quotes.py'),
                     str(self.doc), '--root', str(self.root), '--require-online'],
                    capture_output=True, text=True, timeout=15)
                self.assertEqual(process.returncode, expected_exit, process.stderr)
                self.assertEqual(process.stderr, '')
                report = json.loads(process.stdout)
                self.assertIs(report['passed'], expected_exit == 0)
                result = report['documents'][str(self.doc)]
                self.assertEqual((result['checked'], result['unchecked_offline']), (1, 0))
                expected = [] if expected_exit == 0 else [
                    ['verdict-word-not-in-source', 'record.md', 'VERIFIED: VERIFIED']]
                self.assertEqual(result['failures'], expected)


if __name__ == '__main__':
    unittest.main()
