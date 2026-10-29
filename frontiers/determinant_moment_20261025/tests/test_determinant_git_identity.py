"""Real isolated Git/source tests only. No Lean or native gate execution."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/'determinant_git_identity.py'
spec=importlib.util.spec_from_file_location('determinant_git_identity_under_test',MODULE)
identity=importlib.util.module_from_spec(spec) if MODULE.exists() else None
if identity is not None:
    exec(compile(MODULE.read_bytes(),str(MODULE),'exec'),identity.__dict__)
COMPONENT='frontiers/determinant_moment_20261025'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class DeterminantGitIdentityTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(identity,'determinant Git identity module is missing')
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT);self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.repo=self.base/'repo';self.repo.mkdir()
        self.pkg=self.repo/COMPONENT;self.pkg.mkdir(parents=True)
        self.environment={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        self.environment.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_SYSTEM=os.devnull)
        self.git('init','-q');self.git('config','user.name','Isolated Identity Fixture')
        self.git('config','user.email','fixture@example.invalid')
        self.git('config','core.autocrlf','false')
        payloads={'README.md':b'bound fixture readme\n','gate.py':b'# fixture gate; never executed\n',
          'lean-toolchain':b'fixture toolchain; no runtime installed\n',
          'ResearchFormalCoreR1.lean':b'import ResearchFormalCoreR1.A\n',
          'ResearchFormalCoreR1/A.lean':b'namespace ResearchFormalCoreR1\ntheorem a : True := True.intro\nend ResearchFormalCoreR1\n',
          'determinant_git_identity.py':MODULE.read_bytes()}
        for name,raw in payloads.items():
            p=self.pkg/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        self.helper=self.repo/'tools/lean_packet_admission.py';self.helper.parent.mkdir();self.helper.write_bytes(b'# shared source helper fixture\n')
        (self.repo/'UNRELATED.md').write_text('outside qualified scope\n')
        (self.repo/'.gitattributes').write_text('*.lean filter=identity_fixture\n')
        self.manifest={'files':{name:sha(raw) for name,raw in payloads.items()},
          'source_modules':['ResearchFormalCoreR1/A.lean'],'targets':['ResearchFormalCoreR1.a'],
          'source_admission':{'helper_sha256':sha(self.helper.read_bytes())},'fixture_metadata':True}
        self.write_manifest();self.commit('initial isolated source')

    def git(self,*args):
        p=subprocess.run(['git','-C',str(self.repo),*args],env=self.environment,capture_output=True)
        self.assertEqual(p.returncode,0,p.stderr.decode(errors='replace'))
        return p.stdout.decode().strip()

    def commit(self,message):
        self.git('add','--all');self.git('commit','-q','-m',message)

    def write_manifest(self):
        raw=(json.dumps(self.manifest,indent=2)+'\n').encode()
        (self.pkg/'manifest.json').write_bytes(raw);self.digest=sha(raw)

    def qualify(self,**kwargs):
        return identity.qualify_source(self.repo,self.manifest,self.digest,**kwargs)

    def accepted(self,**kwargs):
        try:return self.qualify(**kwargs)
        except ValueError as error:self.fail('clean isolated Git source must qualify: '+str(error))

    def test_clean_exact_source_records_and_repeated_state(self):
        record=self.accepted()
        self.assertEqual(record['checked_commit'],self.git('rev-parse','HEAD'))
        self.assertEqual(record['checked_tree'],self.git('rev-parse','HEAD^{tree}'))
        self.assertEqual(record['manifest_sha256'],self.digest)
        self.assertEqual(len(record['source_records']),len(self.manifest['files'])+2)
        self.assertEqual(self.qualify(previous=record),record)
        self.assertEqual(record['kernel_or_cbz_status'],'NOT_AWARDED')

    def test_nongit_and_nested_root_are_refused(self):
        for root in (self.base,self.pkg):
            with self.subTest(root=str(root)),self.assertRaises(ValueError):
                identity.qualify_source(root,self.manifest,self.digest)

    def test_dirty_tracked_bytes_are_refused(self):
        (self.pkg/'README.md').write_text('dirty bytes\n')
        with self.assertRaises(ValueError):self.qualify()

    def test_self_consistently_rebound_dirty_source_and_manifest_refuse(self):
        (self.pkg/'README.md').write_text('dirty rebound bytes\n')
        self.manifest['files']['README.md']=sha((self.pkg/'README.md').read_bytes());self.write_manifest()
        with self.assertRaises(ValueError):self.qualify()

    def test_assume_unchanged_and_skip_worktree_do_not_hide_dirty_bytes(self):
        for flag in ('--assume-unchanged','--skip-worktree'):
            with self.subTest(flag=flag):
                self.git('update-index',flag,COMPONENT+'/README.md')
                (self.pkg/'README.md').write_text('hidden dirty source\n')
                with self.assertRaises(ValueError):self.qualify()
                (self.pkg/'README.md').write_text('bound fixture readme\n')
                self.git('update-index','--no-assume-unchanged','--no-skip-worktree',COMPONENT+'/README.md')

    def test_staged_file_differs_from_head_even_when_live_bytes_restored(self):
        path=self.pkg/'README.md';original=path.read_bytes();path.write_text('staged source\n')
        self.git('add',COMPONENT+'/README.md');path.write_bytes(original)
        with self.assertRaises(ValueError):self.qualify()

    def test_staged_manifest_differs_from_head_even_when_live_bytes_restored(self):
        path=self.pkg/'manifest.json';original=path.read_bytes()
        path.write_bytes(original+b' ');self.git('add',COMPONENT+'/manifest.json');path.write_bytes(original)
        with self.assertRaises(ValueError):self.qualify()

    def test_unmerged_single_stage_index_entry_is_refused(self):
        path=COMPONENT+'/README.md';blob=self.git('rev-parse','HEAD:'+path)
        self.git('update-index','--force-remove',path)
        process=subprocess.run(['git','-C',str(self.repo),'update-index','--index-info'],
            input=('100644 '+blob+' 1\t'+path+'\n').encode(),env=self.environment,capture_output=True)
        self.assertEqual(process.returncode,0,process.stderr.decode(errors='replace'))
        with self.assertRaises(ValueError):self.qualify()

    def test_new_native_head_requires_new_execution_identity(self):
        before=self.accepted();self.git('commit','--allow-empty','-q','-m','ordinary new native HEAD')
        with self.assertRaises(ValueError):self.qualify(previous=before)

    def test_new_commit_with_changed_rebound_source_cannot_match_prior_state(self):
        before=self.accepted();(self.pkg/'README.md').write_text('committed successor bytes\n')
        self.manifest['files']['README.md']=sha((self.pkg/'README.md').read_bytes());self.write_manifest();self.commit('source successor')
        with self.assertRaises(ValueError):self.qualify(previous=before)
        self.assertNotEqual(self.accepted()['checked_commit'],before['checked_commit'])

    def test_different_caller_manifest_refuses_even_with_original_digest(self):
        self.manifest['fixture_metadata']=False
        with self.assertRaises(ValueError):self.qualify()

    def test_boolean_and_integer_caller_metadata_are_distinct(self):
        self.manifest['fixture_metadata']=1
        with self.assertRaises(ValueError):self.qualify()

    def test_wrong_manifest_digest_is_refused(self):
        for value in ('0'*64,True,'HEAD'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                identity.qualify_source(self.repo,self.manifest,value)

    def test_changed_shared_source_helper_is_refused(self):
        self.helper.write_text('# changed source helper\n')
        with self.assertRaises(ValueError):self.qualify()

    def test_shared_helper_directory_symlink_is_refused(self):
        directory=self.helper.parent;outside=self.base/'same-helper-directory'
        directory.rename(outside);directory.symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ValueError):self.qualify()

    def test_source_symlink_with_identical_bytes_is_refused(self):
        path=self.pkg/'README.md';outside=self.base/'same-readme';outside.write_bytes(path.read_bytes())
        path.unlink();path.symlink_to(outside)
        with self.assertRaises(ValueError):self.qualify()

    def test_source_directory_symlink_with_identical_bytes_is_refused(self):
        directory=self.pkg/'ResearchFormalCoreR1';outside=self.base/'same-sources';directory.rename(outside);directory.symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ValueError):self.qualify()

    def test_symlink_repository_root_is_refused(self):
        alias=self.base/'repo-alias';alias.symlink_to(self.repo,target_is_directory=True)
        with self.assertRaises(ValueError):identity.qualify_source(alias,self.manifest,self.digest)

    def test_actual_executable_mode_drift_refuses_even_when_git_filemode_disabled(self):
        self.git('config','core.filemode','false');(self.pkg/'README.md').chmod(0o755)
        with self.assertRaises(ValueError):self.qualify()

    def assert_owner_execute_loss_refuses(self,path):
        relative=path.relative_to(self.repo).as_posix()
        path.chmod(0o755);self.commit('commit owner-executable source fixture')
        before=self.accepted()
        self.assertEqual(next(row['mode'] for row in before['source_records'] if row['path']==relative),'100755')
        for filemode in ('true','false'):
            self.git('config','core.filemode',filemode)
            for mode in (0o645,0o654,0o655):
                with self.subTest(path=relative,filemode=filemode,mode=oct(mode)):
                    path.chmod(mode)
                    self.assertEqual(path.stat().st_mode & 0o777,mode)
                    self.assertTrue(self.git('ls-tree','HEAD','--',relative).startswith('100755 '))
                    self.assertTrue(self.git('ls-files','--stage','--',relative).startswith('100755 '))
                    with self.assertRaisesRegex(ValueError,'source mode differs from HEAD'):
                        self.qualify(previous=before)
        path.chmod(0o755)

    def assert_non_owner_execute_bits_qualify(self,path):
        relative=path.relative_to(self.repo).as_posix();before=self.accepted()
        self.assertEqual(next(row['mode'] for row in before['source_records'] if row['path']==relative),'100644')
        for filemode in ('true','false'):
            self.git('config','core.filemode',filemode)
            for mode in (0o645,0o654,0o655):
                with self.subTest(path=relative,filemode=filemode,mode=oct(mode)):
                    path.chmod(mode)
                    self.assertEqual(path.stat().st_mode & 0o777,mode)
                    self.assertTrue(self.git('ls-tree','HEAD','--',relative).startswith('100644 '))
                    self.assertTrue(self.git('ls-files','--stage','--',relative).startswith('100644 '))
                    self.assertEqual(self.accepted(previous=before),before)
        path.chmod(0o644)

    def test_non_owner_execute_bits_do_not_preserve_executable_component_source(self):
        self.assert_owner_execute_loss_refuses(self.pkg/'gate.py')

    def test_non_owner_execute_bits_do_not_preserve_executable_shared_helper(self):
        self.assert_owner_execute_loss_refuses(self.helper)

    def test_non_owner_execute_bits_keep_nonexecutable_component_source_identity(self):
        self.assert_non_owner_execute_bits_qualify(self.pkg/'gate.py')

    def test_non_owner_execute_bits_keep_nonexecutable_shared_helper_identity(self):
        self.assert_non_owner_execute_bits_qualify(self.helper)

    def test_staged_executable_mode_drift_is_refused(self):
        self.git('update-index','--chmod=+x',COMPONENT+'/README.md')
        with self.assertRaises(ValueError):self.qualify()

    def test_unregistered_lean_and_python_sources_are_refused(self):
        for name in ('Unregistered.lean','unregistered.py'):
            with self.subTest(name=name):
                path=self.pkg/name;path.write_text('-- source fixture\n')
                with self.assertRaises(ValueError):self.qualify()
                path.unlink()

    def test_committed_unregistered_source_is_refused(self):
        (self.pkg/'Unregistered.lean').write_text('-- unregistered tracked source\n');self.commit('unregistered source')
        with self.assertRaises(ValueError):self.qualify()

    def test_hidden_head_only_unbound_lean_and_python_sources_are_refused(self):
        for name in ('Unbound.lean','unbound.py'):
            with self.subTest(name=name):
                path=self.pkg/'Hidden'/name;path.parent.mkdir(exist_ok=True);path.write_text('-- unbound HEAD fixture\n')
                relative=path.relative_to(self.repo).as_posix();self.commit('commit unbound HEAD source')
                self.git('update-index','--force-remove',relative);path.unlink()
                self.assertTrue(self.git('ls-tree','HEAD','--',relative).startswith('100644 '))
                self.assertEqual(self.git('ls-files','--stage','--',relative),'')
                self.assertFalse(path.exists())
                with self.assertRaisesRegex(ValueError,'unregistered Lean/Python source'):self.qualify()
                self.commit('remove unbound HEAD source')

    def test_hidden_index_only_unbound_lean_and_python_sources_are_refused(self):
        for name in ('Unbound.lean','unbound.py'):
            with self.subTest(name=name):
                path=self.pkg/'Hidden'/name;path.parent.mkdir(exist_ok=True);path.write_text('-- unbound staged fixture\n')
                relative=path.relative_to(self.repo).as_posix();self.git('add',relative);path.unlink()
                self.assertEqual(self.git('ls-tree','HEAD','--',relative),'')
                self.assertTrue(self.git('ls-files','--stage','--',relative).startswith('100644 '))
                self.assertFalse(path.exists())
                with self.assertRaisesRegex(ValueError,'unregistered Lean/Python source'):self.qualify()
                self.git('update-index','--force-remove',relative)

    def test_skip_worktree_absent_unbound_lean_and_python_sources_are_refused(self):
        for name in ('Unbound.lean','unbound.py'):
            with self.subTest(name=name):
                path=self.pkg/'Hidden'/name;path.parent.mkdir(exist_ok=True);path.write_text('-- unbound skip-worktree fixture\n')
                relative=path.relative_to(self.repo).as_posix();self.commit('commit unbound skip-worktree source')
                self.git('update-index','--skip-worktree',relative);path.unlink()
                self.assertTrue(self.git('ls-files','-t','--',relative).startswith('S '))
                self.assertFalse(path.exists())
                with self.assertRaisesRegex(ValueError,'unregistered Lean/Python source'):self.qualify()
                self.git('update-index','--no-skip-worktree',relative);self.commit('remove unbound skip-worktree source')

    def make_hidden_sparse_index(self):
        path=self.pkg/'Hidden/Unbound.lean';path.parent.mkdir();path.write_text('-- sparse unbound fixture\n')
        self.commit('commit hidden sparse-index source')
        self.git('sparse-checkout','init','--cone','--sparse-index')
        self.git('sparse-checkout','set',COMPONENT+'/ResearchFormalCoreR1','tools')
        self.assertFalse(path.exists())
        sparse=self.git('ls-files','--stage','--sparse')
        expanded=self.git('ls-files','--stage')
        self.assertRegex(sparse,r'(?m)^040000 [0-9a-f]{40} 0\t'+COMPONENT+'/Hidden/$')
        self.assertRegex(expanded,r'(?m)^100644 [0-9a-f]{40} 0\t'+COMPONENT+'/Hidden/Unbound.lean$')
        return path

    def test_sparse_index_hidden_unbound_source_is_refused(self):
        self.make_hidden_sparse_index()
        with self.assertRaisesRegex(ValueError,'unregistered Lean/Python source'):self.qualify()

    def test_sparse_index_only_hidden_unbound_source_is_refused(self):
        clean_head=self.git('rev-parse','HEAD');path=self.make_hidden_sparse_index()
        self.git('reset','--soft',clean_head)
        relative=path.relative_to(self.repo).as_posix()
        self.assertEqual(self.git('ls-tree','HEAD','--',relative),'')
        self.assertRegex(self.git('ls-files','--stage','--sparse'),r'(?m)^040000 [0-9a-f]{40} 0\t'+COMPONENT+'/Hidden/$')
        self.assertRegex(self.git('ls-files','--stage'),r'(?m)^100644 [0-9a-f]{40} 0\t'+relative+'$')
        with self.assertRaisesRegex(ValueError,'unregistered Lean/Python source'):self.qualify()

    def test_git_source_inventory_excludes_only_exact_cache_components_and_other_components(self):
        ignored=['.lake/cache.lean','__pycache__/cache.py','Hidden/.lake/cache.py','Hidden/__pycache__/cache.lean']
        for relative in ignored:
            path=self.pkg/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('-- excluded cache fixture\n')
        outside=self.repo/(COMPONENT+'_other')/'Unbound.lean';outside.parent.mkdir();outside.write_text('-- outside fixed component\n')
        self.commit('commit cache and unrelated component source');before=self.accepted()
        for relative in ignored:
            self.git('update-index','--skip-worktree',COMPONENT+'/'+relative);(self.pkg/relative).unlink()
        self.assertEqual(self.accepted(previous=before),before)
        for directory in ('.lakeish','__pycache___'):
            with self.subTest(directory=directory):
                path=self.pkg/directory/'unbound.py';path.parent.mkdir();path.write_text('# hidden non-cache source\n')
                relative=path.relative_to(self.repo).as_posix();self.git('add',relative);path.unlink()
                with self.assertRaisesRegex(ValueError,'unregistered Lean/Python source'):self.qualify()
                self.git('update-index','--force-remove',relative)

    def test_unbound_source_added_to_index_during_observation_is_refused(self):
        original=identity._git;changed=False
        def actual_git(repo,*args):
            nonlocal changed
            result=original(repo,*args)
            if args[:2]==('ls-files','--stage') and not changed:
                changed=True;path=self.pkg/'late_unbound.py';path.write_text('# staged after initial index observation\n')
                self.git('add',COMPONENT+'/late_unbound.py');path.unlink()
            return result
        with patch.object(identity,'_git',side_effect=actual_git),self.assertRaisesRegex(ValueError,'unregistered Lean/Python source'):
            self.qualify()
        self.assertTrue(changed)

    def test_explicit_directory_inventory_io_error_is_refused(self):
        directory=self.pkg/'InventoryError';directory.mkdir()
        (directory/'unbound.py').write_text('# source in the synthetically skipped directory\n')
        real_walk=os.walk;observed=[]
        injected=OSError(5,'synthetic directory inventory I/O error',str(directory))
        def walk_with_directory_error(top,topdown=True,onerror=None,followlinks=False):
            for current,dirs,names in real_walk(top,topdown=topdown,onerror=onerror,followlinks=followlinks):
                if Path(current)==directory:
                    observed.append(current)
                    if onerror is not None:onerror(injected)
                    continue
                yield current,dirs,names
        with patch.object(identity.os,'walk',new=walk_with_directory_error):
            with self.assertRaisesRegex(ValueError,'source inventory I/O error') as refused:
                self.qualify()
        self.assertEqual(observed,[str(directory)])
        self.assertIs(refused.exception.__cause__,injected)

    def test_bound_file_absent_from_head_is_refused(self):
        (self.pkg/'new.txt').write_text('new untracked bytes\n');self.manifest['files']['new.txt']=sha((self.pkg/'new.txt').read_bytes());self.write_manifest()
        self.git('add',COMPONENT+'/manifest.json');self.git('commit','-q','-m','manifest references untracked bytes')
        with self.assertRaises(ValueError):self.qualify()

    def test_bound_sha_must_match_even_when_head_and_live_blob_match(self):
        self.manifest['files']['README.md']='0'*64;self.write_manifest();self.commit('incorrect source SHA binding')
        with self.assertRaises(ValueError):self.qualify()

    def test_build_outputs_are_excluded_and_unrelated_dirty_bytes_not_claimed_clean(self):
        before=self.accepted();(self.pkg/'.lake/build').mkdir(parents=True)
        (self.pkg/'.lake/build/generated.lean').write_text('-- runtime output\n')
        (self.repo/'UNRELATED.md').write_text('unrelated dirty bytes\n')
        after=self.accepted(previous=before)
        self.assertEqual(after['unrelated_tracked_worktree'],'NOT_EVALUATED')

    def test_foreign_git_environment_does_not_redirect_identity(self):
        other=self.base/'foreign';other.mkdir()
        subprocess.run(['git','init','-q',str(other)],env=self.environment,check=True,capture_output=True)
        with patch.dict(os.environ,{'GIT_DIR':str(other/'.git'),'GIT_WORK_TREE':str(other),
            'GIT_INDEX_FILE':str(other/'foreign-index'),'GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'core.bare','GIT_CONFIG_VALUE_0':'true'}):
            record=self.accepted()
        self.assertEqual(record['checked_commit'],self.git('rev-parse','HEAD'))

    def test_configured_filters_fsmonitor_and_diff_are_never_executed(self):
        marker=self.base/'configured-command-ran';script=self.base/'configured-command.sh'
        script.write_text('#!/bin/sh\necho ran > '+str(marker)+'\ncat\n');script.chmod(0o755)
        self.git('config','filter.identity_fixture.clean',str(script));self.git('config','filter.identity_fixture.smudge',str(script))
        self.git('config','filter.identity_fixture.required','true');self.git('config','core.fsmonitor',str(script))
        self.git('config','diff.external',str(script));self.accepted();self.assertFalse(marker.exists())
        (self.pkg/'ResearchFormalCoreR1/A.lean').write_text('-- dirty source must refuse without running filter\n')
        with self.assertRaises(ValueError):self.qualify()
        self.assertFalse(marker.exists())

    def test_duplicate_manifest_keys_are_refused(self):
        raw=(self.pkg/'manifest.json').read_text();raw=raw.replace('{','{"fixture_metadata":false,',1)
        (self.pkg/'manifest.json').write_text(raw);self.digest=sha(raw.encode());self.commit('duplicate JSON key')
        with self.assertRaises(ValueError):self.qualify()

    def test_unsafe_bound_path_is_refused_even_if_committed(self):
        self.manifest['files']['../UNRELATED.md']=sha((self.repo/'UNRELATED.md').read_bytes());self.write_manifest();self.commit('unsafe path fixture')
        with self.assertRaises(ValueError):self.qualify()

    def test_head_change_during_observation_is_refused(self):
        original=identity._git;changed=False
        def actual_git(repo,*args):
            nonlocal changed
            result=original(repo,*args)
            if args[:2]==('ls-files','--stage') and not changed:
                changed=True;self.git('commit','--allow-empty','-q','-m','real concurrent HEAD change')
            return result
        with patch.object(identity,'_git',side_effect=actual_git),self.assertRaises(ValueError):self.qualify()
        self.assertTrue(changed)

    def test_index_change_during_observation_is_refused(self):
        original=identity._git;changed=False
        def actual_git(repo,*args):
            nonlocal changed
            result=original(repo,*args)
            if args[:2]==('ls-files','--stage') and not changed:
                changed=True;self.git('update-index','--chmod=+x',COMPONENT+'/README.md')
            return result
        with patch.object(identity,'_git',side_effect=actual_git),self.assertRaises(ValueError):self.qualify()
        self.assertTrue(changed)


if __name__=='__main__':unittest.main()
