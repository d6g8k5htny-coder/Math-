"""Unexecuted59 archive candidate. Called only inside final metadata worker after rootGO."""
from pathlib import Path
import json
import custody as f
R,P,U,B,A,E=f.R,f.P,f.U,f.B,f.A,f.E
SOURCE=f.SOURCE
BAD={'.olean','.ilean','.c','.o','.so','.a','.pyc','.bin','.pickle','.pkl'}
def artifact(p):return any(x in p.name for x in ['.olean','.ilean']) or p.suffix in BAD or '__pycache__' in p.parts or '.lake' in p.parts

def prepare(c):
    f.require(c['status']=='ROOT_GO_FINAL59_ASSEMBLY_AND_ONE_METADATA_ATTEMPT','Explicit final rootGO required')
    f.require(all(c[k] for k in ['all_math_complete','final_review_pass','source_cut_committed','own_object_copied_once','immutable_payloads_frozen']),'All actual final gates must precede any archive')
    f.require(c['qualified_baseline']==f.BASE and len(c['source_cut'])==40,'Actual59 cut/baseline')
    if (R/'ARCHIVE_RESULT.json').exists():
        prior=f.read(R/'ARCHIVE_RESULT.json');f.require(prior['source_cut']==c['source_cut'],'Preserve prior archive; changed cut requires separate binding');return prior
    f.CUT=c['source_cut']
    f.retain(B/SOURCE,{'bytes':99430,'sha256':f.SRC_SHA})
    # Reuse the producer current-stamp cache; never bind historical canonical-path IDs to changed bytes.
    cache=json.loads((P/'RECORDED_IDENTITY_CACHE.json').read_text())
    for path,x in cache.items():
        p=Path(path)
        if not p.is_file() or artifact(p) or not(P in p.parents or p==B/SOURCE):continue
        st=p.stat()
        if x['stat_stamp']==[st.st_ino,st.st_size,st.st_mtime_ns]:f.retain(p,x['identity'])
    run_receipts=[Path(p) if Path(p).is_absolute() else P/p for p in c['run_receipts']]
    runs=[]
    for p in run_receipts:
        q=f.read(p);f.require('exit_code'in q and 'ended_utc'in q,'No unfinished actual run '+str(p))
        d=p.parent;r={'label':q.get('label',d.name),'receipt':str(p),'record':q};runs.append(r)
        src=d/SOURCE
        if src.exists():f.retain(src,q['before']['source'])
        for k in ['stdout','stderr']:
            x=q[k];f.retain(d/(k+'.log'),x)
        for x in q.get('harness_snapshots',[]):
            sp=Path(x['snapshot'])
            if sp.exists()and x.get('original_identity'):f.retain(sp,x['original_identity'])
    # Frozen original helper identities are remapped to their retained producer copies, not rehashed.
    def helper_records(value,directory):
        if isinstance(value,dict):
            if 'bytes'in value and 'sha256'in value:
                n=value.get('name',value.get('file',Path(value.get('path','')).name));p=directory/n
                if n and p.is_file()and not artifact(p):f.retain(p,value)
            for v in value.values():helper_records(v,directory)
        elif isinstance(value,list):
            for v in value:helper_records(v,directory)
    lineage=f.read(P/'AUTHOR_HELPER_LINEAGE.json')
    for x in lineage['records']:
        helper_records(f.read(P/x['original_identity_source']),P/x['original_directory'])
    numeric_ids=P/'NUMERIC_HELPER_FIRST_IDENTITIES.json'
    if numeric_ids.exists():
        def numeric_records(value):
            if isinstance(value,dict):
                if 'bytes' in value and 'sha256' in value:
                    names=[value.get(k) for k in ['copied_to','path','source','file','name'] if isinstance(value.get(k),str)]
                    for name in names:
                        candidates=[Path(name)] if Path(name).is_absolute() else [P/name,P/'helper-actual-controls-frozen'/name]
                        for p in candidates:
                            if p.is_file() and not artifact(p):f.retain(p,value);break
                for v in value.values():numeric_records(v)
            elif isinstance(value,list):
                for v in value:numeric_records(v)
        numeric_records(f.read(numeric_ids))
    pre=f.read(U/'PRECODE59_IDENTITIES.json')['files'];bindings=[]
    for x in pre:f.retain(B/Path(x['path']).name,x)
    for x in c.get('existing_file_identities',[]):f.retain(Path(x['source']),x)
    members=[];excluded=[]
    def archive(src,relative):
        rec=f.copied(src,A/E/relative);members.append({'path':relative,'source':str(src),'bytes':rec['bytes'],'sha256':rec['sha256'],'identity_origin':rec['origin']})
    for directory in c['immutable_directories']:
        base=Path(directory['source']);prefix=directory['archive_prefix']
        for p in sorted(base.rglob('*')):
            if not p.is_file():continue
            if artifact(p) or 'build'in p.relative_to(base).parts:
                excluded.append({'path':str(p),'bytes':p.stat().st_size,'action':'EXCLUDE_ALL_ARTIFACTS_AND_CACHE_COPIES'});continue
            archive(p,prefix+'/'+str(p.relative_to(base)))
    for x in c['immutable_files']:archive(Path(x['source']),x['archive_path'])
    for x in c['packaging_scripts']:
        archive(R/x,'raw/packaging-scripts/'+x)
    for name in [SOURCE,*[Path(x['path']).name for x in pre]]:
        rec=f.copied(B/name,A/'bindings'/name);bindings.append({'path':name,'bytes':rec['bytes'],'sha256':rec['sha256'],'action':'SKIP_ROOT_INSTALLED_UNCHANGED_BINDING'})
    actual_stream_paths={str(Path(x['receipt']).parent/(stream+'.log')) for x in runs for stream in ['stdout','stderr']}
    stream_members=[m for m in members if m['source'] in actual_stream_paths]
    result={'status':'NEW59_IMMUTABLE_ARCHIVE_COMPLETE_NO_SHARED_APPLY','source_cut':c['source_cut'],'qualified_baseline':f.BASE,'members':members,'excluded_artifacts':excluded,'bindings':bindings,'runs':runs,'actual_run_count':len(runs),'actual_split_stream_files':len(stream_members),'actual_split_stream_bytes':sum(m['bytes']for m in stream_members),'helper_lineage':lineage,'four_production_helpers_once':True,'fifth_controls_only_helper_separate_qualification':True,'historical_pending_records_preserved_verbatim':True,'old_hashes_or_math_replays':0,'own_object_action':'SKIP_ROOT_ALREADY_COPIED_ONCE'}
    f.write(R/'ARCHIVE_RESULT.json',result);return result
