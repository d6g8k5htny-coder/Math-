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


class VerdictVocabulary(unittest.TestCase):
    """Lexical family checks, not semantic entailment or scope verification."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='verdict-vocabulary-')
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.source = self.root / 'record.md'
        self.doc = self.root / 'nav.md'

    def _report(self, body, summary):
        self.source.write_text(body, encoding='utf-8')
        self.doc.write_text(HEADER + '| #1 | [r](record.md) — summary: '
                            + summary + ' |\n', encoding='utf-8')
        return check_doc_quotes.check_document(str(self.doc), str(self.root))

    def _rejected(self, body, word):
        report = self._report(body, word)
        self.assertEqual([f[0] for f in report['failures']],
                         ['verdict-word-not-in-source'])
        self.assertTrue(report['failures'][0][2].startswith(word + ': '))
        self.assertEqual((report['checked'], report['summaries']), (1, 1))

    def test_all_bare_verdicts_remain_valid(self):
        for word in check_doc_quotes.VERDICT:
            with self.subTest(word=word):
                self.assertEqual(self._report(word, word)['failures'], [])

    def test_inflected_verdicts_share_the_explicit_family(self):
        for root in ('ACCEPT', 'AMEND', 'REJECT'):
            for body in (root, root + 'ED'):
                for summary in (root, root + 'ED'):
                    with self.subTest(body=body, summary=summary):
                        self.assertEqual(self._report(body, summary)['failures'], [])

    def test_uppercase_scope_tags_remain_valid(self):
        for word in check_doc_quotes.VERDICT:
            for suffix in ('_SCOPED', '_ENGINEERING_SCOPED', '_R1', '_A_23'):
                with self.subTest(word=word, suffix=suffix):
                    self.assertEqual(self._report(word + suffix, word)['failures'], [])
                    self.assertEqual(self._report(word, word + suffix)['failures'], [])

    def test_embedded_word_prefixes_cannot_supply_a_verdict(self):
        for word in check_doc_quotes.VERDICT:
            for prefix in ('UN', 'PRE', 'x'):
                with self.subTest(word=word, prefix=prefix):
                    self._rejected(prefix + word, word)

    def test_embedded_word_suffixes_cannot_supply_a_verdict(self):
        for word in check_doc_quotes.VERDICT:
            for suffix in ('NESS', 'LIKE', 'x'):
                with self.subTest(word=word, suffix=suffix):
                    self._rejected(word + suffix, word)

    def test_underscore_prefixes_cannot_supply_a_verdict(self):
        for word in check_doc_quotes.VERDICT:
            for prefix in ('NOT_', 'OTHER_', '_'):
                with self.subTest(word=word, prefix=prefix):
                    self._rejected(prefix + word, word)

    def test_unicode_word_boundaries_are_preserved(self):
        for word in check_doc_quotes.VERDICT:
            for body in ('α' + word, word + 'β', '９' + word):
                with self.subTest(body=body):
                    self._rejected(body, word)

    def test_malformed_scope_tags_cannot_supply_a_verdict(self):
        for word in check_doc_quotes.VERDICT:
            for suffix in ('_', '__SCOPED', '_scoped'):
                with self.subTest(word=word, suffix=suffix):
                    self._rejected(word + suffix, word)

    def test_nonverdict_summary_words_do_not_invent_status_claims(self):
        for word in check_doc_quotes.VERDICT:
            for summary in ('UN' + word, word + 'NESS', 'NOT_' + word):
                with self.subTest(summary=summary):
                    self.assertEqual(self._report('No status supplied.', summary)['failures'], [])

    def test_different_verdict_families_still_reject(self):
        for body in check_doc_quotes.VERDICT:
            for summary in check_doc_quotes.VERDICT:
                if body != summary:
                    with self.subTest(body=body, summary=summary):
                        self._rejected(body, summary)

    def test_each_claimed_family_is_checked(self):
        report = self._report('ACCEPT_SCOPED', 'ACCEPT; HOLD; VERIFIED')
        self.assertEqual([f[2].split(':', 1)[0] for f in report['failures']],
                         ['HOLD', 'VERIFIED'])

    def test_markdown_and_punctuation_do_not_hide_real_tokens(self):
        for word in check_doc_quotes.VERDICT:
            for wrapped in ('**' + word + '**', '`' + word + '`', '(' + word + ')'):
                with self.subTest(wrapped=wrapped):
                    self.assertEqual(self._report(wrapped, wrapped)['failures'], [])

    def test_quotation_matching_is_unchanged(self):
        self.source.write_text('Recorded word UNVERIFIED.', encoding='utf-8')
        self.doc.write_text(HEADER + '| #1 | [r](record.md) — “UNVERIFIED.” |\n',
                            encoding='utf-8')
        report = check_doc_quotes.check_document(str(self.doc), str(self.root))
        self.assertEqual(report['failures'], [])
        self.assertEqual((report['quotes'], report['summaries']), (1, 0))

    def test_offline_links_remain_explicitly_unchecked(self):
        self.doc.write_text(HEADER + '| #1 | [r](https://github.com/o/r/pull/1'
                            '#issuecomment-2) — summary: VERIFIED |\n', encoding='utf-8')
        report = check_doc_quotes.check_document(str(self.doc), str(self.root))
        self.assertEqual((report['checked'], report['unchecked_offline']), (0, 1))
        self.assertEqual(report['failures'], [])

    def test_fetched_source_uses_the_same_lexical_boundary(self):
        # Synthetic source transport only; not an actual remote verification.
        from unittest.mock import patch
        self.doc.write_text(HEADER + '| #1 | [r](https://github.com/o/r/pull/1'
                            '#issuecomment-2) — summary: VERIFIED |\n', encoding='utf-8')
        with patch.object(check_doc_quotes.Sources, '_fetch', return_value=('UNVERIFIED', 'ok')):
            report = check_doc_quotes.check_document(str(self.doc), str(self.root), github=True)
        self.assertEqual(report['unchecked_offline'], 0)
        self.assertEqual([f[0] for f in report['failures']], ['verdict-word-not-in-source'])

    def test_cli_fails_for_a_lookalike_source(self):
        import contextlib
        import io
        import json
        self._report('UNVERIFIED', 'VERIFIED')
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            rc = check_doc_quotes.main([str(self.doc), '--root', str(self.root)])
        self.assertEqual(rc, 1)
        self.assertFalse(json.loads(output.getvalue())['passed'])

    def test_compact_decimal_record_references_remain_valid(self):
        for word in check_doc_quotes.VERDICT:
            for number in ('1', '5344158101', '5344767944'):
                for suffix in ('', '_SCOPED'):
                    with self.subTest(word=word, number=number, suffix=suffix):
                        compact = word + number + suffix
                        self.assertEqual(self._report(compact, word)['failures'], [])
                        self.assertEqual(self._report(word, compact)['failures'], [])

    def test_actual_compact_amend_review_openings(self):
        for body, summary in (
            ('Catalog AMEND5344158101 is addressed at exact head9baa6609.',
             'Catalog AMEND 5344158101 is addressed at exact head 9baa6609'),
            ('AMEND5344767944 addressed at exact head077e3d5.',
             'AMEND 5344767944 addressed at exact head 077e3d5'),
        ):
            with self.subTest(body=body):
                self.assertEqual(self._report(body, summary)['failures'], [])

    def test_compact_reference_inflections_share_the_family(self):
        for word in ('ACCEPT', 'AMEND', 'REJECT'):
            with self.subTest(word=word):
                self.assertEqual(self._report(word + 'ED123', word)['failures'], [])
                self.assertEqual(self._report(word, word + 'ED123')['failures'], [])

    def test_reference_suffix_does_not_allow_word_lookalikes(self):
        for word in check_doc_quotes.VERDICT:
            for body in ('UN' + word + '123', 'NOT_' + word + '123',
                         word + '123abc', word + '123β', word + '１２３'):
                with self.subTest(body=body):
                    self._rejected(body, word)

    def test_negation_and_scope_entailment_are_not_claimed(self):
        # This comparator checks vocabulary presence only, not what it means.
        self.assertEqual(self._report('not VERIFIED', 'VERIFIED')['failures'], [])
        self.assertEqual(self._report('AMEND_ENGINEERING_SCOPED', 'AMEND')['failures'], [])


if __name__ == '__main__':
    unittest.main()
