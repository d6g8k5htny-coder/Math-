from pathlib import Path
import json, subprocess, datetime, shutil

repo = Path('/workspace/Math-curvature-20261026')
work = Path('/workspace/scratch/actual-source-torus-regular-slab-construct')
pub = Path('/workspace/scratch/actual-source-regular-slab-publication')
commands = []

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def run(args):
    index = len(commands) + 1
    start = now()
    result = subprocess.run(args, cwd=repo, capture_output=True, text=True)
    end = now()
    out = pub / f'SOURCE_CUT_{index:02d}.stdout.txt'
    err = pub / f'SOURCE_CUT_{index:02d}.stderr.txt'
    out.write_text(result.stdout)
    err.write_text(result.stderr)
    commands.append(dict(command=args, cwd=str(repo), started_utc=start,
        ended_utc=end, exit_code=result.returncode, stdout=str(out), stderr=str(err)))
    (pub / 'ROOT_SOURCE_CUT_COMMANDS.json').write_text(json.dumps(commands, indent=2) + '\n')
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()

frozen = json.loads((work / 'FINAL_SOURCE_OBJECT_IDS.PRE_KERNEL.json').read_text())
source_id, object_id = frozen['source'], frozen['object']
source, obj = Path(source_id['path']), Path(object_id['path'])
dest = repo / 'frontiers/source_derivative_gaussian_20261025/.lake/build/lib/lean/SourceActualTorusRegularSlab.olean'
assert not dest.exists(), 'Never repeat an own-object placement'
assert not (pub / 'ROOT_OWN_OBJECT_COPY.json').exists()
assert not (pub / 'ROOT_SOURCE_CUT.json').exists()
assert source.stat().st_size == source_id['bytes'] and obj.stat().st_size == object_id['bytes']
receipts = {}
for label in ('compile-final', 'inventory-001', 'kernel-001'):
    entry = json.loads((work / 'runs' / label / 'receipt.json').read_text())
    assert entry['exit_code'] == 0
    for side in ('before', 'after'):
        seen = entry[side][str(source)]
        assert seen['sha256'] == source_id['sha256'] and seen['bytes'] == source_id['bytes']
    for side in (('after',) if label == 'compile-final' else ('before', 'after')):
        seen = entry[side][str(obj)]
        assert seen['sha256'] == object_id['sha256'] and seen['bytes'] == object_id['bytes']
    receipts[label] = {key: entry[key] for key in
        ('command', 'cwd', 'started_utc', 'ended_utc', 'exit_code', 'stdout', 'stderr')}
    receipts[label]['receipt'] = str(work / 'runs' / label / 'receipt.json')
assert len(list((work / 'runs').glob('kernel-*'))) == 1
assert run(['git', 'diff', '--cached', '--name-only']) == ''
parent = run(['git', 'rev-parse', 'HEAD'])
assert parent == 'c18ad0b8f62060cb78670f5f806af25f1307614b'
rel = str(source.relative_to(repo))
run(['git', 'add', '--', rel])
assert run(['git', 'diff', '--cached', '--name-only']) == rel
run(['git', 'commit', '-m', 'Prove actual regular-slab component inclusion bijective'])
cut = run(['git', 'rev-parse', 'HEAD'])
blob = run(['git', 'rev-parse', f'{cut}:{rel}'])
inventory = json.loads((work / 'INVENTORY.json').read_text())
record = dict(created_utc=now(),
    status='SOURCE_ONLY62_PRODUCTION_QUALIFIED_ORDINARY_CONTROLS_AND_REGISTRATION_PENDING',
    source_cut=cut, parent=parent, source=source_id, own_object=object_id,
    source_git_blob=blob, qualification_receipts=receipts,
    inventory_summary={key: value for key, value in inventory.items() if key != 'declarations'},
    kernel_count=1, historical_source_freeze_record=str(work / 'FINAL_SOURCE_OBJECT_IDS.PRE_KERNEL.json'),
    root_reading='BOUNDED production: selected component-map assembly/endpoint repair, fixture phase/derivative sections and final literal public declaration. Full proper contract/shared context read. NOT full1141 source/all73/raw streams. Nonauthor reviewer full source early PASS; final evidence/custody review pending.',
    qualified_registry_remains=dict(modules=61, written=1131, Prop=1122, data=9, inputs=32),
    mathematical_replays=0, old_hashes=0, scientific_effect='NONE')
(pub / 'ROOT_SOURCE_CUT.json').write_text(json.dumps(record, indent=2) + '\n')
intent = dict(created_utc=now(), source_cut=cut, source=str(obj), destination=str(dest),
    source_identity=source_id, eligible_own_object_identity=object_id,
    qualification_receipts=receipts, copy_once=True,
    copy_scope='ONLY newly qualified62 own .olean; no helper/Controls/ilean/old-object copy',
    all_further_copy_actions='SKIP')
(pub / 'ROOT_OWN_OBJECT_COPY_INTENT.json').write_text(json.dumps(intent, indent=2) + '\n')
shutil.copy2(obj, dest)
copy = dict(intent, completed_utc=now(), action='COPIED_ONCE',
    destination_size_metadata=dest.stat().st_size,
    identity_reused_no_rehash=object_id['sha256'], old_object_copies=0,
    helper_or_controls_copies=0, ilean_copies=0, mathematical_checks=0)
(pub / 'ROOT_OWN_OBJECT_COPY.json').write_text(json.dumps(copy, indent=2) + '\n')
print(json.dumps(dict(source_cut=cut, parent=parent, source_git_blob=blob,
    only_eligible_own_copy_completed_utc=copy['completed_utc'], further_copies='SKIP',
    qualified_registry_still=61, checks_and_ids='REUSED_NO_MATH_OR_HASH_REPLAY')))
