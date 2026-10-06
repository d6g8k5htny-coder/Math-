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


class VerdictSourceBoundaries(unittest.TestCase):
    """Source verdict prefixes obey the same left boundary as summary prefixes.

    These are lexical checks, not an entailment or negation classifier. Suffixes,
    case sensitivity and literal quotation behavior retain the existing policy.
    """
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='verdict-boundary-')
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.source = self.root / 'source.md'
        self.doc = self.root / 'table.md'

    def report(self, source, passage, kind='summary'):
        self.source.write_text(source, encoding='utf-8')
        claim = 'summary: ' + passage if kind == 'summary' else '“' + passage + '”'
        self.doc.write_text(HEADER + '| #1 | [r](source.md) — ' + claim + ' |\n', encoding='utf-8')
        return check_doc_quotes.check_document(str(self.doc), str(self.root))

    def test_attached_word_prefix_cannot_supply_source_verdict(self):
        for word in check_doc_quotes.VERDICT:
            for prefix in ('UN', 'PRE', 'NON', '_', '9', 'λ'):
                with self.subTest(word=word, prefix=prefix):
                    result = self.report(prefix + word, word)
                    self.assertEqual(result['checked'], 1)
                    self.assertEqual(result['unchecked_offline'], 0)
                    self.assertEqual(result['failures'], [
                        ['verdict-word-not-in-source', 'source.md', word + ': ' + word + ' ']])

    def test_existing_suffix_and_punctuation_policy_is_preserved(self):
        for word in check_doc_quotes.VERDICT:
            for left in ('', ' ', '(', ':', '—', '“', '**', '`'):
                for right in ('', '_SCOPED', '-WITH-SCOPE', 'ED'):
                    with self.subTest(word=word, left=left, right=right):
                        self.assertEqual(self.report(left + word + right, word)['failures'], [])

    def test_later_valid_occurrence_can_supply_source_verdict(self):
        for word in check_doc_quotes.VERDICT:
            with self.subTest(word=word):
                self.assertEqual(self.report('UN' + word + '; later: ' + word, word)['failures'], [])

    def test_verdict_cannot_be_borrowed_from_another_linked_record(self):
        self.source.write_text('UNVERIFIED', encoding='utf-8')
        (self.root / 'other.md').write_text('VERIFIED', encoding='utf-8')
        self.doc.write_text(HEADER + '| #1 | [r](source.md) — summary: VERIFIED'
                            '<br>[s](other.md) — summary: VERIFIED |\n', encoding='utf-8')
        result = check_doc_quotes.check_document(str(self.doc), str(self.root))
        self.assertEqual((result['checked'], result['summaries']), (2, 2))
        self.assertEqual(len(result['failures']), 1)
        self.assertEqual(result['failures'][0][:2], ['verdict-word-not-in-source', 'source.md'])

    def test_summary_word_prefix_and_case_policy_is_unchanged(self):
        for word in check_doc_quotes.VERDICT:
            for passage in ('UN' + word, '_' + word, word.lower()):
                with self.subTest(passage=passage):
                    self.assertEqual(self.report('no selected vocabulary', passage)['failures'], [])

    def test_literal_quote_semantics_is_unchanged(self):
        self.assertEqual(self.report('UNVERIFIED', 'UNVERIFIED', kind='quote')['failures'], [])
        # A literal excerpt remains a substring check; this patch changes summaries only.
        self.assertEqual(self.report('UNVERIFIED', 'VERIFIED', kind='quote')['failures'], [])

    def test_negation_and_suffixes_are_not_semantic_entailment(self):
        for source in ('not VERIFIED', 'VERIFIED only for a different scope', 'VERIFIED_SCOPED'):
            with self.subTest(source=source):
                self.assertEqual(self.report(source, 'VERIFIED')['failures'], [])

    def test_real_cli_rejects_false_support_and_preserves_valid_exit(self):
        import json
        import subprocess
        flags = ['-B', '-S']
        if sys.flags.optimize:
            flags.append('-O')
        for source, expected in [('UNVERIFIED', 1), ('VERIFIED_SCOPED', 0)]:
            with self.subTest(source=source):
                self.report(source, 'VERIFIED')
                result = subprocess.run(
                    [sys.executable, *flags, str(ROOT / 'tools' / 'check_doc_quotes.py'),
                     str(self.doc), '--root', str(self.root)],
                    capture_output=True, text=True, timeout=10, check=False)
                self.assertEqual(result.returncode, expected)
                self.assertEqual(result.stderr, '')
                self.assertEqual(json.loads(result.stdout)['passed'], expected == 0)


if __name__ == '__main__':
    unittest.main()
