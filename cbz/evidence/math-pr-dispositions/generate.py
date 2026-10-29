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
EMPTY_TREE = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'


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
    changed = lib.changed_paths(repo, merge_base, head)
    diff_text = _git(repo, '-c', 'core.quotePath=false', 'diff', '--no-renames', merge_base, head, '--', *changed) if changed else ''
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


def list_refs(repo):
    """Snapshot of refs/remotes/origin/* as {branch name: tip sha}; recorded in CONTEXT.json for replay."""
    out = {}
    for line in _git(repo, 'for-each-ref', '--format=%(refname)%09%(objectname)', 'refs/remotes/origin/').splitlines():
        ref, tip = line.split('\t')
        name = ref[len('refs/remotes/origin/'):]
        if name != 'HEAD':
            out[name] = tip
    return out


def observation_context(repo, *, offline_dir, now):
    """The cut a run describes. Live: the clone's origin/main, its ref snapshot and the clock. Offline:
    the recorded CONTEXT.json, so a replay reproduces the committed observation (Codex finding on #529)."""
    if offline_dir:
        ctx_path = os.path.join(offline_dir, 'CONTEXT.json')
        if os.path.exists(ctx_path):
            return _load(ctx_path)
    return {'observed_at_utc': now, 'main_sha': _git(repo, 'rev-parse', 'refs/remotes/origin/main').strip(),
            'refs': list_refs(repo)}


def build_branch_records(repo, *, main_sha, refs, open_pr_refs, protected):
    out = []
    for name, tip in sorted(refs.items()):
        date = _git(repo, 'log', '-1', '--format=%cI', tip).strip()
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


def build_unmerged_branch_records(repo, *, main_sha, branches, refs, open_pr_heads, now):
    """Content facts for branches that are unmerged and have no PR. ``refs`` maps branch name -> tip sha
    (the recorded ref snapshot); ``open_pr_heads`` maps head ref -> sha."""
    out = []
    for name in branches:
        tip = refs[name]
        mb = subprocess.run(['git', '-C', repo, 'merge-base', tip, main_sha], capture_output=True, text=True)
        merge_base = mb.stdout.strip() if mb.returncode == 0 else None
        unrelated = merge_base is None
        base_for_diff = merge_base or EMPTY_TREE
        changed = lib.changed_paths(repo, base_for_diff, tip)
        diff_text = _git(repo, '-c', 'core.quotePath=false', 'diff', '--no-renames', base_for_diff, tip, '--', *changed) if changed else ''
        signals = lib.layer_a_signals(diff_text)
        equal = sum(1 for p in changed if lib.tree_entry(repo, tip, p) == lib.tree_entry(repo, main_sha, p))
        container = next((h for h, sha in sorted(open_pr_heads.items()) if lib.is_ancestor(repo, tip, sha)), False)
        last = _git(repo, 'log', '-1', '--format=%cI', tip).strip()
        days = (_parse(now) - _parse(last)).days
        dirs = sorted({p.rsplit('/', 1)[0] if '/' in p else '.' for p in changed})
        facts = {
            'unrelated_history': unrelated,
            'contained_in_open_pr_head': container,
            'all_changed_blobs_equal_on_main': bool(changed) and equal == len(changed),
            'updated_within_24h': (_parse(now) - _parse(last)) <= dt.timedelta(hours=24),
            'merge_tree_clean_onto_main': lib.merge_tree_clean(repo, main_sha, tip),
            'signals_total': sum(signals.values()),
            'changed_path_count': len(changed),
            'days_since_last_commit': days,
        }
        rec = {
            'branch': name, 'tip': tip, 'lane_prefix': name.split('/', 1)[0] if '/' in name else '(none)',
            'last_commit_date': last, 'merge_base_with_main': merge_base,
            'commits_ahead_of_main': int(_git(repo, 'rev-list', '--count', f'{main_sha}..{tip}').strip()),
            'changed_paths': changed[:200],
            'changed_paths_sha256': hashlib.sha256(''.join(p + '\n' for p in sorted(changed)).encode()).hexdigest(),
            'changed_directories': dirs[:40], 'changed_directory_count': len(dirs),
            'changed_blobs_equal_on_main': equal,
            'layer_a_signals': signals,
            'recreate_command': f'git push origin {tip}:refs/heads/{name}',
        }
        rec.update(facts)
        rec['recommended_disposition'] = lib.recommend_branch(facts)
        rec['integrable_if_wanted'] = lib.integrable_if_wanted(facts)
        out.append(rec)
    return sorted(out, key=lambda r: (r['recommended_disposition'], r['branch']))


