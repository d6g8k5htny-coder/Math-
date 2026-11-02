"""C166 event routing for the one PR-time full regression suite; stdlib only.

full-regression-suite.yml runs the complete tests/ suite in both Python modes
for the former c6-palm-route / d5-dimension-lift / c6-factorial-moment PR
trigger union (widened to tools/**). Those three workflows keep the same suite
before their packet for workflow_dispatch only. These are synthetic controls of
the restricted workflow layout and of a minimal local step runner that models
GitHub's default `bash -e` run steps, default success() step conditions and
skipped-step semantics. No packet checker is executed here; the packet step is
replaced by a sentinel. Not GitHub's scheduler, not mathematical evidence.
"""
from pathlib import Path
import hashlib
import os
import re
import subprocess
import sys
import shutil
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / '.github/workflows'
CENTRAL = 'full-regression-suite'
TRIO = {
    'c6-palm-route': 'c6_palm_route_20260929',
    'd5-dimension-lift': 'd5_dimension_lift_20260929',
    'c6-factorial-moment': 'c6_factorial_moment_20260929',
}
REGRESSION = 'Full repository regression suite in both Python modes'
PACKET = 'Verify sources, replay both modes, reject mutants'
BIND = 'Bind tested commit'
CONFIRM = 'Confirm the suite left the tested commit unchanged'
MANUAL_GUARD = "github.event_name == 'workflow_dispatch'"
ORIGINAL_SUITE_BLOCK = ('set -euo pipefail\n'
               'python -B -S -m unittest discover -s tests -v\n'
               'python -B -O -S -m unittest discover -s tests -v\n')
CENTRAL_SUITE_BLOCK = (
    "set -euo pipefail\n"
    "log_dir=\"$(mktemp -d)\"\n"
    "trap 'rm -rf \"$log_dir\"' EXIT\n"
    "python -B -S -m unittest discover -s tests -v 2>&1 | tee \"$log_dir/normal.log\"\n"
    "grep -Eq '^Ran [1-9][0-9]* tests? in [0-9]+([.][0-9]+)?s$' \"$log_dir/normal.log\"\n"
    "python -B -O -S -m unittest discover -s tests -v 2>&1 | tee \"$log_dir/optimized.log\"\n"
    "grep -Eq '^Ran [1-9][0-9]* tests? in [0-9]+([.][0-9]+)?s$' \"$log_dir/optimized.log\"\n"
)
MANUAL_SUITE_BLOCK = CENTRAL_SUITE_BLOCK
NORMAL = ['-B', '-S', '-m', 'unittest', 'discover', '-s', 'tests', '-v']
OPTIMIZED = ['-B', '-O', '-S', '-m', 'unittest', 'discover', '-s', 'tests', '-v']
# The complete PR trigger union of the three workflows at Math- 7014efec.
OLD_UNION = (
    '.github/workflows/c6-factorial-moment.yml',
    '.github/workflows/c6-palm-route.yml',
    '.github/workflows/d5-dimension-lift.yml',
    'frontiers/c6_factorial_moment_20260929/**',
    'frontiers/c6_palm_route_20260929/**',
    'frontiers/d5_dimension_lift_20260929/**',
    'tests/**',
    'tools/d5_c6_replay.py',
)
CENTRAL_PATHS = (
    '.github/workflows/full-regression-suite.yml',
    '.github/workflows/c6-factorial-moment.yml',
    '.github/workflows/c6-palm-route.yml',
    '.github/workflows/d5-dimension-lift.yml',
    'frontiers/c6_factorial_moment_20260929/**',
    'frontiers/c6_palm_route_20260929/**',
    'frontiers/d5_dimension_lift_20260929/**',
    'tests/**',
    'tools/**',
)
# Packet step bytes (step header through end of file) at Math- 7014efec. C166
# keeps packet semantics unchanged; an intended packet change updates these.
PACKET_SHA256 = {
    'c6-palm-route': '01fc8f4b833c935f355a2217a63ec7482977ea1cb5a6103c44940fd83a380418',
    'd5-dimension-lift': '2b217795b3628bb3b4a243eef9fdff0ea419333054c3a4a2ea38592d3794eef7',
    'c6-factorial-moment': '425bcd1b15ceaf2f11480b03f046566fb9b4f0ac993ee0c00450e29e02ff4786',
}
STEP_KEYS = {'name', 'uses', 'with', 'env', 'run', 'if'}
# R55-A concurrency block reviewed on main#419 (6228007083) and added by
# Math-#469 to full-regression-suite.yml and lifetime-dd-model-d.yml. Only these
# exact bytes are accepted; reruns get their own group, first attempts of one PR
# share a cancelling group, every other event gets a per-run group.
CONCURRENCY_LINES = (
    'concurrency:',
    "  group: ${{ github.workflow }}-${{ github.event_name == 'pull_request' && "
    "github.run_attempt == '1' && format('pr-{0}', github.event.pull_request.number) || "
    "github.event_name == 'pull_request' && format('pr-rerun-{0}-{1}-{2}', "
    "github.event.pull_request.number, github.run_id, github.run_attempt) || "
    "format('{0}-{1}', github.event_name, github.run_id) }}",
    "  cancel-in-progress: ${{ github.event_name == 'pull_request' && github.run_attempt == '1' }}",
)
CONCURRENCY_BLOCK = ''.join(line + '\n' for line in CONCURRENCY_LINES)
# The authenticated insertion: the block plus its one separating blank line,
# placed directly after the permissions block and directly before jobs:.
CONCURRENCY_INSERTION = CONCURRENCY_BLOCK + '\n'
CONCURRENCY_BEFORE = 'permissions:\n  contents: read\n\n'
CONCURRENCY_AFTER = 'jobs:\n'
CONCURRENCY_WORKFLOWS = (CENTRAL, 'lifetime-dd-model-d')
ORIGINAL_CENTRAL_SHA256 = '505e20940473c5a1fefaf5559e3f2ec2425fdb0e03de7c16d05e5371235e3e26'
# Historical setup-python pin inside 49fb197c / blob ea291276 and the three
# manual workflow blobs authenticated at 6e502c1f. The current pin is a
# separate contract. Reconstruction restores the historical pin; the digest
# constants above are not retargeted.
HISTORICAL_SETUP_PYTHON = 'actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97'
CURRENT_SETUP_PYTHON = 'actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0'


