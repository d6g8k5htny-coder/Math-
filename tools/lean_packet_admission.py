"""Bounded Lean source declaration census, NOT an all-compiled-constant audit.

Only the existing packet command subset is admitted. Declaration keywords are
checked at every indentation; supported declarations must start at column zero.
Private names below are source names, never Lean's generated private names.
No imports from this file occur until each adapter verifies its exact bytes.
"""
import hashlib
import re

IDENT = r"[A-Za-z_][A-Za-z0-9_'₀-₉]*"
NAME = IDENT + r'(?:\.' + IDENT + r')*'
WORDS = re.compile(r"[\w']+", re.UNICODE)
KINDS = {'theorem', 'lemma', 'def', 'abbrev', 'instance', 'structure'}
FORBIDDEN = frozenset(('sorry admit sorryAx axiom native_decide implemented_by extern unsafe opaque partial '
                       'ofReduceBool trustCompiler debug').split())
UNSUPPORTED = frozenset(('protected class inductive coinductive mutual example syntax macro macro_rules '
                         'elab elab_rules declare_syntax_cat initialize builtin_initialize '
                         'run_cmd run_elab run_meta run_tac by_elab attribute notation infix infixl infixr '
                         'prefix postfix deriving export alias local scoped Lean MetaM TermElabM TacticM CoreM '
                         'CommandElabM addDecl evalTactic decreasing_by').split())
DECL = re.compile(r'^(?:(private)[ \t]+)?(?:noncomputable[ \t]+)?(theorem|lemma|def|abbrev|instance|structure)[ \t]+(' + NAME + r')(?=\s|:|\(|\{|\[|$)')
SCOPE = re.compile(r'^(namespace|section|end) (' + NAME + r')\s*$')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def code_only(text):
    """Blank nested comments and non-interpolated literals, retaining token gaps/newlines.

    Raw strings and escaped plain strings/characters are recognized. Interpolation,
    quoted identifiers and malformed input are refused instead of being guessed.
    Literal contents never become command text; a marker prevents token joining.
    """
    out, i, depth = [], 0, 0
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1; i += 2
            elif text.startswith('-/', i):
                depth -= 1; i += 2
            else:
                if text[i] == '\n':
                    out.append('\n')
                i += 1
            continue
        if text.startswith('/-', i):
            out.append(' '); depth = 1; i += 2
        elif text.startswith('-/', i):
            raise ValueError('unmatched block comment terminator')
        elif text.startswith('--', i):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
        elif text[i] in '«»`':
            raise ValueError('unsupported quoted identifier or syntax quotation')
        elif text[i] == 'r' and (not i or not (text[i - 1].isalnum() or text[i - 1] in "_'")) and re.match(r'r#*"', text[i:]):
            opening = re.match(r'r(#*)"', text[i:])
            end = text.find('"' + opening[1], i + len(opening[0]))
            require(end >= 0, 'unterminated raw string literal')
            end += 1 + len(opening[1])
            out.append(' $literal ' + '\n' * text[i:end].count('\n')); i = end
        elif text[i] == '"':
            require(not i or text[i - 1] != '!', 'unsupported interpolated string literal')
            end = i + 1
            while end < len(text) and text[end] != '"':
                end += 2 if text[end] == '\\' else 1
            require(end < len(text), 'unterminated string literal')
            require('{' not in text[i:end + 1], 'unsupported possible string interpolation')
            out.append(' $literal ' + '\n' * text[i:end + 1].count('\n')); i = end + 1
        elif text.startswith("''", i):
            out.append("''"); i += 2  # Lean's set-image notation
        elif text[i] == "'" and (not i or not (text[i - 1].isalnum() or text[i - 1] in "_'.")):
            literal = re.match(r"'(?:\\(?:x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|[nrt\\'\"])|[^\\'\n])'", text[i:])
            require(literal is not None, 'unsupported or unterminated character literal')
            out.append(' $literal '); i += len(literal[0])
        else:
            out.append(text[i]); i += 1
    require(depth == 0, 'unterminated block comment')
    return ''.join(out)


def continuation_binding(text):
    """Bind opaque continuations and their preceding column-zero code anchors.

    This is reviewed source admission, not a proof parser. Blank/comment text is
    irrelevant; each retained indented code line stays ordered and attached to
    its preceding nonindented code line. Literal contents are already lexed out.
    Rebinding an ordinary source-file hash never changes this separate boundary.
    """
    return _continuation_binding(code_only(text))


def _continuation_binding(code):
    records, anchor = [], ''
    for line in code.splitlines():
        if not line.strip():
            continue
        if line[0].isspace():
            records.append(anchor + '\0' + line + '\n')
        else:
            anchor = line
    data = ''.join(records).encode('utf-8')
    return {'sha256': hashlib.sha256(data).hexdigest(), 'lines': len(records)}


def declaration_binding(text):
    """Fingerprint every opaque declaration/header line, including one-line bodies.

    This binds reviewed lexical code; it does not parse the opaque tail as Lean.
    Lexical code selects headers; their whole physical lines are bound, including
    literal/comment text. Ordinary source-file digest rebinding cannot update it.
    """
    return _declaration_binding(text, code_only(text))


def _declaration_binding(text, code):
    lines = [raw + '\n' for raw, line in zip(text.splitlines(), code.splitlines()) if DECL.match(line)]
    return {'sha256': hashlib.sha256(''.join(lines).encode('utf-8')).hexdigest(),
            'lines': len(lines)}


