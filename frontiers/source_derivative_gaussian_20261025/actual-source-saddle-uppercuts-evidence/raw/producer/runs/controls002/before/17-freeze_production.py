import datetime,json,pathlib,shutil
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
PROJECT=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text())
source=PROJECT/'SourceActualSaddleUppercuts.lean'; obj=BASE/'build/SourceActualSaddleUppercuts.olean'
row=cache[str(source)]; dst=BASE/'frozen/FINAL_SOURCE.lean'; shutil.copyfile(source,dst); st=dst.stat()
cache[str(dst)]={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
 'origin':'known final strict source identity reused, exact immutable copy','copied_from':str(source)}
record={'observed_final_source_freeze_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'source':row,'source_snapshot':cache[str(dst)],'own_object':cache[str(obj)],
 'strict_pass_receipt':str(BASE/'runs/fixtures004/receipt.json'),
 'source_lines':len(source.read_text().splitlines()),'kernel_count_at_this_historical_pre_kernel_freeze':0,
 'public64_calls':source.read_text().count('I4SourceActualQuotientSaddleCollar.actualSource_quotient_saddle_local_collar'),
 'public_theorem':'I4SourceActualSaddleUppercuts.actualSource_quotient_saddle_uniform_closed_uppercuts',
 'remaining':'dynamic own inventory/std3, early review then ONE final production kernel; ordinary strict+separate inventory+soleFalse remain new scope',
 'no_replay':'all qualified64 and passed unchanged65 scopes reused'}
(BASE/'FINAL_SOURCE_PRE_KERNEL_IDS.json').write_text(json.dumps(record,indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps(record))
