#!/usr/bin/env python3
"""Quotation check for navigation records (standard library only; fail-closed).

In the table rows of the given Markdown documents, a passage in curly quotation marks
``“…”`` claims to be a VERBATIM excerpt of the record reached by the nearest preceding
Markdown link in the same cell segment (segments are split at ``<br>``); a passage
introduced by ``summary:`` is a labelled paraphrase of that record. For each passage:

* a local link is resolved from the directory of the containing document, and a quoted
  passage must occur in that file — as a whole, or as an ordered sequence of pieces when
  the passage marks omissions with ``…`` / ``...`` — after normalising whitespace,
  Markdown emphasis, curly quotes/dashes and table-cell pipe escapes;
* a GitHub pull-request review / comment link is checked against the live body only with
  ``--github`` (token read from ``GITHUB_TOKEN``); without it the passage is reported as
  ``unchecked_offline`` and does not fail the check. Online lookup requires the
  complete canonical fragment and matching response id, html_url and parent-PR URL;
* a ``summary:`` passage must not use a verdict word (ACCEPT, AMEND, HOLD, CONFIRMED,
  VERIFIED, REJECT) that the linked record does not use, under the same offline rule.
  The same leading word boundary applies to both texts; suffix forms remain allowed.
  This lexical check does not establish semantic agreement or resolve negation;
* a passage with no preceding link in its segment fails (``no-source-link``).

Header and separator rows are skipped. Exit status 0 only when no checked passage fails;
the JSON report lists every failure as ``[kind, source, passage-prefix]``. Usage::

    python -B -S tools/check_doc_quotes.py docs/integration/FILE.md [--github]

Scientific effect: NONE — this checks that a navigation document quotes its sources
faithfully; it does not read, weigh or change any verdict.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]*)\)')
QUOTE = re.compile(r'“([^”]*)”')
SUMMARY = re.compile(r'(?<![\w-])summary:\s*')
VERDICT = ('ACCEPT', 'AMEND', 'HOLD', 'CONFIRMED', 'VERIFIED', 'REJECT')
GITHUB = re.compile(r'https://github\.com/([^/]+)/([^/]+)/pull/(\d+)#(issuecomment|pullrequestreview|discussion_r)-?(\d+)')


def normalise(text):
    text = text.replace('\\|', '|').replace('**', '').replace('`', '').replace('*', '')
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'),
                 ('—', '-'), ('–', '-'), ('−', '-'), (' ', ' ')):
        text = text.replace(a, b)
    return re.sub(r'\s+', ' ', text).strip()


def pieces_in_order(passage, haystack):
    """True when every omission-separated piece of the passage occurs in order."""
    parts = re.split(r'…|\.\.\.', normalise(passage))
    parts = [p.strip(' .;,') for p in parts]
    parts = [p for p in parts if p]
    if not parts:
        return False
    position = 0
    for part in parts:
        found = haystack.find(part, position)
        if found < 0:
            return False
        position = found + len(part)
    return True


def split_cells(row):
    return re.split(r'(?<!\\)\|', row)[1:-1]


def table_data_rows(lines):
    """Yield (line_number, row) for table rows that are neither header nor separator."""
    for index, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        cells = split_cells(line)
        if cells and all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in cells):
            continue
        if index + 1 < len(lines) and lines[index + 1].startswith('|'):
            next_cells = split_cells(lines[index + 1])
            if next_cells and all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in next_cells):
                continue
        yield index + 1, line


def github_locator(target):
    """Canonical supported locator identity; only owner/repository case is folded."""
    if not isinstance(target, str):
        return None
    match = GITHUB.fullmatch(target)
    if not match:
        return None
    owner, repo, number, kind, ident = match.groups()
    marker = kind + ('' if kind == 'discussion_r' else '-')
    canonical = 'https://github.com/%s/%s/pull/%s#%s%s' % (owner, repo, number, marker, ident)
    if (target != canonical or not number.isascii() or not ident.isascii()
            or number.startswith('0') or ident.startswith('0')):
        return None
    return owner.casefold(), repo.casefold(), number, kind, ident


class Sources:
    def __init__(self, root, doc_dir, github, token):
        self.root, self.doc_dir, self.github, self.token = root, doc_dir, github, token
        self.cache = {}

    def body(self, target):
        """Return (normalised body, status) with status describes success, intentional offline mode, or an explicit source failure."""
        if target in self.cache:
            return self.cache[target]
        match = GITHUB.match(target)
        if match:
            if not self.github:
                result = (None, 'offline')
            elif github_locator(target) is None:
                result = (None, 'invalid-locator')
            else:
                result = self._fetch(match)
        elif target.startswith('http://') or target.startswith('https://'):
            result = (None, 'offline')
        else:
            path = os.path.realpath(os.path.join(self.doc_dir, target.split('#', 1)[0]))
            if path != self.root and not path.startswith(self.root + os.sep):
                result = (None, 'missing')
            elif not os.path.isfile(path):
                result = (None, 'missing')
            else:
                with open(path, encoding='utf-8') as handle:
                    result = (normalise(handle.read()), 'ok')
        self.cache[target] = result
        return result

    def _fetch(self, match):
        owner, repo, number, kind, ident = match.groups()
        api = 'https://api.github.com/repos/%s/%s/' % (owner, repo)
        if kind == 'issuecomment':
            url = api + 'issues/comments/' + ident
        elif kind == 'pullrequestreview':
            url = api + 'pulls/' + number + '/reviews/' + ident
        else:
            url = api + 'pulls/comments/' + ident
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'check-doc-quotes'}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
                data = json.load(response)
        except Exception:  # noqa: BLE001 - any transport failure is reported, never hidden
            return (None, 'unreachable')
        expected = github_locator(match.group(0))
        parent_key = 'issue_url' if kind == 'issuecomment' else 'pull_request_url'
        parent_family = 'issues' if kind == 'issuecomment' else 'pulls'
        parent_url = api + parent_family + '/' + number
        if (expected is None or not isinstance(data, dict)
                or type(data.get('id')) is not int or str(data['id']) != ident
                or github_locator(data.get('html_url')) != expected
                or not isinstance(data.get(parent_key), str)
                or data[parent_key].casefold() != parent_url.casefold()
                or not isinstance(data.get('body'), str)):
            return (None, 'identity-mismatch')
        return (normalise(data['body']), 'ok')


def check_document(doc_path, root, github=False, token=None):
    """Return a report dict for one document."""
    root = os.path.realpath(root)
    doc_real = os.path.realpath(doc_path)
    report = {'checked': 0, 'unchecked_offline': 0, 'quotes': 0, 'summaries': 0, 'failures': []}
    if not doc_real.startswith(root + os.sep):
        report['failures'].append(['document-outside-root', doc_path, ''])
        return report
    with open(doc_real, encoding='utf-8') as handle:
        lines = handle.read().split('\n')
    sources = Sources(root, os.path.dirname(doc_real), github, token)
    for _line_no, row in table_data_rows(lines):
        for cell in split_cells(row):
            for segment in cell.split('<br>'):
                links = [(m.start(), m.group(1)) for m in LINK.finditer(segment)]
                claims = [(m.start(), 'quote', m.group(1)) for m in QUOTE.finditer(segment)]
                for m in SUMMARY.finditer(segment):
                    end = len(segment)
                    nxt = QUOTE.search(segment, m.end())
                    if nxt:
                        end = nxt.start()
                    following_links = [pos for pos, _ in links if pos > m.end()]
                    if following_links:
                        end = min(end, following_links[0])
                    claims.append((m.start(), 'summary', segment[m.end():end]))
                for position, kind, passage in sorted(claims):
                    report['quotes' if kind == 'quote' else 'summaries'] += 1
                    preceding = [target for pos, target in links if pos < position]
                    prefix = passage[:80]
                    if not preceding:
                        report['failures'].append(['no-source-link', '', prefix])
                        continue
                    source = preceding[-1]
                    body, status = sources.body(source)
                    if status == 'offline':
                        report['unchecked_offline'] += 1
                        continue
                    report['checked'] += 1
                    if status != 'ok':
                        report['failures'].append(['source-' + status, source, prefix])
                        continue
                    if kind == 'quote':
                        if not pieces_in_order(passage, body):
                            report['failures'].append(['not-verbatim', source, prefix])
                    else:
                        for word in VERDICT:
                            pattern = r'\b' + word
                            if re.search(pattern, passage) and not re.search(pattern, body):
                                report['failures'].append(['verdict-word-not-in-source', source, word + ': ' + prefix])
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('documents', nargs='+')
    parser.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parser.add_argument('--github', action='store_true', help='also check GitHub review/comment links (GITHUB_TOKEN)')
    parser.add_argument('--require-online', action='store_true', help='fail if any linked GitHub/HTTP source is left unchecked offline')
    args = parser.parse_args(argv)
    token = os.environ.get('GITHUB_TOKEN')
    report = {'root': os.path.realpath(args.root), 'github': args.github, 'require_online': args.require_online, 'documents': {}, 'passed': True}
    for doc in args.documents:
        result = check_document(doc, args.root, args.github, token)
        report['documents'][doc] = result
        if result['failures']:
            report['passed'] = False
        if args.require_online and result['unchecked_offline']:
            result['failures'].append(['unchecked-offline-required', '', str(result['unchecked_offline'])])
            report['passed'] = False
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