def render_unmerged_table(records):
    out = ['| Branch | Tip | Last commit | Ahead | Paths | Dirs | Blobs = main | Signals | merge-tree→main | In open PR | Recommended | Integrable if wanted |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in records:
        out.append('| `{b}` | `{t}` | {d} | {a} | {p} | {dc} | {e} | {s} | {m} | {c} | **{rec}** | {iw} |'.format(
            iw='yes' if r.get('integrable_if_wanted') else '',
            b=r['branch'], t=r['tip'][:8], d=r['last_commit_date'][:10], a=r['commits_ahead_of_main'],
            p=r['changed_path_count'], dc=r['changed_directory_count'], e=r['changed_blobs_equal_on_main'],
            s=r['signals_total'], m='clean' if r['merge_tree_clean_onto_main'] else 'CONFLICT',
            c=f"`{r['contained_in_open_pr_head']}`" if r['contained_in_open_pr_head'] else '—',
            rec=r['recommended_disposition']))
    return '\n'.join(out) + '\n'


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

    clock = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    fetched_dir = a.offline or os.path.join(a.out, 'fetched')
    ctx = observation_context(a.repo, offline_dir=a.offline, now=clock)
    now, main_sha, refs = ctx['observed_at_utc'], ctx['main_sha'], ctx['refs']
    if not a.offline:
        os.makedirs(fetched_dir, exist_ok=True)
        _dump(ctx, os.path.join(fetched_dir, 'CONTEXT.json'))
    prs, data = load_offline(fetched_dir) if a.offline else fetch_all(a.owner_repo, fetched_dir)
    open_heads = {pr['head']['ref'] for pr in prs}
    open_refs = open_heads | {pr['base']['ref'] for pr in prs}
    protected = set(a.protected.split(',')) if a.protected else set()

    pr_records = [build_pr_record(a.repo, pr, main_sha=main_sha, comments=data[pr['number']]['comments'],
                                  reviews=data[pr['number']]['reviews'], check_runs=data[pr['number']]['check_runs'],
                                  now=now, open_pr_heads=open_heads) for pr in sorted(prs, key=lambda p: p['number'])]
    branch_records = build_branch_records(a.repo, main_sha=main_sha, refs=refs, open_pr_refs=open_refs, protected=protected)
    unmerged_names = [r['branch'] for r in branch_records if r['class'] == 'UNMERGED_NO_PR']
    unmerged_records = build_unmerged_branch_records(
        a.repo, main_sha=main_sha, branches=unmerged_names, refs=refs,
        open_pr_heads={pr['head']['ref']: pr['head']['sha'] for pr in prs}, now=now)

    meta = {'observed_at_utc': now, 'repository': a.owner_repo, 'main_sha': main_sha,
            'replay': 'offline from CONTEXT.json' if a.offline else 'live',
            'open_pr_count': len(pr_records), 'branch_count': len(branch_records),
            'disposition_counts': {}, 'branch_class_counts': {}, 'note': (
                'Evidence only. layer_a_signals are lexical hits on added/removed diff lines, never certification. '
                'recommended_disposition is a decision table over observed facts; the integrator decides.')}
    for r in pr_records:
        meta['disposition_counts'][r['recommended_disposition']] = meta['disposition_counts'].get(r['recommended_disposition'], 0) + 1
    for r in branch_records:
        meta['branch_class_counts'][r['class']] = meta['branch_class_counts'].get(r['class'], 0) + 1
    meta['unmerged_branch_disposition_counts'] = {}
    for r in unmerged_records:
        k = r['recommended_disposition']
        meta['unmerged_branch_disposition_counts'][k] = meta['unmerged_branch_disposition_counts'].get(k, 0) + 1
    meta['unmerged_integrable_if_wanted'] = sum(1 for r in unmerged_records if r['integrable_if_wanted'])
    meta['unmerged_unrelated_history'] = sum(1 for r in unmerged_records if r.get('unrelated_history'))

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
    _dump({'meta': meta, 'unmerged_branches': unmerged_records}, os.path.join(a.out, 'unmerged_branches.json'))
    with open(os.path.join(a.out, 'UNMERGED_BRANCHES.md'), 'w') as f:
        f.write(f"# Math- branches that are unmerged and have no pull request — content facts\n\n"
                f"Observed {now} at `main` `{main_sha}`. {len(unmerged_records)} branches. "
                f"Counts: {json.dumps(meta['unmerged_branch_disposition_counts'])}.\n\n"
                "Recommendations come from `disposition_lib.recommend_branch` (documented thresholds); Layer A signals are lexical. "
                "Every row is recoverable with `git push origin <tip>:refs/heads/<branch>`.\n\n")
        f.write(render_unmerged_table(unmerged_records))
        f.write('\n## Per-branch directories\n\n')
        for r in unmerged_records:
            f.write(f"- `{r['branch']}` `{r['tip'][:8]}` ({r['lane_prefix']}, {r['commits_ahead_of_main']} ahead, {r['changed_path_count']} paths): "
                    + ', '.join(f'`{d}`' for d in r['changed_directories'][:8])
                    + (f' … (+{r["changed_directory_count"] - 8} more)' if r['changed_directory_count'] > 8 else '')
                    + (f"; signals {json.dumps({k: v for k, v in r['layer_a_signals'].items() if v})}" if r['signals_total'] else '') + '\n')
    with open(os.path.join(a.out, 'BRANCHES.md'), 'w') as f:
        f.write(f"# Math- branches — classification\n\nObserved {now} at `main` `{main_sha}`. {len(branch_records)} branches. "
                f"Counts: {json.dumps(meta['branch_class_counts'])}.\n\n")
        f.write(render_branch_table(branch_records))
    print(json.dumps(meta, indent=1))


if __name__ == '__main__':
    main()
