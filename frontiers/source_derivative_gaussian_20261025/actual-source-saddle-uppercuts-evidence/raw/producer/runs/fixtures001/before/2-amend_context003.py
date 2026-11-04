import datetime,difflib,hashlib,json,pathlib,shutil
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
path=BASE/'CONTEXT.md'; old=path.read_text()
new=old.replace('I4Torus.torusProjection 2 2 \'\' Metric.ball (![x,y] : Fin 2 → ℝ) (1/8)',
  'I4Torus.torusProjection 2 2 \'\' (I4LifetimeField.coordinates 2 \'\'\n    Metric.ball (fixturePoint x y) (1/8))')
assert new!=old
new=new.replace('Small O is actual projected ball1/8.','Small O is the actual projected PHYSICAL E2 ball1/8, transported by coordinates as a homeomorphism without an isometry claim.')
new+='''
## Amendment003: literal physical small neighborhood

The fixtureOpen definition now retains ROOT_GO's exact projected PHYSICAL E2 ball of radius1/8, first mapped by the actual coordinates map and then the torus projection. The earlier Pi-ball shape is historical001/002 only. This corrects the concrete reviewer GO/context alignment finding. No isometry, norm equality, public/math/geometry interface, control mutation or helper scope changes. Full earlier context reading plus entire003delta is the effective preTEXT context.
'''
(BASE/'context/context-003.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='CONTEXT.002.md',tofile='CONTEXT.003.md')))
path.write_text(new); cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text()); st=path.stat()
row={'path':str(path),'bytes':st.st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'marker':[st.st_size,st.st_mtime_ns],'first_observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'origin':'new actual context003 identity calculated once'}
cache[str(path)]=row; dst=BASE/'context/CONTEXT.003.md'; shutil.copyfile(path,dst); st=dst.stat()
copied={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
 'origin':'known exact byte-copy identity reused','copied_from':str(path)}
cache[str(dst)]=copied
(BASE/'context/FIRST_ID.003.json').write_text(json.dumps({'context':row,'immutable_snapshot':copied,
 'patch':str(BASE/'context/context-003.patch'),'reason':'concrete reviewer ROOT_GO physical-ball alignment finding'},indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n'); print(json.dumps(row))