def parse(text):
    """Strict parser for this restricted single-job layout; fails closed."""
    lines = text.split('\n')
    if lines[-1] != '':
        raise ValueError('missing final newline')
    lines = lines[:-1]
    i = 0
    on = {}
    job = None
    steps = []
    events_seen = False
    permissions_seen = False
    jobs_seen = False
    concurrency = False

    def indent(line):
        return len(line) - len(line.lstrip(' '))

    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.startswith('#'):
            i += 1
            continue
        if line == 'concurrency:':
            # Exact approved block only, at most once, after permissions and
            # before jobs; any other concurrency text falls through to failure.
            if (concurrency or not permissions_seen or jobs_seen
                    or tuple(lines[i:i + 3]) != CONCURRENCY_LINES):
                raise ValueError('unsupported, duplicate or misplaced concurrency block')
            concurrency = True
            i += 3
            continue
        if line.startswith('name: ') or line in ('permissions:', '  contents: read', 'jobs:'):
            permissions_seen = permissions_seen or line == 'permissions:'
            jobs_seen = jobs_seen or line == 'jobs:'
            i += 1
            continue
        if line == "'on':":
            if events_seen:
                raise ValueError('duplicate on')
            events_seen = True
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith('  ')):
                ev = lines[i]
                if not ev.strip():
                    i += 1
                    continue
                m = re.fullmatch(r'  ([a-z_]+):', ev)
                if not m or m.group(1) in on:
                    raise ValueError('unsupported or duplicate event: ' + ev)
                name = m.group(1)
                on[name] = None
                i += 1
                if i < len(lines) and lines[i].startswith('    '):
                    if lines[i] != '    paths:' or name != 'pull_request':
                        raise ValueError('unsupported event filter: ' + lines[i])
                    i += 1
                    paths = []
                    while i < len(lines) and lines[i].startswith('      - '):
                        pm = re.fullmatch(r"      - '([A-Za-z0-9_./-]+(?:/\*\*)?)'", lines[i])
                        if not pm:
                            raise ValueError('unsupported path syntax: ' + lines[i])
                        paths.append(pm.group(1))
                        i += 1
                    if not paths or len(paths) != len(set(paths)):
                        raise ValueError('empty or duplicate path list')
                    on[name] = paths
            continue
        m = re.fullmatch(r'  ([a-z][a-z0-9-]*):', line)
        if m and job is None:
            job = {'id': m.group(1)}
            i += 1
            while i < len(lines) and lines[i].startswith('    ') and not lines[i].startswith('      '):
                km = re.fullmatch(r'    (runs-on|timeout-minutes|steps):(.*)', lines[i])
                if not km or km.group(1) in job:
                    raise ValueError('unsupported job key: ' + lines[i])
                job[km.group(1)] = km.group(2).strip()
                i += 1
                if km.group(1) == 'steps':
                    while i < len(lines) and lines[i].startswith('      '):
                        sm = re.fullmatch(r'      - ([a-z-]+): ?(.*)', lines[i])
                        if not sm:
                            raise ValueError('unsupported step line: ' + lines[i])
                        step = {}
                        key, value = sm.group(1), sm.group(2)
                        while True:
                            if key not in STEP_KEYS or key in step:
                                raise ValueError('unsupported or duplicate step key: ' + key)
                            i += 1
                            if key in ('with', 'env'):
                                if value:
                                    raise ValueError('inline mapping unsupported')
                                mapping = {}
                                while i < len(lines) and indent(lines[i]) == 10 and lines[i].strip():
                                    mm = re.fullmatch(r'          ([A-Za-z_][A-Za-z0-9_-]*): (.+)', lines[i])
                                    if not mm or mm.group(1) in mapping:
                                        raise ValueError('unsupported mapping line: ' + lines[i])
                                    mapping[mm.group(1)] = mm.group(2)
                                    i += 1
                                step[key] = mapping
                            elif key == 'run':
                                if value != '|':
                                    raise ValueError('run must be a literal block')
                                body = []
                                while i < len(lines) and (not lines[i].strip() or indent(lines[i]) >= 10):
                                    body.append(lines[i][10:])
                                    i += 1
                                while body and not body[-1]:
                                    body.pop()
                                step['run'] = '\n'.join(body) + '\n'
                            else:
                                if not value:
                                    raise ValueError('empty step value: ' + key)
                                step[key] = value
                            if i < len(lines) and re.fullmatch(r'        [a-z-]+:.*', lines[i]):
                                km2 = re.fullmatch(r'        ([a-z-]+): ?(.*)', lines[i])
                                key, value = km2.group(1), km2.group(2)
                                continue
                            break
                        steps.append(step)
                    job['steps'] = steps
            continue
        raise ValueError('unsupported top-level line: ' + line)
    if job is None or not steps or not events_seen:
        raise ValueError('incomplete workflow')
    job['concurrency'] = concurrency
    return on, job


def strip_concurrency_insertion(text):
    """Remove exactly the authenticated insertion; never a missing-block fallback."""
    count = text.count(CONCURRENCY_INSERTION)
    if count != 1:
        raise ValueError('expected exactly one approved concurrency insertion, found ' + str(count))
    at = text.index(CONCURRENCY_INSERTION)
    end = at + len(CONCURRENCY_INSERTION)
    if not text[:at].endswith(CONCURRENCY_BEFORE) or not text[end:].startswith(CONCURRENCY_AFTER):
        raise ValueError('approved concurrency insertion is not between permissions and jobs')
    stripped = text[:at] + text[end:]
    if 'concurrency' in stripped:
        raise ValueError('concurrency text outside the approved insertion')
    return stripped


def reconstruct_original_central(text):
    """Historical central workflow at 49fb197c / blob ea291276, authenticated.

    Remove only the approved concurrency insertion, restore the historical
    20-minute budget from the current 45-minute budget, restore the historical
    setup-python pin, then revert only the suite body. The result must hash to
    the unchanged historical digest.
    """
    text = strip_concurrency_insertion(text)
    text = mutate(text, '\n    timeout-minutes: 45\n', '\n    timeout-minutes: 20\n')
    text = mutate(text, CURRENT_SETUP_PYTHON, HISTORICAL_SETUP_PYTHON)
    block = named(parse(text)[1], REGRESSION)['run']
    rendered = lambda body: ''.join('          ' + line + '\n'
                                    for line in body.splitlines())
    original = mutate(text, rendered(block), rendered(ORIGINAL_SUITE_BLOCK))
    if hashlib.sha256(original.encode()).hexdigest() != ORIGINAL_CENTRAL_SHA256:
        raise AssertionError('historical central workflow digest mismatch')
    return original


def _tokens(expr):
    pos = 0
    out = []
    pattern = re.compile(r"\s*(?:(&&|\|\||==|[(),])|'([^']*)'|([A-Za-z_][A-Za-z0-9_.]*))")
    while pos < len(expr):
        if not expr[pos:].strip():
            break
        m = pattern.match(expr, pos)
        if not m:
            raise ValueError('unsupported expression text: ' + expr[pos:])
        out.append(('op', m.group(1)) if m.group(1) else
                   ('str', m.group(2)) if m.group(2) is not None else ('id', m.group(3)))
        pos = m.end()
    return out


def evaluate(expr, context):
    """Evaluate the small GitHub expression subset used by the approved block.

    Supports string literals, context lookups, format(), ==, && and || with
    GitHub's value-returning short-circuit semantics. Anything else fails.
    """
    toks = _tokens(expr)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else (None, None)

    def take(kind=None, value=None):
        tok = peek()
        if tok[0] is None or (kind and tok[0] != kind) or (value and tok[1] != value):
            raise ValueError('unexpected token in expression: ' + repr(tok))
        pos[0] += 1
        return tok

    def primary():
        kind, value = take()
        if kind == 'str':
            return value
        if kind == 'op' and value == '(':
            result = disjunction()
            take('op', ')')
            return result
        if kind == 'id' and value == 'format':
            take('op', '(')
            args = [disjunction()]
            while peek() == ('op', ','):
                take()
                args.append(disjunction())
            take('op', ')')
            return re.sub(r'\{(\d+)\}', lambda m: str(args[1 + int(m.group(1))]), args[0])
        if kind == 'id':
            if value not in context:
                raise ValueError('unknown context value: ' + value)
            return context[value]
        raise ValueError('unexpected token: ' + repr((kind, value)))

    def comparison():
        left = primary()
        while peek() == ('op', '=='):
            take()
            left = str(left) == str(primary())
        return left

    def conjunction():
        left = comparison()
        while peek() == ('op', '&&'):
            take()
            right = comparison()
            left = right if left else left
        return left

    def disjunction():
        left = conjunction()
        while peek() == ('op', '||'):
            take()
            right = conjunction()
            left = left if left else right
        return left

    result = disjunction()
    if pos[0] != len(toks):
        raise ValueError('trailing expression tokens')
    return result


def render(template, context):
    def value(m):
        v = evaluate(m.group(1), context)
        return ('true' if v else 'false') if isinstance(v, bool) else str(v)
    return re.sub(r'\$\{\{ (.*?) \}\}', value, template)


