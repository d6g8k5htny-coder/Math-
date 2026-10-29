"""Endpoint Git/blob qualification for the determinant producer; no Lean verdict.

The source checker remains responsible for the manifest's source/ABI policy. This
module authenticates its complete files map and fixed shared source helper to HEAD.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess

COMPONENT='frontiers/determinant_moment_20261025'
HELPER='tools/lean_packet_admission.py'
HEX40=re.compile('[0-9a-f]{40}')
HEX64=re.compile('[0-9a-f]{64}')


def _require(condition,message):
    if not condition:
        raise ValueError(message)


def _git(repo,*args):
    # Read only builtin metadata. Never run status/diff/hash-object --path or a
    # configured clean/smudge filter, external diff, fsmonitor or foreign index.
    environment={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
    environment.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_SYSTEM=os.devnull,
        GIT_NO_REPLACE_OBJECTS='1',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0')
    command=['git','--no-replace-objects','--literal-pathspecs','-c','core.fsmonitor=false',
             '-c','core.untrackedCache=false','-C',str(repo),*args]
    try:
        result=subprocess.run(command,env=environment,capture_output=True,timeout=30)
    except (OSError,subprocess.TimeoutExpired) as error:
        raise ValueError('Git source identity command failed') from error
    _require(result.returncode==0,'Git source identity command failed: '+result.stderr.decode(errors='replace')[:200])
    return result.stdout


def _entries(raw,*,index=False):
    _require(bool(raw) and raw.endswith(b'\0'),'empty or malformed Git metadata')
    result={}
    for row in raw[:-1].split(b'\0'):
        try:
            metadata,path=row.split(b'\t',1);first,second,third=metadata.decode('ascii').split(' ')
            path=path.decode('utf-8')
        except (ValueError,UnicodeError) as error:
            raise ValueError('malformed Git metadata entry') from error
        if index:
            mode,blob,stage=first,second,third
            _require(stage=='0','unmerged Git index refused')
            kind='commit' if mode=='160000' else 'blob'
        else:
            mode,kind,blob=first,second,third
        _require(re.fullmatch('[0-7]{6}',mode) and HEX40.fullmatch(blob) and path not in result,
                 'duplicate or malformed Git metadata entry')
        result[path]=(mode,kind,blob)
    return result


def _source_path(repo,relative):
    _require(type(relative) is str and bool(relative) and '\0' not in relative,'invalid source path')
    pure=PurePosixPath(relative)
    _require(not pure.is_absolute() and pure.as_posix()==relative and
             not any(part in ('.','..','.git','.lake','__pycache__') for part in pure.parts),
             'unsafe source path: '+relative)
    path=repo.joinpath(*pure.parts)
    _require(not any(p.is_symlink() for p in (path,*path.parents)),'symlink source or ancestor: '+relative)
    _require(path.is_file(),'missing regular source file: '+relative)
    return path


def _require_bound_git_sources(entries,files,origin):
    # HEAD and the expanded index can contain sources absent from the worktree.
    prefix=COMPONENT+'/'
    for path in entries:
        if not path.startswith(prefix):continue
        relative=path[len(prefix):]
        if any(part in ('.lake','__pycache__') for part in PurePosixPath(relative).parts):continue
        if relative.endswith(('.lean','.py')):
            _require(relative in files,'unregistered Lean/Python source in '+origin+': '+relative)


def _attest(repo,tree,index,relative,expected_sha256):
    _require(type(expected_sha256) is str and HEX64.fullmatch(expected_sha256),'invalid source SHA256: '+relative)
    entry=tree.get(relative)
    _require(entry is not None and entry[0] in ('100644','100755') and entry[1]=='blob',
             'missing or non-regular HEAD blob: '+relative)
    _require(index.get(relative)==entry,'source index differs from HEAD: '+relative)
    path=_source_path(repo,relative);mode=path.lstat().st_mode
    _require(stat.S_ISREG(mode),'non-regular source: '+relative)
    _require(('100755' if mode & stat.S_IXUSR else '100644')==entry[0],'source mode differs from HEAD: '+relative)
    raw=path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    _require(blob==entry[2],'source bytes differ from HEAD blob: '+relative)
    digest=hashlib.sha256(raw).hexdigest()
    _require(digest==expected_sha256,'source bytes differ from bound SHA256: '+relative)
    return dict(path=relative,git_blob=blob,sha256=digest,mode=entry[0],bytes=len(raw)),raw


def qualify_source(repo,manifest,manifest_sha256,*,previous=None):
    """Qualify before first Lean and again after the final command with previous=before.

    The deterministic record covers the complete committed manifest/files and shared
    helper. Unrelated tracked changes, runtime caches and unseen intervening writes
    are not claimed clean; this is an endpoint observation, not a filesystem lock.
    """
    repo=Path(repo).absolute()
    _require(repo.is_dir() and repo==repo.resolve() and not any(p.is_symlink() for p in (repo,*repo.parents)),
             'real non-symlink repository root required')
    _require(not (repo/'.git').is_symlink(),'symlink Git administrative entry refused')
    _require(_git(repo,'rev-parse','--is-inside-work-tree')==b'true\n','real Git worktree required')
    top=_git(repo,'rev-parse','--show-toplevel').decode('utf-8').rstrip('\n')
    _require(top==str(repo),'caller must supply the exact Git repository root')
    head=_git(repo,'rev-parse','--verify','HEAD^{commit}').decode('ascii').strip()
    tree_id=_git(repo,'rev-parse','--verify','HEAD^{tree}').decode('ascii').strip()
    _require(HEX40.fullmatch(head) and HEX40.fullmatch(tree_id),'exact SHA1 HEAD/tree required')
    tree=_entries(_git(repo,'ls-tree','-r','-z','--full-tree',head))
    # Without --sparse, ls-files expands sparse-directory index entries.
    index=_entries(_git(repo,'ls-files','--stage','-z'),index=True)
    manifest_path=COMPONENT+'/manifest.json'
    manifest_record,raw=_attest(repo,tree,index,manifest_path,manifest_sha256)
    def unique(pairs):
        value={}
        for key,item in pairs:
            _require(key not in value,'duplicate manifest JSON key: '+key)
            value[key]=item
        return value
    try:
        actual=json.loads(raw,object_pairs_hook=unique)
        _require(type(manifest) is dict and type(actual) is dict,'manifest must be a JSON object')
        canonical=lambda value:json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
        _require(canonical(manifest)==canonical(actual),'caller manifest differs from committed manifest bytes')
    except (TypeError,UnicodeError) as error:
        raise ValueError('invalid caller or committed manifest') from error
    files=actual.get('files')
    _require(type(files) is dict and bool(files),'complete bound files map required')
    _require_bound_git_sources(tree,files,'HEAD')
    _require_bound_git_sources(index,files,'index')
    records=[manifest_record]
    for relative,digest in sorted(files.items()):
        _require(type(relative) is str and relative!='manifest.json','invalid bound component file')
        # Validate relative spelling before prefixing; a prefix must not normalize ..
        _source_path(repo/COMPONENT,relative)
        record,_=_attest(repo,tree,index,COMPONENT+'/'+relative,digest);records.append(record)
    source_admission=actual.get('source_admission')
    _require(type(source_admission) is dict,'missing shared source helper binding')
    helper,_=_attest(repo,tree,index,HELPER,source_admission.get('helper_sha256'));records.append(helper)
    modules=actual.get('source_modules')
    _require(type(modules) is list and all(type(p) is str and p.endswith('.lean') for p in modules)
             and len(set(modules))==len(modules),'invalid registered source modules')
    registered=set(modules)|{'ResearchFormalCoreR1.lean'}
    _require(registered<=set(files),'unbound registered Lean source')
    observed_lean=set()
    def inventory_error(error):
        raise ValueError('source inventory I/O error') from error
    for directory,dirs,names in os.walk(repo/COMPONENT,followlinks=False,onerror=inventory_error):
        dirs[:]=[name for name in dirs if name not in ('.lake','__pycache__')]
        _require(not any((Path(directory)/name).is_symlink() for name in dirs),'symlink source directory')
        for name in names:
            if name.endswith(('.lean','.py')):
                relative=(Path(directory)/name).relative_to(repo/COMPONENT).as_posix()
                _require(relative in files,'unregistered Lean/Python source: '+relative)
                if name.endswith('.lean'):observed_lean.add(relative)
    _require(observed_lean==registered,'Lean file inventory differs from registered modules')
    records.sort(key=lambda row:row['path'])
    final_head=_git(repo,'rev-parse','--verify','HEAD^{commit}').decode('ascii').strip()
    final_tree=_git(repo,'rev-parse','--verify','HEAD^{tree}').decode('ascii').strip()
    final_index=_entries(_git(repo,'ls-files','--stage','-z'),index=True)
    _require_bound_git_sources(final_index,files,'final index')
    _require(final_head==head and final_tree==tree_id,'HEAD/tree changed during source qualification')
    _require(all(final_index.get(row['path'])==index[row['path']] for row in records),
             'source index changed during qualification')
    state=dict(schema_version=1,scope='DETERMINANT_MANIFEST_FILES_AND_SHARED_SOURCE_HELPER_ONLY',
        repository_root=str(repo),checked_commit=head,checked_tree=tree_id,manifest_sha256=manifest_record['sha256'],
        source_records=records,source_records_sha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),
        index_state='MATCHES_HEAD_FOR_QUALIFIED_FILES',unrelated_tracked_worktree='NOT_EVALUATED',
        excluded=['.lake runtime/cache/output files','__pycache__','unrelated unbound repository files',
                  'unobserved intervening writes between endpoint qualifications'],
        kernel_or_cbz_status='NOT_AWARDED')
    if previous is not None:
        _require(type(previous) is dict and canonical(previous)==canonical(state),
                 'qualified source state/HEAD differs from pre-execution identity')
    return state
