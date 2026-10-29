"""Pure classification logic for CBZ-0 Phase 2 disposition evidence on Math- pull requests and branches.

Everything here is *evidence*, not certification:
- ``layer_a_signals`` is a lexical scan of a unified diff. A hit means "a reader must look", a miss
  means nothing. It never establishes Layer A compliance.
- ``recommend`` is a decision table over observed facts; the integrator decides.

Standard library only. Tested by ``test_disposition_lib.py``.
"""
from __future__ import annotations

import re
import subprocess

SIGNAL_KEYS = (
    'lean_sorry_added', 'lean_admit_added', 'lean_axiom_added', 'lean_native_decide_added',
    'test_functions_removed', 'test_files_deleted', 'skips_added', 'float_in_certificate_code_added',
)

_VERDICT_PATTERNS = (
    ('DO_NOT_MERGE', re.compile(r'\bdo not merge\b', re.I)),
    ('PASS_SCOPED', re.compile(r'\bPASS_SCOPED\w*')),
    ('PASS', re.compile(r'(?<![A-Z_])PASS(?![A-Z_])')),
    ('AMEND', re.compile(r'(?<![A-Z_])AMEND\w*')),
    ('BLOCK', re.compile(r'(?<![A-Z_])BLOCK\w*')),
    ('HOLD', re.compile(r'(?<![A-Z_])HOLD\w*')),
    ('REJECTED', re.compile(r'(?<![A-Z_])REJECTED\b')),
)
_VERDICT_PRIORITY = ('DO_NOT_MERGE', 'BLOCK', 'REJECTED', 'HOLD', 'AMEND', 'PASS_SCOPED', 'PASS')

_CERT_PATH = re.compile(r'(certif|certify|gate|check|verify|enclos|bound)', re.I)
_TEST_PATH = re.compile(r'(^|/)(tests?/|test_[^/]*\.py$)')


def layer_a_signals(diff_text: str) -> dict:
    """Count lexical Layer A signals in a unified diff (added lines only, except test removals)."""
    counts = {k: 0 for k in SIGNAL_KEYS}
    path = ''
    deleted_file = False
    for line in diff_text.splitlines():
        if line.startswith('diff --git '):
            # "diff --git a/x b/x" -> x
            path = line.split(' b/', 1)[1] if ' b/' in line else ''
            deleted_file = False
            continue
        if line.startswith('deleted file mode'):
            deleted_file = True
            if _TEST_PATH.search(path):
                counts['test_files_deleted'] += 1
            continue
        if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
            continue
        is_lean = path.endswith('.lean')
        is_test = bool(_TEST_PATH.search(path))
        if line.startswith('+'):
            body = line[1:]
            if is_lean:
                if re.search(r'\bsorry\b', body):
                    counts['lean_sorry_added'] += 1
                if re.search(r'\badmit\b', body):
                    counts['lean_admit_added'] += 1
                if re.match(r'\s*(noncomputable\s+)?axiom\b', body):
                    counts['lean_axiom_added'] += 1
                if 'native_decide' in body:
                    counts['lean_native_decide_added'] += 1
            if is_test and re.search(r'(@unittest\.skip|\.skipTest\(|pytest\.skip|pytest\.mark\.skip)', body):
                counts['skips_added'] += 1
            if path.endswith('.py') and not is_test and _CERT_PATH.search(path):
                if re.search(r'\bfloat\(|\b\d+\.\d+\b|\bimport math\b|\bnumpy\b', body):
                    counts['float_in_certificate_code_added'] += 1
        elif line.startswith('-'):
            body = line[1:]
            if is_test and re.match(r'\s*def test_', body):
                counts['test_functions_removed'] += 1
    return counts


def latest_verdict(comments) -> dict | None:
    """Latest comment (by created_at) that carries a verdict token; None when none does."""
    best = None
    for c in comments:
        body = c.get('body') or ''
        found = [name for name, pat in _VERDICT_PATTERNS if pat.search(body)]
        if not found:
            continue
        verdict = next(v for v in _VERDICT_PRIORITY if v in found)
        key = c.get('created_at') or ''
        if best is None or key > best['created_at']:
            best = {'verdict': verdict, 'comment_id': c.get('id'), 'created_at': key}
    return best


