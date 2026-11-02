from pathlib import Path
import json
import subprocess
import datetime
import shutil

r = Path('/workspace/Math-curvature-20261026')
p = Path('/workspace/scratch/actual-source-torus-superlevel-local-basis-construct')
q = Path('/workspace/scratch/actual-source-torus-superlevel-local-basis-publication')
commands = []

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def run(args):
    n = len(commands) + 1
    start = now()
    x = subprocess.run(args, cwd=r, capture_output=True, text=True)
    end = now()
    so, se = q / f'SOURCE_CUT_{n:02d}.stdout.txt', q / f'SOURCE_CUT_{n:02d}.stderr.txt'
    so.write_text(x.stdout)
    se.write_text(x.stderr)
    commands.append(dict(command=args, cwd=str(r), started_utc=start, ended_utc=end,
                         exit_code=x.returncode, stdout=str(so), stderr=str(se)))
    (q / 'ROOT_SOURCE_CUT_COMMANDS.json').write_text(json.dumps(commands, indent=2) + '\n')
    assert x.returncode == 0, (args, x.stderr)
    return x.stdout.strip()

ids = json.loads((p / 'FINAL_SOURCE_OBJECT_IDS.json').read_text())['identities']
source = r / 'frontiers/source_derivative_gaussian_20261025/SourceActualTorusSuperlevelLocalBasis.lean'
obj = p / 'build/SourceActualTorusSuperlevelLocalBasis.olean'
dest = r / 'frontiers/source_derivative_gaussian_20261025/.lake/build/lib/lean/SourceActualTorusSuperlevelLocalBasis.olean'
source_id, object_id = ids[str(source)], ids[str(obj)]
assert not dest.exists(), 'Never recopy an existing eligible own object'
assert not (q / 'ROOT_OWN_OBJECT_COPY.json').exists()
assert not (q / 'ROOT_SOURCE_CUT.json').exists()
receipts = {}
for label in ('compile-final', 'inventory-001', 'kernel-001'):
    j = json.loads((p / 'runs' / label / 'receipt.json').read_text())
    assert j['exit_code'] == 0
    for side in ('before', 'after'):
        v = j[side][str(source)]
        assert v['sha256'] == source_id['sha256'] and v['bytes'] == source_id['bytes']
    for side in (('after',) if label == 'compile-final' else ('before', 'after')):
        v = j[side][str(obj)]
        assert v['sha256'] == object_id['sha256'] and v['bytes'] == object_id['bytes']
    receipts[label] = dict(receipt=str(p / 'runs' / label / 'receipt.json'),
        command=j['command'], started_utc=j['started_utc'], ended_utc=j['ended_utc'],
        exit_code=j['exit_code'], stdout=j['stdout'], stderr=j['stderr'])
assert len(list((p / 'runs').glob('kernel-*'))) == 1
assert source.stat().st_size == source_id['bytes'] and obj.stat().st_size == object_id['bytes']
assert run(['git', 'diff', '--cached', '--name-only']) == ''
parent = run(['git', 'rev-parse', 'HEAD'])
assert parent == '526d696ce49a574610f614cfd93ba6db76225066'
rel = str(source.relative_to(r))
run(['git', 'add', '--', rel])
assert run(['git', 'diff', '--cached', '--name-only']) == rel
run(['git', 'commit', '-m', 'Prove actual torus closed-superlevel local path connectivity'])
cut = run(['git', 'rev-parse', 'HEAD'])
blob = run(['git', 'rev-parse', f'{cut}:{rel}'])
inventory = json.loads((p / 'INVENTORY.json').read_text())
record = dict(created_utc=now(),
    status='SOURCE_ONLY_CUT_NEW61_PRODUCTION_MATH_PASSED_ORDINARY_CONTROLS_AND_REGISTRATION_PENDING',
    source_cut=cut, parent=parent, source=source_id, source_git_blob=blob, own_object=object_id,
    qualification_receipts=receipts,
    inventory_summary={k: v for k, v in inventory.items() if k != 'declarations'},
    root_actual_reading='Bounded final source header1–52/declaration map/tail525–629; full initial producer Main/Public section text before final small corrections. Root read selected receipt source/object bindings/command/times/exit/stream identities, not all65 inventory bodies/raw stream contents. Independent reviewer personally full source1–629/source-surface PASS; final evidence review pending.',
    qualified_registry_remains=dict(modules=60, written=1130, Prop=1121, data=9, inputs=32),
    old_checks_replayed=0, old_hashes_replayed=0, scientific_effect='NONE', draft=True,
    routine_correction_record=str(q / 'ROOT_PRECUT_ROUTINE_CORRECTION.json'))
(q / 'ROOT_SOURCE_CUT.json').write_text(json.dumps(record, indent=2) + '\n')
intent = dict(created_utc=now(), source_cut=cut, source=str(obj), destination=str(dest),
    eligible_own_object_identity=object_id, source_identity=source_id, qualification=receipts,
    copy_scope='ONLY newly qualified61 own .olean; no helper/Controls/ilean/old-object copies; no math or hash replay',
    copy_once=True, all_further_copy_actions='SKIP')
(q / 'ROOT_OWN_OBJECT_COPY_INTENT.json').write_text(json.dumps(intent, indent=2) + '\n')
shutil.copy2(obj, dest)
out = dict(intent, completed_utc=now(), action='COPIED_ONCE',
    destination_size_metadata=dest.stat().st_size,
    sha256_identity_reused_from_frozen_producer=object_id['sha256'],
    additional_verification_commands=0, old_object_copies=0,
    helper_or_controls_object_copies=0, ilean_copies=0)
(q / 'ROOT_OWN_OBJECT_COPY.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(dict(sourcecut=cut, parent=parent, blob=blob,
    copy_completed_utc=out['completed_utc'], destination=str(dest),
    action='COPIED_ONLY_NEW_OWN_ONCE', registry_still=60,
    production_checks='REUSED strict/inventory/ONEkernel, no replay')))