def concurrency_problems(block):
    """Semantic rerun/cancellation contract of one concurrency block text."""
    lines = block.split('\n')
    if len(lines) != 4 or lines[0] != 'concurrency:' or lines[3] != '':
        return ['concurrency block shape changed']
    gm = re.fullmatch(r'  group: (.+)', lines[1])
    cm = re.fullmatch(r'  cancel-in-progress: (.+)', lines[2])
    if not gm or not cm:
        return ['concurrency keys changed']

    def run(event, pr, run_id, attempt):
        context = {'github.workflow': 'W', 'github.event_name': event,
                   'github.event.pull_request.number': pr if event == 'pull_request' else '',
                   'github.run_id': run_id, 'github.run_attempt': attempt}
        return render(gm.group(1), context), render(cm.group(1), context)

    problems = []
    try:
        first = {(pr, rid): run('pull_request', pr, rid, '1')
                 for pr in ('7', '8') for rid in ('100', '101')}
        reruns = {(pr, rid, a): run('pull_request', pr, rid, a)
                  for pr in ('7', '8') for rid in ('100', '101') for a in ('2', '3')}
        others = {(ev, rid, a): run(ev, '', rid, a)
                  for ev in ('workflow_dispatch', 'push') for rid in ('100', '101')
                  for a in ('1', '2')}
    except ValueError as exc:
        return ['concurrency expression: ' + str(exc)]
    if first[('7', '100')][0] != first[('7', '101')][0]:
        problems.append('first attempts of one PR must share a group')
    if first[('7', '100')][0] == first[('8', '100')][0]:
        problems.append('first attempts of different PRs share a group')
    if any(cancel != 'true' for _, cancel in first.values()):
        problems.append('first-attempt PR runs must cancel in progress')
    rerun_groups = [g for g, _ in reruns.values()]
    other_groups = [g for g, _ in others.values()]
    first_groups = {g for g, _ in first.values()}
    if len(set(rerun_groups)) != len(rerun_groups):
        problems.append('rerun-group collision between reruns')
    if set(rerun_groups) & first_groups:
        problems.append('rerun-group collision with first-attempt PR group')
    # Attempts of one non-PR run reuse that run's group (they never overlap and
    # never cancel); distinct non-PR runs and all PR runs stay apart.
    per_run = {(ev, rid): {g for (e, r, _), (g, _) in others.items() if (e, r) == (ev, rid)}
               for ev, rid, _ in others}
    if (any(len(groups) != 1 for groups in per_run.values())
            or len(set().union(*per_run.values())) != len(per_run)
            or set(other_groups) & (first_groups | set(rerun_groups))):
        problems.append('dispatch/other run shares a group')
    if any(cancel != 'false' for _, cancel in list(reruns.values()) + list(others.values())):
        problems.append('reruns and non-PR runs must not cancel in progress')
    return problems


def concurrency_contract(text):
    """Current-candidate contract: exact block, once, at the approved location."""
    try:
        strip_concurrency_insertion(text)
    except ValueError as exc:
        return [str(exc)]
    return concurrency_problems(CONCURRENCY_BLOCK)


def covered(paths, changed):
    return any(changed.startswith(p[:-2]) if p.endswith('/**') else changed == p for p in paths)


def named(job, name):
    found = [s for s in job['steps'] if s.get('name') == name]
    if len(found) != 1:
        raise ValueError('expected one step named ' + name)
    return found[0]


def condition(expr, event, failed):
    """Model GitHub step conditions; only the intended manual guard exists."""
    if expr is None:
        return not failed
    if expr == MANUAL_GUARD:
        return not failed and event == 'workflow_dispatch'
    raise AssertionError('unexpected step condition: ' + expr)


def run_job(text, event, fail=(), sha_override=None, counts=(2, 2),
            summaries=None, fail_capture=(), real_cases=None):
    """Run actual shell steps with controlled children; packet -> sentinel.

    Default children emit synthetic unittest summaries. real_cases instead runs
    this interpreter on tiny generated fixtures, not the repository test suite.
    """
    _, job = parse(text)
    with tempfile.TemporaryDirectory(prefix='full-suite-routing-') as td:
        root = Path(td)
        repo = root / 'repo'
        repo.mkdir()
        (repo / 'tracked.txt').write_text('fixture\n')
        # A temporary cwd does not override inherited repository/index selectors.
        # Keep one isolated Git environment for setup, reads and Bash descendants.
        template = root / 'empty-template'
        template.mkdir()
        env = {key: value for key, value in os.environ.items()
               if not key.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_TEMPLATE_DIR=str(template))
        for cmd in (['git', 'init', '-q'], ['git', 'add', '.'],
                    ['git', '-c', 'user.name=Routing Fixture', '-c', 'user.email=fixture@example.invalid',
                     '-c', 'commit.gpgsign=false', '-c', 'maintenance.auto=false',
                     'commit', '-qm', 'synthetic routing fixture']):
            subprocess.run(cmd, cwd=repo, env=env, check=True, capture_output=True)
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, env=env, check=True,
                              capture_output=True, text=True).stdout.strip()
        bindir = root / 'bin'
        bindir.mkdir()
        log = root / 'python.log'
        fake = bindir / 'python'
        if summaries is None:
            summaries = tuple('Ran ' + str(count) + ' test' +
                              ('' if count == 1 else 's') + ' in 0.001s'
                              for count in counts)
        fake.write_text('#!/bin/sh\n'
                        'printf "%s\\n" "$*" >> "$FAKE_LOG"\n'
                        'case " $* " in *" -O "*) mode=optimized ;; *) mode=normal ;; esac\n'
                        'if [ "$FAKE_REAL" = 1 ]; then\n'
                        '  cd "$REAL_FIXTURE_ROOT/$mode" || exit 9\n'
                        '  exec "$REAL_PYTHON" "$@"\n'
                        'fi\n'
                        'case "$mode" in\n'
                        '  normal) summary=$NORMAL_SUMMARY ;;\n'
                        '  optimized) summary=$OPTIMIZED_SUMMARY ;;\n'
                        'esac\n'
                        'if [ -n "$summary" ]; then printf "%s\\n" "$summary" >&2; fi\n'
                        'case " $FAKE_FAIL " in *" $mode "*) exit 7 ;; esac\n'
                        'exit 0\n')
        fake.chmod(0o755)
        temp = root / 'temp'
        temp.mkdir()
        real_root = root / 'real-discovery'
        if real_cases is not None:
            for mode, case in zip(('normal', 'optimized'), real_cases):
                tests = real_root / mode / 'tests'
                tests.mkdir(parents=True)
                if case not in ('empty', 'pass', 'fail'):
                    raise ValueError('unsupported real discovery case: ' + case)
                if case != 'empty':
                    (tests / 'test_control.py').write_text(
                        'import unittest\nclass Control(unittest.TestCase):\n'
                        '    def test_control(self):\n'
                        '        self.assertEqual(1, ' + ('1' if case == 'pass' else '2') + ')\n')
        if fail_capture:
            capture = bindir / 'tee'
            capture.write_text('#!/bin/sh\n'
                               'n=0\n'
                               '[ ! -f "$CAPTURE_COUNT" ] || read -r n < "$CAPTURE_COUNT"\n'
                               'n=$((n + 1))\n'
                               'printf "%s\\n" "$n" > "$CAPTURE_COUNT"\n'
                               'case " $CAPTURE_FAIL " in *" $n "*) cat; exit 8 ;; esac\n'
                               'exec "$REAL_TEE" "$@"\n')
            capture.chmod(0o755)
        sentinel = root / 'packet.sentinel'
        context = {
            'github.sha': sha_override or head,
            'github.event.pull_request.head.sha': ('1' * 40) if event == 'pull_request' else '',
            'github.event_name': event,
            'github.run_id': '1234',
            'github.run_attempt': '1',
        }
        summary = root / 'summary.txt'
        outcomes = []
        streams = []
        failed = False
        for step in job['steps']:
            name = step.get('name') or step.get('uses')
            if not condition(step.get('if'), event, failed):
                outcomes.append((name, 'skipped'))
                continue
            if 'run' not in step:
                outcomes.append((name, 'success'))
                continue
            step_env = dict(env, PATH=str(bindir) + os.pathsep + env.get('PATH', ''),
                            FAKE_LOG=str(log), FAKE_FAIL=' '.join(fail),
                            GITHUB_STEP_SUMMARY=str(summary), TMPDIR=str(temp),
                            RUNNER_TEMP=str(temp), NORMAL_SUMMARY=summaries[0],
                            OPTIMIZED_SUMMARY=summaries[1],
                            FAKE_REAL='1' if real_cases is not None else '0',
                            REAL_PYTHON=sys.executable, REAL_FIXTURE_ROOT=str(real_root),
                            CAPTURE_COUNT=str(root / 'capture-count'),
                            CAPTURE_FAIL=' '.join(map(str, fail_capture)),
                            REAL_TEE=shutil.which('tee') or '')
            for key, value in step.get('env', {}).items():
                m = re.fullmatch(r'\$\{\{ ([a-z_.]+) \}\}', value)
                if m:
                    if m.group(1) not in context:
                        raise AssertionError('unexpected expression: ' + value)
                    value = context[m.group(1)]
                elif '${{' in value:
                    raise AssertionError('unsupported expression: ' + value)
                step_env[key] = value
            block = step['run']
            if name == PACKET:
                block = 'touch "$PACKET_SENTINEL"\n'
                step_env['PACKET_SENTINEL'] = str(sentinel)
            elif '${{' in block:
                raise AssertionError('inline expression in run block: ' + name)
            cp = subprocess.run(['bash', '-e', '-c', block], cwd=repo, env=step_env,
                                capture_output=True, timeout=30)
            streams.append((name, cp.returncode, cp.stdout, cp.stderr))
            outcomes.append((name, 'success' if cp.returncode == 0 else 'failure'))
            failed = failed or cp.returncode != 0
        calls = [line.split() for line in log.read_text().splitlines()] if log.exists() else []
        return {
            'conclusion': 'failure' if failed else 'success',
            'outcomes': outcomes,
            'streams': streams,
            'calls': calls,
            'sentinel': sentinel.exists(),
            'summary': summary.read_text() if summary.exists() else '',
            'head': head,
        }


