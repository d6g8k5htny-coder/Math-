"""Tests for the pure classification logic behind the Math- PR/branch disposition evidence.

Run from this directory:  python3 -m unittest test_disposition_lib -v   (and with -O)
"""
import os
import subprocess
import tempfile
import unittest

import disposition_lib as lib


def _write(path, text):
    with open(path, 'w') as fh:
        fh.write(text)


LEAN_DIFF = """diff --git a/formal/A.lean b/formal/A.lean
--- a/formal/A.lean
+++ b/formal/A.lean
@@ -1,3 +1,6 @@
 theorem old : True := trivial
-theorem gone : True := by sorry
+theorem new : 1 = 1 := by sorry
+axiom extra : False
+theorem dec : 2 + 2 = 4 := by native_decide
+theorem adm : True := by admit
"""

PY_DIFF = """diff --git a/tests/test_thing.py b/tests/test_thing.py
--- a/tests/test_thing.py
+++ b/tests/test_thing.py
@@ -1,6 +1,6 @@
 import unittest
-    def test_removed(self):
-        self.assertTrue(True)
+    @unittest.skip("later")
+    def test_kept(self):
+        self.skipTest("later")
diff --git a/tests/test_deleted.py b/tests/test_deleted.py
deleted file mode 100644
--- a/tests/test_deleted.py
+++ /dev/null
@@ -1,2 +0,0 @@
-def test_a():
-    pass
diff --git a/certificates/certify_bound.py b/certificates/certify_bound.py
--- a/certificates/certify_bound.py
+++ b/certificates/certify_bound.py
@@ -1,2 +1,3 @@
 from fractions import Fraction
+bound = float(3) / 7.0
+import math
"""

CLEAN_DIFF = """diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1 +1,2 @@
 # Title
+A sentence mentioning sorry and axiom in prose, not Lean.
"""


class LayerASignalTests(unittest.TestCase):
    def test_lean_additions_are_counted_and_removals_are_not(self):
        s = lib.layer_a_signals(LEAN_DIFF)
        self.assertEqual(s['lean_sorry_added'], 1)
        self.assertEqual(s['lean_admit_added'], 1)
        self.assertEqual(s['lean_axiom_added'], 1)
        self.assertEqual(s['lean_native_decide_added'], 1)

    def test_python_test_removal_skip_and_float_signals(self):
        s = lib.layer_a_signals(PY_DIFF)
        self.assertEqual(s['test_functions_removed'], 2)   # test_removed + test_a
        self.assertEqual(s['test_files_deleted'], 1)
        self.assertEqual(s['skips_added'], 2)              # decorator + skipTest call
        self.assertEqual(s['float_in_certificate_code_added'], 2)  # float(3)/7.0 line + import math

    def test_prose_mentions_outside_lean_are_not_signals(self):
        s = lib.layer_a_signals(CLEAN_DIFF)
        self.assertEqual(sum(s.values()), 0)

    def test_signal_keys_are_stable(self):
        self.assertEqual(sorted(lib.layer_a_signals('').keys()), sorted(lib.SIGNAL_KEYS))


class VerdictTests(unittest.TestCase):
    def comments(self):
        return [
            {'id': 1, 'created_at': '2026-10-20T10:00:00Z', 'body': 'Pickup of slice A at abc.'},
            {'id': 2, 'created_at': '2026-10-21T10:00:00Z', 'body': 'Verdict: **AMEND** one line.'},
            {'id': 3, 'created_at': '2026-10-22T10:00:00Z', 'body': 'Readback **PASS_SCOPED**, no findings.'},
        ]

    def test_latest_verdict_wins(self):
        v = lib.latest_verdict(self.comments())
        self.assertEqual(v, {'verdict': 'PASS_SCOPED', 'comment_id': 3, 'created_at': '2026-10-22T10:00:00Z'})

    def test_no_verdict_returns_none(self):
        self.assertIsNone(lib.latest_verdict([{'id': 9, 'created_at': 'x', 'body': 'hello'}]))

    def test_do_not_merge_is_a_verdict(self):
        v = lib.latest_verdict([{'id': 4, 'created_at': 'y', 'body': 'Draft, do not merge.'}])
        self.assertEqual(v['verdict'], 'DO_NOT_MERGE')

    def test_order_is_by_created_at_not_list_position(self):
        c = list(reversed(self.comments()))
        self.assertEqual(lib.latest_verdict(c)['comment_id'], 3)


