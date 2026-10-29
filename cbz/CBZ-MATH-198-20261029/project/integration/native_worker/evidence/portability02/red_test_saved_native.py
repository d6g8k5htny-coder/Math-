import copy,json
from pathlib import Path
import shutil,tempfile,unittest
import verify_native_saved as verifier

class SavedNativeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'campaign'
        shutil.copytree(verifier.HERE/'evidence/session04',self.path)
        self.controller=verifier.HERE/'sources/session04_controller'
    def write(self,path,value): path.write_text(json.dumps(value))
    def test_complete_native_saved_campaign_replays(self):
        result=verifier.check(self.path,controller_source_root=self.controller)
        self.assertEqual(result['native_endpoint_certificates'],49)
        self.assertEqual(result['fresh_endpoint_rechecks'],49)
        self.assertFalse(result['kernel_executed_by_this_verifier'])
    def test_export_cannot_change_while_native_closed_and_verify_payload_stay(self):
        path=self.path/'produce/results.json';value=json.loads(path.read_text());row=value['records'][0]
        certificate=self.path/'produce'/row['certificate'];proof=json.loads(certificate.read_text())
        proof['proof']={'schema':'ul-expr-dag-v1','nodes':[{'bvar':0}],'root':0}
        self.write(certificate,proof);row['certificate_sha256']=verifier.rt._hash(certificate);self.write(path,value)
        with self.assertRaises(ValueError):verifier.check(self.path,controller_source_root=self.controller)
    def test_duplicate_fresh_target_cannot_replace_complete_coverage(self):
        path=self.path/'recheck/results.json';value=json.loads(path.read_text())
        value['records'][-1]=value['records'][0];self.write(path,value)
        with self.assertRaises(ValueError):verifier.check(self.path,controller_source_root=self.controller)
    def test_repeated_negative_response_cannot_replace_three_controls(self):
        path=self.path/'recheck/results.json';value=json.loads(path.read_text())
        wrong=value['negative_controls']['forbidden_axiom']
        value['negative_controls']={label:wrong for label in value['negative_controls']}
        self.write(path,value)
        with self.assertRaises(ValueError):verifier.check(self.path,controller_source_root=self.controller)
    def test_omitted_budget_search_cannot_hide_paid_requests(self):
        path=self.path/'budget/results.json';value=json.loads(path.read_text())
        del value['searches'][0];self.write(path,value)
        with self.assertRaises(ValueError):verifier.check(self.path,controller_source_root=self.controller)
    def test_current_final_campaign_cannot_hide_forced_teardown(self):
        path=self.path/'budget/worker/receipt.json';value=json.loads(path.read_text())
        value['returncode']=-9;value['forced_termination']=True;self.write(path,value)
        events=path.parent/'events.jsonl';rows=[json.loads(line) for line in events.read_text().splitlines()]
        rows[-1]={'event':'worker_stopped',**value}
        events.write_text(''.join(json.dumps(row)+'\n' for row in rows))
        with self.assertRaises(ValueError):verifier.check(self.path,controller_source_root=self.controller)

    def test_request_payload_tamper_rejects_despite_original_accepted_response(self):
        path=self.path/'recheck/worker/events.jsonl'
        rows=[json.loads(line) for line in path.read_text().splitlines()]
        for row in rows:
            if row['event']=='request_started' and row['request']['op']=='verify':
                row['request']['certificate']['proof']={'schema':'ul-expr-dag-v1','nodes':[{'bvar':0}],'root':0};break
        path.write_text(''.join(json.dumps(r)+'\n' for r in rows))
        with self.assertRaises(ValueError):verifier.check(self.path,controller_source_root=self.controller)

    def test_empty_controller_source_map_cannot_erase_the_binding(self):
        path=self.path/'results.json';value=json.loads(path.read_text())
        value['controller_transport_sources_sha256']={};self.write(path,value)
        with self.assertRaisesRegex(ValueError,'source inventory mismatch'):
            verifier.check(self.path,controller_source_root=self.controller)

    def test_partial_controller_source_map_cannot_omit_runtime(self):
        path=self.path/'results.json';value=json.loads(path.read_text())
        del value['controller_transport_sources_sha256']['integration/native_worker/runtime_support.py']
        self.write(path,value)
        with self.assertRaisesRegex(ValueError,'source inventory mismatch'):
            verifier.check(self.path,controller_source_root=self.controller)

    def test_extra_controller_source_claim_is_refused_before_path_access(self):
        path=self.path/'results.json';value=json.loads(path.read_text())
        value['controller_transport_sources_sha256']['../forged-controller.py']='0'*64
        self.write(path,value)
        with self.assertRaisesRegex(ValueError,'source inventory mismatch'):
            verifier.check(self.path,controller_source_root=self.controller)

    def test_controller_source_map_and_digest_types_are_checked(self):
        path=self.path/'results.json';original=json.loads(path.read_text())
        for bad in [None,[],False,'controller-map',
                    {**original['controller_transport_sources_sha256'],
                     'integration/native_worker/runtime_support.py':False}]:
            with self.subTest(bad=bad):
                value=copy.deepcopy(original);value['controller_transport_sources_sha256']=bad
                self.write(path,value)
                with self.assertRaises(ValueError):
                    verifier.check(self.path,controller_source_root=self.controller)

    def test_incomplete_controller_source_root_cannot_define_a_smaller_campaign(self):
        source=Path(self.temp.name)/'incomplete-source'
        path=self.path/'results.json';value=json.loads(path.read_text())
        value['controller_transport_sources_sha256']={}
        for rel in ['integration/engine_audit/ul_engine/search.py','integration/engine_audit/ul_engine/worker.py']:
            target=source/rel;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(self.controller/rel,target)
            value['controller_transport_sources_sha256'][rel]=verifier.rt._hash(target)
        self.write(path,value)
        with self.assertRaisesRegex(ValueError,'source inventory mismatch'):
            verifier.check(self.path,controller_source_root=source)

if __name__=='__main__':unittest.main()