def check_continuation(actual, expected):
    """Unbound indentation is refused; bound continuation records must match exactly."""
    if expected is None:
        require(actual['lines'] == 0, 'unsupported unbound source continuation')
        return
    require(isinstance(expected, dict) and set(expected) == {'sha256', 'lines'}
            and isinstance(expected['sha256'], str)
            and re.fullmatch(r'[0-9a-f]{64}', expected['sha256'])
            and type(expected['lines']) is int and expected['lines'] >= 0,
            'unsupported malformed source continuation binding')
    require(actual == expected, 'unsupported changed source continuation binding')


def check_declarations(actual, expected):
    """Opaque declaration/header tails need a separate reviewed exact binding."""
    if expected is None:
        require(actual['lines'] == 0, 'unsupported unbound source declaration header')
        return
    require(isinstance(expected, dict) and set(expected) == {'sha256', 'lines'}
            and isinstance(expected['sha256'], str)
            and re.fullmatch(r'[0-9a-f]{64}', expected['sha256'])
            and type(expected['lines']) is int and expected['lines'] >= 0,
            'unsupported malformed source declaration header binding')
    require(actual == expected, 'unsupported changed source declaration header binding')


def census(text, module, continuation=None, declarations=None):
    """Return ordered source records; reject command/declaration forms outside the subset."""
    require(isinstance(module, str) and re.fullmatch(NAME, module), 'invalid source module name')
    code = code_only(text)
    words = set(WORDS.findall(code))
    bad = words & FORBIDDEN
    require(not bad, 'forbidden token in source module ' + module + ': ' + repr(sorted(bad)))
    # `scoped` is allowed only in a canonical `open scoped ...` command below.
    unsupported = words & (UNSUPPORTED - {'scoped'})
    require(not unsupported and '@[' not in code and '#' not in code,
            'unsupported metaprogramming or declaration syntax in ' + module + ': ' + repr(sorted(unsupported)))
    admitted_continuation = _continuation_binding(code)
    admitted_declarations = _declaration_binding(text, code)
    records, scopes, seen = [], [], set()
    for number, line in enumerate(code.splitlines(), 1):
        if not line.strip():
            continue
        where = module + ':' + str(number)
        tokens = WORDS.findall(line)
        decl_words = set(tokens) & KINDS
        scope_words = set(tokens) & {'namespace', 'section', 'end'}
        if scope_words:
            scope = SCOPE.fullmatch(line)
            require(scope is not None, 'unsupported namespace or section spelling at ' + where)
            kind, name = scope.groups()
            if kind == 'end':
                require(scopes and scopes[-1][1] == name, 'unbalanced namespace or section at ' + where)
                scopes.pop()
            else:
                scopes.append((kind, name))
            continue
        if decl_words:
            declaration = DECL.match(line)
            require(declaration is not None and sum(t in KINDS for t in tokens) == 1,
                    'unsupported declaration spelling at ' + where)
            privacy, kind, short = declaration.groups()
            namespace = '.'.join(n for k, n in scopes if k == 'namespace')
            name = '.'.join(n for n in (namespace, short) if n)
            require(name not in seen, 'duplicate source declaration at ' + where)
            seen.add(name)
            records.append(dict(module=module, namespace=namespace, name=name, kind=kind,
                                privacy='private' if privacy else 'public'))
            continue
        require(not (set(tokens) & {'private', 'noncomputable'}), 'unsupported declaration modifier at ' + where)
        if 'set_option' in tokens:
            require(line == 'set_option autoImplicit false', 'unsupported set_option at ' + where)
            continue
        if 'scoped' in tokens:
            require(re.fullmatch(r'open scoped ' + NAME + r'(?: ' + NAME + r')*\s*', line), 'unsupported scoped command at ' + where)
        if line[0].isspace():
            # Opaque proof/header/structure continuation: never admitted merely
            # because it is indented. Exact reviewed binding is checked below.
            continue
        require(not (tokens and tokens[0] == 'open' and 'in' in tokens), 'unsupported command wrapper at ' + where)
        allowed = (re.fullmatch(r'import ' + NAME + r'\s*', line)
                   or re.fullmatch(r'open (?:scoped )?' + NAME + r'(?: ' + NAME + r')*\s*', line)
                   or re.fullmatch(r'variable(?:[ \t]+(?:\{[^{}\n]*\}|\[[^\[\]\n]*\]|\([^()\n]*\)))+[ \t]*', line)
                   or line == 'omit [NormedSpace ℝ E] in')
        require(allowed, 'unsupported command at ' + where + ': ' + line[:80])
    require(not scopes, 'unclosed namespace or section in ' + module)
    check_continuation(admitted_continuation, continuation)
    check_declarations(admitted_declarations, declarations)
    return records


def check_census(actual, expected):
    """Require the exact ordered, typed census, including every record field."""
    fields = {'module', 'namespace', 'name', 'kind', 'privacy'}
    require(isinstance(expected, list) and bool(expected), 'source declaration census must be a nonempty list')
    for item in expected:
        require(isinstance(item, dict) and set(item) == fields
                and all(isinstance(item[k], str) for k in fields)
                and item['kind'] in KINDS and item['privacy'] in {'public', 'private'},
                'source declaration census malformed record')
    require(actual == expected, 'source declaration census mismatch')
