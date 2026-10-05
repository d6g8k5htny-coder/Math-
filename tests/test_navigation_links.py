"""Tests for tools/check_doc_links.py: document-relative resolution, escaping paths,
commentary inside link targets, and the two navigation documents themselves."""
import os
import pathlib
import shutil
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check_doc_links  # noqa: E402

NAV_DOCS = ['PROOF_INDEX.md', 'docs/integration/2026-09-29-navigation-refresh.md']


class NavigationDocumentsResolve(unittest.TestCase):
    def test_navigation_documents_have_no_failing_links(self):
        for doc in NAV_DOCS:
            failures = check_doc_links.check_document(str(ROOT / doc), str(ROOT))
            self.assertEqual(failures, [], doc)

    def test_main_exit_status(self):
        rc = check_doc_links.main([str(ROOT / d) for d in NAV_DOCS] + ['--root', str(ROOT)])
        self.assertEqual(rc, 0)


class DocumentRelativeSemantics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='doclinks-')
        self.root = pathlib.Path(self.tmp)
        (self.root / 'reviews').mkdir()
        (self.root / 'reviews' / 'x.md').write_text('x\n')
        (self.root / 'docs' / 'nested').mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _doc(self, rel, body):
        path = self.root / rel
        path.write_text(body)
        return str(path)

    def test_root_joined_target_in_nested_document_is_rejected(self):
        # The file exists at the repository root, but the link is inside docs/nested and
        # therefore resolves to docs/nested/reviews/x.md, which does not exist.
        doc = self._doc('docs/nested/a.md', '[x](reviews/x.md)\n')
        self.assertEqual(check_doc_links.check_document(doc, self.tmp), [('missing', 'reviews/x.md')])

    def test_document_relative_target_in_nested_document_is_accepted(self):
        doc = self._doc('docs/nested/a.md', '[x](../../reviews/x.md) and [y](../../reviews/x.md#frag)\n')
        self.assertEqual(check_doc_links.check_document(doc, self.tmp), [])

    def test_root_document_root_relative_target_is_accepted(self):
        doc = self._doc('index.md', '[x](reviews/x.md)\n')
        self.assertEqual(check_doc_links.check_document(doc, self.tmp), [])

    def test_escaping_target_is_rejected(self):
        doc = self._doc('docs/nested/a.md', '[bad](../../../outside.md)\n')
        self.assertEqual(check_doc_links.check_document(doc, self.tmp), [('escapes-tree', '../../../outside.md')])

    def test_commentary_inside_url_is_rejected(self):
        doc = self._doc('index.md',
                        '[r](https://github.com/o/r/pull/1#pullrequestreview-2 (rebound at abc))\n')
        failures = check_doc_links.check_document(doc, self.tmp)
        self.assertEqual([f[0] for f in failures], ['commentary-in-url'])

    def test_commentary_inside_local_target_is_rejected(self):
        doc = self._doc('index.md', '[r](reviews/x.md (blob 0123, 5 B))\n')
        failures = check_doc_links.check_document(doc, self.tmp)
        self.assertEqual([f[0] for f in failures], ['commentary-in-target'])

    def test_anchor_only_and_bare_external_are_accepted(self):
        doc = self._doc('index.md', '[a](#section) [b](https://example.org/p?q=1#frag)\n')
        self.assertEqual(check_doc_links.check_document(doc, self.tmp), [])

    def test_missing_local_target_is_rejected(self):
        doc = self._doc('index.md', '[m](reviews/nope.md)\n')
        self.assertEqual(check_doc_links.check_document(doc, self.tmp), [('missing', 'reviews/nope.md')])

    def test_images_are_ignored(self):
        doc = self._doc('index.md', '![img](https://example.org/a b.png)\n')
        self.assertEqual(check_doc_links.check_document(doc, self.tmp), [])


if __name__ == '__main__':
    unittest.main()
