"""Source identity contracts; HTTP responses are mocked, not live fetch evidence."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'tools/check_doc_quotes.py'
spec = importlib.util.spec_from_file_location('quote_identity_subject', SOURCE)
quotes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quotes)

KINDS = ('issuecomment', 'pullrequestreview', 'discussion_r')
OWNER, REPO, PR, ID = 'example', 'research', '71', 7001
API = 'https://api.github.com/repos/' + OWNER + '/' + REPO
BODY = 'Evidence text. ACCEPT_SCOPED at fixed dimension; not global.'


def target(kind, pr=PR, ident=ID):
    return f'https://github.com/{OWNER}/{REPO}/pull/{pr}#{kind}-{ident}'


def payload(kind):
    result = {'id': ID, 'body': BODY, 'html_url': target(kind)}
    parent_key = 'issue_url' if kind == 'issuecomment' else 'pull_request_url'
    parent_type = 'issues' if kind == 'issuecomment' else 'pulls'
    result[parent_key] = f'{API}/{parent_type}/{PR}'
    # Review objects have no top-level REST `url` field; do not require one.
    if kind == 'issuecomment':
        result['url'] = f'{API}/issues/comments/{ID}'
    elif kind == 'discussion_r':
        result['url'] = f'{API}/pulls/comments/{ID}'
        result['html_url'] = target(kind).replace('discussion_r-', 'discussion_r')
    return result


class CitationIdentity(unittest.TestCase):
    def invoke(self, url, record, passage=None, extra=None):
        if passage is None:
            passage = '“Evidence text.”'
        with tempfile.TemporaryDirectory(prefix='quote-identity-') as td:
            doc = Path(td) / 'navigation.md'
            doc.write_text('| source | statement |\n|---|---|\n'
                           f'| [record]({url}) | [record]({url}) {passage} |\n', encoding='utf-8')
            output = io.StringIO()
            def response(request, timeout):
                return io.BytesIO(json.dumps(record).encode())
            with patch.object(quotes.urllib.request, 'urlopen', side_effect=response) as fetch, \
                 contextlib.redirect_stdout(output):
                rc = quotes.main([str(doc), '--root', td, '--github', '--require-online', *(extra or [])])
            report = json.loads(output.getvalue())
            return rc, report, report['documents'][str(doc)], fetch

    def test_all_three_genuine_record_shapes(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                rc, report, doc, fetch = self.invoke(target(kind), payload(kind))
                self.assertEqual(rc, 0)
                self.assertTrue(report['passed'])
                self.assertEqual((doc['checked'], doc['unchecked_offline']), (1, 0))
                self.assertEqual(doc['failures'], [])
                self.assertEqual(fetch.call_count, 1)
                req = fetch.call_args.args[0]
                suffix = f'/issues/comments/{ID}' if kind == 'issuecomment' else \
                         f'/pulls/{PR}/reviews/{ID}' if kind == 'pullrequestreview' else f'/pulls/comments/{ID}'
                self.assertEqual(req.full_url, API + suffix)

    def test_other_parent_is_rejected_even_when_body_matches(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                record = payload(kind)
                key = 'issue_url' if kind == 'issuecomment' else 'pull_request_url'
                record[key] = record[key].rsplit('/', 1)[0] + '/999'
                rc, report, doc, _ = self.invoke(target(kind), record)
                self.assertEqual(rc, 1)
                self.assertFalse(report['passed'])
                self.assertEqual([f[0] for f in doc['failures']], ['source-identity-mismatch'])
                self.assertEqual(doc['unchecked_offline'], 0)

    def test_mislinked_pr_cannot_borrow_repository_wide_comment(self):
        for kind in ('issuecomment', 'discussion_r'):
            with self.subTest(kind=kind):
                rc, _, doc, fetch = self.invoke(target(kind, pr='999'), payload(kind))
                self.assertEqual(fetch.call_count, 1)
                self.assertEqual(rc, 1)
                self.assertEqual([f[0] for f in doc['failures']], ['source-identity-mismatch'])

    def test_wrong_id_or_id_type(self):
        for kind in KINDS:
            for bad in (ID + 1, str(ID), True, None):
                with self.subTest(kind=kind, bad=bad):
                    record = payload(kind)
                    record['id'] = bad
                    rc, _, doc, _ = self.invoke(target(kind), record)
                    self.assertEqual(rc, 1)
                    self.assertEqual([f[0] for f in doc['failures']], ['source-identity-mismatch'])

    def test_html_locator_must_bind_repository_pr_kind_and_id(self):
        for kind in KINDS:
            original = payload(kind)['html_url']
            for bad in (original.replace('/research/', '/other/'),
                        original.replace('/pull/71', '/pull/999'),
                        original.replace(str(ID), str(ID + 1)),
                        original + '-extra',
                        original.replace('https://github.com/', 'https://example.invalid/')):
                with self.subTest(kind=kind, bad=bad):
                    record = payload(kind)
                    record['html_url'] = bad
                    rc, _, doc, _ = self.invoke(target(kind), record)
                    self.assertEqual(rc, 1)
                    self.assertEqual([f[0] for f in doc['failures']], ['source-identity-mismatch'])

    def test_missing_identity_fields(self):
        for kind in KINDS:
            fields = ['id', 'html_url', 'issue_url' if kind == 'issuecomment' else 'pull_request_url']
            for field in fields:
                with self.subTest(kind=kind, missing=field):
                    record = payload(kind)
                    del record[field]
                    rc, _, doc, _ = self.invoke(target(kind), record)
                    self.assertEqual(rc, 1)
                    self.assertEqual([f[0] for f in doc['failures']], ['source-identity-mismatch'])

    def test_url_suffix_does_not_get_truncated_into_a_valid_citation(self):
        for kind in KINDS:
            for suffix in ('garbage', '/extra', '?extra=1', '#second', '\n'):
                with self.subTest(kind=kind, suffix=repr(suffix)):
                    # A raw newline is not a table cell URL; exercise Sources directly instead.
                    if suffix == '\n':
                        with patch.object(quotes.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(payload(kind)).encode())):
                            _, status = quotes.Sources('/', '/', True, None).body(target(kind) + suffix)
                        self.assertNotEqual(status, 'ok')
                        continue
                    rc, report, doc, fetch = self.invoke(target(kind) + suffix, payload(kind))
                    self.assertEqual(rc, 1)
                    self.assertFalse(report['passed'])
                    self.assertEqual(fetch.call_count, 0)
                    self.assertGreater(len(doc['failures']), 0)

    def test_identity_check_applies_to_summaries_as_well_as_quotes(self):
        record = payload('issuecomment')
        record['issue_url'] = f'{API}/issues/999'
        rc, _, doc, _ = self.invoke(target('issuecomment'), record, passage='summary: ACCEPT_SCOPED')
        self.assertEqual(rc, 1)
        self.assertEqual([f[0] for f in doc['failures']], ['source-identity-mismatch'])

    def test_valid_but_false_quote_still_rejected(self):
        rc, _, doc, _ = self.invoke(target('issuecomment'), payload('issuecomment'), passage='“Different claim.”')
        self.assertEqual(rc, 1)
        self.assertEqual([f[0] for f in doc['failures']], ['not-verbatim'])

    def test_case_insensitive_repo_identity_and_canonical_anchor(self):
        for kind in KINDS:
            record = payload(kind)
            for key, value in list(record.items()):
                if isinstance(value, str) and 'example/research' in value:
                    record[key] = value.replace('example/research', 'Example/Research')
            rc, _, _, _ = self.invoke(target(kind), record)
            self.assertEqual(rc, 0)

    def test_empty_review_body_retains_legacy_summary_scope(self):
        record = payload('pullrequestreview')
        record['body'] = None
        rc, _, _, _ = self.invoke(target('pullrequestreview'), record, passage='summary: no tracked vocabulary')
        self.assertEqual(rc, 0)  # Explicitly NOT semantic-entailment validation.

    def test_offline_path_performs_no_http(self):
        with patch.object(quotes.urllib.request, 'urlopen') as fetch:
            self.assertEqual(quotes.Sources('/', '/', False, None).body(target('issuecomment')), (None, 'offline'))
            fetch.assert_not_called()


    def test_lexical_and_quotation_policies_remain_separate(self):
        record = payload('issuecomment')
        record['body'] = 'UNVERIFIED'
        rc, _, doc, _ = self.invoke(target('issuecomment'), record, passage='summary: VERIFIED')
        self.assertEqual(rc, 1)
        self.assertEqual([f[0] for f in doc['failures']], ['verdict-word-not-in-source'])
        rc, _, _, _ = self.invoke(target('issuecomment'), record, passage='“VERIFIED”')
        self.assertEqual(rc, 0)  # Retained substring excerpt policy, not whole-word quotation.
        record['body'] = 'not VERIFIED'
        rc, _, _, _ = self.invoke(target('issuecomment'), record, passage='summary: VERIFIED')
        self.assertEqual(rc, 0)  # Retained absence of negation/entailment analysis.

    def test_missing_or_nonstr_body_is_not_a_valid_source(self):
        for value in ([], 7, True):
            with self.subTest(body=value):
                record = payload('issuecomment')
                record['body'] = value
                rc, _, doc, _ = self.invoke(target('issuecomment'), record)
                self.assertEqual(rc, 1)
                self.assertEqual([f[0] for f in doc['failures']], ['source-identity-mismatch'])
        record = payload('issuecomment')
        del record['body']
        rc, _, doc, _ = self.invoke(target('issuecomment'), record, passage='summary: no tracked vocabulary')
        self.assertEqual(rc, 1)
        self.assertEqual([f[0] for f in doc['failures']], ['source-identity-mismatch'])

    def test_failed_transport_and_malformed_json_keep_failure_class(self):
        from urllib.error import HTTPError, URLError
        for error in (HTTPError('https://api.github.com/', c, 'failure', {}, None) for c in (401, 403, 404, 429, 500, 503)):
            with self.subTest(code=error.code), patch.object(quotes.urllib.request, 'urlopen', side_effect=error):
                self.assertEqual(quotes.Sources('/', '/', True, None).body(target('issuecomment')), (None, 'unreachable'))
        for error in (TimeoutError('timeout'), URLError('DNS fixture')):
            with self.subTest(error=type(error).__name__), patch.object(quotes.urllib.request, 'urlopen', side_effect=error):
                self.assertEqual(quotes.Sources('/', '/', True, None).body(target('issuecomment')), (None, 'unreachable'))
        with patch.object(quotes.urllib.request, 'urlopen', return_value=io.BytesIO(b'{invalid')):
            self.assertEqual(quotes.Sources('/', '/', True, None).body(target('issuecomment')), (None, 'unreachable'))

    def test_cached_rejection_cannot_become_success(self):
        record = payload('issuecomment')
        record['issue_url'] = f'{API}/issues/999'
        source = quotes.Sources('/', '/', True, None)
        with patch.object(quotes.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(record).encode())) as fetch:
            self.assertEqual(source.body(target('issuecomment')), (None, 'identity-mismatch'))
            self.assertEqual(source.body(target('issuecomment')), (None, 'identity-mismatch'))
            self.assertEqual(fetch.call_count, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
