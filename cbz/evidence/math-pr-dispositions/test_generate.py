"""Tests for the record builders in generate.py, run against a tiny real git repository with
pre-fetched GitHub data supplied as plain dicts (no network)."""
import os
import subprocess
import tempfile
import unittest

import generate


def _write(path, text):
    with open(path, 'w') as fh:
        fh.write(text)


class BuildRecordTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        env = {'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@x', 'GIT_COMMITTER_NAME': 't',
               'GIT_COMMITTER_EMAIL': 't@x', 'PATH': os.environ['PATH']}

        def git(*a):
            return subprocess.run(['git', '-C', self.repo, *a], check=True, capture_output=True,
                                  text=True, env=env).stdout.strip()
        self.git = git
        git('init', '-q', '-b', 'main')
        _write(os.path.join(self.repo, 'a.txt'), 'one\n')
        git('add', 'a.txt'); git('commit', '-q', '-m', 'c1')
        git('checkout', '-q', '-b', 'feature')
        os.makedirs(os.path.join(self.repo, 'formal'))
        _write(os.path.join(self.repo, 'formal', 'X.lean'), 'theorem t : True := by sorry\n')
        git('add', 'formal'); git('commit', '-q', '-m', 'c2')
        git('checkout', '-q', 'main')
        # the generator reads refs as refs/remotes/origin/<name>; mirror them locally
        git('update-ref', 'refs/remotes/origin/main', 'main')
        git('update-ref', 'refs/remotes/origin/feature', 'feature')
        self.head = git('rev-parse', 'feature')
        self.main = git('rev-parse', 'main')

    def tearDown(self):
        self.tmp.cleanup()

    def pr(self):
        return {'number': 7, 'title': 'Feature', 'draft': True, 'updated_at': '2026-10-01T00:00:00Z',
                'created_at': '2026-09-30T00:00:00Z', 'body': 'body text',
                'head': {'ref': 'feature', 'sha': self.head}, 'base': {'ref': 'main', 'sha': self.main},
                'html_url': 'https://example/pr/7'}

    def test_record_carries_facts_signals_and_recommendation(self):
        rec = generate.build_pr_record(
            self.repo, self.pr(), main_sha=self.main,
            comments=[{'id': 1, 'created_at': '2026-10-01T01:00:00Z', 'body': 'Read: **AMEND** x'}],
            reviews=[{'state': 'COMMENTED', 'commit_id': self.head, 'submitted_at': '2026-10-01T02:00:00Z'}],
            check_runs=[{'name': 'math-downstream-gates', 'status': 'completed', 'conclusion': 'failure'}],
            now='2026-10-29T17:00:00Z', open_pr_heads={'feature'})
        self.assertEqual(rec['number'], 7)
        self.assertFalse(rec['head_is_ancestor_of_main'])
        self.assertFalse(rec['all_changed_blobs_equal_on_main'])
        self.assertTrue(rec['base_is_main'])
        self.assertTrue(rec['merge_tree_clean_onto_main'])
        self.assertEqual(rec['changed_paths'], ['formal/X.lean'])
        self.assertEqual(rec['layer_a_signals']['lean_sorry_added'], 1)
        self.assertEqual(rec['signals_total'], 1)
        self.assertEqual(rec['latest_verdict'], 'AMEND')
        self.assertEqual(rec['required_check_conclusion'], 'failure')
        self.assertFalse(rec['updated_within_24h'])
        self.assertEqual(rec['recommended_disposition'], 'QUARANTINE-ARCHIVE')
        self.assertEqual(rec['recoverable_ref_command'], f'git push origin {self.head}:refs/heads/feature')

    def test_do_not_merge_into_another_branch_is_not_a_pr_hold(self):
        pr = self.pr(); pr['body'] = "Do not merge into or modify #362's owner branch."
        rec = generate.build_pr_record(self.repo, pr, main_sha=self.main, comments=[], reviews=[],
                                       check_runs=[], now='2026-10-29T17:00:00Z', open_pr_heads={'feature'})
        self.assertFalse(rec['explicit_do_not_merge'])

    def test_do_not_merge_in_title_is_a_pr_hold(self):
        pr = self.pr(); pr['title'] = 'Draft: thing (do not merge)'
        rec = generate.build_pr_record(self.repo, pr, main_sha=self.main, comments=[], reviews=[],
                                       check_runs=[], now='2026-10-29T17:00:00Z', open_pr_heads={'feature'})
        self.assertTrue(rec['explicit_do_not_merge'])

    def test_changed_paths_are_capped_but_bound_by_hash(self):
        import hashlib
        rec = generate.build_pr_record(self.repo, self.pr(), main_sha=self.main, comments=[], reviews=[],
                                       check_runs=[], now='2026-10-29T17:00:00Z', open_pr_heads={'feature'},
                                       path_cap=0)
        self.assertEqual(rec['changed_paths'], [])
        self.assertEqual(rec['changed_path_count'], 1)
        self.assertEqual(rec['changed_paths_sha256'], hashlib.sha256(b'formal/X.lean\n').hexdigest())

    def test_updated_within_24h_uses_the_supplied_clock(self):
        pr = self.pr(); pr['updated_at'] = '2026-10-29T10:00:00Z'
        rec = generate.build_pr_record(self.repo, pr, main_sha=self.main, comments=[], reviews=[],
                                       check_runs=[], now='2026-10-29T17:00:00Z', open_pr_heads={'feature'})
        self.assertTrue(rec['updated_within_24h'])
        self.assertEqual(rec['recommended_disposition'], 'ACTIVE-OWNER-LANE')

    def test_branch_records_classify_merged_unmerged_and_pr_refs(self):
        self.git('checkout', '-q', '-b', 'done'); self.git('checkout', '-q', 'main')
        self.git('update-ref', 'refs/remotes/origin/done', 'done')
        recs = generate.build_branch_records(self.repo, main_sha=self.main,
                                             open_pr_refs={'feature'}, protected=set())
        by = {r['branch']: r for r in recs}
        self.assertEqual(by['done']['class'], 'MERGED_NO_PR_PRUNE_ELIGIBLE')
        self.assertEqual(by['feature']['class'], 'OPEN_PR_REF')
        self.assertEqual(by['main']['class'], 'PROTECTED')
        self.assertEqual(by['done']['tip'], self.main)
        self.assertIn('last_commit_date', by['done'])
        self.assertEqual(by['feature']['commits_ahead_of_main'], 1)
        self.assertEqual(by['done']['commits_ahead_of_main'], 0)


if __name__ == '__main__':
    unittest.main()
