"""Prepared63 archive association. Importing is not authority to execute."""
from pathlib import Path
import custody as f
R,P,U,B,A,E=f.R,f.P,f.U,f.B,f.A,f.E
BAD={'.olean','.ilean','.c','.o','.so','.a','.pyc','.bin','.pkl','.pickle'}
def artifact(p):
    return any(s in p.name for s in ['.olean','.ilean']) or p.suffix in BAD or any(s in p.parts for s in ['.lake','__pycache__'])
def gate(c):
    f.require(c['status']=='ROOT_GO_FINAL63_ASSEMBLY_AND_ONE_METADATA_ATTEMPT','Actual final63 root GO required')
    go=Path(c['root_finalization_go']);f.require(go.is_file(),'Missing root final GO')
    f.require(f.read(go)['status']==c['status'],'Root GO status mismatch')
    f.require(all(c[k] for k in ['all_math_complete','final_review_pass','source_cut_committed','own_object_copied_once','immutable_payloads_frozen']),'No pending production/archive payload')
    f.require(c['qualified_baseline']==f.BASE and len(c['source_cut'])==40,'Actual63 cut/qualified62 baseline')
    f.require(c['inventory_summary']['authored_public_Prop']==1 and c['inventory_summary']['authored_public_data']==0,'63 one public Prop/no data')
def record_path(value):
    p=Path(value);return p if p.is_absolute() else P/p
def prepare(c):
    gate(c)
    if (R/'ARCHIVE_RESULT.json').exists():
        old=f.read(R/'ARCHIVE_RESULT.json');f.require(old['source_cut']==c['source_cut'],'Changed cut requires separate process binding');return old
    f.retain(B/f.SOURCE,c['source_identity'])
    # Explicit final canonical identities never silently inherit a historical path ID.
    # Historical payloads are supplied by root using their actual immutable snapshot paths.
    for x in c['existing_file_identities']:
        p=Path(x['source'])
        if not artifact(p):f.retain(p,x)
    # The actual63 runner snapshots every tracked source/harness/runner/context version.
    # Do not bind a historical before/after identity to a later changed canonical file.
    runs=[]
    for value in c['run_records']:
        p=record_path(value);q=f.read(p)
        f.require(p.name=='receipt.json' and 'exit_code' in q and 'ended_utc' in q,'Unfinished or unexpected actual63 receipt')
        f.require(all(k in q for k in ['command','cwd','started_utc','stdout','stderr']),'Incomplete actual command/time/stream receipt')
        runs.append({'label':q.get('label',p.parent.name),'record_path':str(p),'record':q})
        for x in q.get('snapshots',[]):
            z=Path(x['immutable_path']);rec=x['existing_identity']
            if z.is_file() and not artifact(z):f.retain(z,rec)
        for key in ['stdout','stderr']:
            x=q[key];z=Path(x.get('path',p.parent/(key+'.log')))
            f.require(z==p.parent/(key+'.log'),'Actual63 original split-stream path differs')
            f.retain(z,x)
    pre=f.read(U/'PRECODE63_IDENTITIES.json')['files']
    f.require(len(pre)==4,'Four precommitted63 bindings')
    for x in pre:f.retain(B/Path(x['path']).name,x)
    members=[];excluded=[];destinations=set()
    def add(src,relative):
        f.require(relative not in destinations,'Duplicate archive destination '+relative);destinations.add(relative)
        rec=f.copied(src,A/E/relative)
        members.append({'path':relative,'source':str(src),'bytes':rec['bytes'],'sha256':rec['sha256'],'identity_origin':rec['origin']})
    for x in c['immutable_directories']:
        base=Path(x['source'])
        for p in sorted(base.rglob('*')):
            if not p.is_file():continue
            if artifact(p) or {'objects','build'}&set(p.relative_to(base).parts):
                excluded.append({'source':str(p),'bytes':p.stat().st_size,'action':'EXCLUDE_ALL_ACTUAL_ARTIFACTS_AND_CACHE_COPIES'});continue
            add(p,x['archive_prefix']+'/'+str(p.relative_to(base)))
    for x in c['immutable_files']:add(Path(x['source']),x['archive_path'])
    for directory in c.get('excluded_artifact_directories',[]):
        for p in sorted(Path(directory).rglob('*')):
            if p.is_file():excluded.append({'source':str(p),'bytes':p.stat().st_size,'action':'EXCLUDE_ALL_ACTUAL_ARTIFACTS_AND_CACHE_COPIES'})
    for name in c['packaging_scripts']:add(R/name,'raw/packaging-scripts/'+name)
    bindings=[]
    for name in [f.SOURCE,*[Path(x['path']).name for x in pre]]:
        rec=f.copied(B/name,A/'bindings'/name)
        bindings.append({'path':name,'bytes':rec['bytes'],'sha256':rec['sha256'],'action':'SKIP_ROOT_INSTALLED_BINDING'})
    actual={str(Path(x['record_path']).parent/(s+'.log')) for x in runs for s in ['stdout','stderr']}
    streams=[x for x in members if x['source'] in actual]
    result={'status':'IMMUTABLE63_ARCHIVE_READY_NO_SHARED_APPLY','source_cut':c['source_cut'],'qualified_baseline':f.BASE,'members':members,'excluded_artifacts':excluded,'bindings':bindings,'runs':runs,'actual_run_count':len(runs),'actual_split_stream_files':len(streams),'actual_split_stream_bytes':sum(x['bytes'] for x in streams),'production_helpers':c['production_helper_integrations'],'ordinary_controls_custody':c['ordinary_controls_custody'],'historical_pending_records_preserved':True,'own_object_action':'SKIP_ROOT_COPIED_ONCE_ALL_FURTHER_COPIES_SKIP','old_payload_hashes':0,'proof_replays':0}
    f.write(R/'ARCHIVE_RESULT.json',result);return result
