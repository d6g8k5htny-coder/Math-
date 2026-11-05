import datetime,difflib,hashlib,json,pathlib,shutil
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
HELP=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-geometry-text')
PROJECT=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text()); target=BASE/'helper-originals'; target.mkdir()
rows=[]
for name in ['ClosedUpperGeometrySection.ORIGINAL.lean.txt','Imports.ORIGINAL.txt','Context.ORIGINAL.md','Provenance.ORIGINAL.md','Frozen.ORIGINAL.json']:
    p=HELP/name; data=p.read_bytes(); st=p.stat()
    row={'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
      'marker':[st.st_size,st.st_mtime_ns],'first_observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'origin':'FIRST actual complete helper original identity, computed once; this context is a distinct provenance document, not copied complete context'}
    cache[str(p)]=row; dst=target/name; shutil.copyfile(p,dst); st=dst.stat()
    copied={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
      'origin':'known exact original byte-copy identity reused','copied_from':str(p)}
    cache[str(dst)]=copied; rows.append({'original':row,'immutable_copy':copied})
source=PROJECT/'SourceActualSaddleUppercuts.lean'; before=source.read_text()
assert before.endswith('end I4SourceActualSaddleUppercuts\n')
section=(target/'ClosedUpperGeometrySection.ORIGINAL.lean.txt').read_text()
after=before.removesuffix('end I4SourceActualSaddleUppercuts\n')+section+'\nend I4SourceActualSaddleUppercuts\n'
record={'first_ids_before_integration_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'helper':'/root/actual_canonical_partner_preflight','originals':rows,'integration_count':1,
 'producer_full_original_read':'complete section/import/context/provenance/freeze read before this worker',
 'qualification':'unelaborated candidate, no helper execution/hash/object; all later actual amendments producer-owned',
 'context_binding':'effective frozen004 accepted root21:23:23.431998, release21:23:23.432477; ACKs in actual original provenance'}
(BASE/'B_ORIGINAL_CUSTODY.json').write_text(json.dumps(record,indent=2)+'\n')
(BASE/'geometry-integration001.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='common-source',tofile='whole-geometry-source')))
source.write_text(after)
# These are already-known exact copies, retained without a second identity calculation.
for dst,original in [(BASE/'context/record_run.002.py',BASE/'context/INITIAL-record_run.py')]:
    if dst.exists():
        known=next((v for k,v in cache.items() if k.endswith('/record_run.py') and v['bytes']==dst.stat().st_size),None)
        if known:
            st=dst.stat(); cache[str(dst)]={**known,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
              'origin':'known runner002 copy identity reused from runner-amend001 after binding'}
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps({'integration':'ONE complete frozen helper original, original FIRST IDs recorded before source write','bytes':len(section.encode()),'custody':str(BASE/'B_ORIGINAL_CUSTODY.json')}))
