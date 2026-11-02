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

    def test_prefixed_source_verdict_does_not_authorize_summary(self):
        for word in check_doc_quotes.VERDICT:
            for prefix in ('UN', 'RE', '_', '9', 'é'):
                with self.subTest(word=word, prefix=prefix):
                    (self.root / 'reviews' / 'r.md').write_text(prefix + word, encoding='utf-8')
                    report = self._report('| #1 | [r](../../reviews/r.md) — summary: ' + word + ' |')
                    self.assertEqual((report['checked'], report['summaries'], report['unchecked_offline']), (1, 1, 0))
                    self.assertEqual([f[0] for f in report['failures']], ['verdict-word-not-in-source'])
                    self.assertTrue(report['failures'][0][2].startswith(word + ': '))

    def test_word_start_and_existing_suffix_families_remain_accepted(self):
        for word in check_doc_quotes.VERDICT:
            for text in (word, '(' + word + ')', '**' + word + '_SCOPED**'):
                with self.subTest(word=word, text=text):
                    (self.root / 'reviews' / 'r.md').write_text(text, encoding='utf-8')
                    report = self._report('| #1 | [r](../../reviews/r.md) — summary: ' + word + '_SCOPED |')
                    self.assertEqual(report['failures'], [])
                    self.assertEqual(report['checked'], 1)

    def test_prefixed_summary_is_not_an_unprefixed_verdict_claim(self):
        (self.root / 'reviews' / 'r.md').write_text('No tracked verdict.', encoding='utf-8')
        for word in check_doc_quotes.VERDICT:
            with self.subTest(word=word):
                report = self._report('| #1 | [r](../../reviews/r.md) — summary: UN' + word + ' |')
                self.assertEqual(report['failures'], [])
                self.assertEqual(report['summaries'], 1)

    def test_standalone_verdict_after_prefixed_word_is_found(self):
        for word in check_doc_quotes.VERDICT:
            with self.subTest(word=word):
                (self.root / 'reviews' / 'r.md').write_text('UN' + word + '; ' + word, encoding='utf-8')
                report = self._report('| #1 | [r](../../reviews/r.md) — summary: ' + word + ' |')
                self.assertEqual(report['failures'], [])

    def test_cli_preserves_positive_and_rejects_prefixed_source(self):
        import json
        import subprocess

        doc = self.root / 'docs' / 'nested' / 'a.md'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else []) + ['-S']
        for word in check_doc_quotes.VERDICT:
            for prefix, expected in (('', 0), ('UN', 1)):
                with self.subTest(word=word, prefix=prefix):
                    (self.root / 'reviews' / 'r.md').write_text(prefix + word, encoding='utf-8')
                    doc.write_text(HEADER + '| #1 | [r](../../reviews/r.md) — summary: ' + word + ' |\n', encoding='utf-8')
                    result = subprocess.run(
                        [sys.executable, *flags, str(ROOT / 'tools' / 'check_doc_quotes.py'),
                         str(doc), '--root', self.tmp, '--require-online'],
                        capture_output=True, check=False, timeout=15)
                    self.assertEqual(result.returncode, expected)
                    self.assertEqual(result.stderr, b'')
                    report = json.loads(result.stdout)
                    self.assertIs(report['passed'], expected == 0)
                    self.assertTrue(report['require_online'])
                    actual = report['documents'][str(doc)]
                    self.assertEqual((actual['checked'], actual['summaries'], actual['unchecked_offline']), (1, 1, 0))
                    self.assertEqual([f[0] for f in actual['failures']],
                                     ['verdict-word-not-in-source'] if expected else [])

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


