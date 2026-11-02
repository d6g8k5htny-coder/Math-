import datetime,difflib,hashlib,json,pathlib,shutil
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
path=BASE/'CONTEXT.md'; old=path.read_text()
new=old.replace('private def nonnegativeUpperMutation : Prop :=','def nonnegativeUpperMutation : Prop :=')
assert new!=old
new+='''
## Amendment002: ordinary public mutation interface and reused64 lineage

The ordinary `nonnegativeUpperMutation` Prop definition is PUBLIC within ActualSaddleUppercutsControls. Thus the sole importing-only False harness can name the precise false premise using public APIs. All production names/privacy/output and the sole mutation remain unchanged. Ordinary `nonnegativeUpperMutation_false` is public as already stated. B geometry has no dependent change; personal FULL001 reading plus entire002delta ACK before proof text.

Qualified PUBLIC64 lineage is REUSED, never rechecked/rehashed/copied: published normal head ee5b141d5ff41a0a9040256a8025690ec22d7266; source-only cut57f73698fb84efd56166fda57639557794312754, parentf4825c3e3bd0e2d2c46157096e76b9ab17dbbb71; source40252B SHAe0e0a0f77bd75bbbd8994d620ee43b18b2edd50d7649cd8cb9837e7148762265, Gitblob39bce1145fcd714b049bfd4ec941390a0b286f10; ownobject1654224B SHAa57489eb917c4f2fd4d314ab5f7ae9dea60619caf9160e044700114551c1e15e. Root canonical eligible64 copy occurred ONCE20:25:01.660046; all further copies SKIP. Existing authoritative /workspace/scratch/actual-source-quotient-saddle-collar-publication/ROOT_SOURCE_CUT.json and ROOT_OWN_OBJECT_COPY.json bind these known identities. All prior64 mathematical and metadata checks/full nonauthor review and all4CI SUCCESS already completed; no new65 session/process reason changes that evidence.
'''
patch=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='CONTEXT.001.md',tofile='CONTEXT.002.md'))
(BASE/'context/context-002.patch').write_text(patch)
path.write_text(new)
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text()); st=path.stat()
row={'path':str(path),'bytes':st.st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'marker':[st.st_size,st.st_mtime_ns],'first_observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'origin':'new actual context002 identity calculated once'}
cache[str(path)]=row
dst=BASE/'context/CONTEXT.002.md'; shutil.copyfile(path,dst); st=dst.stat()
copied={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
 'origin':'known exact byte-copy identity reused','copied_from':str(path)}
cache[str(dst)]=copied
(BASE/'context/FIRST_ID.002.json').write_text(json.dumps({'context':row,'immutable_snapshot':copied,
 'patch':str(BASE/'context/context-002.patch'),'reason':'concrete reviewer preTEXT interface finding + reused lineage reference'},indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps(row))
