#!/usr/bin/env python3
"""Generate CBZ-0 Phase 2 disposition evidence for every open Math- pull request and every branch.

Read-only. Standard library + git + the ``gh`` CLI (REST only). It closes, merges, deletes nothing.

Usage (from a Math- clone whose ``refs/remotes/origin/*`` are freshly fetched with ``--prune``):

    python3 generate.py --repo /path/to/Math- --out . [--owner-repo d6g8k5htny-coder/Math-]
    python3 generate.py --repo R --out . --offline data/   # replay from previously fetched JSON

Outputs in ``--out``: ``dispositions.json``, ``DISPOSITIONS.md``, ``branches.json``, ``BRANCHES.md``,
and ``fetched/`` (the raw GitHub responses the records were computed from, for replay).

Record builders (``build_pr_record``, ``build_branch_records``) are pure given their inputs and are
exercised by ``test_generate.py`` against a tiny real repository.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import disposition_lib as lib  # noqa: E402

REQUIRED_CHECK = 'math-downstream-gates'


def _git(repo, *args, check=True):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, check=check).stdout


def _dump(obj, path):
    with open(path, 'w') as fh:
        json.dump(obj, fh, indent=1)


def _load(path):
    with open(path) as fh:
        return json.load(fh)


def _parse(ts: str) -> dt.datetime:
    return dt.datetime.fromisoformat(ts.replace('Z', '+00:00'))


_DNM_RE = re.compile(r'\b(do[- ]not[- ]merge|not for merge)\b(?!\s+(into|to|onto)\b)', re.I)


def _explicit_do_not_merge(title: str, body: str) -> bool:
    """A hold on *this* PR: the phrase in the title, or in the body when it is not aimed at another branch
    ("do not merge into X" is a scope note, not a hold)."""
    return bool(_DNM_RE.search(title or '')) or bool(_DNM_RE.search(body or ''))


def build_pr_record(repo, pr, *, main_sha, comments, reviews, check_runs, now, open_pr_heads, path_cap=200):
    head = pr['head']['sha']
    head_ref = pr['head']['ref']
    base_ref = pr['base']['ref']
    base_is_main = base_ref == 'main'
    base_rev = main_sha if base_is_main else f'refs/remotes/origin/{base_ref}'
    merge_base = _git(repo, 'merge-base', head, main_sha).strip()
    changed = [p for p in _git(repo, 'diff', '--name-only', merge_base, head).splitlines() if p]
    diff_text = _git(repo, 'diff', merge_base, head, '--', *changed) if changed else ''
    signals = lib.layer_a_signals(diff_text)
    verdict = lib.latest_verdict(comments)
    req = [c for c in check_runs if c.get('name') == REQUIRED_CHECK]
    req_conclusion = None
    if req:
        latest = sorted(req, key=lambda c: c.get('completed_at') or c.get('started_at') or '')[-1]
        req_conclusion = latest.get('conclusion') if latest.get('status') == 'completed' else latest.get('status')
    explicit_dnm = _explicit_do_not_merge(pr.get('title', ''), pr.get('body') or '')
    updated_within = (_parse(now) - _parse(pr['updated_at'])) <= dt.timedelta(hours=24)
    facts = {
        'head_is_ancestor_of_main': lib.is_ancestor(repo, head, main_sha),
        'all_changed_blobs_equal_on_main': lib.all_changed_blobs_equal(repo, head, main_sha),
        'base_is_main': base_is_main,
        'updated_within_24h': updated_within,
        'explicit_do_not_merge': explicit_dnm,
        'merge_tree_clean_onto_main': lib.merge_tree_clean(repo, main_sha, head),
        'latest_verdict': verdict['verdict'] if verdict else None,
        'required_check_conclusion': req_conclusion,
    }
    rec = {
        'number': pr['number'], 'title': pr['title'], 'draft': bool(pr.get('draft')),
        'url': pr.get('html_url'), 'created_at': pr.get('created_at'), 'updated_at': pr['updated_at'],
        'head_ref': head_ref, 'head_sha': head, 'base_ref': base_ref, 'base_sha': pr['base']['sha'],
        'base_has_open_pr': (not base_is_main) and base_ref in open_pr_heads,
        'merge_base_with_main': merge_base,
        'merge_tree_clean_onto_base': lib.merge_tree_clean(repo, base_rev, head) if not base_is_main else None,
        'commits_ahead_of_main': int(_git(repo, 'rev-list', '--count', f'{main_sha}..{head}').strip()),
        'commits_behind_main': int(_git(repo, 'rev-list', '--count', f'{head}..{main_sha}').strip()),
        'changed_paths': changed[:path_cap],
        'changed_path_count': len(changed),
        'changed_paths_sha256': hashlib.sha256(''.join(p + '\n' for p in sorted(changed)).encode()).hexdigest(),
        'layer_a_signals': signals,
        'signals_total': sum(signals.values()),
        'latest_verdict_comment': verdict,
        'review_states': [{'state': r.get('state'), 'commit': (r.get('commit_id') or '')[:8],
                           'submitted_at': r.get('submitted_at')} for r in reviews],
        'check_runs': {c['name']: (c.get('conclusion') if c.get('status') == 'completed' else c.get('status'))
                       for c in check_runs},
        'recoverable_ref_command': f'git push origin {head}:refs/heads/{head_ref}',
    }
    rec.update(facts)
    rec['recommended_disposition'] = lib.recommend(facts)
    return rec


def build_branch_records(repo, *, main_sha, open_pr_refs, protected):
    out = []
    lines = _git(repo, 'for-each-ref', '--format=%(refname:short)%09%(objectname)%09%(committerdate:iso-strict)',
                 'refs/remotes/origin/').splitlines()
    for line in lines:
        ref, tip, date = line.split('\t')
        name = ref.split('/', 1)[1] if ref.startswith('origin/') else ref
        if name == 'HEAD':
            continue
        is_prot = name in protected or name == 'main'
        rec = {
            'branch': name, 'tip': tip, 'last_commit_date': date,
            'tip_is_ancestor_of_main': lib.is_ancestor(repo, tip, main_sha),
            'is_open_pr_ref': name in open_pr_refs,
            'commits_ahead_of_main': int(_git(repo, 'rev-list', '--count', f'{main_sha}..{tip}').strip()),
            'protected': is_prot,
            'recreate_command': f'git push origin {tip}:refs/heads/{name}',
        }
        rec['class'] = lib.classify_branch(rec['tip_is_ancestor_of_main'], rec['is_open_pr_ref'], is_prot)
        out.append(rec)
    return sorted(out, key=lambda r: (r['class'], r['branch']))


# --- GitHub fetching (REST via gh) ----------------------------------------------------------

def gh_json(endpoint):
    items = []
    for page in range(1, 60):
        sep = '&' if '?' in endpoint else '?'
        r = subprocess.run(['gh', 'api', f'{endpoint}{sep}per_page=100&page={page}'], capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip()[:400])
        chunk = json.loads(r.stdout)
        if isinstance(chunk, dict):
            chunk = chunk.get('check_runs') or chunk.get('items') or []
        items.extend(chunk)
        if len(chunk) < 100:
            break
    return items


def write_fetched_manifest(fetched_dir, out_path):
    """Bind the raw GitHub responses by SHA-256 without committing their bodies."""
    rows = []
    for name in sorted(os.listdir(fetched_dir)):
        p = os.path.join(fetched_dir, name)
        if not name.endswith('.json'):
            continue
        with open(p, 'rb') as fh:
            data = fh.read()
        rows.append({'file': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    _dump({'fetched_dir': os.path.basename(fetched_dir), 'files': rows}, out_path)
    return rows


def fetch_all(owner_repo, fetched_dir):
    os.makedirs(fetched_dir, exist_ok=True)
    prs = gh_json(f'repos/{owner_repo}/pulls?state=open')
    _dump(prs, os.path.join(fetched_dir, 'pulls.json'))
    data = {}
    for pr in prs:
        n = pr['number']
        d = {
            'comments': gh_json(f'repos/{owner_repo}/issues/{n}/comments'),
            'reviews': gh_json(f'repos/{owner_repo}/pulls/{n}/reviews'),
            'check_runs': gh_json(f"repos/{owner_repo}/commits/{pr['head']['sha']}/check-runs"),
        }
        _dump(d, os.path.join(fetched_dir, f'pr{n}.json'))
        data[n] = d
    return prs, data


def load_offline(fetched_dir):
    prs = _load(os.path.join(fetched_dir, 'pulls.json'))
    data = {pr['number']: _load(os.path.join(fetched_dir, f"pr{pr['number']}.json")) for pr in prs}
    return prs, data


def render_branch_table(records):
    out = ['| Class | Branch | Tip | Last commit | Ahead of main | Recreate |', '|---|---|---|---|---|---|']
    for r in records:
        out.append(f"| {r['class']} | `{r['branch']}` | `{r['tip']}` | {r['last_commit_date'][:10]} | {r['commits_ahead_of_main']} | `{r['recreate_command']}` |")
    return '\n'.join(out) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--owner-repo', default='d6g8k5htny-coder/Math-')
    ap.add_argument('--offline', help='directory with previously fetched JSON (replay, no network)')
    ap.add_argument('--protected', default='main', help='comma-separated protected branch names')
    a = ap.parse_args(argv)

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    main_sha = _git(a.repo, 'rev-parse', 'refs/remotes/origin/main').strip()
    fetched_dir = a.offline or os.path.join(a.out, 'fetched')
    prs, data = load_offline(fetched_dir) if a.offline else fetch_all(a.owner_repo, fetched_dir)
    open_heads = {pr['head']['ref'] for pr in prs}
    open_refs = open_heads | {pr['base']['ref'] for pr in prs}
    protected = set(a.protected.split(',')) if a.protected else set()

    pr_records = [build_pr_record(a.repo, pr, main_sha=main_sha, comments=data[pr['number']]['comments'],
                                  reviews=data[pr['number']]['reviews'], check_runs=data[pr['number']]['check_runs'],
                                  now=now, open_pr_heads=open_heads) for pr in sorted(prs, key=lambda p: p['number'])]
    branch_records = build_branch_records(a.repo, main_sha=main_sha, open_pr_refs=open_refs, protected=protected)

    meta = {'observed_at_utc': now, 'repository': a.owner_repo, 'main_sha': main_sha,
            'open_pr_count': len(pr_records), 'branch_count': len(branch_records),
            'disposition_counts': {}, 'branch_class_counts': {}, 'note': (
                'Evidence only. layer_a_signals are lexical hits on added/removed diff lines, never certification. '
                'recommended_disposition is a decision table over observed facts; the integrator decides.')}
    for r in pr_records:
        meta['disposition_counts'][r['recommended_disposition']] = meta['disposition_counts'].get(r['recommended_disposition'], 0) + 1
    for r in branch_records:
        meta['branch_class_counts'][r['class']] = meta['branch_class_counts'].get(r['class'], 0) + 1

    os.makedirs(a.out, exist_ok=True)
    meta['fetched_manifest'] = 'FETCHED_MANIFEST.json'
    write_fetched_manifest(fetched_dir, os.path.join(a.out, 'FETCHED_MANIFEST.json'))
    _dump({'meta': meta, 'pull_requests': pr_records}, os.path.join(a.out, 'dispositions.json'))
    _dump({'meta': meta, 'branches': branch_records}, os.path.join(a.out, 'branches.json'))
    with open(os.path.join(a.out, 'DISPOSITIONS.md'), 'w') as f:
        f.write(f"# Math- open pull requests — CBZ-0 Phase 2 disposition evidence\n\n"
                f"Observed {now} at `{a.owner_repo}` `main` `{main_sha}`. {len(pr_records)} open PRs. "
                f"Counts: {json.dumps(meta['disposition_counts'])}.\n\n{meta['note']}\n\n")
        f.write(lib.render_pr_table(pr_records))
        f.write('\n## Per-PR facts\n\n')
        for r in pr_records:
            f.write(f"### #{r['number']} {r['title']}\n\n")
            f.write(f"- head `{r['head_ref']}` `{r['head_sha']}`; base `{r['base_ref']}` `{r['base_sha']}`"
                    f"{' (base has an open PR)' if r['base_has_open_pr'] else ''}; ahead {r['commits_ahead_of_main']} / behind {r['commits_behind_main']} of main\n")
            f.write(f"- ancestor of main: {r['head_is_ancestor_of_main']}; all changed blobs already on main: {r['all_changed_blobs_equal_on_main']}; "
                    f"merge-tree onto main: {'clean' if r['merge_tree_clean_onto_main'] else 'CONFLICT'}"
                    + (f"; onto base: {'clean' if r['merge_tree_clean_onto_base'] else 'CONFLICT'}" if r['merge_tree_clean_onto_base'] is not None else '') + '\n')
            f.write(f"- changed paths: {r['changed_path_count']}; Layer A signals: {json.dumps({k: v for k, v in r['layer_a_signals'].items() if v})}\n")
            v = r['latest_verdict_comment']
            f.write(f"- latest verdict token: {r['latest_verdict'] or '—'}" + (f" (comment {v['comment_id']}, {v['created_at']})" if v else '') + '\n')
            f.write(f"- checks at head: {json.dumps(r['check_runs'])}\n")
            f.write(f"- explicit do-not-merge in title/body: {r['explicit_do_not_merge']}; updated within 24 h of observation: {r['updated_within_24h']}\n")
            f.write(f"- **recommended: {r['recommended_disposition']}**; recoverable ref: `{r['recoverable_ref_command']}`\n\n")
    with open(os.path.join(a.out, 'BRANCHES.md'), 'w') as f:
        f.write(f"# Math- branches — classification\n\nObserved {now} at `main` `{main_sha}`. {len(branch_records)} branches. "
                f"Counts: {json.dumps(meta['branch_class_counts'])}.\n\n")
        f.write(render_branch_table(branch_records))
    print(json.dumps(meta, indent=1))


if __name__ == '__main__':
    main()
