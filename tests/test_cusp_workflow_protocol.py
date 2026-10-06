"""Complete-shell protocol tests; synthetic checkers, real Git and subprocesses.

The expected report bodies below are characterized from the unchanged checker
at 11f9127f. No mathematical result or subprocess outcome is mocked. A child
emits recorded carriers instead of redoing the numerical calculation. Source
preflight and final clean-tree checks run unchanged around those real children.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(os.environ.get('CUSP_WORKFLOW_ROOT', Path(__file__).resolve().parents[1]))
WORKFLOW = ROOT / '.github/workflows/cusp-second-order.yml'
PACKET = Path('frontiers/cusp_second_order_20261001')
LABELS = ('M1', 'M2', 'M3', 'M4', 'M5')
REASONS = {
    'M1': ('C2_elder_window_exact_maximin', 'elder window fails at phi = -29/60 (death level None)'),
    'M2': ('C6_cusp_integrals', 'elder cusp integral'),
    'M3': ('C4_cusp_limit_field_pinned_polynomials', 'cusp limit field mismatch (m = 1): -181/240 vs -67/80'),
    'M4': ('C3_fiber_reduction', 'fiber identity fails (m = 1)'),
    'M5': ('C8_gap_affine_structure_and_cand_constants', 'd det K_M / dk != -6 det A_M (m = 1)'),
}

def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def carriers():
    baseline = (ROOT / PACKET / 'RESULTS.json').read_bytes()
    if digest(baseline) != '038e0d0554a7575679d24492d110e1a823136dfb88dc556e45c58cc386c86339':
        raise ValueError('test reference must be deliberately rebound to a changed original report')
    outputs = {'baseline': baseline}
    for label, (check, reason) in REASONS.items():
        doc = json.loads(baseline)
        doc['mutant'] = label
        doc['passed'] = False
        doc['checks'][check] = {'passed': False, 'info': reason}
        outputs[label] = (json.dumps(doc, indent=1, sort_keys=True) + '\n').encode()
    return outputs


def shell():
    text = WORKFLOW.read_text()
    heading = '      - name: Verify sources, replay both modes, reject mutants\n'
    begin = text.index('          set -euo pipefail\n', text.index(heading))
    final = '          git diff --exit-code\n'
    end = text.index(final, begin) + len(final)
    return textwrap.dedent(text[begin:end])


def child_source(behavior, target, mode):
    return ('''import json, os, sys
from pathlib import Path
OUTPUTS = ''' + repr(carriers()) + '''
BEHAVIOR = ''' + repr(behavior) + '''
TARGET = ''' + repr(target) + '''
MODE = ''' + repr(mode) + '''
label = sys.argv[-1] if len(sys.argv) > 1 else 'baseline'
with open(os.environ['CUSP_TRACE'], 'a') as f:
    f.write(json.dumps([sys.flags.optimize, label])+'\\n')
active = label == TARGET and sys.flags.optimize == MODE
raw = OUTPUTS.get(label, b'')
rc = 0 if label == 'baseline' else 2 if label == 'M9' else 1
err = b'unknown mutant label\\n' if label == 'M9' else b''
if active:
    if BEHAVIOR == 'crash': raise RuntimeError('unrelated synthetic crash')
    if BEHAVIOR == 'silent': raw, err = b'', b''
    if BEHAVIOR == 'stderr': err += b'unrelated stderr\\n'
    if BEHAVIOR == 'wrong_exit': rc = 0 if label != 'baseline' else 1
    if BEHAVIOR == 'wrong_reason':
        if label == 'M9': err = b'wrong reason\\n'
        else:
            doc = json.loads(raw)
            doc['checks'][next(k for k,v in doc['checks'].items() if not v['passed'])]['info'] = 'wrong reason'
            raw = (json.dumps(doc, indent=1, sort_keys=True)+'\\n').encode()
    if BEHAVIOR == 'wrong_check':
        doc = json.loads(raw)
        for v in doc['checks'].values(): v['passed'] = True
        doc['checks']['C1_quartic_ridge_identities']['passed'] = False
        raw = (json.dumps(doc, indent=1, sort_keys=True)+'\\n').encode()
    if BEHAVIOR == 'boolean_int': raw = raw.replace(b'"passed": false', b'"passed": 0')
    if BEHAVIOR == 'duplicate': raw = raw.replace(b'"mutant":', b'"mutant": "duplicate", "mutant":', 1)
    if BEHAVIOR == 'nonfinite': raw = raw.replace(b'"passed": false', b'"passed": NaN')
    if BEHAVIOR == 'trailing': raw += b'garbage\\n'
    if BEHAVIOR == 'extra_field':
        doc=json.loads(raw); doc['unexpected']=True
        raw=(json.dumps(doc, indent=1, sort_keys=True)+'\\n').encode()
    if BEHAVIOR == 'formatting': raw=json.dumps(json.loads(raw)).encode()
    if BEHAVIOR == 'stdout': raw=b'unexpected unknown-label output\\n'
    if BEHAVIOR == 'dirty': Path('tracked.txt').write_text('changed')
sys.stdout.buffer.write(raw)
sys.stderr.buffer.write(err)
raise SystemExit(rc)
''').encode()


def identity(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': digest(raw),
            'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}


def run_case(case):
    behavior, target, mode, success, prefix = case
    with tempfile.TemporaryDirectory(prefix='cusp-protocol-') as td:
        outer = Path(td)
        root = outer / 'repo'; root.mkdir()
        packet = root / PACKET; packet.mkdir(parents=True)
        payloads = {'cusp_check.py': child_source(behavior, target, mode),
                    'RESULTS.json': carriers()['baseline'], 'NOTE.md': b'synthetic protocol fixture\n'}
        for name, data in payloads.items(): (packet / name).write_bytes(data)
        manifest = {'files': [identity(n,b) for n,b in payloads.items()], 'mutants': list(LABELS)}
        for kind in ('consumed', 'cited_only', 'consumed_unmerged'):
            path = kind + '.md'; data = ('nonempty ' + kind).encode()
            (root / path).write_bytes(data)
            manifest[kind] = [identity(path, data)]
        if behavior == 'drop_labels': manifest['mutants'] = list(LABELS[:-1])
        if behavior == 'reverse_labels': manifest['mutants'].reverse()
        if behavior == 'duplicate_label': manifest['mutants'].append('M1')
        (packet / 'SOURCES.json').write_text(json.dumps(manifest))
        (root / 'tracked.txt').write_text('original')
        if behavior == 'packet_tamper': (packet / 'NOTE.md').write_bytes(b'wrong')
        if behavior == 'extra_member': (packet / 'extra').write_text('extra')
        if behavior == 'symlink':
            (packet / 'NOTE.md').unlink(); (packet / 'NOTE.md').symlink_to(packet / 'RESULTS.json')
        if behavior in ('consumed_tamper','cited_only_tamper','consumed_unmerged_tamper'):
            (root / (behavior[:-7] + '.md')).write_text('wrong')
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env.pop('PYTHONOPTIMIZE', None)
        env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH='', GH_TOKEN='synthetic-only',
                   GH_REPOSITORY='synthetic/protocol', CUSP_TRACE=str(outer / 'children.jsonl'))
        for command in (['git','init','-q'], ['git','add','.'],
                        ['git','-c','user.name=Protocol Fixture','-c','user.email=fixture@example.invalid',
                         '-c','commit.gpgsign=false','-c','maintenance.auto=false','commit','-qm','synthetic sources']):
            subprocess.run(command, cwd=root, env=env, check=True, capture_output=True, timeout=15)
        result = subprocess.run(['bash','-c',shell()], cwd=root, env=env, capture_output=True, timeout=45)
        trace = outer / 'children.jsonl'
        children = [json.loads(s) for s in trace.read_text().splitlines()] if trace.exists() else []
        evidence = os.environ.get('CUSP_CASE_EVIDENCE')
        if evidence:
            folder = Path(evidence) / ('%s-%s-%d' % (behavior,target,mode)); folder.mkdir(parents=True,exist_ok=False)
            (folder/'stdout').write_bytes(result.stdout); (folder/'stderr').write_bytes(result.stderr)
            (folder/'result.json').write_text(json.dumps({'case':case,'returncode':result.returncode,'children':children})+'\n')
        return case, result, children


def expected_prefix(label, mode):
    all_children = [(m,l) for m in (0,1) for l in ('baseline',*LABELS,'M9')]
    return all_children[:all_children.index((mode,label))+1]


class CuspWorkflowProtocolTests(unittest.TestCase):
    def check_cases(self, cases):
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(run_case, cases))
        for case, cp, children in results:
            behavior, target, mode, success, prefix = case
            with self.subTest(behavior=behavior,target=target,mode=mode):
                self.assertEqual(cp.returncode == 0, success, cp.stdout.decode(errors='replace')+cp.stderr.decode(errors='replace'))
                self.assertEqual([tuple(v) for v in children], prefix)
                if success:
                    self.assertEqual(cp.stderr, b'')
                else:
                    errors = {
                        'packet_tamper': 'packet file identity mismatch: NOTE.md',
                        'extra_member': 'packet tree differs from manifest',
                        'symlink': 'symlink: NOTE.md',
                        'consumed_tamper': 'merged source drifted: consumed.md',
                        'cited_only_tamper': 'merged source drifted: cited_only.md',
                        'consumed_unmerged_tamper': 'consumed unmerged dependency differs from the pinned blob',
                        'drop_labels': 'cusp mutant inventory differs',
                        'reverse_labels': 'cusp mutant inventory differs',
                        'duplicate_label': 'cusp mutant inventory differs',
                    }
                    if behavior in errors:
                        self.assertIn(errors[behavior].encode(), cp.stderr)
                    elif behavior == 'dirty':
                        self.assertIn(b'diff --git', cp.stdout)
                    elif target in LABELS and behavior != 'wrong_exit':
                        self.assertIn(('mutant '+target+' did not emit its exact ').encode(), cp.stderr)
                    elif target == 'M9' and behavior != 'wrong_exit':
                        self.assertIn(b'complete expected exit-2 diagnostic', cp.stderr)

    def test_valid_original_carriers(self):
        self.check_cases([('valid','baseline',0,True,[(m,l) for m in (0,1) for l in ('baseline',*LABELS,'M9')])])

    def test_every_mutant_rejects_unrelated_process_failure(self):
        self.check_cases([(b,l,m,False,expected_prefix(l,m)) for m in (0,1) for l in LABELS
                          for b in ('crash','silent','stderr','wrong_exit')])

    def test_complete_report_identity(self):
        self.check_cases([(b,'M1',m,False,expected_prefix('M1',m)) for m in (0,1)
                          for b in ('wrong_reason','wrong_check','boolean_int','duplicate','nonfinite','trailing','extra_field','formatting')])

    def test_baseline_and_unknown_label_contracts(self):
        cases=[(b,l,m,False,expected_prefix(l,m)) for m in (0,1)
               for l,behaviors in [('baseline',('silent','stderr','wrong_exit','trailing')),
                                   ('M9',('silent','stderr','wrong_exit','wrong_reason','stdout'))] for b in behaviors]
        self.check_cases(cases)

    def test_source_guards_precede_all_children(self):
        self.check_cases([(b,'baseline',0,False,[]) for b in
                          ('packet_tamper','extra_member','symlink','consumed_tamper','cited_only_tamper','consumed_unmerged_tamper')])

    def test_exact_mutant_inventory_before_children(self):
        self.check_cases([(b,'baseline',0,False,[]) for b in ('drop_labels','reverse_labels','duplicate_label')])

    def test_final_clean_tree_guard(self):
        self.check_cases([('dirty','M9',1,False,[(m,l) for m in (0,1) for l in ('baseline',*LABELS,'M9')])])

    def test_regression_is_wired_without_relaxed_settings(self):
        text = WORKFLOW.read_text()
        self.assertIn("- 'tests/test_cusp_workflow_protocol.py'",text)
        for flags in ('-B -S','-B -O -S'):
            self.assertIn('python '+flags+' -m unittest discover -s tests -p test_cusp_workflow_protocol.py -v',text)
        self.assertIn("python-version: '3.11.16'",text)
        self.assertIn('timeout-minutes: 10',text)
        self.assertIn('contents: read',text)
        self.assertNotIn('continue-on-error',text)


if __name__ == '__main__':
    unittest.main()