def facts(**over):
    base = {
        'head_is_ancestor_of_main': False,
        'all_changed_blobs_equal_on_main': False,
        'base_is_main': True,
        'updated_within_24h': False,
        'explicit_do_not_merge': False,
        'merge_tree_clean_onto_main': True,
        'latest_verdict': 'PASS_SCOPED',
        'required_check_conclusion': 'success',
    }
    base.update(over)
    return base


class RecommendationTests(unittest.TestCase):
    def test_ancestor_of_main_is_superseded(self):
        self.assertEqual(lib.recommend(facts(head_is_ancestor_of_main=True)), 'SUPERSEDED')

    def test_blob_equality_is_superseded(self):
        self.assertEqual(lib.recommend(facts(all_changed_blobs_equal_on_main=True)), 'SUPERSEDED')

    def test_stacked_pr_is_stack_dependent(self):
        self.assertEqual(lib.recommend(facts(base_is_main=False)), 'STACK-DEPENDENT')

    def test_recent_activity_is_left_to_its_lane(self):
        self.assertEqual(lib.recommend(facts(updated_within_24h=True)), 'ACTIVE-OWNER-LANE')

    def test_explicit_do_not_merge_is_quarantine(self):
        self.assertEqual(lib.recommend(facts(explicit_do_not_merge=True)), 'QUARANTINE-ARCHIVE')

    def test_clean_green_pass_is_integrate_candidate(self):
        self.assertEqual(lib.recommend(facts()), 'INTEGRATE-CANDIDATE')

    def test_conflict_or_red_or_no_pass_is_quarantine(self):
        self.assertEqual(lib.recommend(facts(merge_tree_clean_onto_main=False)), 'QUARANTINE-ARCHIVE')
        self.assertEqual(lib.recommend(facts(required_check_conclusion='failure')), 'QUARANTINE-ARCHIVE')
        self.assertEqual(lib.recommend(facts(latest_verdict='AMEND')), 'QUARANTINE-ARCHIVE')
        self.assertEqual(lib.recommend(facts(latest_verdict=None)), 'QUARANTINE-ARCHIVE')

    def test_precedence_superseded_beats_everything(self):
        self.assertEqual(lib.recommend(facts(head_is_ancestor_of_main=True, base_is_main=False,
                                             updated_within_24h=True)), 'SUPERSEDED')


def bfacts(**over):
    base = {
        'contained_in_open_pr_head': False,
        'all_changed_blobs_equal_on_main': False,
        'updated_within_24h': False,
        'merge_tree_clean_onto_main': True,
        'signals_total': 0,
        'changed_path_count': 5,
        'days_since_last_commit': 3,
    }
    base.update(over)
    return base


class BranchRecommendationTests(unittest.TestCase):
    def test_tip_inside_an_open_pr_rides_that_pr(self):
        self.assertEqual(lib.recommend_branch(bfacts(contained_in_open_pr_head=True)), 'SUPERSEDED-BY-OPEN-PR')

    def test_content_already_on_main_is_superseded(self):
        self.assertEqual(lib.recommend_branch(bfacts(all_changed_blobs_equal_on_main=True)), 'SUPERSEDED-CONTENT-ON-MAIN')

    def test_recent_activity_is_left_to_its_lane(self):
        self.assertEqual(lib.recommend_branch(bfacts(updated_within_24h=True)), 'ACTIVE-LANE')

    def test_small_clean_quiet_recent_branch_is_integrate_review(self):
        self.assertEqual(lib.recommend_branch(bfacts()), 'INTEGRATE-REVIEW')

    def test_integrable_if_wanted_flag_ignores_age_only(self):
        self.assertTrue(lib.integrable_if_wanted(bfacts(days_since_last_commit=40)))
        self.assertFalse(lib.integrable_if_wanted(bfacts(signals_total=2)))
        self.assertFalse(lib.integrable_if_wanted(bfacts(merge_tree_clean_onto_main=False)))
        self.assertFalse(lib.integrable_if_wanted(bfacts(changed_path_count=51)))
        self.assertFalse(lib.integrable_if_wanted(bfacts(unrelated_history=True)))

    def test_otherwise_archive_bundle(self):
        self.assertEqual(lib.recommend_branch(bfacts(signals_total=1)), 'ARCHIVE-BUNDLE')
        self.assertEqual(lib.recommend_branch(bfacts(merge_tree_clean_onto_main=False)), 'ARCHIVE-BUNDLE')
        self.assertEqual(lib.recommend_branch(bfacts(changed_path_count=51)), 'ARCHIVE-BUNDLE')
        self.assertEqual(lib.recommend_branch(bfacts(days_since_last_commit=15)), 'ARCHIVE-BUNDLE')


