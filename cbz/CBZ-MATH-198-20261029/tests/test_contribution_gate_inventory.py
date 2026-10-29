"""Source freeze includes active data and exact names, not only known code hashes."""
import importlib.util,json,sys,tempfile,unittest
from pathlib import Path

TOOL=Path(__file__).resolve().parents[1]/'tools/contribution_gate.py'

class InventoryTests(unittest.TestCase):
 def module(self):
  spec=importlib.util.spec_from_file_location('gate_inventory_review',TOOL);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
 def test_whole_inventory_rejects_new_code_and_changed_active_json(self):
  for change in ('add','json','remove','excluded-name'):
   with self.subTest(change=change),tempfile.TemporaryDirectory() as temp:
    m=self.module();root=Path(temp);source=root/'source';source.mkdir();(source/'module.py').write_text('pass\n');(source/'catalog.json').write_text('{"eligible": false}')
    inventory=m.freeze_inputs([source]);frozen=inventory['files_sha256']
    script={'add':"(p/'new_proof.lean').write_text('axiom injected : False')",'json':"(p/'catalog.json').write_text('{\\\"eligible\\\": true}')",'remove':"(p/'catalog.json').unlink()",'excluded-name':"(p/'support/evidence').mkdir(parents=True); (p/'support/evidence/new.py').write_text('pass')"}[change]
    argv=[sys.executable,'-B','-c','from pathlib import Path; import sys; p=Path(sys.argv[1]); '+script,str(source)]
    result=m.execute_jobs([{'id':'mutate','argv':argv,'cwd':str(root)}],root/'out',frozen,inventory=inventory)
    self.assertEqual(result['status'],'FAILED');self.assertEqual(result['failure'],'SOURCE_DRIFT')
 def test_added_file_before_first_job_cannot_be_repaired_and_accepted(self):
  with tempfile.TemporaryDirectory() as temp:
   m=self.module();root=Path(temp);source=root/'source';source.mkdir();(source/'known.py').write_text('pass');inventory=m.freeze_inputs([source])
   new=source/'unrecorded.json';new.write_text('{}');marker=root/'ran'
   argv=[sys.executable,'-c','from pathlib import Path; import sys; Path(sys.argv[1]).unlink(); Path(sys.argv[2]).write_text("ran")',str(new),str(marker)]
   result=m.execute_jobs([{'id':'repair','argv':argv,'cwd':str(root)}],root/'out',inventory['files_sha256'],inventory=inventory)
   self.assertEqual(result['failure'],'SOURCE_DRIFT');self.assertFalse(marker.exists());self.assertTrue(new.exists());self.assertEqual(result['records'],[])
 def test_only_explicit_operational_paths_are_excluded(self):
  with tempfile.TemporaryDirectory() as temp:
   m=self.module();root=Path(temp);source=root/'source';source.mkdir();(source/'module.py').write_text('pass');inventory=m.freeze_inputs([source],exclude=[source/'build'])
   argv=[sys.executable,'-c','from pathlib import Path; import sys; p=Path(sys.argv[1]); p.mkdir(); (p/"cache.json").write_text("{}")',str(source/'build')]
   result=m.execute_jobs([{'id':'cache','argv':argv,'cwd':str(root)}],root/'out',inventory['files_sha256'],inventory=inventory)
   self.assertEqual(result['status'],'LOCAL_CONTRIBUTION_PASS')
 def test_symlinked_source_input_is_not_silently_followed(self):
  with tempfile.TemporaryDirectory() as temp:
   m=self.module();root=Path(temp);source=root/'source';source.mkdir();outside=root/'outside';outside.write_text('pass');(source/'module.py').symlink_to(outside)
   with self.assertRaises(ValueError):m.freeze_inputs([source])

 def test_unreadable_subtree_cannot_be_silently_omitted(self):
  with tempfile.TemporaryDirectory() as temp:
   m=self.module();root=Path(temp);blocked=root/'unreadable';blocked.mkdir();(blocked/'input.json').write_text('{}');blocked.chmod(0)
   try:
    try:list(blocked.iterdir())
    except PermissionError:pass
    else:self.skipTest('OS grants this process read access despite mode000')
    with self.assertRaises(OSError):m.freeze_inputs([root])
   finally:blocked.chmod(0o700)

 def test_owned_kernel_gate_uses_the_fresh_cache_and_verified_parent_lock(self):
  m=self.module();jobs=m.plan(Path('/source'),Path('/newrun'),Path('/newbuild'),Path('/lean'),Path('/mathlib'))
  ids=[job['id'] for job in jobs];self.assertEqual(ids.index('owned-kernel-audit'),ids.index('fresh-proof')+1)
  self.assertLess(ids.index('owned-kernel-audit'),ids.index('native-build'))
  owned=jobs[ids.index('owned-kernel-audit')];argv=owned['argv']
  self.assertTrue(all(type(value) is str for value in argv))
  self.assertEqual(argv[argv.index('--formal-cache')+1],'/newbuild/formal')
  self.assertEqual(argv[argv.index('--formal-evidence')+1],'/newrun/formal-evidence/results.json')
  self.assertIn('--parent-lock-held',argv)

 def test_last_source_observation_cannot_disagree_with_pass_status(self):
  with tempfile.TemporaryDirectory() as temp:
   m=self.module();root=Path(temp);source=root/'input.json';source.write_text('before');frozen={str(source):m.sha(source)}
   original=m._sources_match;calls=[0]
   def observed(current,inventory):
    calls[0]+=1
    if calls[0]==3:source.write_text('changed at final observation')
    return original(current,inventory)
   m._sources_match=observed
   result=m.execute_jobs([{'id':'real','argv':[sys.executable,'-B','-c','print("finished")'],'cwd':str(root)}],root/'out',frozen)
   self.assertEqual(result['status'],'FAILED');self.assertEqual(result['failure'],'SOURCE_DRIFT');self.assertFalse(result['source_unchanged_final'])
   self.assertEqual(len(result['records']),1);self.assertTrue(result['records'][0]['succeeded'])

 def test_path_cwd_is_normalized_before_child_and_result_serialization(self):
  with tempfile.TemporaryDirectory() as temp:
   m=self.module();root=Path(temp)
   result=m.execute_jobs([{'id':'real','argv':[sys.executable,'-B','-c','print("observed")'],'cwd':root}],root/'out',{})
   self.assertEqual(result['status'],'LOCAL_CONTRIBUTION_PASS')
   saved=json.loads((root/'out/results.json').read_text())
   self.assertEqual(saved['plan'][0]['cwd'],str(root.resolve()))
   self.assertTrue(saved['records'][0]['succeeded'])

if __name__=='__main__':unittest.main()
