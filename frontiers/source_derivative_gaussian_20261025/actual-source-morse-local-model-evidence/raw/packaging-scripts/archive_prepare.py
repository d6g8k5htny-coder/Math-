"""Prepared60 archive logic; never executed before final rootGO. Correct60 RECORD/.txt schema."""
from pathlib import Path
import custody as f
R,P,U,B,A,E=f.R,f.P,f.U,f.B,f.A,f.E
SOURCE=f.SOURCE
BAD={'.olean','.ilean','.c','.o','.so','.a','.pyc','.bin','.pkl','.pickle'}
def artifact(p):return any(s in p.name for s in ['.olean','.ilean'])or p.suffix in BAD or any(s in p.parts for s in ['.lake','__pycache__'])
def prepare(c):
    f.require(c['status']=='ROOT_GO_FINAL60_ASSEMBLY_AND_ONE_METADATA_ATTEMPT','Actual final60 rootGO required')
    f.require(all(c[k]for k in ['all_math_complete','final_review_pass','source_cut_committed','own_object_copied_once','immutable_payloads_frozen']),'No mutable/pending archive')
    f.require(c['qualified_baseline']==f.BASE and len(c['source_cut'])==40,'Actual cut/baseline')
    if (R/'ARCHIVE_RESULT.json').exists():
        old=f.read(R/'ARCHIVE_RESULT.json');f.require(old['source_cut']==c['source_cut'],'Changed cut requires separate process binding');return old
    f.CUT=c['source_cut']
    f.retain(B/SOURCE,{'bytes':65754,'sha256':f.SRC_SHA})
    # The60 binder records immutable snapshots by role; its path can be historical/mutable.
    # Seed SNAPSHOT bytes, not the latest canonical file merely because the name matches.
    for x in f.read(P/'ARTIFACT_IDENTITIES.json')['artifacts']:
        p=Path(x['snapshot'])
        if p.is_file()and not artifact(p):f.retain(p,x)
    helper=f.read(P/'HELPER_INTEGRATIONS.json');ordinary=f.read(P/'CONTROLS_INTEGRATION.json')
    for block in helper['integrations']+[ordinary]:
        for x in block['original_identities']:
            p=Path(x['snapshot'])
            if p.is_file()and not artifact(p):f.retain(p,x)
    runs=[]
    for value in c['run_records']:
        p=Path(value)if Path(value).is_absolute()else P/value
        q=f.read(p);f.require('exit_code'in q and'end_utc'in q,'Unfinished actual60 run')
        f.require(p.name=='RECORD.json','60 record format must not be parsed as59 receipt')
        runs.append({'label':q.get('label',p.parent.name),'record_path':str(p),'record':q})
        for key in ['source_identity','harness_identity']:
            x=q.get(key)
            if not x:continue
            for z in [Path(x['snapshot']),p.parent/Path(x['path']).name]:
                if z.is_file()and not artifact(z):f.retain(z,x)
        # Streams are stdout.txt/stderr.txt; final producer custody supplies existing IDs.
        for key in ['stdout_identity','stderr_identity']:
            x=q.get(key)
            if x:
                z=p.parent/('stdout.txt'if key=='stdout_identity'else'stderr.txt')
                f.retain(z,x)
    pre=f.read(U/'PRECODE60_IDENTITIES.json')['files']
    for x in pre:f.retain(B/Path(x['path']).name,x)
    for x in c.get('existing_file_identities',[]):f.retain(Path(x['source']),x)
    members=[];excluded=[]
    def add(src,relative):
        rec=f.copied(src,A/E/relative);members.append({'path':relative,'source':str(src),'bytes':rec['bytes'],'sha256':rec['sha256'],'identity_origin':rec['origin']})
    for x in c['immutable_directories']:
        base=Path(x['source'])
        for p in sorted(base.rglob('*')):
            if not p.is_file():continue
            if artifact(p)or'objects'in p.relative_to(base).parts or'build'in p.relative_to(base).parts:
                excluded.append({'source':str(p),'bytes':p.stat().st_size,'action':'EXCLUDE_ALL_ACTUAL_ARTIFACTS_AND_CACHE_COPIES'});continue
            add(p,x['archive_prefix']+'/'+str(p.relative_to(base)))
    for x in c['immutable_files']:add(Path(x['source']),x['archive_path'])
    for n in c['packaging_scripts']:add(R/n,'raw/packaging-scripts/'+n)
    bindings=[]
    for n in [SOURCE,*[Path(x['path']).name for x in pre]]:
        rec=f.copied(B/n,A/'bindings'/n);bindings.append({'path':n,'bytes':rec['bytes'],'sha256':rec['sha256'],'action':'SKIP_ROOT_INSTALLED_BINDING'})
    actual={str(Path(r['record_path']).parent/(s+'.txt'))for r in runs for s in ['stdout','stderr']}
    streams=[m for m in members if m['source']in actual]
    result={'status':'IMMUTABLE60_ARCHIVE_READY_NO_SHARED_APPLY','source_cut':c['source_cut'],'qualified_baseline':f.BASE,'members':members,'excluded_artifacts':excluded,'bindings':bindings,'runs':runs,'actual_run_count':len(runs),'actual_split_stream_files':len(streams),'actual_split_stream_bytes':sum(x['bytes']for x in streams),'production_helpers':helper,'ordinary_controls_integration':ordinary,'historical_pending_records_preserved':True,'own_object_action':'SKIP_ROOT_COPIED_ONCE_ALL_FURTHER_COPIES_SKIP','old_payload_hashes':0,'proof_replays':0}
    f.write(R/'ARCHIVE_RESULT.json',result);return result
