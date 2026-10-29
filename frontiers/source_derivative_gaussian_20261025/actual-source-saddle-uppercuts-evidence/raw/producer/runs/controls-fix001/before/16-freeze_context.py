import datetime,json,pathlib,shutil
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text())
records=[]
for src,dst in [(BASE/'CONTEXT.md',BASE/'context/CONTEXT.001.md')]+[
    (p,BASE/'context'/('INITIAL-'+p.name)) for p in sorted((BASE/'runner').glob('*.py'))]:
    row=cache[str(src)]; shutil.copyfile(src,dst); st=dst.stat()
    reused={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
      'origin':'known exact byte-copy identity reused','copied_from':str(src)}
    cache[str(dst)]=reused; records.append(reused)
record={'observed_freeze_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'context_version':'001','copies':records,
 'ordering':'before helper proof text, Lean, production source and first mathematical execution',
 'source_bootstrap':'none yet; full literal declarations are frozen in context before root acceptance',
 'known_prior_evidence':'all qualified64 evidence reused; no old checks/hash/object/copy',
 'ordinary_obligation':'separate exact ordinary module inventory/std3 after ordinary strict PASS before ONEFalse; no ordinary kernel',
 'static_creation':'apply_patch tool writes created context/runner before this first important worker; actual tool transcripts retained, no invented per-write OS UTC'}
(BASE/'context/FIRST_ID.001.json').write_text(json.dumps(record,indent=2)+'\n')
(BASE/'INITIAL_RUNNER_CUSTODY.json').write_text(json.dumps(record,indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps({'frozen':record['observed_freeze_utc'],'context_id':cache[str(BASE/'CONTEXT.md')]}))