def violations(workflow, text):
    """All C166 contract violations for one workflow text (empty when clean)."""
    problems = []
    try:
        on, job = parse(text)
    except ValueError as exc:
        return ['parse: ' + str(exc)]
    paths = on.get('pull_request') or []
    if workflow == CENTRAL:
        if not job['concurrency']:
            problems.append('central must carry the approved concurrency block')
        problems.extend(concurrency_contract(text))
    elif job['concurrency']:
        problems.append('manual trio workflows must not carry a concurrency block')
    if set(on) != {'pull_request', 'workflow_dispatch'} or on['workflow_dispatch'] is not None:
        problems.append('events must be exactly pull_request(paths) + workflow_dispatch')
    for key in ('continue-on-error', 'always()', 'failure()', 'cancelled()', 'background:'):
        if key in text:
            problems.append('bypass marker present: ' + key)
    uses = [s.get('uses') for s in job['steps'] if 'uses' in s]
    if uses != ['actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1',
                CURRENT_SETUP_PYTHON]:
        problems.append('checkout/setup-python pins changed')
    if job['steps'][0].get('with') != {'persist-credentials': 'false', 'fetch-depth': '0'}:
        problems.append('checkout must keep full history without credentials')
    if job['steps'][1].get('with') != {'python-version': "'3.11.16'"}:
        problems.append('python pin changed')
    names = [s.get('name') for s in job['steps'] if 'name' in s]
    try:
        bind = named(job, BIND)
        suite = named(job, REGRESSION)
    except ValueError as exc:
        return problems + [str(exc)]
    expected_suite = CENTRAL_SUITE_BLOCK if workflow == CENTRAL else MANUAL_SUITE_BLOCK
    if suite.get('run') != expected_suite:
        problems.append('suite block must preserve its exact central/manual discovery contract')
    central_bind = named(parse((WORKFLOWS / (CENTRAL + '.yml')).read_text())[1], BIND)
    if bind != central_bind:
        problems.append('tested-commit binding step differs from the central workflow')
    if workflow == CENTRAL:
        if job['id'] != 'full-suite' or job.get('timeout-minutes') != '45':
            problems.append('central job id/budget changed')
        if names != [BIND, REGRESSION, CONFIRM]:
            problems.append('central step order changed: ' + repr(names))
        if any('if' in s for s in job['steps']):
            problems.append('central steps must be unconditional')
        if tuple(paths) != CENTRAL_PATHS:
            problems.append('central path list changed')
        for old in OLD_UNION:
            probe = old[:-2] + 'probe.py' if old.endswith('/**') else old
            if not covered(paths, probe):
                problems.append('old trigger lost: ' + old)
        for probe in ('tools/any_new_tool.py', 'tests/test_any_new.py', 'tests/nested/test_x.py'):
            if not covered(paths, probe):
                problems.append('central misses ' + probe)
    else:
        packet_dir = TRIO[workflow]
        if names != [BIND, REGRESSION, PACKET]:
            problems.append('regression must precede packet: ' + repr(names))
        if suite.get('if') != MANUAL_GUARD:
            problems.append('regression must be guarded by exactly the manual-dispatch condition')
        for step in job['steps']:
            if step is not suite and 'if' in step:
                problems.append('unexpected condition on ' + str(step.get('name') or step.get('uses')))
        start = text.find('      - name: ' + PACKET + '\n')
        if start < 0 or hashlib.sha256(text[start:].encode()).hexdigest() != PACKET_SHA256[workflow]:
            problems.append('packet step bytes changed')
        for need in ('frontiers/' + packet_dir + '/**', '.github/workflows/' + workflow + '.yml',
                     'tools/d5_c6_replay.py', 'tests/test_d5_c6_workflows.py'):
            if need not in paths:
                problems.append('packet trigger lost: ' + need)
        if covered(paths, 'tests/test_unrelated_probe.py'):
            problems.append('tests-only PRs must not replay this packet')
    # Execution: a real bash -e run of the suite/binding blocks with fake python.
    try:
        events = ('pull_request', 'workflow_dispatch')
        for event in events:
            ok = run_job(text, event)
            runs_suite = workflow == CENTRAL or event == 'workflow_dispatch'
            if ok['conclusion'] != 'success':
                problems.append(f'{event}: passing suite did not pass')
            if ok['calls'] != ([NORMAL, OPTIMIZED] if runs_suite else []):
                problems.append(f'{event}: suite invocations {ok["calls"]!r}')
            if workflow != CENTRAL and not ok['sentinel']:
                problems.append(f'{event}: packet sentinel not reached')
            if 'tested-commit sha=' + ok['head'] not in ok['summary']:
                problems.append(f'{event}: tested commit not recorded')
            if runs_suite:
                for mode in ('normal', 'optimized'):
                    bad = run_job(text, event, fail=(mode,))
                    if bad['conclusion'] != 'failure':
                        problems.append(f'{event}: {mode} suite failure swallowed')
                    if bad['sentinel']:
                        problems.append(f'{event}: packet ran after {mode} suite failure')
            else:
                skipped = run_job(text, event, fail=('normal', 'optimized'))
                if skipped['conclusion'] != 'success' or not skipped['sentinel'] or skipped['calls']:
                    problems.append(f'{event}: PR must skip only the duplicate suite and run the packet')
            mismatch = run_job(text, event, sha_override='0' * 40)
            if mismatch['conclusion'] != 'failure' or mismatch['calls'] or mismatch['sentinel']:
                problems.append(f'{event}: tested-commit mismatch not fatal before suite/packet')
    except (AssertionError, ValueError, KeyError) as exc:
        problems.append('execution: ' + str(exc))
    return problems


def source(workflow):
    return (WORKFLOWS / (workflow + '.yml')).read_text()


def mutate(text, old, new, count=1):
    if text.count(old) != count:
        raise AssertionError('mutation anchor not found: ' + old)
    return text.replace(old, new)


