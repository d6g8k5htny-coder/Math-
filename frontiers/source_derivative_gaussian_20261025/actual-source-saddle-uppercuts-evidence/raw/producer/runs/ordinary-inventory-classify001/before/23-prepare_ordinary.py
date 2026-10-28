import datetime,json,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text())
kernel=json.loads((BASE/'runs/kernel001/receipt.json').read_text()); assert kernel['exit_code']==0
p=BASE/'SaddleUppercutsControls.lean'; dst=BASE/'frozen/Controls.INITIAL.lean'
assert p.read_bytes()==dst.read_bytes()
row=cache[str(p)]; st=dst.stat(); copied={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
 'origin':'known exact initial ordinary byte-copy identity reused','copied_from':str(p)}
cache[str(dst)]=copied
record={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'ordinary_initial_source':row,'immutable_snapshot':copied,
 'production_dependency':json.loads((BASE/'FINAL_SOURCE_PRE_KERNEL_IDS.json').read_text()),
 'one_final_production_kernel_receipt':str(BASE/'runs/kernel001/receipt.json'),
 'kernel_scope':'EXACTLY ONE final production named-module kernel PASS; does not qualify ordinary math',
 'ordinary_next':'new strict ordinary compile, separate ALL-owned module inventory/std3, then sole closed no-premise negative',
 'ordinary_named_kernels':0,'shared_copies_by_producer':0}
(BASE/'ORDINARY_INITIAL_IDS.json').write_text(json.dumps(record,indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps({'ordinary_initial':row,'kernel_pass':kernel['end_utc']}))