class BranchClassTests(unittest.TestCase):
    def test_classes(self):
        self.assertEqual(lib.classify_branch(True, False, False), 'MERGED_NO_PR_PRUNE_ELIGIBLE')
        self.assertEqual(lib.classify_branch(False, False, False), 'UNMERGED_NO_PR')
        self.assertEqual(lib.classify_branch(True, True, False), 'OPEN_PR_REF')
        self.assertEqual(lib.classify_branch(False, True, False), 'OPEN_PR_REF')
        self.assertEqual(lib.classify_branch(True, False, True), 'PROTECTED')


class GitHelperTests(unittest.TestCase):
    """Real git, tiny repository: ancestry, blob equality and merge-tree cleanliness."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        env = {'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@x', 'GIT_COMMITTER_NAME': 't',
               'GIT_COMMITTER_EMAIL': 't@x', 'PATH': os.environ['PATH']}
        self.env = env

        def git(*a):
            return subprocess.run(['git', '-C', self.repo, *a], check=True, capture_output=True,
                                  text=True, env=env).stdout.strip()
        self.git = git
        git('init', '-q', '-b', 'main')
        _write(os.path.join(self.repo, 'a.txt'), 'one\n')
        git('add', 'a.txt'); git('commit', '-q', '-m', 'c1')
        git('checkout', '-q', '-b', 'merged')
        _write(os.path.join(self.repo, 'b.txt'), 'two\n')
        git('add', 'b.txt'); git('commit', '-q', '-m', 'c2')
        git('checkout', '-q', 'main'); git('merge', '-q', '--no-ff', '-m', 'm', 'merged')
        git('checkout', '-q', '-b', 'samebytes', 'HEAD~1')
        _write(os.path.join(self.repo, 'b.txt'), 'two\n')
        git('add', 'b.txt'); git('commit', '-q', '-m', 'c2-again')
        git('checkout', '-q', '-b', 'conflict', 'main~1')
        _write(os.path.join(self.repo, 'b.txt'), 'other\n')
        git('add', 'b.txt'); git('commit', '-q', '-m', 'c3')
        git('checkout', '-q', 'main')

    def tearDown(self):
        self.tmp.cleanup()

    def test_is_ancestor(self):
        self.assertTrue(lib.is_ancestor(self.repo, 'merged', 'main'))
        self.assertFalse(lib.is_ancestor(self.repo, 'samebytes', 'main'))

    def test_blob_equality_against_main(self):
        self.assertTrue(lib.all_changed_blobs_equal(self.repo, 'samebytes', 'main'))
        self.assertFalse(lib.all_changed_blobs_equal(self.repo, 'conflict', 'main'))

    def test_merge_tree_cleanliness(self):
        self.assertTrue(lib.merge_tree_clean(self.repo, 'main', 'samebytes'))
        self.assertFalse(lib.merge_tree_clean(self.repo, 'main', 'conflict'))


class RenderTests(unittest.TestCase):
    def test_markdown_table_has_one_row_per_pr_and_escapes_pipes(self):
        rows = [{'number': 1, 'title': 'a | b', 'draft': True, 'head_ref': 'h', 'head_sha': 'a' * 40,
                 'base_ref': 'main', 'recommended_disposition': 'SUPERSEDED', 'latest_verdict': None,
                 'required_check_conclusion': None, 'updated_at': '2026-10-01T00:00:00Z',
                 'signals_total': 0, 'merge_tree_clean_onto_main': True}]
        md = lib.render_pr_table(rows)
        self.assertEqual(md.count('\n| #1 '), 1)
        self.assertIn('a \\| b', md)


if __name__ == '__main__':
    unittest.main()
