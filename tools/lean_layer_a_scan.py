#!/usr/bin/env python3
"""Layer A source scan for every tracked Lean file (CBZ-0 gate G1).

Lexes Lean 4 source well enough to tell code from comments and literals, then reports
every code occurrence of a forbidden name:

  A1 placeholders:      sorry, admit, sorryAx
  A2 axiom injection:   the `axiom` command (and `axioms` is not a keyword, so only `axiom`)
  A1/A2 trust escapes:  native_decide, ofReduceBool, trustCompiler, implemented_by,
                        extern, unsafe
  A3 floating point:    Float, Float32

A name matches when the whole identifier, or any dotted component of it, is forbidden
(`Lean.ofReduceBool`, `Float.ofScientific`), including «guillemet»-quoted identifiers.
Text inside line comments (`--`), nested block and doc comments (`/- -/`, `/-- -/`,
`/-! -/`), string literals, raw strings (`r"..."`, `r#"..."#`, which have no escapes) and
character literals is ignored, so prose such as "densities admit versions" is not a hit.
The `{...}` holes of interpolated strings (`s!"..."`, `m!"..."`, `f!"..."`) are code and
are scanned.

This is a static scan. It does not replace a kernel build or `#print axioms`; it closes
the gap for Lean files that no gated package compiles. Standard library only.

Usage: lean_layer_a_scan.py [--root DIR] [--json] [PATH ...]
With no PATH it scans every `*.lean` file tracked by git under the root, skipping `.lake/`.
Exit status: 0 no findings, 1 findings, 2 a file could not be lexed (unterminated
comment or string): that file is reported, never silently skipped.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

FORBIDDEN = {
    'sorry': 'A1', 'admit': 'A1', 'sorryAx': 'A1',
    'axiom': 'A2',
    'native_decide': 'A2', 'ofReduceBool': 'A2', 'trustCompiler': 'A2',
    'implemented_by': 'A2', 'extern': 'A2', 'unsafe': 'A2',
    'Float': 'A3', 'Float32': 'A3',
}


class LexError(ValueError):
    pass


def _ident_start(c: str) -> bool:
    return c.isalpha() or c == '_'


def _ident_char(c: str) -> bool:
    return c.isalnum() or c in "_'!?"


RAW_OPEN = re.compile(r'r(#*)"')


def _hole_end(text: str, i: int) -> int:
    """Index of the '}' closing the interpolation hole that opens at text[i] == '{'.

    Nested braces and string literals inside the hole are skipped. An unclosed hole is a
    LexError, so a malformed interpolation can never hide code.
    """
    depth, j, n = 0, i, len(text)
    while j < n:
        ch = text[j]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return j
        elif ch == '"':
            j += 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == '\\' else 1
        j += 1
    raise LexError('unterminated interpolation hole')


def code_identifiers(text: str):
    """Yield (line, name) for each identifier outside comments and literals.

    A dotted name such as `Lean.ofReduceBool` is yielded as one name. Raises LexError on
    an unterminated block comment, string or guillemet identifier.
    """
    i, n, line = 0, len(text), 1
    while i < n:
        c = text[i]
        if c == '\n':
            line += 1
            i += 1
        elif text.startswith('--', i):
            j = text.find('\n', i)
            i = n if j < 0 else j
        elif text.startswith('/-', i):
            depth, start, i = 1, line, i + 2
            while depth:
                if i >= n:
                    raise LexError('unterminated block comment opened on line %d' % start)
                if text.startswith('/-', i):
                    depth, i = depth + 1, i + 2
                elif text.startswith('-/', i):
                    depth, i = depth - 1, i + 2
                else:
                    line += text[i] == '\n'
                    i += 1
        elif c == 'r' and RAW_OPEN.match(text, i) and (i == 0 or not (_ident_char(text[i - 1]) or text[i - 1] == '.')):
            # raw string r"..." / r#"..."#: no escapes; closes at '"' followed by the same hashes
            hashes = RAW_OPEN.match(text, i).group(1)
            start, close = line, '"' + hashes
            j = text.find(close, i + 2 + len(hashes))
            if j < 0:
                raise LexError('unterminated raw string opened on line %d' % start)
            line += text.count('\n', i, j)
            i = j + len(close)
        elif c == '"':
            # s!"..{e}.." / m!"..." / f!"...": the braced holes are code and are scanned
            interpolated = i >= 2 and text[i - 1] == '!' and _ident_char(text[i - 2])
            start, i = line, i + 1
            while True:
                if i >= n:
                    raise LexError('unterminated string opened on line %d' % start)
                if text[i] == '\\':
                    line += text[i + 1:i + 2] == '\n'
                    i += 2
                elif text[i] == '"':
                    i += 1
                    break
                elif interpolated and text[i] == '{':
                    j = _hole_end(text, i)
                    for hole_line, name, parts in code_identifiers(text[i + 1:j]):
                        yield line + hole_line - 1, name, parts
                    line += text.count('\n', i, j)
                    i = j + 1
                else:
                    line += text[i] == '\n'
                    i += 1
        elif c == "'" and i + 2 < n and (text[i + 2] == "'" or (text[i + 1] == '\\' and "'" in text[i + 3:i + 12])):
            # character literal 'a' or '\n' / '\x41' / '\u{..}'
            i = text.index("'", i + 2 if text[i + 1] != '\\' else i + 3) + 1
        elif c == '«' or _ident_start(c):
            parts, start = [], line
            while True:
                if i < n and text[i] == '«':
                    j = text.find('»', i)
                    if j < 0:
                        raise LexError('unterminated guillemet identifier on line %d' % start)
                    parts.append(text[i + 1:j])
                    i = j + 1
                elif i < n and _ident_start(text[i]):
                    j = i
                    while j < n and _ident_char(text[j]):
                        j += 1
                    parts.append(text[i:j])
                    i = j
                else:
                    break
                if i + 1 < n and text[i] == '.' and (text[i + 1] == '«' or _ident_start(text[i + 1])):
                    i += 1
                else:
                    break
            yield start, '.'.join(parts), parts
        else:
            i += 1


def findings_for_text(text: str):
    found = []
    for line, name, parts in code_identifiers(text):
        hits = [p for p in parts if p in FORBIDDEN]
        if hits:
            found.append({'line': line, 'name': name, 'token': hits[0], 'invariant': FORBIDDEN[hits[0]]})
    return found


def tracked_lean_files(root: pathlib.Path):
    out = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--', '*.lean'],
                         check=True, capture_output=True).stdout
    return sorted(p for p in out.decode().split('\0') if p and '/.lake/' not in '/' + p)


def scan(root: pathlib.Path, paths):
    report = {'files': 0, 'findings': [], 'lex_errors': []}
    for rel in paths:
        report['files'] += 1
        try:
            text = (root / rel).read_text(encoding='utf-8')
            for f in findings_for_text(text):
                report['findings'].append(dict(f, path=rel))
        except (LexError, UnicodeDecodeError) as exc:
            report['lex_errors'].append({'path': rel, 'error': str(exc)})
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', default='.')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('paths', nargs='*')
    args = ap.parse_args(argv)
    root = pathlib.Path(args.root).resolve()
    paths = args.paths or tracked_lean_files(root)
    report = scan(root, paths)
    if args.json:
        print(json.dumps(report, indent=1, sort_keys=True))
    else:
        for f in report['findings']:
            print('%s:%d: %s %s (%s)' % (f['path'], f['line'], f['invariant'], f['name'], f['token']))
        for e in report['lex_errors']:
            print('%s: LEX ERROR %s' % (e['path'], e['error']))
        print('scanned %d Lean files: %d findings, %d lex errors'
              % (report['files'], len(report['findings']), len(report['lex_errors'])))
    return 2 if report['lex_errors'] else 1 if report['findings'] else 0


if __name__ == '__main__':
    sys.exit(main())