class GitHubLocatorIdentity(unittest.TestCase):
    """Controlled HTTP bytes exercise real parsing/CLI; these are not live-source claims."""

    def response(self, kind='issuecomment'):
        marker = kind + ('' if kind == 'discussion_r' else '-')
        parent = 'issue_url' if kind == 'issuecomment' else 'pull_request_url'
        family = 'issues' if kind == 'issuecomment' else 'pulls'
        return {'id': 12345, 'body': 'Exact source text. ACCEPT at scope.',
                'html_url': 'https://github.com/Example/Research/pull/31#' + marker + '12345',
                parent: 'https://api.github.com/repos/Example/Research/' + family + '/31'}

    def execute(self, target, response, *, online=True, required=True, transport=False):
        import contextlib
        import io
        import json
        import os
        from unittest import mock

        calls = []
        def fetch(request, timeout):
            calls.append((request.full_url, timeout))
            if transport:
                raise OSError('synthetic unreachable transport')
            return io.BytesIO(json.dumps(response).encode('utf-8'))
        with tempfile.TemporaryDirectory() as directory:
            doc = pathlib.Path(directory) / 'table.md'
            doc.write_text('| Source | Passage |\n|---|---|\n| row | [record](' + target +
                           ') “Exact source text.” |\n', encoding='utf-8')
            args = [str(doc), '--root', directory]
            if online:
                args.append('--github')
            if required:
                args.append('--require-online')
            output = io.StringIO()
            with mock.patch.object(check_doc_quotes.urllib.request, 'urlopen', side_effect=fetch), \
                 mock.patch.dict(os.environ, {'GITHUB_TOKEN': ''}), contextlib.redirect_stdout(output):
                try:
                    code = check_doc_quotes.main(args)
                except Exception as exc:
                    self.fail('source response must fail explicitly, not escape as ' + type(exc).__name__)
            report = json.loads(output.getvalue())
            return code, next(iter(report['documents'].values())), calls

    def test_all_three_canonical_families_and_repository_case(self):
        for kind in ('issuecomment', 'pullrequestreview', 'discussion_r'):
            for case in (False, True):
                with self.subTest(kind=kind, case=case):
                    response = self.response(kind)
                    target = response['html_url']
                    if case:
                        target = target.replace('/Example/Research/', '/example/research/')
                    code, report, calls = self.execute(target, response)
                    self.assertEqual(code, 0)
                    self.assertEqual(report['failures'], [])
                    self.assertEqual((report['checked'], report['unchecked_offline']), (1, 0))
                    self.assertEqual(len(calls), 1)
                    self.assertEqual(calls[0][1], 60)

    def test_wrong_pr_number_never_authenticates_another_comments_body(self):
        for kind in ('issuecomment', 'pullrequestreview', 'discussion_r'):
            with self.subTest(kind=kind):
                response = self.response(kind)
                code, report, _ = self.execute(response['html_url'].replace('/31#', '/32#'), response)
                self.assertEqual(code, 1)
                self.assertEqual([f[0] for f in report['failures']], ['source-identity-mismatch'])
                self.assertEqual(report['unchecked_offline'], 0)

    def test_suffix_and_wrong_fragment_separator_fail_before_transport(self):
        for kind in ('issuecomment', 'pullrequestreview', 'discussion_r'):
            response = self.response(kind)
            canonical = response['html_url']
            wrong = canonical.replace('discussion_r', 'discussion_r-') if kind == 'discussion_r' else canonical.replace(kind+'-', kind)
            for target in [canonical+'junk', canonical+'#other', canonical+'/tail', wrong]:
                with self.subTest(target=target):
                    code, report, calls = self.execute(target, response)
                    self.assertEqual(code, 1)
                    self.assertEqual([f[0] for f in report['failures']], ['source-invalid-locator'])
                    self.assertEqual(calls, [])

    def test_missing_mismatched_or_noninteger_response_identity_fails(self):
        for kind in ('issuecomment', 'pullrequestreview', 'discussion_r'):
            parent = 'issue_url' if kind == 'issuecomment' else 'pull_request_url'
            variants = [('id', 7), ('id', True), ('id', '12345'), ('id', None),
                        ('html_url', 'https://github.com/Example/Research/pull/32#issuecomment-12345'),
                        (parent, 'https://api.github.com/repos/Example/Research/pulls/32'),
                        (parent, None), ('body', None), ('body', 17)]
            for field, value in variants:
                with self.subTest(kind=kind, field=field, value=value):
                    response = self.response(kind); target = response['html_url']
                    response[field] = value
                    code, report, _ = self.execute(target, response)
                    self.assertEqual(code, 1)
                    self.assertEqual([f[0] for f in report['failures']], ['source-identity-mismatch'])

    def test_wrong_response_shape_is_explicit_failure(self):
        target = self.response()['html_url']
        for response in (None, [], 'not-an-object', {}, {'body': 'Exact source text.'}):
            with self.subTest(response=response):
                code, report, _ = self.execute(target, response)
                self.assertEqual(code, 1)
                self.assertEqual([f[0] for f in report['failures']], ['source-identity-mismatch'])

    def test_failed_identity_is_cached_without_becoming_success(self):
        import io
        import json
        from unittest import mock
        response = self.response(); response['id'] = 0
        with mock.patch.object(check_doc_quotes.urllib.request, 'urlopen',
                               side_effect=lambda *a, **k: io.BytesIO(json.dumps(response).encode())) as fetch:
            sources = check_doc_quotes.Sources('/unused', '/unused', True, None)
            first = sources.body(response['html_url'])
            second = sources.body(response['html_url'])
        self.assertEqual(first, (None, 'identity-mismatch'))
        self.assertEqual(second, first)
        self.assertEqual(fetch.call_count, 1)

    def test_transport_failure_and_default_offline_remain_distinct(self):
        response = self.response(); target = response['html_url']
        code, report, calls = self.execute(target, response, transport=True)
        self.assertEqual(code, 1)
        self.assertEqual([f[0] for f in report['failures']], ['source-unreachable'])
        self.assertEqual(len(calls), 1)
        for required in (False, True):
            with self.subTest(required=required):
                code, report, calls = self.execute(target, response, online=False, required=required)
                self.assertEqual(code, int(required))
                self.assertEqual(report['unchecked_offline'], 1)
                self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