class FullSuiteRoutingTests(unittest.TestCase):
    def original_central(self):
        # Remove only the authenticated concurrency insertion, restore only the
        # historical budget and suite body, and authenticate the original at
        # 49fb197c / blob ea291276, not a hand-written shell surrogate.
        original = reconstruct_original_central(source(CENTRAL))
        self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), ORIGINAL_CENTRAL_SHA256)
        return original

    def test_historical_and_current_concurrency_expectations_are_distinct(self):
        original = self.original_central()
        self.assertNotIn('concurrency', original)
        self.assertFalse(parse(original)[1]['concurrency'])
        self.assertTrue(parse(source(CENTRAL))[1]['concurrency'])
        # The historical input is not a valid current candidate: no fallback.
        self.assertIn('central must carry the approved concurrency block',
                      violations(CENTRAL, original))
        with self.assertRaises(ValueError):
            strip_concurrency_insertion(original)
        for workflow in TRIO:
            with self.subTest(workflow=workflow):
                self.assertFalse(parse(source(workflow))[1]['concurrency'])

    def test_both_workflow_concurrency_contracts(self):
        self.assertEqual(concurrency_problems(CONCURRENCY_BLOCK), [])
        for workflow in CONCURRENCY_WORKFLOWS:
            with self.subTest(workflow=workflow):
                text = source(workflow)
                self.assertEqual(text.count('concurrency'), 1)
                self.assertEqual(concurrency_contract(text), [])

    def test_concurrency_negative_controls(self):
        central = source(CENTRAL)
        group = CONCURRENCY_LINES[1]
        cancel = CONCURRENCY_LINES[2]
        rerun_fmt = ("format('pr-rerun-{0}-{1}-{2}', github.event.pull_request.number, "
                     "github.run_id, github.run_attempt)")
        collide_first = mutate(central, group, group.replace(
            rerun_fmt, "format('pr-{0}', github.event.pull_request.number)"))
        collide_reruns = mutate(central, group, group.replace(
            rerun_fmt, "format('pr-rerun-{0}', github.event.pull_request.number)"))
        bare = mutate(central, CONCURRENCY_INSERTION, '')
        cases = {
            'missing': bare,
            'duplicated': mutate(central, CONCURRENCY_INSERTION, CONCURRENCY_INSERTION * 2),
            'duplicated before permissions': mutate(central, CONCURRENCY_BEFORE,
                                                    CONCURRENCY_INSERTION + CONCURRENCY_BEFORE),
            'altered cancel': mutate(central, cancel, '  cancel-in-progress: true'),
            'altered group': mutate(central, group, group.replace("'pr-{0}'", "'pull-{0}'")),
            'altered spacing': mutate(central, 'concurrency:\n', 'concurrency: \n'),
            'extra key': mutate(central, cancel + '\n', cancel + '\n  queue: max\n'),
            'misplaced before permissions': mutate(bare, CONCURRENCY_BEFORE,
                                                   CONCURRENCY_INSERTION + CONCURRENCY_BEFORE),
            'misplaced after jobs': mutate(bare, 'jobs:\n', 'jobs:\n' + CONCURRENCY_BLOCK),
            'misplaced without separator': mutate(central, CONCURRENCY_INSERTION, CONCURRENCY_BLOCK),
            'rerun collides with first attempt': collide_first,
            'reruns collide with each other': collide_reruns,
        }
        for label, text in cases.items():
            with self.subTest(mutant=label):
                self.assertNotEqual(text, central)
                self.assertNotEqual(violations(CENTRAL, text), [], label)
                with self.assertRaises((ValueError, AssertionError)):
                    reconstruct_original_central(text)
        # Semantic check is independent of the byte pin: collisions are found
        # in the block text itself, not only by the exact-match parser.
        for label, text in (('first', collide_first), ('reruns', collide_reruns)):
            with self.subTest(semantic=label):
                start = text.index('concurrency:\n')
                block = text[start:text.index('\n\njobs:\n', start) + 1]
                self.assertTrue(any('rerun-group collision' in p
                                    for p in concurrency_problems(block)), label)
        dd = source('lifetime-dd-model-d')
        dd_bare = mutate(dd, CONCURRENCY_INSERTION, '')
        for label, text in (('lifetime-dd missing', dd_bare),
                            ('lifetime-dd duplicated', mutate(dd, CONCURRENCY_INSERTION,
                                                              CONCURRENCY_INSERTION * 2)),
                            ('lifetime-dd altered', mutate(dd, cancel, '  cancel-in-progress: true')),
                            ('lifetime-dd misplaced', mutate(dd_bare, "'on':\n",
                                                             CONCURRENCY_INSERTION + "'on':\n"))):
            with self.subTest(mutant=label):
                self.assertNotEqual(concurrency_contract(text), [])

    def test_historical_bytes_outside_insertion_are_authenticated(self):
        central = source(CENTRAL)
        self.assertEqual(reconstruct_original_central(central), self.original_central())
        for old, new in (('# This check is not required', '# This check is now required'),
                         ('    timeout-minutes: 45\n', '    timeout-minutes: 46\n'),
                         ('permissions:\n  contents: read\n\nconcurrency:',
                          'permissions:\n  contents: read\n\n\nconcurrency:'),
                         (CONCURRENCY_INSERTION + 'jobs:\n', CONCURRENCY_INSERTION + '\njobs:\n'),
                         ('name: Full repository regression suite\n',
                          'name: Full repository regression suite \n')):
            with self.subTest(old=old):
                with self.assertRaises((ValueError, AssertionError)):
                    reconstruct_original_central(mutate(central, old, new))

    def test_current_and_historical_budgets_have_separate_exact_contracts(self):
        central = source(CENTRAL)
        self.assertEqual(parse(central)[1]['timeout-minutes'], '45')
        original = self.original_central()
        self.assertEqual(parse(original)[1]['timeout-minutes'], '20')
        for budget in ('0', '20', '30', '44', '46', '360', "'45'"):
            with self.subTest(budget=budget):
                changed = mutate(central, '    timeout-minutes: 45\n',
                                 '    timeout-minutes: ' + budget + '\n')
                self.assertIn('central job id/budget changed', violations(CENTRAL, changed))
                with self.assertRaises((ValueError, AssertionError)):
                    reconstruct_original_central(changed)
        relocated = mutate(central, '\n    timeout-minutes: 45\n',
                           '\n    timeout-minutes: 20\n')
        relocated = mutate(relocated, '          log_dir="$(mktemp -d)"\n',
                           '          #    timeout-minutes: 45\n'
                           '          log_dir="$(mktemp -d)"\n')
        self.assertEqual(parse(relocated)[1]['timeout-minutes'], '20')
        self.assertIn('central job id/budget changed', violations(CENTRAL, relocated))
        with self.assertRaises((ValueError, AssertionError)):
            reconstruct_original_central(relocated)

    def test_original_accepts_synthetic_empty_success_but_preserves_failures(self):
        original = self.original_central()
        for event in ('pull_request', 'workflow_dispatch'):
            for counts in ((0, 2), (2, 0), (0, 0), (1, 1), (2, 3)):
                with self.subTest(event=event, counts=counts):
                    result = run_job(original, event, counts=counts)
                    self.assertEqual(result['conclusion'], 'success', result)
                    self.assertEqual(result['calls'], [NORMAL, OPTIMIZED])
                    self.assertEqual(result['outcomes'][-1], (CONFIRM, 'success'))
            for mode, calls in (('normal', [NORMAL]), ('optimized', [NORMAL, OPTIMIZED])):
                with self.subTest(event=event, failure=mode):
                    result = run_job(original, event, fail=(mode,))
                    self.assertEqual(result['conclusion'], 'failure', result)
                    self.assertEqual(result['calls'], calls)
                    self.assertEqual(result['outcomes'][-1], (CONFIRM, 'skipped'))

    def test_central_rejects_empty_success_before_confirmation(self):
        for event in ('pull_request', 'workflow_dispatch'):
            for counts, calls in (((0, 2), [NORMAL]), ((2, 0), [NORMAL, OPTIMIZED]),
                                  ((0, 0), [NORMAL])):
                with self.subTest(event=event, counts=counts):
                    result = run_job(source(CENTRAL), event, counts=counts)
                    self.assertEqual(result['conclusion'], 'failure', result)
                    self.assertEqual(result['calls'], calls)
                    self.assertEqual(result['outcomes'][-1], (CONFIRM, 'skipped'))

    def test_central_accepts_singular_and_multiple_successful_tests(self):
        for event in ('pull_request', 'workflow_dispatch'):
            for counts in ((1, 1), (2, 13), (13, 2)):
                with self.subTest(event=event, counts=counts):
                    result = run_job(source(CENTRAL), event, counts=counts)
                    self.assertEqual(result['conclusion'], 'success', result)
                    self.assertEqual(result['calls'], [NORMAL, OPTIMIZED])
                    self.assertEqual(result['outcomes'][-1], (CONFIRM, 'success'))

    def test_central_requires_well_formed_positive_summary_in_each_mode(self):
        good = 'Ran 2 tests in 0.001s'
        for bad in ('', 'Ran 00 tests in 0.001s', 'Ran 01 tests in 0.001s',
                    'Ran -1 tests in 0.001s', 'Ran 1.0 tests in 0.001s',
                    'Ran 1 test in unknown', 'prefix Ran 1 test in 0.001s',
                    'Ran 1 test in 0.001s suffix'):
            for index in (0, 1):
                with self.subTest(summary=bad, mode=index):
                    summaries = [good, good]
                    summaries[index] = bad
                    result = run_job(source(CENTRAL), 'pull_request', summaries=summaries)
                    self.assertEqual(result['conclusion'], 'failure', result)
                    self.assertEqual(result['calls'], [NORMAL] if index == 0
                                     else [NORMAL, OPTIMIZED])
                    self.assertEqual(result['outcomes'][-1], (CONFIRM, 'skipped'))

    def test_positive_summary_cannot_hide_child_or_capture_failure(self):
        for event in ('pull_request', 'workflow_dispatch'):
            for mode, calls in (('normal', [NORMAL]), ('optimized', [NORMAL, OPTIMIZED])):
                with self.subTest(event=event, failed_child=mode):
                    result = run_job(source(CENTRAL), event, fail=(mode,))
                    self.assertEqual(result['conclusion'], 'failure', result)
                    self.assertEqual(result['calls'], calls)
                    self.assertEqual(result['outcomes'][-1], (CONFIRM, 'skipped'))
                    self.assertEqual(next(x[1] for x in result['streams']
                                          if x[0] == REGRESSION), 7)
            for capture, calls in ((1, [NORMAL]), (2, [NORMAL, OPTIMIZED])):
                with self.subTest(event=event, failed_capture=capture):
                    result = run_job(source(CENTRAL), event, fail_capture=(capture,))
                    self.assertEqual(result['conclusion'], 'failure', result)
                    self.assertEqual(result['calls'], calls)
                    self.assertEqual(result['outcomes'][-1], (CONFIRM, 'skipped'))
                    self.assertEqual(next(x[1] for x in result['streams']
                                          if x[0] == REGRESSION), 8)

    @unittest.skipUnless(sys.version_info[:2] == (3, 11),
                         'real empty-discovery contract requires hosted CPython 3.11')
    def test_real_python311_original_and_candidate_zero_pass_fail_controls(self):
        original = self.original_central()
        for cases in (('empty', 'pass'), ('pass', 'empty'), ('empty', 'empty'),
                      ('pass', 'pass'), ('fail', 'pass'), ('pass', 'fail')):
            for candidate, text in ((False, original), (True, source(CENTRAL))):
                with self.subTest(candidate=candidate, cases=cases):
                    result = run_job(text, 'pull_request', real_cases=cases)
                    fails = 'fail' in cases or (candidate and 'empty' in cases)
                    expected = 'failure' if fails else 'success'
                    self.assertEqual(result['conclusion'], expected, result)
                    first_stops = cases[0] == 'fail' or (candidate and cases[0] == 'empty')
                    self.assertEqual(result['calls'], [NORMAL] if first_stops
                                     else [NORMAL, OPTIMIZED])
                    self.assertEqual(result['outcomes'][-1],
                                     (CONFIRM, 'skipped' if fails else 'success'))
                    regression = next(x for x in result['streams'] if x[0] == REGRESSION)
                    output = (regression[2] + regression[3]).decode()
                    self.assertIn('Ran ' + ('0 tests' if cases[0] == 'empty' else '1 test'),
                                  output)
                    if cases[0] == 'pass' and cases[1] == 'empty':
                        self.assertIn('Ran 0 tests', output)
                    if 'fail' in cases:
                        self.assertIn('FAILED (failures=1)', output)

    def test_job_preserves_foreign_git_state(self):
        # Real foreign repositories, never a caller's checkout. Setup and
        # observations use their own clean environment, independent of run_job.
        for selector in ('clean', 'GIT_DIR', 'GIT_INDEX_FILE', 'GIT_WORK_TREE',
                         'GIT_COMMON_DIR', 'GIT_OBJECT_DIRECTORY'):
            with self.subTest(selector=selector), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                foreign = root / 'foreign'
                foreign.mkdir()
                empty_template = root / 'empty-template'
                empty_template.mkdir()
                clean = {key: value for key, value in os.environ.items()
                         if not key.startswith('GIT_')}
                clean.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                             GIT_TEMPLATE_DIR=str(empty_template))

                def git(*args):
                    return subprocess.run(['git', *args], cwd=foreign, env=clean,
                                          check=True, capture_output=True, timeout=30).stdout

                tracked = foreign / 'foreign.txt'
                tracked.write_bytes(b'committed foreign content\n')
                git('init', '-q')
                git('add', '.')
                git('-c', 'user.name=Foreign Fixture', '-c', 'user.email=fixture@example.invalid',
                    '-c', 'commit.gpgsign=false', '-c', 'maintenance.auto=false',
                    'commit', '-qm', 'foreign fixture')
                tracked.write_bytes(b'unstaged foreign content\n')
                index = foreign / '.git/index'

                def snapshot():
                    return {'head': git('rev-parse', 'HEAD'),
                            'tree': git('rev-parse', 'HEAD^{tree}'),
                            'index_bytes': index.read_bytes(),
                            'index_entries': git('ls-files', '--stage'),
                            'worktree_bytes': tracked.read_bytes(),
                            'object_bytes': {str(p.relative_to(foreign)): p.read_bytes()
                                             for p in (foreign / '.git/objects').rglob('*')
                                             if p.is_file()}}

                before = snapshot()
                targets = {'GIT_DIR': foreign / '.git', 'GIT_INDEX_FILE': index,
                           'GIT_WORK_TREE': foreign, 'GIT_COMMON_DIR': foreign / '.git',
                           'GIT_OBJECT_DIRECTORY': foreign / '.git/objects'}
                caller = dict(clean)
                if selector != 'clean':
                    caller[selector] = str(targets[selector])
                with mock.patch.dict(os.environ, caller, clear=True):
                    try:
                        result = run_job(source(CENTRAL), 'pull_request')
                    except subprocess.CalledProcessError as exc:
                        self.fail('fixture must succeed under ' + selector + ': ' +
                                  repr(exc.stderr))
                    self.assertEqual(dict(os.environ), caller, 'caller environment was changed')
                after = snapshot()
                self.assertEqual(result['conclusion'], 'success', result)
                self.assertEqual(result['calls'], [NORMAL, OPTIMIZED])
                self.assertEqual(result['outcomes'][-1], (CONFIRM, 'success'))
                self.assertIn('tested-commit sha=' + result['head'], result['summary'])
                for field in before:
                    with self.subTest(field=field):
                        self.assertEqual(after[field], before[field])

    def test_job_ignores_inherited_git_config_and_templates(self):
        # Each real hook would leave a marker while returning success. Refusal
        # or a broken fixture is not accepted as successful isolation.
        for origin in ('count', 'parameters', 'global', 'system', 'home', 'template'):
            with self.subTest(origin=origin), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                hooks = root / 'template/hooks'
                hooks.mkdir(parents=True)
                hook = hooks / 'pre-commit'
                hook.write_text('#!/bin/sh\n: > "$FIXTURE_HOOK_MARKER"\n')
                hook.chmod(0o755)
                marker = root / 'hook-ran'
                config = root / 'config'
                config.write_text('[core]\n\thooksPath = ' + str(hooks) + '\n')
                home = root / 'home'
                home.mkdir()
                caller = {key: value for key, value in os.environ.items()
                          if not key.startswith('GIT_')}
                caller.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                              HOME=str(home), XDG_CONFIG_HOME=str(home / 'xdg'),
                              FIXTURE_HOOK_MARKER=str(marker))
                if origin == 'count':
                    caller.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.hooksPath',
                                  GIT_CONFIG_VALUE_0=str(hooks))
                elif origin == 'parameters':
                    caller['GIT_CONFIG_PARAMETERS'] = "'core.hooksPath=" + str(hooks) + "'"
                elif origin == 'global':
                    caller['GIT_CONFIG_GLOBAL'] = str(config)
                elif origin == 'system':
                    caller.pop('GIT_CONFIG_NOSYSTEM')
                    caller['GIT_CONFIG_SYSTEM'] = str(config)
                elif origin == 'home':
                    caller.pop('GIT_CONFIG_GLOBAL')
                    (home / '.gitconfig').write_bytes(config.read_bytes())
                else:
                    caller['GIT_TEMPLATE_DIR'] = str(hooks.parent)
                with mock.patch.dict(os.environ, caller, clear=True):
                    result = run_job(source(CENTRAL), 'pull_request')
                    self.assertEqual(dict(os.environ), caller, 'caller environment was changed')
                self.assertEqual(result['conclusion'], 'success', result)
                self.assertEqual(result['calls'], [NORMAL, OPTIMIZED])
                self.assertFalse(marker.exists(), 'inherited Git hook executed: ' + origin)

    def test_current_workflows_satisfy_contract(self):
        for workflow in (CENTRAL, *TRIO):
            with self.subTest(workflow=workflow):
                self.assertEqual(violations(workflow, source(workflow)), [])

    def original_manual(self, workflow):
        # Reverse only the manual suite body and the successor setup-python pin,
        # then authenticate the whole source at 6e502c1f. The packet, event
        # condition, and historical blob constants remain original.
        text = source(workflow)
        block = named(parse(text)[1], REGRESSION)['run']
        rendered = lambda body: ''.join('          ' + line + '\n'
                                        for line in body.splitlines())
        original = mutate(text, rendered(block), rendered(ORIGINAL_SUITE_BLOCK))
        original = mutate(original, CURRENT_SETUP_PYTHON, HISTORICAL_SETUP_PYTHON)
        data = original.encode()
        original_blobs = {
            'c6-palm-route': 'a9f1549911f68027b5ea778aeb74a82d1c76c16c',
            'd5-dimension-lift': '00a40395ea7ef0276259c84c345a61e98fa42d33',
            'c6-factorial-moment': 'b02e07ceedce6317013a8eea1c083a3cca989ff8',
        }
        self.assertEqual(hashlib.sha1(b'blob ' + str(len(data)).encode() +
                                      b'\0' + data).hexdigest(), original_blobs[workflow])
        return original

    def test_manual_original_accepts_synthetic_empty_success(self):
        for workflow in TRIO:
            original = self.original_manual(workflow)
            for counts in ((0, 2), (2, 0), (0, 0)):
                with self.subTest(workflow=workflow, counts=counts):
                    result = run_job(original, 'workflow_dispatch', counts=counts)
                    self.assertEqual(result['conclusion'], 'success', result)
                    self.assertEqual(result['calls'], [NORMAL, OPTIMIZED])
                    self.assertTrue(result['sentinel'])

    def test_manual_rejects_empty_success_before_packet(self):
        for workflow in TRIO:
            for counts, calls in (((0, 2), [NORMAL]), ((2, 0), [NORMAL, OPTIMIZED]),
                                  ((0, 0), [NORMAL])):
                with self.subTest(workflow=workflow, counts=counts):
                    result = run_job(source(workflow), 'workflow_dispatch', counts=counts)
                    self.assertEqual(result['conclusion'], 'failure', result)
                    self.assertEqual(result['calls'], calls)
                    self.assertFalse(result['sentinel'])
                    self.assertEqual(result['outcomes'][-1], (PACKET, 'skipped'))

    def test_manual_accepts_singular_and_multiple_successful_tests(self):
        for workflow in TRIO:
            for counts in ((1, 1), (2, 13), (13, 2)):
                with self.subTest(workflow=workflow, counts=counts):
                    result = run_job(source(workflow), 'workflow_dispatch', counts=counts)
                    self.assertEqual(result['conclusion'], 'success', result)
                    self.assertEqual(result['calls'], [NORMAL, OPTIMIZED])
                    self.assertTrue(result['sentinel'])

    def test_manual_requires_positive_summary_in_each_mode(self):
        good = 'Ran 2 tests in 0.001s'
        for workflow in TRIO:
            for bad in ('', 'Ran 00 tests in 0.001s', 'Ran 01 tests in 0.001s',
                        'Ran -1 tests in 0.001s', 'Ran 1.0 tests in 0.001s',
                        'Ran 1 test in unknown', 'prefix Ran 1 test in 0.001s',
                        'Ran 1 test in 0.001s suffix'):
                for index in (0, 1):
                    with self.subTest(workflow=workflow, summary=bad, mode=index):
                        summaries = [good, good]
                        summaries[index] = bad
                        result = run_job(source(workflow), 'workflow_dispatch',
                                         summaries=summaries)
                        self.assertEqual(result['conclusion'], 'failure', result)
                        self.assertEqual(result['calls'], [NORMAL] if index == 0
                                         else [NORMAL, OPTIMIZED])
                        self.assertFalse(result['sentinel'])
                        self.assertEqual(result['outcomes'][-1], (PACKET, 'skipped'))

    def test_manual_positive_summary_cannot_hide_child_or_capture_failure(self):
        for workflow in TRIO:
            for mode, calls in (('normal', [NORMAL]), ('optimized', [NORMAL, OPTIMIZED])):
                with self.subTest(workflow=workflow, failed_child=mode):
                    result = run_job(source(workflow), 'workflow_dispatch', fail=(mode,))
                    self.assertEqual(result['conclusion'], 'failure', result)
                    self.assertEqual(result['calls'], calls)
                    self.assertFalse(result['sentinel'])
                    self.assertEqual(result['outcomes'][-1], (PACKET, 'skipped'))
                    self.assertEqual(next(x[1] for x in result['streams']
                                          if x[0] == REGRESSION), 7)
            for capture, calls in ((1, [NORMAL]), (2, [NORMAL, OPTIMIZED])):
                with self.subTest(workflow=workflow, failed_capture=capture):
                    result = run_job(source(workflow), 'workflow_dispatch',
                                     fail_capture=(capture,))
                    self.assertEqual(result['conclusion'], 'failure', result)
                    self.assertEqual(result['calls'], calls)
                    self.assertFalse(result['sentinel'])
                    self.assertEqual(result['outcomes'][-1], (PACKET, 'skipped'))
                    self.assertEqual(next(x[1] for x in result['streams']
                                          if x[0] == REGRESSION), 8)

    def test_manual_real_discovery_original_and_guarded_controls(self):
        # No synthetic Python result here: run_job forwards unchanged argv to
        # this interpreter on generated fixtures. CPython 3.11 accepts empty
        # discovery; 3.12+ rejects it. Neither outcome is relabelled as the other.
        for workflow in TRIO:
            original = self.original_manual(workflow)
            for cases in (('empty', 'pass'), ('pass', 'empty'), ('empty', 'empty'),
                          ('pass', 'pass'), ('fail', 'pass'), ('pass', 'fail')):
                for candidate, text in ((False, original), (True, source(workflow))):
                    with self.subTest(workflow=workflow, candidate=candidate, cases=cases):
                        result = run_job(text, 'workflow_dispatch', real_cases=cases)
                        empty_fails = candidate or sys.version_info[:2] >= (3, 12)
                        fails = 'fail' in cases or (empty_fails and 'empty' in cases)
                        first_stops = cases[0] == 'fail' or (empty_fails and cases[0] == 'empty')
                        self.assertEqual(result['conclusion'], 'failure' if fails else 'success',
                                         result)
                        self.assertEqual(result['calls'], [NORMAL] if first_stops
                                         else [NORMAL, OPTIMIZED])
                        self.assertEqual(result['sentinel'], not fails)
                        self.assertEqual(result['outcomes'][-1],
                                         (PACKET, 'skipped' if fails else 'success'))
                        regression = next(x for x in result['streams'] if x[0] == REGRESSION)
                        output = (regression[2] + regression[3]).decode()
                        self.assertIn('Ran ' + ('0 tests' if cases[0] == 'empty' else '1 test'),
                                      output)
                        if cases == ('pass', 'empty'):
                            self.assertIn('Ran 0 tests', output)
                        if 'fail' in cases:
                            self.assertIn('FAILED (failures=1)', output)

    def test_manual_dispatch_runs_both_modes_before_packet(self):
        for workflow in TRIO:
            text = source(workflow)
            with self.subTest(workflow=workflow, case='pass'):
                result = run_job(text, 'workflow_dispatch')
                self.assertEqual(result['conclusion'], 'success')
                self.assertEqual(result['calls'], [NORMAL, OPTIMIZED])
                self.assertTrue(result['sentinel'])
            for mode, calls in (('normal', [NORMAL]), ('optimized', [NORMAL, OPTIMIZED])):
                with self.subTest(workflow=workflow, case=mode + ' fails'):
                    result = run_job(text, 'workflow_dispatch', fail=(mode,))
                    self.assertEqual(result['conclusion'], 'failure')
                    self.assertEqual(result['calls'], calls)
                    self.assertFalse(result['sentinel'])
                    self.assertIn((PACKET, 'skipped'), result['outcomes'])

    def test_pull_request_skips_only_duplicate_suite(self):
        for workflow in TRIO:
            with self.subTest(workflow=workflow):
                result = run_job(source(workflow), 'pull_request', fail=('normal', 'optimized'))
                self.assertEqual(result['conclusion'], 'success')
                self.assertEqual(result['calls'], [])
                self.assertTrue(result['sentinel'])
                self.assertEqual(result['outcomes'][3:], [(REGRESSION, 'skipped'), (PACKET, 'success')])

    def test_central_suite_runs_and_fails_in_both_modes(self):
        text = source(CENTRAL)
        for event in ('pull_request', 'workflow_dispatch'):
            with self.subTest(event=event):
                result = run_job(text, event)
                self.assertEqual(result['conclusion'], 'success')
                self.assertEqual(result['calls'], [NORMAL, OPTIMIZED])
                self.assertEqual(result['outcomes'][-1], (CONFIRM, 'success'))
                pr_head = ('1' * 40) if event == 'pull_request' else 'none'
                self.assertIn(f'tested-commit sha={result["head"]} ', result['summary'])
                self.assertIn(f' pr_head={pr_head} event={event} run=1234/1', result['summary'])
            for mode in ('normal', 'optimized'):
                with self.subTest(event=event, mode=mode):
                    result = run_job(text, event, fail=(mode,))
                    self.assertEqual(result['conclusion'], 'failure')
                    self.assertEqual(result['outcomes'][-1], (CONFIRM, 'skipped'))

    def test_trigger_split_routes_tests_only_changes_centrally(self):
        central = parse(source(CENTRAL))[0]['pull_request']
        for changed in ('tests/test_w8c_commit_identity_control.py', 'tools/any_shared_tool.py'):
            with self.subTest(changed=changed):
                self.assertTrue(covered(central, changed))
                for workflow in TRIO:
                    trio = parse(source(workflow))[0]['pull_request']
                    self.assertFalse(covered(trio, changed), workflow)
        for workflow, packet_dir in TRIO.items():
            trio = parse(source(workflow))[0]['pull_request']
            for changed in ('frontiers/' + packet_dir + '/RESULTS.json', 'tools/d5_c6_replay.py',
                            'tests/test_d5_c6_workflows.py', '.github/workflows/' + workflow + '.yml'):
                with self.subTest(workflow=workflow, changed=changed):
                    self.assertTrue(covered(trio, changed))
                    self.assertTrue(covered(central, changed))

    def test_meaningful_negatives_are_detected(self):
        central = source(CENTRAL)
        cases = {
            'central drops normal mode': (CENTRAL, central,
                                          '          python -B -S -m unittest discover -s tests -v 2>&1 | tee "$log_dir/normal.log"\n', ''),
            'central drops optimized mode': (CENTRAL, central,
                                             '          python -B -O -S -m unittest discover -s tests -v 2>&1 | tee "$log_dir/optimized.log"\n', ''),
            'central swallows failure': (CENTRAL, central, '.log"\n', '.log" || true\n', 4),
            'central loses tests trigger': (CENTRAL, central, "      - 'tests/**'\n", ''),
            'central loses tools trigger': (CENTRAL, central, "      - 'tools/**'\n", ''),
            'central loses a frontier trigger': (CENTRAL, central, "      - 'frontiers/c6_palm_route_20260929/**'\n", ''),
            'central loses a workflow trigger': (CENTRAL, central, "      - '.github/workflows/d5-dimension-lift.yml'\n", ''),
            'central adds push': (CENTRAL, central, '  workflow_dispatch:\n', '  workflow_dispatch:\n  push:\n'),
            'central gains a condition': (CENTRAL, central, '      - name: Full repository regression suite in both Python modes\n',
                                          '      - name: Full repository regression suite in both Python modes\n'
                                          "        if: github.event_name == 'workflow_dispatch'\n"),
            'central continue-on-error': (CENTRAL, central, '    timeout-minutes: 45\n', '    timeout-minutes: 45\n    continue-on-error: true\n'),
            'central unbinds commit': (CENTRAL, central, '          if [ "$checked_out" != "$TESTED_SHA" ]; then\n',
                                       '          if false; then\n'),
        }
        for workflow in TRIO:
            text = source(workflow)
            cases.update({
                workflow + ' drops manual guard': (workflow, text, "        if: github.event_name == 'workflow_dispatch'\n", ''),
                workflow + ' always-runs suite': (workflow, text, "if: github.event_name == 'workflow_dispatch'", 'if: always()'),
                workflow + ' broad guard': (workflow, text, "if: github.event_name == 'workflow_dispatch'",
                                            "if: github.event_name != 'pull_request'"),
                workflow + ' guards packet too': (workflow, text, '      - name: ' + PACKET + '\n',
                                                  '      - name: ' + PACKET + '\n'
                                                  "        if: github.event_name == 'workflow_dispatch'\n"),
                workflow + ' removes suite step': (workflow, text,
                                                   "      - name: " + REGRESSION + "\n"
                                                   "        if: github.event_name == 'workflow_dispatch'\n"
                                                   "        run: |\n" + ''.join('          ' + l + '\n' for l in MANUAL_SUITE_BLOCK.splitlines()),
                                                   ''),
                workflow + ' drops optimized mode': (workflow, text, '          python -B -O -S -m unittest discover -s tests -v 2>&1 | tee "$log_dir/optimized.log"\n', ''),
                workflow + ' swallows failure': (workflow, text, 'python -B -S -m unittest discover -s tests -v 2>&1 | tee "$log_dir/normal.log"\n',
                                                 'python -B -S -m unittest discover -s tests -v 2>&1 | tee "$log_dir/normal.log" || true\n'),
                workflow + ' restores tests/** duplication': (workflow, text, "      - 'tests/test_d5_c6_workflows.py'\n",
                                                             "      - 'tests/test_d5_c6_workflows.py'\n      - 'tests/**'\n"),
                workflow + ' loses helper trigger': (workflow, text, "      - 'tools/d5_c6_replay.py'\n", ''),
                workflow + ' changes packet bytes': (workflow, text, "              replay(script, expected, mutants, ",
                                                     "              replay(script, expected, mutants[:-1], "),
                workflow + ' unbinds commit': (workflow, text, '            exit 1\n', '            true\n'),
            })
        for label, spec in cases.items():
            workflow, text, old, new = spec[:4]
            count = spec[4] if len(spec) > 4 else 1
            with self.subTest(mutant=label):
                self.assertNotEqual(violations(workflow, mutate(text, old, new, count)), [], label)

    def test_parser_fails_closed(self):
        text = source(CENTRAL)
        for old, new in (("      - 'tools/**'\n", "      - tools/**\n"),
                         ('    steps:\n', '    strategy: {}\n    steps:\n'),
                         ('        run: |\n          set -euo pipefail\n          log_dir=',
                          '        run: set -euo pipefail\n        shell: bash\n        run2: |\n          log_dir=')):
            with self.subTest(old=old):
                with self.assertRaises(ValueError):
                    parse(mutate(text, old, new))


if __name__ == '__main__':
    unittest.main()
