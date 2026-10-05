#!/usr/bin/env python3
"""Document-relative Markdown link check (standard library only; fail-closed).

For every Markdown link ``[text](target)`` in the given documents:

* an external target (``http://`` / ``https://``) must be a bare URL: no whitespace,
  parentheses or quotes inside the target (commentary belongs outside the link);
* an anchor-only target (``#...``) is accepted as written;
* a local target is resolved FROM THE DIRECTORY OF THE CONTAINING DOCUMENT (not the
  repository root), must stay inside the repository tree, and must exist in the
  checked-out tree.

Exit status 0 only when every link in every document passes; otherwise the failing
links are listed and the exit status is 1. Usage::

    python -B -S tools/check_doc_links.py PROOF_INDEX.md docs/integration/FILE.md

The optional ``--root DIR`` names the repository root (default: the parent of this
file's directory). Scientific effect: NONE — this checks navigation only.
"""
import argparse
import json
import os
import re
import sys

LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]*)\)')


def check_document(doc_path, root):
    """Return a list of (kind, target) failures for one document."""
    root = os.path.realpath(root)
    doc_real = os.path.realpath(doc_path)
    if not doc_real.startswith(root + os.sep):
        return [('document-outside-root', doc_path)]
    with open(doc_real, encoding='utf-8') as handle:
        text = handle.read()
    doc_dir = os.path.dirname(doc_real)
    failures = []
    for match in LINK.finditer(text):
        target = match.group(1)
        if target.startswith('http://') or target.startswith('https://'):
            if re.search(r'[\s()"\']', target):
                failures.append(('commentary-in-url', target))
            continue
        if target.startswith('#'):
            continue
        if re.search(r'[\s()"\']', target) or not target:
            failures.append(('commentary-in-target', target))
            continue
        path_part = target.split('#', 1)[0]
        resolved = os.path.realpath(os.path.join(doc_dir, path_part))
        if resolved != root and not resolved.startswith(root + os.sep):
            failures.append(('escapes-tree', target))
            continue
        if not os.path.exists(resolved):
            failures.append(('missing', target))
    return failures


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('documents', nargs='+')
    parser.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = parser.parse_args(argv)
    report = {'root': os.path.realpath(args.root), 'documents': {}, 'passed': True}
    for doc in args.documents:
        failures = check_document(doc, args.root)
        report['documents'][doc] = {'failures': [list(f) for f in failures]}
        if failures:
            report['passed'] = False
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
