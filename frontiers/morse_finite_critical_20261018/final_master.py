"""Once-only C293 artifact binding; no compiler/network. Contract: evidence/MASTER_CONTRACT.md.
Existing build/kernel receipts are evidence inputs, not proof execution by this master.
Only subprocess: exact canonical delivery builder's read-only `verify` operation.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, subprocess, sys, zipfile

ROOT = Path(__file__).resolve().parent
MODULES = ['Lifetime', 'TorusTopology', 'MorseFiniteCritical', 'MorseFiniteControls', 'MorseFiniteAxiomAudit']
NEW = MODULES[2:]
TARGET = 'TorusMorseFinite.quotientCriticalSet_finite'
BUILDER = '88d6e30182ae682d27f4d156f6c935f8373168ca6ff14d3141cd69c4b036d3a3'
FROZEN = 'f1a429935146b4e406e9ba8cc9ff8b84f7d40c22cc4fea74920dfc013c4911de'
EXES = {'build': '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554',
        'kernel': 'cfde41cb11dde58c84e9c60c551fd104bb2fc1104ad44dca932a923120272a35'}
checks, observed = [], {}
digest = lambda b: hashlib.sha256(b).hexdigest()
blob = lambda b: hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
now = lambda: datetime.now(timezone.utc).isoformat()

def check(name, ok):
    checks.append({'name': name, 'pass': bool(ok)})
    if not ok: raise ValueError(name)

def read(path):
    p = ROOT / path
    check('regular nonsymlink: ' + str(p), p.is_file() and all(not q.is_symlink() for q in [p, *p.parents]))
    b = p.read_bytes(); h = digest(b)
    check('stable reread: ' + str(p), p not in observed or observed[p] == h)
    observed[p] = h
    return b

def document(path): return json.loads(read(path))
def local_name(name):
    p = Path(name)
    check('safe relative member: ' + name, not p.is_absolute() and '..' not in p.parts and bool(p.parts))
    return p

def verify():
    check('master identity', digest(read(Path(__file__))) == document('FINAL_MASTER_START.json')['master_sha256'])
    read('evidence/MASTER_CONTRACT.md')
    inv = document('FINAL_SOURCE_INVENTORY.json'); ih = digest(read('FINAL_SOURCE_INVENTORY.json'))
    check('exact frozen inventory', ih == FROZEN)
    src = {r['name']: r['sha256'] for r in inv['sources']}
    check('exact five source identities', len(inv['sources']) == 5 and set(src) == {m + '.lean' for m in MODULES})
    check('exact isolated source pathset', {p.name for p in (ROOT/'final-project').iterdir()} == set(src))
    for r in inv['sources']:
        for base in ['project', 'final-project']:
            b = read(Path(base)/r['name']); check(base + '/' + r['name'], len(b) == r['bytes'] and digest(b) == r['sha256'])
    inputs = document('SOURCE_INPUTS.json')['sources']
    check('exact two immutable source inputs', len(inputs) == 2 and {Path(r['project_path']).name for r in inputs} == {'Lifetime.lean', 'TorusTopology.lean'})
    for r in inputs:
        b = read(local_name(r['project_path']))
        check(r['project_path'] + ': SHA and Git blob', len(b) == r['bytes'] and digest(b) == r['sha256'] == src[Path(r['project_path']).name] and blob(b) == r['blob'] == r['verified_blob'])
    check('frozen phase runner', digest(read('run_final_phase.py')) == inv['runner_sha256'])
    dep = document('FINAL_DEPENDENCY_ARTIFACTS.json')
    check('bound dependency inventory', observed[ROOT/'FINAL_DEPENDENCY_ARTIFACTS.json'] == inv['dependency_artifact_inventory_sha256'])
    seq = document('FINAL_SEQUENCE_RESULT.json'); start = document('FINAL_SEQUENCE_START.json')
    phases = [('build', m) for m in MODULES] + [('kernel', m) for m in NEW]
    check('once sequence completed', seq['status'] == 'PASS_FROZEN_BUILD_AND_STANDARD_KERNEL_REPLAY' and seq['inventory_sha256'] == start['inventory_sha256'] == ih)
    check('sequence driver binding', start['driver_sha256'] == digest(read('run_final_sequence.py')))
    check('exact eight successful phases', [(r['kind'], r['module']) for r in seq['phases']] == phases and all(r['returncode'] == 0 for r in seq['phases']))
    paths = sorted((ROOT/'final-runs').glob('*/RECEIPT.json')); rows = [document(p) for p in paths]
    check('exact eight unique final receipts', len(rows) == 8 and len({(r['kind'], r['module']) for r in rows}) == 8)
    receipts = {(r['kind'], r['module']): (p.parent, r) for p, r in zip(paths, rows)}
    check('receipt phase set', set(receipts) == set(phases))
    known = {}; audit = ''
    for kind, module in phases:
        folder, r = receipts[kind, module]; label = kind + ':' + module
        check(label + ': successful exact execution', r['status'] == 'PASS' and r['returncode'] == 0 and r['timed_out'] is False and r['process_reaped'] is True and r['inventory_sha256'] == ih and r['runner_sha256'] == inv['runner_sha256'] and r['executable_sha256'] == EXES[kind])
        check(label + ': stable sources and imported objects', r['source_before'] == r['source_after'] == src and r['source_unchanged'] is True and r['imported_objects_unchanged'] is True and r['objects_before'] == known)
        for phase in ['before', 'after']:
            d = r['dependency_' + phase]; check(label + ': dependency census ' + phase, d['reused'] + len(d['rehashed']) == len(dep['artifacts']))
        for stream in ['stdout', 'stderr']:
            b = read(folder/(stream + '.txt')); check(label + ':' + stream, digest(b) == r[stream + '_sha256'])
            if kind == 'build' and module != 'MorseFiniteAxiomAudit': check(label + ': clean ' + stream, b == b'')
        if kind == 'build':
            produced = r['produced_objects']; allowed = {module+s for s in ['.olean', '.olean.private', '.olean.server', '.ir', '.ir.sig']}
            check(label + ': module outputs', module+'.olean' in produced and set(produced) <= allowed and not set(produced) & set(known))
            if module in NEW: check(label + ': warnings as errors', '-DwarningAsError=true' in r['command'])
            known.update(produced)
            if module == 'MorseFiniteAxiomAudit': audit = read(folder/'stdout.txt').decode()
        else: check(label + ': standard named-module kernel', r['command'][1:] == ['-v', module] and Path(r['command'][0]).name == 'leanchecker' and '--fresh' not in r['command'])
        check(label + ': output binding', r['objects_after'] == known and r['object_sha256'] == known[module+'.olean'])
    check('final object pathset', {p.name for p in (ROOT/'final-build').iterdir()} == set(known))
    for name, h in known.items(): check(name + ': current object', digest(read(Path('final-build')/name)) == h)
    census, names, section = {}, [], None
    # Lean wraps axiom lists. Match full-text records, bounded by brackets and size.
    pattern = r'MORSE_AUDIT_MODULE (?P<module>\S+) COUNT (?P<count>\d+)|MORSE_AUDIT_DECL (?P<name>\S+) AXIOMS \[(?P<axioms>[^\[\]]{0,4096})\]'
    for m in re.finditer(pattern, audit):
        if m['module'] is not None:
            section = m['module']; check('unique census module ' + section, section not in census); census[section] = [int(m['count']), 0]
        else:
            check('census declaration has module', section in census)
            axs = {x.strip() for x in m['axioms'].split(',') if x.strip()}
            check('standard axioms: ' + m['name'], axs <= {'propext', 'Classical.choice', 'Quot.sound'})
            names.append(m['name']); census[section][1] += 1
    totals = re.findall(r'MORSE_AUDIT_STANDARD_ONLY_PASS COUNT (\d+)', audit)
    check('complete unique declaration census', set(census) == set(MODULES[:4]) and all(a == b and a > 0 for a, b in census.values()) and len(names) == len(set(names)) == audit.count('MORSE_AUDIT_DECL ') == 169 and totals == [str(len(names))])
    required_text = read('final-project/MorseFiniteAxiomAudit.lean').decode().split('let required : Array Name := #[', 1)[1].split(']', 1)[0]
    required = re.findall(r'`([A-Za-z0-9_.]+)', required_text)
    check('all required declarations including target', TARGET in required and set(required) <= set(names))
    n = document('negative-final/RECEIPT.json'); text = ''
    for stream in ['stdout', 'stderr']:
        b = read('negative-final/' + stream + '.txt'); check('N1 ' + stream, digest(b) == n[stream+'_sha256']); text += b.decode()
    check('N1 actual missing-premise rejection', n['status'] == 'PASS_EXPECTED_MISSING_PREMISE_REJECTION' and n['returncode'] != 0 and n['timed_out'] is False and n['diagnostic_match'] is True and 'type mismatch' in text.lower() and 'IsMorseDistinct' in text and not any(x in text.lower() for x in ['unknown module', 'unknown identifier', 'unexpected token', 'object file']))
    check('N1 frozen bindings', n['inventory_sha256'] == ih and n['source_before'] == src and n['objects_before'] == known and n['lean_sha256'] == EXES['build'] and all(n[k] is True for k in ['source_unchanged', 'imported_sources_unchanged', 'imported_objects_unchanged']) and n['source_sha256'] == digest(read('negative-project/WithoutMorse.lean')) and n['runner_sha256'] == digest(read('run_negative.py')))
    a = document('ROOT_ACCEPTANCE.json')
    check('scoped exact formal acceptance', a['verdict'] == 'ACCEPT_SCOPED_FORMAL' and a['source_sha256'] == src['MorseFiniteCritical.lean'] and a['source_inventory_sha256'] == ih and a['review_sha256'] == digest(read(local_name(a['review_path']))))
    check('no independent or scientific credit', a['organizational_independence_credit'] == 0 and a['human_review_credit'] == 0 and a['scientific_effect'] == 'NONE')
    gh = document('GITHUB_READBACK.json'); files = gh['files']; published = set()
    check('standalone public scope', gh['path_prefix'] == 'frontiers/morse_finite_critical_20261018/' and re.fullmatch('[0-9a-f]{40}', gh['head']) is not None)
    for r in files:
        p = local_name(r['relative_path']); check('unique published path', str(p) not in published); published.add(str(p)); b = read(Path('publication-package')/p)
        check(str(p)+': native/remote/tree bytes', len(b) == r['bytes'] and digest(b) == r['sha256'] == r['remote_sha256'] and r['raw_byte_match'] is True and blob(b) == r['git_blob'] == r['tree_blob'])
    check('complete publication file set', published == {str(p.relative_to(ROOT/'publication-package')) for p in (ROOT/'publication-package').rglob('*') if p.is_file()} and set(src.values()) <= {r['sha256'] for r in files})
    ci = document('HOSTED_CI_READBACK.json'); jobs = ci['jobs']
    check('exact head three successful hosted jobs', ci['head'] == gh['head'] and len(jobs) == len({j['id'] for j in jobs}) == 3 and all(j['head_sha'] == gh['head'] and j['status'] == 'completed' and j['conclusion'] == 'success' for j in jobs))
    check('local-only new formal execution', ci['new_formal_execution'] == 'LOCAL_ONLY_NOT_REGISTERED_IN_HOSTED_FORMAL' and ci['scientific_effect'] == 'NONE')
    tool = ROOT.parent/'continuation288/PACKET/TOOLS/research_delivery.py'; check('canonical builder', digest(read(tool)) == BUILDER)
    archive = ROOT/'C293_MORSE_FINITE_CRITICAL_DELIVERY.zip'; raw = read(archive)
    run = subprocess.run([sys.executable, '-B', str(tool), 'verify', str(archive)], capture_output=True, text=True, timeout=120)
    check('canonical archive verification', run.returncode == 0)
    with zipfile.ZipFile(archive) as z:
        manifest = json.loads(z.read('DELIVERY_MANIFEST.json')); members = [r['filename'] for r in manifest['files']]
        check('exact unique archive members', len(members) == len(set(members)) and len(z.namelist()) == len(set(z.namelist())) and set(z.namelist()) == set(members) | {'DELIVERY_MANIFEST.json'})
        check('complete native packet set', set(members) == {str(p.relative_to(ROOT/'PACKET')) for p in (ROOT/'PACKET').rglob('*') if p.is_file()})
        for r in manifest['files']:
            b = z.read(r['filename']); check(r['filename']+': archive/native equality', len(b) == r['size'] and digest(b) == r['sha256'] and b == read(Path('PACKET')/local_name(r['filename'])))
    custody = document('PRIVATE_CUSTODY_RECEIPT.json')
    check('private exact uploaded/downloaded archive', custody['owner_only'] is True and custody['actual_raw_download_equal'] is True and custody['bytes'] == len(raw) and custody['sha256'] == digest(raw) and read('REMOTE_READBACK.zip') == raw)
    for p, h in list(observed.items()): check('final stable bytes: '+str(p), p.is_file() and all(not q.is_symlink() for q in [p, *p.parents]) and digest(p.read_bytes()) == h)
    check('final source/object pathsets', {p.name for p in (ROOT/'final-project').iterdir()} == set(src) and {p.name for p in (ROOT/'final-build').iterdir()} == set(known))
    check('final publication/packet pathsets', published == {str(p.relative_to(ROOT/'publication-package')) for p in (ROOT/'publication-package').rglob('*') if p.is_file()} and set(members) == {str(p.relative_to(ROOT/'PACKET')) for p in (ROOT/'PACKET').rglob('*') if p.is_file()})
    return {'axiom_census': census, 'axiom_count': len(names), 'canonical_verify_stdout': run.stdout, 'canonical_verify_stderr': run.stderr}

def main():
    start, output = ROOT/'FINAL_MASTER_START.json', ROOT/'FINAL_MASTER.json'
    if start.exists() or output.exists():
        print('REFUSED: final master already started; prior evidence preserved', file=sys.stderr); return 1
    try:
        with start.open('x') as f: json.dump({'started_utc': now(), 'master_sha256': digest(Path(__file__).read_bytes()), 'scientific_effect': 'NONE'}, f, indent=2)
    except FileExistsError: return 1
    report = {'status': 'HOLD_ARTIFACT_VERIFICATION', 'scientific_effect': 'NONE'}
    try:
        report.update(verify()); report['status'] = 'PASS_ARTIFACT_VERIFICATION_NOT_THEOREM_PROOF'
    except BaseException as exc: report['error'] = repr(exc)
    report.update(finished_utc=now(), checks=checks, check_count=len(checks), observed_sha256={str(p): h for p, h in observed.items()})
    with output.open('x') as f: json.dump(report, f, indent=2, sort_keys=True); f.write('\n')
    print(json.dumps({'status': report['status'], 'checks': len(checks)}))
    return 0 if report['status'].startswith('PASS_') else 1

if __name__ == '__main__': raise SystemExit(main())
