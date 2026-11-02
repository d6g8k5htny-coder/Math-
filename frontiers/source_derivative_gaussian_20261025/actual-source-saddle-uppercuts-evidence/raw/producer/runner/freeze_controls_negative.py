import datetime,hashlib,json,pathlib,re,shutil
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text())
strict=json.loads((BASE/'runs/controls003/receipt.json').read_text())
inv=json.loads((BASE/'runs/ordinary-inventory001/receipt.json').read_text())
classified=json.loads((BASE/'CONTROLS_INVENTORY_CLASSIFIED.json').read_text())
assert strict['exit_code']==inv['exit_code']==0 and classified['owned_constants']==123
assert strict['end_utc']<inv['start_utc']
assert not (BASE/'runs/false-control001').exists()
p=BASE/'SaddleUppercutsControls.lean'; dst=BASE/'frozen/Controls.FINAL.lean'; shutil.copyfile(p,dst)
row=cache[str(p)]; st=dst.stat(); cache[str(dst)]={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
 'origin':'known exact passed ordinary final source identity reused','copied_from':str(p)}
blocks=re.findall(r'```lean\n(.*?)```',(BASE/'CONTEXT.md').read_text(),re.S)
harness=blocks[-1]; assert harness.startswith('import SaddleUppercutsControls\n')
assert 'example : ActualSaddleUppercutsControls.nonnegativeUpperMutation := by' in harness
fp=BASE/'FalseControl.lean'; fp.write_text(harness); st=fp.stat()
fr={'path':str(fp),'bytes':st.st_size,'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),
 'marker':[st.st_size,st.st_mtime_ns],'first_observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'origin':'FIRST actual complete sole closed no-premise harness identity, computed once BEFORE execution'}
cache[str(fp)]=fr; fdst=BASE/'frozen/FalseControl.ORIGINAL.lean'; shutil.copyfile(fp,fdst); st=fdst.stat()
cache[str(fdst)]={**fr,'path':str(fdst),'marker':[st.st_size,st.st_mtime_ns],
 'origin':'known exact complete sole harness byte-copy identity reused','copied_from':str(fp)}
record={'observed_freeze_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'ordinary_source':row,'ordinary_final_snapshot':cache[str(dst)],
 'ordinary_object':cache[str(BASE/'build/SaddleUppercutsControls.olean')],
 'strict_receipt':str(BASE/'runs/controls003/receipt.json'),
 'ordinary_all_owned_inventory':classified['owned_constants'],
 'ordinary_inventory_receipt':str(BASE/'runs/ordinary-inventory001/receipt.json'),
 'ordinary_classification':str(BASE/'CONTROLS_INVENTORY_CLASSIFIED.json'),
 'ordinary_named_kernels':0,'production_named_kernels':1,
 'sole_harness':fr,'sole_harness_snapshot':cache[str(fdst)],
 'negative_status':'NOT YET EXECUTED; exactly one planned after this first identity/freeze',
 'mutation':'ONLY eps>0 to eps>=0, same chosen phi/rho/source/field/CLOSED cut/upper bound; CLOSED assertion without any mutation premise',
 'counterproof':'independent structural inverse vertical path, full target/source/zero-cut membership, actual midpoint q, negative endpoint coordinate product; no upperbranch/lowerPC shortcut',
 'ordinary_lines':len(p.read_text().splitlines()),'no_old_replay':'all qualified64 and completed unchanged65 verification reused'}
(BASE/'CONTROL_IDS_PRE_NEGATIVE.json').write_text(json.dumps(record,indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps({'ordinary_source':row,'ordinary_object':record['ordinary_object'],'harness':fr,
 'ordinary_inventory':classified['owned_constants'],'ordinary_lines':record['ordinary_lines']}))
