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
SUITE_BLOCK = ('set -euo pipefail\n'
               'python -B -S -m unittest discover -s tests -v\n'
               'python -B -O -S -m unittest discover -s tests -v\n')
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

    def indent(line):
        return len(line) - len(line.lstrip(' '))

    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.startswith('#'):
            i += 1
            continue
        if line.startswith('name: ') or line in ('permissions:', '  contents: read', 'jobs:'):
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
    return on, job


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


def run_job(text, event, fail=(), sha_override=None):
    """Run the job's steps locally with a fake python; packet -> sentinel."""
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
        fake.write_text('#!/bin/sh\n'
                        'printf "%s\\n" "$*" >> "$FAKE_LOG"\n'
                        'case " $* " in *" -O "*) mode=optimized ;; *) mode=normal ;; esac\n'
                        'case " $FAKE_FAIL " in *" $mode "*) exit 7 ;; esac\n'
                        'exit 0\n')
        fake.chmod(0o755)
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
                            GITHUB_STEP_SUMMARY=str(summary))
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
            outcomes.append((name, 'success' if cp.returncode == 0 else 'failure'))
            failed = failed or cp.returncode != 0
        calls = [line.split() for line in log.read_text().splitlines()] if log.exists() else []
        return {
            'conclusion': 'failure' if failed else 'success',
            'outcomes': outcomes,
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
    if set(on) != {'pull_request', 'workflow_dispatch'} or on['workflow_dispatch'] is not None:
        problems.append('events must be exactly pull_request(paths) + workflow_dispatch')
    for key in ('continue-on-error', 'always()', 'failure()', 'cancelled()', 'background:'):
        if key in text:
            problems.append('bypass marker present: ' + key)
    uses = [s.get('uses') for s in job['steps'] if 'uses' in s]
    if uses != ['actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1',
                'actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97']:
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
    if suite.get('run') != SUITE_BLOCK:
        problems.append('suite block must be both literal discovery modes under set -euo pipefail')
    central_bind = named(parse((WORKFLOWS / (CENTRAL + '.yml')).read_text())[1], BIND)
    if bind != central_bind:
        problems.append('tested-commit binding step differs from the central workflow')
    if workflow == CENTRAL:
        if job['id'] != 'full-suite' or job.get('timeout-minutes') != '20':
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
            'central drops normal mode': (CENTRAL, central, '          python -B -S -m unittest discover -s tests -v\n', ''),
            'central drops optimized mode': (CENTRAL, central, '          python -B -O -S -m unittest discover -s tests -v\n', ''),
            'central swallows failure': (CENTRAL, central, 'discover -s tests -v\n', 'discover -s tests -v || true\n', 2),
            'central loses tests trigger': (CENTRAL, central, "      - 'tests/**'\n", ''),
            'central loses tools trigger': (CENTRAL, central, "      - 'tools/**'\n", ''),
            'central loses a frontier trigger': (CENTRAL, central, "      - 'frontiers/c6_palm_route_20260929/**'\n", ''),
            'central loses a workflow trigger': (CENTRAL, central, "      - '.github/workflows/d5-dimension-lift.yml'\n", ''),
            'central adds push': (CENTRAL, central, '  workflow_dispatch:\n', '  workflow_dispatch:\n  push:\n'),
            'central gains a condition': (CENTRAL, central, '      - name: Full repository regression suite in both Python modes\n',
                                          '      - name: Full repository regression suite in both Python modes\n'
                                          "        if: github.event_name == 'workflow_dispatch'\n"),
            'central continue-on-error': (CENTRAL, central, '    timeout-minutes: 20\n', '    timeout-minutes: 20\n    continue-on-error: true\n'),
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
                                                   "        run: |\n" + ''.join('          ' + l + '\n' for l in SUITE_BLOCK.splitlines()),
                                                   ''),
                workflow + ' drops optimized mode': (workflow, text, '          python -B -O -S -m unittest discover -s tests -v\n', ''),
                workflow + ' swallows failure': (workflow, text, 'python -B -S -m unittest discover -s tests -v\n',
                                                 'python -B -S -m unittest discover -s tests -v || true\n'),
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
                         ('        run: |\n          set -euo pipefail\n          python',
                          '        run: set -euo pipefail\n        shell: bash\n        run2: |\n          python')):
            with self.subTest(old=old):
                with self.assertRaises(ValueError):
                    parse(mutate(text, old, new))


if __name__ == '__main__':
    unittest.main()
