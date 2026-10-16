"""Complete-shell regression fixtures; synthetic protocols, not theorem proofs."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKET = 'frontiers/remainder_rate_20260930'
WORKFLOW = ROOT / '.github/workflows/remainder-rate.yml'
HELPER = ROOT / 'tools/remainder_rate_replay.py'
STAGES = ('baseline', 'M1', 'M2', 'M3', 'M4', 'M9')
# Independently measured native reports, not imported from the production helper.
BASELINE = {'checks': {'E1_exponent_ledger': {'info': {'grid_points': 208, 'relative_exponents': {'v1': '1/2', 'v1.1': '7/12'}, 'twelfth_power_points': 4, 'v1': {'rate': '1/6', 'theta': '1/6'}, 'v1.1': {'rate': '1/4', 'theta': '1/12'}}, 'passed': True}, 'E2_barrier_arithmetic': {'info': {'barrier_cases': 48, 'solved_form_points': 4}, 'passed': True}, 'E3_soft_eigenvalue_determinant': {'info': {'matrices': 5, 'sizes': [2, 3, 4]}, 'passed': True}, 'E4_integrals_and_cutoff_ledger': {'info': {'cutoff_ledger_points': 3, 'integral_points': 3, 'window_integral_points': 3}, 'passed': True}, 'E5_sign_window': {'info': {'exact_equality_cases': 0, 'near_boundary_case': True, 'same_sign_instances': 13858, 'typed_instances': 15962}, 'passed': True}}, 'mutant': None, 'object': 'CL-D2-REMAINDER-RATE-20260930-v1.1', 'passed': True, 'scientific_effect': 'NONE'}
MUTATIONS = {'M1': ('E1_exponent_ledger', {'info': 'v1.1 ledger minimum at theta = 1/12 is 1/4, not the claimed rate 1/3', 'passed': False}), 'M2': ('E2_barrier_arithmetic', {'info': 'cubic term not dominated at t = 3/25 (lambda 1/5, K 3)', 'passed': False}), 'M3': ('E3_soft_eigenvalue_determinant', {'info': "det <= lambda_min lambda_max^(d-1) fails (spectrum ['1/100', '2'])", 'passed': False}), 'M4': ('E5_sign_window', {'info': '|det K_i| bound fails at (Fraction(0, 1), Fraction(-2, 1), Fraction(-3, 1), Fraction(1, 3), Fraction(-2, 5), Fraction(1, 10))', 'passed': False})}
REPORTS = {'baseline': BASELINE}
for name, (check, value) in MUTATIONS.items():
    report = copy.deepcopy(BASELINE)
    report['mutant'] = name
    report['passed'] = False
    report['checks'][check] = value
    REPORTS[name] = report


def replay_shell(text):
    marker = '      - name: Verify sources, replay both modes, reject mutants\n'
    if text.count(marker) != 1:
        raise ValueError('exactly one original replay step required')
    tail = text.split(marker, 1)[1].split('        run: |\n', 1)[1]
    lines = []
    for line in tail.splitlines():
        if line and not line.startswith('          '):
            break
        lines.append(line[10:] if line else '')
    if not lines or lines[0] != 'set -euo pipefail':
        raise ValueError('strict shell missing')
    return '\n'.join(lines) + '\n'


def identity(path, data):
    return {'path': path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()}


def checker_source():
    # This child never imports production validation or learns its own oracle.
    return 'import json, os, sys\nfrom pathlib import Path\nreports = ' + repr(REPORTS) + r'''
a = sys.argv[1:]
name = 'baseline' if not a else a[1] if len(a) == 2 and a[0] == '--mutant' else 'BAD'
if name not in ('baseline', 'M1', 'M2', 'M3', 'M4', 'M9'):
    raise RuntimeError('unexpected command inventory')
mode = sys.flags.optimize
with open(os.environ['REMAINDER_TRACE'], 'a') as f:
    f.write(json.dumps([mode, name])+'\n')
code = 0 if name == 'baseline' else 2 if name == 'M9' else 1
out = b'' if name == 'M9' else (json.dumps(reports[name], indent=1, sort_keys=True)+'\n').encode()
err = b'unknown mutant label\n' if name == 'M9' else b''
if os.environ['REMAINDER_CASE'] == 'dirty':
    Path(os.environ['REMAINDER_RESULTS']).write_text('changed after preflight\n')
if name == os.environ['REMAINDER_STAGE'] and mode == int(os.environ['REMAINDER_MODE']):
    case = os.environ['REMAINDER_CASE']
    if case == 'crash': raise RuntimeError('unrelated synthetic crash')
    if case == 'silent': out = b''; err = b''
    elif case == 'garbage': out = b'not the intended report\n'
    elif case == 'stderr': err += b'unrelated stderr\n'
    elif case == 'wrong-exit': code = 0 if name != 'baseline' else 1
    elif case == 'signal': os.kill(os.getpid(), 15)
    elif case == 'unknown-wrong': err = b'an unrelated error\n'
    elif case == 'unknown-extra': out = b'not empty\n'
    elif case == 'unknown-prefix': err = b'prefix unknown mutant label\n'
    elif case == 'formatted': out = (' \n'+json.dumps(reports[name], indent=3)+' \n').encode()
    elif name != 'M9':
        row = reports[name]
        if case == 'wrong-reason':
            for v in row['checks'].values():
                if v['passed'] is False: v['info'] = 'unrelated reason'
        elif case == 'wrong-mutant': row['mutant'] = 'M4' if name != 'M4' else 'M1'
        elif case == 'integer-bool': row['passed'] = int(row['passed'])
        elif case == 'nested-bool': row['checks']['E4_integrals_and_cutoff_ledger']['passed'] = 1
        elif case == 'nested-float': row['checks']['E4_integrals_and_cutoff_ledger']['info']['integral_points'] = 3.0
        elif case == 'wrong-positive-info': row['checks']['E4_integrals_and_cutoff_ledger']['info']['integral_points'] = 4
        elif case == 'missing': del row['checks']['E4_integrals_and_cutoff_ledger']
        elif case == 'extra': row['checks']['extra'] = {'passed': True}
        elif case == 'wrong-object': row['object'] = 'UNRELATED'
        elif case == 'array': row = [row]
        out = (json.dumps(row, indent=1, sort_keys=True)+'\n').encode()
        if case == 'duplicate': out = out.rstrip()[:-1] + b',"passed":false}\n'
        elif case == 'nonfinite': out = out.replace(b'15962', b'NaN')
        elif case == 'trailing': out += b'{}\n'
        elif case == 'bad-utf8': out = b'\xff'+out
sys.stdout.buffer.write(out);sys.stderr.buffer.write(err);sys.exit(code)
'''


class RemainderWorkflowTests(unittest.TestCase):
    def run_case(self, case='valid', stage='baseline', mode=0, guard=None):
        with tempfile.TemporaryDirectory(prefix='remainder-fixture-') as tmp:
            home = Path(tmp); repo = home/'repo'; repo.mkdir()
            packet = repo/PACKET; packet.mkdir(parents=True)
            trace = home/'calls.jsonl'
            (packet/'rate_ledger_check.py').write_text(checker_source())
            (packet/'RESULTS.json').write_text(json.dumps(BASELINE, indent=1, sort_keys=True)+'\n')
            records = {}
            for name in ('consumed', 'cited_only', 'consumed_unmerged'):
                data = ('synthetic pinned '+name+'\n').encode()
                (repo/(name+'.txt')).write_bytes(data)
                records[name] = [identity(name+'.txt',data)]
            records.update(files=[identity(x.name,x.read_bytes()) for x in sorted(packet.iterdir())],
                           mutants=['M1','M2','M3','M4'])
            (packet/'SOURCES.json').write_text(json.dumps(records))
            if HELPER.exists():
                (repo/'tools').mkdir();shutil.copyfile(HELPER,repo/'tools'/HELPER.name)
            env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
            env.update(HOME=str(home),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,
                GIT_AUTHOR_NAME='Fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',
                GIT_COMMITTER_NAME='Fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid',
                PYTHONDONTWRITEBYTECODE='1',REMAINDER_TRACE=str(trace),REMAINDER_CASE=case,
                REMAINDER_STAGE=stage,REMAINDER_MODE=str(mode),REMAINDER_RESULTS=str(packet/'RESULTS.json'))
            env['PATH']=str(Path(sys.executable).parent)+os.pathsep+env.get('PATH','')
            for args in (['init','-q'],['config','core.hooksPath',os.devnull],
                         ['config','commit.gpgsign','false'],['config','maintenance.auto','false'],
                         ['config','gc.auto','0'],['add','.'],['commit','-qm','synthetic controls']):
                subprocess.run(['git',*args],cwd=repo,env=env,capture_output=True,check=True,timeout=15)
            if guard == 'source':
                with (packet/'rate_ledger_check.py').open('a') as f:f.write('\n# altered source\n')
            elif guard in ('consumed','cited_only','consumed_unmerged'):
                (repo/(guard+'.txt')).write_bytes(b'changed pin\n')
            elif guard == 'extra': (packet/'extra.txt').write_bytes(b'extra')
            elif guard == 'missing': (packet/'RESULTS.json').unlink()
            elif guard == 'symlink':
                shutil.copyfile(packet/'RESULTS.json',home/'target');(packet/'RESULTS.json').unlink()
                (packet/'RESULTS.json').symlink_to(home/'target')
            elif guard == 'mutant-inventory':
                records['mutants']=['M1','M2','M3'];(packet/'SOURCES.json').write_text(json.dumps(records))
                subprocess.run(['git','add','.'],cwd=repo,env=env,check=True,capture_output=True,timeout=15)
                subprocess.run(['git','commit','-qm','coherent inventory variant'],cwd=repo,env=env,check=True,capture_output=True,timeout=15)
            result=subprocess.run(['bash','--noprofile','--norc','-c',replay_shell(WORKFLOW.read_text())],
                                  cwd=repo,env=env,capture_output=True,timeout=20)
            calls=[json.loads(x) for x in trace.read_text().splitlines()] if trace.exists() else []
            if saved:=os.environ.get('REMAINDER_SAVE'):
                dest=Path(saved)/(case+'-'+stage+'-'+str(mode)+'-'+str(guard));dest.mkdir(parents=True,exist_ok=True)
                (dest/'stdout').write_bytes(result.stdout);(dest/'stderr').write_bytes(result.stderr)
                (dest/'record.json').write_text(json.dumps({'case':case,'stage':stage,'mode':mode,
                    'guard':guard,'returncode':result.returncode,'calls':calls},sort_keys=True)+'\n')
            return result,calls

    def reject_at(self, case, stage, mode):
        result,calls=self.run_case(case,stage,mode)
        order=[[m,s] for m in (0,1) for s in STAGES]
        end=order.index([mode,stage])+1
        self.assertIn([mode,stage],calls,'intended stage not reached')
        self.assertNotEqual(result.returncode,0,'invalid admission: '+repr((case,stage,mode)))
        self.assertEqual(calls,order[:end],'rejection must stop at the intended stage')

    def test_valid_full_inventory(self):
        result,calls=self.run_case()
        self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))
        self.assertEqual(calls,[[m,s] for m in (0,1) for s in STAGES])

    def test_each_mutant_reason_crash_and_silence(self):
        for case in ('wrong-reason','crash','silent','stderr','garbage','wrong-mutant'):
            for mode in (0,1):
                for stage in STAGES[1:5]:
                    with self.subTest(case=case,mode=mode,stage=stage):self.reject_at(case,stage,mode)

    def test_complete_nested_json_contract(self):
        for case in ('integer-bool','nested-bool','nested-float','wrong-positive-info',
                     'missing','extra','wrong-object','array','duplicate','nonfinite','trailing','bad-utf8'):
            for mode in (0,1):
                with self.subTest(case=case,mode=mode):self.reject_at(case,'M1',mode)

    def test_baseline_exact_bytes_exit_and_stderr(self):
        for case in ('silent','garbage','stderr','wrong-exit','formatted'):
            for mode in (0,1):
                with self.subTest(case=case,mode=mode):self.reject_at(case,'baseline',mode)

    def test_unknown_label_exact_contract(self):
        for case in ('silent','unknown-wrong','unknown-extra','unknown-prefix','wrong-exit','signal'):
            for mode in (0,1):
                with self.subTest(case=case,mode=mode):self.reject_at(case,'M9',mode)

    def test_mutant_formatting_and_wrong_exits(self):
        for mode in (0,1):
            for stage in STAGES[1:5]:
                with self.subTest(mode=mode,stage=stage):
                    result,calls=self.run_case('formatted',stage,mode)
                    self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))
                    self.assertEqual(calls,[[m,s]for m in (0,1)for s in STAGES])
                    self.reject_at('wrong-exit',stage,mode)

    def test_guards_stop_before_replay(self):
        for guard in ('source','consumed','cited_only','consumed_unmerged','extra','missing','symlink'):
            with self.subTest(guard=guard):
                result,calls=self.run_case(guard=guard)
                self.assertNotEqual(result.returncode,0);self.assertEqual(calls,[])

    def test_full_mutant_inventory_required(self):
        result,calls=self.run_case(guard='mutant-inventory')
        self.assertNotEqual(result.returncode,0);self.assertEqual(calls,[])

    def test_tracked_mutation_fails_postflight(self):
        result,calls=self.run_case('dirty')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(calls,[[m,s]for m in (0,1)for s in STAGES])
        self.assertIn(b'changed after preflight',result.stdout)

    def test_regression_is_wired_in_both_modes(self):
        text=WORKFLOW.read_text()
        for path in ('tools/remainder_rate_replay.py','tests/test_remainder_rate_workflow.py'):
            self.assertIn("- '"+path+"'",text)
        for flags in ('-B -S','-B -O -S'):
            self.assertIn('python '+flags+' -m unittest discover -s tests -p test_remainder_rate_workflow.py -v',text)


# Persistent successor of the author-side offline #191 fallback diagnostic.
FALLBACK_CASES = [
    ('valid_remote', True, None, None, 1, 1),
    ('valid_two_remote', True, None, None, 2, 2),
    ('valid_tree', True, None, None, 0, 1),
    ('tree_avoids_network_error', True, None, None, 0, 1),
    ('wrong_remote_bytes', False, 'ValueError', 'pinned blob', 1, 0),
    ('wrong_remote_length', False, 'ValueError', 'pinned blob', 1, 0),
    ('wrong_sha256_pin', False, 'ValueError', 'pinned blob', 1, 0),
    ('wrong_blob_pin', False, 'ValueError', 'pinned blob', 1, 0),
    ('wrong_size_pin', False, 'ValueError', 'pinned blob', 1, 0),
    ('wrong_encoding', False, 'ValueError', 'unexpected blob encoding', 1, 0),
    ('missing_content', False, 'KeyError', 'content', 1, 0),
    ('invalid_json', False, 'JSONDecodeError', None, 1, 0),
    ('invalid_base64', False, 'Error', None, 1, 0),
    ('empty_content', False, 'ValueError', 'pinned blob', 1, 0),
    ('http_error', False, 'HTTPError', '503', 1, 0),
    ('network_timeout', False, 'TimeoutError', 'offline timeout', 1, 0),
    ('missing_repository', False, 'KeyError', 'GH_REPOSITORY', 0, 0),
    ('missing_token', False, 'KeyError', 'GH_TOKEN', 0, 0),
    ('tree_tamper', False, 'ValueError', 'via tree', 0, 0),
    ('second_remote_tamper', False, 'ValueError', 'pinned blob', 2, 1),
    ('packet_hash_tamper', False, 'ValueError', 'packet file identity', 0, 0),
    ('consumed_pin_tamper', False, 'ValueError', 'merged source drifted', 0, 0),
    ('cited_pin_tamper', False, 'ValueError', 'merged source drifted', 0, 0),
    ('extra_packet_member', False, 'ValueError', 'packet tree differs', 0, 0),
    ('packet_symlink', False, 'ValueError', 'symlink:', 0, 0),
]


def fallback_observation(case):
    """Run the actual preflight with an offline transport in an isolated child.

    The production change that should break these tests is weakened dependency
    authentication, changed request identity, or replacement of transport errors.
    This function never runs the numerical checker or contacts a remote server.
    """
    import base64
    import contextlib
    import io
    import urllib.error
    import urllib.request

    if case not in {row[0] for row in FALLBACK_CASES}:
        raise ValueError('unknown offline fallback case')
    shell = replay_shell(WORKFLOW.read_text())
    opening = "python -B -S - <<'PY'\n"
    stopping = "sys.path.insert(0, str(pathlib.Path('tools').resolve()))"
    if shell.count(opening) != 1 or shell.count(stopping) != 1:
        raise ValueError('ambiguous source-preflight boundary')
    source = shell.split(opening, 1)[1].split(stopping, 1)[0]
    remote_bytes = b'Synthetic immutable remote source for offline probe.\n'
    repository = 'example/offline-fixture'
    placeholder = 'offline-placeholder-not-a-real-token'
    calls: list[dict] = []
    injected = None
    observed_error = None
    stdout = io.StringIO()
    with tempfile.TemporaryDirectory(prefix='pr356-offline-preflight-') as tmp:
        root = Path(tmp)
        packet = root / PACKET
        packet.mkdir(parents=True)
        payload = b'Synthetic packet member; no checker is executed.\n'
        (packet / 'NOTE.txt').write_bytes(payload)
        consumed = b'Synthetic consumed source\n'
        cited = b'Synthetic cited source\n'
        (root / 'consumed.txt').write_bytes(consumed)
        (root / 'cited.txt').write_bytes(cited)
        remote_rows = [identity('remote/proof.md', remote_bytes)]
        if case in ('valid_two_remote', 'second_remote_tamper'):
            remote_rows.append(identity('remote/second.md', remote_bytes + b'second\n'))
        manifest = {'files': [identity('NOTE.txt', payload)],
                    'consumed': [identity('consumed.txt', consumed)],
                    'cited_only': [identity('cited.txt', cited)],
                    'consumed_unmerged': remote_rows}
        if case in ('valid_tree', 'tree_avoids_network_error', 'tree_tamper'):
            (root / 'remote').mkdir()
            (root / 'remote/proof.md').write_bytes(remote_bytes if case != 'tree_tamper' else remote_bytes.replace(b'Synthetic', b'synthetic', 1))
        if case == 'wrong_sha256_pin': remote_rows[0]['sha256'] = '0' * 64
        if case == 'wrong_blob_pin': remote_rows[0]['git_blob'] = '0' * 40
        if case == 'wrong_size_pin': remote_rows[0]['bytes'] += 1
        if case == 'packet_hash_tamper': (packet / 'NOTE.txt').write_bytes(payload + b'x')
        if case == 'consumed_pin_tamper': (root / 'consumed.txt').write_bytes(consumed + b'x')
        if case == 'cited_pin_tamper': (root / 'cited.txt').write_bytes(cited + b'x')
        if case == 'extra_packet_member': (packet / 'EXTRA').write_bytes(b'x')
        if case == 'packet_symlink':
            (root / 'outside.txt').write_bytes(payload)
            (packet / 'NOTE.txt').unlink()
            (packet / 'NOTE.txt').symlink_to(root / 'outside.txt')
        (packet / 'SOURCES.json').write_text(json.dumps(manifest), encoding='utf-8')

        def transport(request, timeout=None):
            nonlocal injected
            n = len(calls)
            if n >= len(remote_rows):
                raise RuntimeError('unexpected extra network invocation')
            row = remote_rows[n]
            call = {'url': request.full_url, 'method': request.get_method(),
                    'timeout': timeout,
                    'authorization_matches_placeholder': request.get_header('Authorization') == 'Bearer ' + placeholder,
                    'accept': request.get_header('Accept')}
            calls.append(call)
            expected = 'https://api.github.com/repos/' + repository + '/git/blobs/' + row['git_blob']
            if request.full_url != expected or request.get_method() != 'GET':
                raise RuntimeError('offline request URL/method mismatch')
            if timeout != 60 or not call['authorization_matches_placeholder'] or call['accept'] != 'application/vnd.github+json':
                raise RuntimeError('offline request timeout/header mismatch')
            if case in ('http_error', 'tree_avoids_network_error'):
                injected = urllib.error.HTTPError(expected, 503, 'offline service error', {}, None)
                raise injected
            if case == 'network_timeout':
                injected = TimeoutError('offline timeout')
                raise injected
            raw = remote_bytes if n == 0 else remote_bytes + b'second\n'
            if case == 'wrong_remote_bytes' or (case == 'second_remote_tamper' and n == 1):
                raw = raw.replace(b'Synthetic', b'synthetic', 1)
            if case == 'wrong_remote_length': raw += b'x'
            body = {'encoding': 'base64', 'content': base64.b64encode(raw).decode('ascii')}
            if case == 'wrong_encoding': body['encoding'] = 'utf-8'
            if case == 'missing_content': del body['content']
            if case == 'empty_content': body['content'] = ''
            if case == 'invalid_base64': body['content'] = 'a'
            data = b'not json' if case == 'invalid_json' else json.dumps(body).encode('utf-8')
            return io.BytesIO(data)

        old_cwd = Path.cwd()
        saved_env = {k: os.environ.get(k) for k in ('GH_TOKEN', 'GH_REPOSITORY')}
        original_urlopen = urllib.request.urlopen
        try:
            os.chdir(root)
            os.environ['GH_TOKEN'] = placeholder
            os.environ['GH_REPOSITORY'] = repository
            if case == 'missing_token': os.environ.pop('GH_TOKEN')
            if case == 'missing_repository': os.environ.pop('GH_REPOSITORY')
            urllib.request.urlopen = transport
            try:
                with contextlib.redirect_stdout(stdout):
                    exec(compile(source, '<actual-remainder-preflight>', 'exec'), {})
            except Exception as error:
                observed_error = {'type': type(error).__name__, 'message': str(error),
                                  'same_injected_exception': injected is not None and error is injected}
        finally:
            urllib.request.urlopen = original_urlopen
            os.chdir(old_cwd)
            for key, value in saved_env.items():
                if value is None: os.environ.pop(key, None)
                else: os.environ[key] = value
    records = [json.loads(line) for line in stdout.getvalue().splitlines()]
    return {'case': case, 'success': observed_error is None,
            'exception': observed_error, 'network_calls': calls, 'accepted_records': records,
            'preflight_sha256': hashlib.sha256(source.encode()).hexdigest()}


class RemainderFallbackTests(unittest.TestCase):
    """Offline regression of real workflow source, with transport-only injection.

    Each case is a fresh Python process and temporary filesystem. Existing
    complete-shell tests above remain separate and do not mock subprocesses.
    """

    def check_fallback_case(self, expected):
        case, success, error_type, reason, requests, accepted = expected
        flags = ['-B', '-S'] + (['-O'] if sys.flags.optimize else [])
        code = ("import json, runpy, sys; "
                "module=runpy.run_path(sys.argv[1], run_name='offline_fallback'); "
                "print(json.dumps(module['fallback_observation'](sys.argv[2]), sort_keys=True))")
        result = subprocess.run([sys.executable, *flags, '-c', code,
                                 str(Path(__file__).resolve()), case],
                                capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
        self.assertEqual(result.stderr, b'')
        observed = json.loads(result.stdout)
        self.assertEqual(observed['case'], case)
        self.assertEqual(observed['success'], success, 'fallback disposition')
        error = observed['exception']
        self.assertEqual(None if error is None else error['type'], error_type,
                         'source-local failure type')
        if reason is not None:
            self.assertIn(reason, error['message'], 'source-local failure reason')
        self.assertEqual(len(observed['network_calls']), requests, 'transport call count')
        self.assertEqual(len(observed['accepted_records']), accepted,
                         'verified dependency count')
        if case in ('http_error', 'network_timeout'):
            self.assertTrue(error['same_injected_exception'], 'original exception identity')
        for n, record in enumerate(observed['accepted_records']):
            path = 'remote/proof.md' if n == 0 else 'remote/second.md'
            data = b'Synthetic immutable remote source for offline probe.\n'
            if n:
                data += b'second\n'
            via = 'tree' if case in ('valid_tree', 'tree_avoids_network_error') else 'blob api'
            self.assertEqual(record, {'consumed_unmerged_verified': path,
                                      'git_blob': identity(path, data)['git_blob'], 'via': via})

    def test_fallback_valid_remote_and_local_preference(self):
        for case in FALLBACK_CASES:
            if case[1]:
                with self.subTest(case=case[0]):
                    self.check_fallback_case(case)

    def test_fallback_response_and_identity_rejections(self):
        for case in FALLBACK_CASES:
            if case[0] in ('wrong_remote_bytes', 'wrong_remote_length', 'wrong_sha256_pin',
                           'wrong_blob_pin', 'wrong_size_pin', 'wrong_encoding',
                           'missing_content', 'invalid_json', 'invalid_base64', 'empty_content',
                           'missing_repository', 'missing_token', 'second_remote_tamper'):
                with self.subTest(case=case[0]):
                    self.check_fallback_case(case)

    def test_fallback_preflight_guards_stop_network(self):
        for case in FALLBACK_CASES:
            if case[0] in ('tree_tamper', 'packet_hash_tamper', 'consumed_pin_tamper',
                           'cited_pin_tamper', 'extra_packet_member', 'packet_symlink'):
                with self.subTest(case=case[0]):
                    self.check_fallback_case(case)

    def test_fallback_transport_preserves_exception(self):
        for case in FALLBACK_CASES:
            if case[0] in ('http_error', 'network_timeout'):
                with self.subTest(case=case[0]):
                    self.check_fallback_case(case)


if __name__ == '__main__':
    unittest.main()