def recommend(f: dict) -> str:
    """Decision table. Order matters; the first matching row wins."""
    if f.get('head_is_ancestor_of_main') or f.get('all_changed_blobs_equal_on_main'):
        return 'SUPERSEDED'
    if not f.get('base_is_main', True):
        return 'STACK-DEPENDENT'
    if f.get('updated_within_24h'):
        return 'ACTIVE-OWNER-LANE'
    if f.get('explicit_do_not_merge'):
        return 'QUARANTINE-ARCHIVE'
    if (f.get('merge_tree_clean_onto_main') and f.get('required_check_conclusion') == 'success'
            and f.get('latest_verdict') in ('PASS', 'PASS_SCOPED')):
        return 'INTEGRATE-CANDIDATE'
    return 'QUARANTINE-ARCHIVE'


def integrable_if_wanted(f: dict) -> bool:
    """Clean merge-tree, zero lexical signals, at most 50 changed paths, related history: a lane could
    still open a PR for it. Age is deliberately ignored here (ARCHIVE-BUNDLE rows carry this flag)."""
    return bool(f.get('merge_tree_clean_onto_main') and f.get('signals_total', 0) == 0
                and f.get('changed_path_count', 0) <= 50 and not f.get('unrelated_history'))


def recommend_branch(f: dict) -> str:
    """Decision table for an unmerged branch with no pull request. First matching row wins.
    Thresholds (documented in README): INTEGRATE-REVIEW needs a clean merge-tree, zero lexical signals,
    at most 50 changed paths and a last commit within 14 days of observation."""
    if f.get('contained_in_open_pr_head'):
        return 'SUPERSEDED-BY-OPEN-PR'
    if f.get('unrelated_history'):
        return 'ARCHIVE-BUNDLE'
    if f.get('all_changed_blobs_equal_on_main'):
        return 'SUPERSEDED-CONTENT-ON-MAIN'
    if f.get('updated_within_24h'):
        return 'ACTIVE-LANE'
    if (f.get('merge_tree_clean_onto_main') and f.get('signals_total', 0) == 0
            and f.get('changed_path_count', 0) <= 50 and f.get('days_since_last_commit', 999) <= 14):
        return 'INTEGRATE-REVIEW'
    return 'ARCHIVE-BUNDLE'


def classify_branch(tip_is_ancestor_of_main: bool, is_open_pr_ref: bool, protected: bool) -> str:
    if protected:
        return 'PROTECTED'
    if is_open_pr_ref:
        return 'OPEN_PR_REF'
    return 'MERGED_NO_PR_PRUNE_ELIGIBLE' if tip_is_ancestor_of_main else 'UNMERGED_NO_PR'


# --- git helpers (real git, read-only) -------------------------------------------------------

def _git(repo: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, check=check)


def is_ancestor(repo: str, maybe_ancestor: str, descendant: str) -> bool:
    return _git(repo, 'merge-base', '--is-ancestor', maybe_ancestor, descendant, check=False).returncode == 0


def all_changed_blobs_equal(repo: str, head: str, main: str) -> bool:
    """True iff every path changed by head (since merge-base) has, on main, the same blob as on head."""
    base = _git(repo, 'merge-base', head, main).stdout.strip()
    paths = [p for p in _git(repo, 'diff', '--name-only', base, head).stdout.splitlines() if p]
    if not paths:
        return True
    for p in paths:
        h = _git(repo, 'rev-parse', '-q', '--verify', f'{head}:{p}', check=False)
        m = _git(repo, 'rev-parse', '-q', '--verify', f'{main}:{p}', check=False)
        if h.returncode != m.returncode or h.stdout.strip() != m.stdout.strip():
            return False
    return True


def merge_tree_clean(repo: str, base: str, head: str) -> bool:
    r = _git(repo, 'merge-tree', '--write-tree', base, head, check=False)
    return r.returncode == 0


def render_pr_table(rows) -> str:
    def esc(x):
        return str(x).replace('|', '\\|')
    out = ['| PR | Draft | Head | Base | Updated | Latest verdict | Required check | merge-tree→main | Layer A signals | Recommended |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        out.append('| #{n} {t} | {d} | `{h}`@`{s}` | `{b}` | {u} | {v} | {c} | {m} | {g} | **{rec}** |'.format(
            n=r['number'], t=esc(r['title']), d='yes' if r['draft'] else 'no', h=esc(r['head_ref']),
            s=r['head_sha'][:8], b=esc(r['base_ref']), u=r['updated_at'][:10],
            v=esc(r.get('latest_verdict') or '—'), c=esc(r.get('required_check_conclusion') or '—'),
            m='clean' if r.get('merge_tree_clean_onto_main') else 'CONFLICT', g=r.get('signals_total', 0),
            rec=r['recommended_disposition']))
    return '\n'.join(out) + '\n'
