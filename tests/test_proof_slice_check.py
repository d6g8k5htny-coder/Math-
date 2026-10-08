"""Synthetic closed-contract controls. No mathematical implications are tested."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('proof_slice_check', ROOT / 'tools/proof_slice_check.py')
CHECKER = None
if SPEC and Path(SPEC.origin).exists():
    CHECKER = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(CHECKER)
FIXTURE = json.loads((ROOT / 'tests/fixtures/proof_slice_cases.json').read_text())


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(CHECKER, 'Stage A checker has not been implemented')
        self.f = copy.deepcopy(FIXTURE)

    def report(self):
        return CHECKER.validate_proof_slice(
            self.f['companion'], self.f['expected'], self.f['expected_pin'],
            {CHECKER.file_key(self.f['expected']['source']): self.f['source_text'].encode()},
            {'expected': self.f['snapshots'], 'companion': self.f['snapshots']})

    def valid(self):
        r = self.report()
        self.assertTrue(r['valid'], r)
        return r

    def refuses(self, reason):
        r = self.report()
        self.assertFalse(r['valid'], r)
        self.assertEqual(r['reason'], reason, r)
        self.assertNotIn('counts', r)
        self.assertNotIn('review_targets', r)
        return r

    def test_synthetic_inventory_and_companion_valid(self):
        r = self.valid()
        self.assertEqual(r['counts']['units'], 4)
        self.assertEqual(r['counts']['uses'], 4)
        self.assertEqual(r['counts']['by_kind']['premise'], 3)
        self.assertEqual(r['counts']['unknown_annotations'], 1)

    def test_inventory_only_valid(self):
        r = CHECKER.validate_expected_inventory(self.f['expected'],
            {CHECKER.file_key(self.f['expected']['source']): self.f['source_text'].encode()},
            self.f['snapshots'])
        self.assertTrue(r['valid'], r)

    def test_declared_conformance_vectors(self):
        for case in FIXTURE['cases']:
            with self.subTest(case=case['name']):
                self.f = copy.deepcopy(FIXTURE)
                self.mutate(case['mutations'])
                result=self.refuses(case['reason'])
                if 'failed_input' in case:
                    self.assertEqual(result['failed_input'],case['failed_input'])

    def mutate(self, mutations):
        for mutation in mutations:
            obj = self.f['expected_pin' if mutation['input'] == 'pin' else mutation['input']]
            for component in mutation['path'][:-1]:
                obj = obj[component]
            if mutation.get('op') == 'remove':
                del obj[mutation['path'][-1]]
            else:
                obj[mutation['path'][-1]] = copy.deepcopy(mutation['value'])

    def test_portable_target_comparison_vectors(self):
        for case in FIXTURE['target_cases']:
            with self.subTest(case=case['name']):
                self.f=copy.deepcopy(FIXTURE)
                self.mutate(case.get('before',[]))
                self.valid()
                old=CHECKER.resolve_use_target(self.f['companion'],case['use_id'])
                self.mutate(case['mutations'])
                self.valid()
                new=CHECKER.resolve_use_target(self.f['companion'],case['use_id'])
                self.assertEqual(CHECKER.typed_equal(old,new),case['target_equal'])

    def test_portable_historical_intrinsic_vectors(self):
        for case in FIXTURE['historical_cases']:
            with self.subTest(case=case['name']):
                self.f=copy.deepcopy(FIXTURE)
                old=self.historical_with_reading()
                for obj in list(CHECKER.walk(old)):
                    if set(obj)==set(CHECKER.SHAPES[case['type']]):
                        obj.update(copy.deepcopy(case['values']))
                if 'reason' in case:self.refuses(case['reason'])
                else:
                    result=self.valid()
                    self.assertEqual(result['review_targets'][0]['matches_current'],case['matches_current'])

    def test_group_and_member_permutations_preserve_full_target(self):
        self.valid()
        before = CHECKER.resolve_use_target(self.f['companion'], 'U1')
        self.f['companion']['units'][0]['premise_groups'][0]['premise_use_ids'].reverse()
        self.f['companion']['bundles'][0]['group_ids'].reverse()
        self.valid()
        self.assertEqual(before, CHECKER.resolve_use_target(self.f['companion'], 'U1'))
        self.assertEqual(self.f['expected']['expected_bundles'][0]['group_ids'], ['GB', 'GA'])

    def test_narrowed_consumer_spans_are_valid(self):
        self.f['companion']['units'][0]['uses'][1]['binding']['consumer_source']['lines'] = [327, 327]
        self.f['companion']['units'][1]['uses'][0]['binding']['consumer_source']['lines'] = [361, 361]
        self.valid()

    def test_whole_unit_rule_refuses_narrow_span(self):
        self.f['expected']['consumer_span_rule'] = 'whole_unit'
        self.f['companion']['units'][0]['uses'][1]['binding']['consumer_source']['lines'] = [327, 327]
        self.refuses('SOURCE_JOIN_MISMATCH')

    def test_coherent_zero_use_deletion_still_refuses(self):
        self.f['companion']['units'].pop()
        self.refuses('EXPECTED_INVENTORY_MISMATCH')

    def test_same_count_unit_replacement_still_refuses(self):
        self.f['companion']['units'][-1]['id'] = 'REPLACEMENT'
        self.refuses('EXPECTED_INVENTORY_MISMATCH')

    def test_second_distinct_group_under_one_owner_is_unsupported(self):
        g = copy.deepcopy(self.f['companion']['units'][0]['premise_groups'][0])
        g['id'] = 'GA2'
        self.f['companion']['units'][0]['premise_groups'].append(g)
        self.refuses('UNSUPPORTED_INFERENCE')

    def test_duplicate_group_id_is_shape_not_second_route(self):
        self.f['companion']['units'][0]['premise_groups'] *= 2
        self.refuses('CONTRACT_SHAPE')

    def test_distinct_bundles_for_one_conclusion_are_unsupported(self):
        bundle = copy.deepcopy(self.f['companion']['bundles'][0])
        bundle['id'] = 'BC2'
        self.f['companion']['bundles'].append(bundle)
        self.refuses('UNSUPPORTED_INFERENCE')

    def test_duplicate_bundle_id_is_shape(self):
        self.f['companion']['bundles'] *= 2
        self.refuses('CONTRACT_SHAPE')

    def test_join_failure_precedes_composition_failure(self):
        self.f['companion']['units'][2]['source']['lines'] = [441, 442]
        self.f['companion']['bundles'] = []
        self.refuses('SOURCE_JOIN_MISMATCH')

    def test_unsupported_composition_precedes_internal_membership(self):
        self.f['expected']['expected_bundles'][0]['group_ids'] = ['GA', 'missing']
        self.f['companion']['bundles'] = []
        self.refuses('UNSUPPORTED_INFERENCE')

    def test_internal_membership_precedes_expected_comparison(self):
        self.f['companion']['bundles'][0]['group_ids'] = ['GA', 'missing']
        self.f['companion']['bundles'][0]['basis']['text'] = 'Changed'
        self.refuses('CONTRACT_SHAPE')

    def test_shape_precedes_outer_pin(self):
        self.f['expected']['extra'] = 1
        self.f['expected_pin']['commit'] = '3' * 40
        self.refuses('CONTRACT_SHAPE')

    def test_mode_scan_is_type_guarded(self):
        self.f['companion']['units'][0]['premise_groups'] = [None]
        self.refuses('CONTRACT_SHAPE')

    def test_unknowns_empty_reviews_and_unexpanded_supplier_remain_valid(self):
        self.valid()
        self.assertEqual(self.f['companion']['units'][0]['uses'][0]['applicability_reviews'], [])
        self.assertEqual(self.f['companion']['suppliers'][0]['expansion'], 'unexpanded')

    def test_unknown_cycle_refused(self):
        self.f['expected']['unknowns'][0]['description']['unknown_refs'] = ['W']
        self.refuses('CONTRACT_SHAPE')

    def test_missing_source_input_refused(self):
        r = CHECKER.validate_expected_inventory(self.f['expected'], {}, self.f['snapshots'])
        self.assertEqual(r['reason'], 'INPUT_UNAVAILABLE', r)

    def test_changed_retained_body_refused(self):
        self.f['snapshots']['R11']['body'] += 'changed'
        self.refuses('IDENTITY_MISMATCH')

    def test_comment_cannot_carry_native_commit(self):
        self.f['expected']['records'][0]['identity']['native_commit'] = 'a' * 40
        self.refuses('CONTRACT_SHAPE')

    def test_missing_record_capture_refused(self):
        del self.f['snapshots']['R11']
        self.refuses('INPUT_UNAVAILABLE')

    def test_nonrecursive_complete_bundle_tracks_other_owner_core(self):
        before = CHECKER.resolve_use_target(self.f['companion'], 'U1')
        self.f['companion']['units'][1]['uses'][0]['binding']['context']['text'] = 'Changed other-owner scope'
        self.valid()
        after = CHECKER.resolve_use_target(self.f['companion'], 'U1')
        self.assertNotEqual(before, after)
        for g in after['bundle_context']['groups']:
            for m in g['members']:
                self.assertNotIn('bundle_context', m['core'])
                self.assertNotIn('inference_context', m['core'])

    def test_observation_only_change_does_not_change_target(self):
        self.f['companion']['suppliers'][0]['unknown_refs'] = []
        before = CHECKER.resolve_use_target(self.f['companion'], 'U1')
        self.f['companion']['unknowns'][0]['description']['text'] = 'Later direct observation'
        self.valid()
        self.assertEqual(before, CHECKER.resolve_use_target(self.f['companion'], 'U1'))

    def add_review(self):
        u = self.f['companion']['units'][0]['uses'][0]
        t = copy.deepcopy(u['binding']['context'])
        u['applicability_reviews'] = [{'record': {'record_id':'R14','locator':'Synthetic record'},
            'reviewed_use': CHECKER.resolve_use_target(self.f['companion'], 'U1'),
            'scope': t, 'disposition_as_recorded':'Synthetic scope only', 'limitations':[t],
            'later_disposition_records':[]}]
        return u['applicability_reviews'][0]

    def test_current_review_target_and_historical_mismatch_are_distinct(self):
        self.add_review()
        r = self.valid()
        self.assertEqual(r['review_targets'][0]['matches_current'], True)
        self.f['companion']['units'][1]['uses'][0]['binding']['context']['text'] = 'Changed co-premise'
        r = self.valid()
        self.assertEqual(r['review_targets'][0]['matches_current'], False)

    def test_old_target_without_bundle_context_not_migrated(self):
        del self.add_review()['reviewed_use']['bundle_context']
        self.refuses('CONTRACT_SHAPE')

    def test_review_role_and_holding_use_must_match(self):
        r = self.add_review()
        r['record']['record_id'] = 'R11'
        self.refuses('CONTRACT_SHAPE')
        r['record']['record_id'] = 'R14'
        r['reviewed_use']['use_id'] = 'U2'
        self.refuses('CONTRACT_SHAPE')

    def test_historical_valid_different_conclusion_is_not_current_join_failure(self):
        r = self.add_review()
        old = r['reviewed_use']
        for c in [old['inference_context']['conclusion'], old['bundle_context']['conclusion']]:
            c['source']['lines'] = [440, 440]
        for g in old['bundle_context']['groups']:
            g['conclusion']['source']['lines'] = [440, 440]
        result = self.valid()
        self.assertFalse(result['review_targets'][0]['matches_current'])

    def test_both_files_omitting_same_semantic_caveat_is_not_a_prose_verdict(self):
        self.f['expected']['expected_bundles'][0]['basis']['text'] = 'Same reduced synthetic basis'
        self.f['companion']['bundles'][0]['basis']['text'] = 'Same reduced synthetic basis'
        self.valid()

    def test_strict_json_rejects_duplicate_nonfinite_and_invalid_utf8(self):
        for case in FIXTURE['raw_json_cases']:
            with self.subTest(case=case['name']), self.assertRaises(CHECKER.ContractError) as e:
                CHECKER.parse_input(bytes.fromhex(case['hex']), 'synthetic')
            self.assertEqual(e.exception.reason, case['reason'])

    def test_wrong_typed_record_tag_refuses_without_exception(self):
        self.f['expected']['records'][0]['identity']['kind'] = []
        self.refuses('CONTRACT_SHAPE')

    def test_unit_order_retains_independent_inventory_order(self):
        self.f['companion']['units'].reverse()
        self.refuses('EXPECTED_INVENTORY_MISMATCH')

    def test_missing_buffer_maps_report_unavailable(self):
        r = CHECKER.validate_expected_inventory(self.f['expected'],None,None)
        self.assertEqual(r['reason'],'INPUT_UNAVAILABLE',r)
        r = CHECKER.validate_proof_slice(self.f['companion'],self.f['expected'],self.f['expected_pin'],{}, {})
        self.assertEqual(r['reason'],'INPUT_UNAVAILABLE',r)

    def test_historical_duplicate_expanded_suppliers_refused(self):
        r = self.add_review()
        r['reviewed_use']['suppliers'] *= 2
        # Duplicate the own core too, so this is a duplicate-ID discriminator,
        # not an earlier owning-core mismatch.
        own=next(m for m in r['reviewed_use']['inference_context']['premises'] if m['use_id']=='U1')
        own['core']['suppliers'] *= 2
        group=next(g for g in r['reviewed_use']['bundle_context']['groups'] if g['group_id']=='GA')
        next(m for m in group['members'] if m['use_id']=='U1')['core']['suppliers'] *= 2
        self.refuses('CONTRACT_SHAPE')

    def test_historical_contribution_keeps_member_owner(self):
        r=self.add_review()
        other=next(g for g in r['reviewed_use']['bundle_context']['groups'] if g['group_id']=='GB')
        other['members'][0]['core']['consumer_unit_id']='A'
        self.refuses('CONTRACT_SHAPE')

    def test_expected_and_companion_source_record_aliases_resolve_by_identity(self):
        c=self.f['companion']
        for obj in CHECKER.walk(c):
            if obj.get('source_id')=='P':obj['source_id']='P-ALIAS'
            if obj.get('record_id')=='R11':obj['record_id']='R11-ALIAS'
        c['sources'][0]['id']='P-ALIAS'
        c['records'][0]['id']='R11-ALIAS'
        self.f['snapshots']['R11-ALIAS']=self.f['snapshots']['R11']
        self.valid()

    def test_material_source_reading_enters_current_target(self):
        binding=self.f['companion']['units'][0]['uses'][0]['binding']
        binding['source_reading']=[{'boundary_id':'RB','supplier_ids':['S'],
            'applies_to':[{'source_id':'P','lines':[90,90],'locator':'Synthetic imported section','precision':'exact_lines'}],
            'explanation':copy.deepcopy(binding['context'])}]
        self.valid()
        old=CHECKER.resolve_use_target(self.f['companion'],'U1')
        binding['source_reading'][0]['explanation']['text']='Material amended reading'
        self.valid()
        self.assertNotEqual(old,CHECKER.resolve_use_target(self.f['companion'],'U1'))
        binding['source_reading'][0]['applies_to'][0]['lines']=[30,40]
        self.refuses('CONTRACT_SHAPE')

    def test_bad_unicode_and_nonfinite_api_values_refuse_cleanly(self):
        for path,value in [(['schema'],float('nan')),(['records',0,'performer','agent'],'\ud800'),(['extraction','heading_boundaries'],[310,float('nan')])]:
            with self.subTest(path=path):
                self.f=copy.deepcopy(FIXTURE)
                self.mutate([{'input':'expected','path':path,'value':value}])
                self.refuses('CONTRACT_SHAPE')

    def test_closed_observables_array_has_no_invented_minimum(self):
        self.f['expected']['root_boundary']['semantics']['observables']=[]
        self.f['companion']['root']['semantics']['observables']=[]
        self.valid()

    def test_inventory_supplier_may_preserve_unexpanded_marker(self):
        s=self.f['companion']['suppliers'][0]
        s['kind'],s['unit_ids']='inventory_unit',['Z']
        s['source_refs']=[copy.deepcopy(self.f['companion']['units'][-1]['source'])]
        self.assertEqual(s['expansion'],'unexpanded')
        self.valid()

    def add_alias_reading(self, lines, supplier=False):
        c=self.f['companion']
        c['sources'].append({'id':'P_ALIAS','identity':copy.deepcopy(c['sources'][0]['identity'])})
        use=c['units'][0]['uses'][0]
        selected={'source_id':'P_ALIAS','lines':lines,'locator':'Mixed-alias reading control','precision':'exact_lines'}
        use['binding']['source_reading']=[{'boundary_id':'RB','supplier_ids':['S'] if supplier else [],
            'applies_to':[] if supplier else [selected],'explanation':copy.deepcopy(use['binding']['context'])}]
        if supplier:c['suppliers'][0]['source_refs']=[selected]
        return selected

    def test_mixed_alias_reading_exclusion_and_valid_controls(self):
        for supplier in (False,True):
            for alias in ('P','P_ALIAS'):
                with self.subTest(supplier=supplier,alias=alias):
                    self.f=copy.deepcopy(FIXTURE)
                    s=self.add_alias_reading([90,90],supplier)
                    old=CHECKER.resolve_use_target(self.f['companion'],'U1')
                    s['source_id']=alias
                    self.valid()
                    self.assertEqual(old,CHECKER.resolve_use_target(self.f['companion'],'U1'))
                    s['lines']=[30,40]
                    self.refuses('CONTRACT_SHAPE')

    def test_equal_blob_distinct_path_or_commit_is_not_a_source_alias(self):
        for field,value in [('path','synthetic/other-proof.md'),('commit','9'*40)]:
            with self.subTest(field=field):
                self.f=copy.deepcopy(FIXTURE)
                self.add_alias_reading([30,40])
                other=self.f['companion']['sources'][-1]['identity']
                other[field]=value
                buffers={CHECKER.file_key(i):self.f['source_text'].encode() for i in [other,self.f['expected']['source']]}
                r=CHECKER.validate_proof_slice(self.f['companion'],self.f['expected'],self.f['expected_pin'],buffers,
                    {'expected':self.f['snapshots'],'companion':self.f['snapshots']})
                self.assertTrue(r['valid'],r)
                target=CHECKER.resolve_use_target(self.f['companion'],'U1')
                reading=target['source_reading'][0]
                self.assertNotEqual(reading['boundary']['file'],reading['applies_to'][0]['file'])

    def historical_with_reading(self):
        s=self.add_alias_reading([90,90],supplier=True)
        self.f['companion']['units'][0]['uses'][0]['binding']['source_reading'][0]['applies_to']=[copy.deepcopy(s)]
        self.valid()
        return self.add_review()['reviewed_use']

    def test_historical_boundaries_validate_their_own_ranges(self):
        for field,value in [('consumed_lines',[[90000,90001]]),('excluded_lines',[[90,90]]),
                            ('consumed_lines',[[90,100],[49,89]])]:
            with self.subTest(field=field,value=value):
                self.f=copy.deepcopy(FIXTURE)
                old=self.historical_with_reading()
                for obj in CHECKER.walk(old):
                    if set(obj)==set(CHECKER.SHAPES['XBoundary']):obj[field]=copy.deepcopy(value)
                self.refuses('CONTRACT_SHAPE')

    def test_historical_reading_and_supplier_selections_stay_in_own_boundary(self):
        for supplier in (False,True):
            with self.subTest(supplier=supplier):
                self.f=copy.deepcopy(FIXTURE)
                old=self.historical_with_reading()
                for obj in CHECKER.walk(old):
                    if not supplier and set(obj)==set(CHECKER.SHAPES['XReadingUse']):
                        obj['applies_to'][0]['lines']=[30,40]
                    if supplier and set(obj)==set(CHECKER.SHAPES['XSupplier']):
                        obj['source_refs'][0]['lines']=[30,40]
                self.refuses('CONTRACT_SHAPE')

    def test_historical_supplier_intrinsic_constraints(self):
        changes=[{'kind':'external','expansion':'in_slice','external_ref':None},
                 {'kind':'unnamed','expansion':'in_slice'},
                 {'kind':'source_section','source_refs':[]},
                 {'kind':'inventory_unit','unit_ids':[]},
                 {'kind':'external','expansion':'unexpanded','external_ref':None,'unknowns':[]}]
        for delta in changes:
            with self.subTest(delta=delta):
                self.f=copy.deepcopy(FIXTURE)
                old=self.add_review()['reviewed_use']
                for obj in CHECKER.walk(old):
                    if set(obj)==set(CHECKER.SHAPES['XSupplier']):obj.update(copy.deepcopy(delta))
                self.refuses('CONTRACT_SHAPE')

    def test_historical_expanded_unknown_cannot_refer_back_to_itself(self):
        old=self.add_review()['reviewed_use']
        objects=[o for o in CHECKER.walk(old) if set(o)==set(CHECKER.SHAPES['XUnknown'])]
        for obj in objects:
            obj['description']['unknowns']=[copy.deepcopy(obj)]
        self.refuses('CONTRACT_SHAPE')

    def test_well_formed_earlier_boundary_and_supplier_remain_historical(self):
        old=self.historical_with_reading()
        for obj in CHECKER.walk(old):
            if set(obj)==set(CHECKER.SHAPES['XBoundary']):obj['consumed_lines']=[[49,90]]
            if set(obj)==set(CHECKER.SHAPES['XSupplier']):
                obj['kind']='inventory_unit';obj['unit_ids']=['OLD-UNIT-NOT-IN-CURRENT-TABLE']
        result=self.valid()
        self.assertFalse(result['review_targets'][0]['matches_current'])

    def test_every_inventory_id_table_precedes_companion_shape(self):
        paths=[['sources'],['records'],['unknowns'],['expected_units'],['expected_uses'],
               ['expected_groups'],['expected_bundles'],['root_boundary','reading_boundaries']]
        for path in paths:
            with self.subTest(path=path):
                self.f=copy.deepcopy(FIXTURE)
                value=self.f['expected']
                for key in path:value=value[key]
                value.append(copy.deepcopy(value[0]))
                del self.f['companion']['id']
                r=self.refuses('CONTRACT_SHAPE')
                self.assertEqual(r['failed_input'],'inventory')

    def test_duplicate_history_precedes_outer_pin_and_capture_authentication(self):
        for fault in ('pin','capture'):
            with self.subTest(fault=fault):
                self.f=copy.deepcopy(FIXTURE)
                self.f['companion']['history']*=2
                if fault=='pin':self.f['expected_pin']['commit']='4'*40
                else:del self.f['snapshots']['R11']
                r=self.refuses('CONTRACT_SHAPE')
                self.assertEqual(r['failed_input'],'companion')

    def test_explicit_current_mode_still_precedes_duplicate_phase(self):
        self.f['expected']['expected_units']*=2
        self.f['companion']['units'][0]['premise_groups'][0]['combination']='ANY'
        self.refuses('UNSUPPORTED_INFERENCE')

    def test_mixed_alias_refusal_keeps_existing_phase_priority(self):
        self.add_alias_reading([30,40])
        self.f['companion']['bundles'][0]['basis']['text']='Also differs from independent expectation'
        self.refuses('CONTRACT_SHAPE')
        self.f['companion']['bundles']=[]
        self.refuses('UNSUPPORTED_INFERENCE')
        self.f['companion']['units'][2]['source']['lines']=[441,442]
        self.refuses('SOURCE_JOIN_MISMATCH')

    def test_actual_inferential_cycle_is_refused(self):
        s = self.f['companion']['suppliers'][0]
        s['kind'], s['expansion'], s['unit_ids'] = 'inventory_unit', 'in_slice', ['C']
        s['source_refs'] = [copy.deepcopy(self.f['companion']['units'][2]['source'])]
        self.refuses('CONTRACT_SHAPE')

    def test_context_navigation_does_not_create_inferential_cycle(self):
        self.f['companion']['units'][0]['related_unit_ids'] = ['C']
        self.f['companion']['units'][2]['related_unit_ids'] = ['A']
        self.valid()

    def test_authenticated_foreign_file_cannot_replace_zero_use_source(self):
        other = copy.deepcopy(self.f['expected']['source'])
        other['path'] = 'synthetic/other.md'
        self.f['companion']['sources'].append({'id':'Q','identity':other})
        self.f['companion']['units'][-1]['source']['source_id'] = 'Q'
        buffers = {CHECKER.file_key(i):self.f['source_text'].encode() for i in [other,self.f['expected']['source']]}
        r = CHECKER.validate_proof_slice(self.f['companion'],self.f['expected'],self.f['expected_pin'],buffers,
            {'expected':self.f['snapshots'],'companion':self.f['snapshots']})
        self.assertEqual(r['reason'],'SOURCE_JOIN_MISMATCH',r)


class GitInputTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(CHECKER)
        self.temp = tempfile.TemporaryDirectory(prefix='proof-slice-test-')
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git('init','-q')
        self.raw = b'original bytes with trailing space \n\n'
        (self.repo/'source.txt').write_bytes(self.raw)
        self.commit('source')
        self.source_commit = self.git('rev-parse','HEAD').decode().strip()
        self.identity = self.identity_at(self.source_commit,'source.txt')

    def git(self,*args):
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,
            GIT_AUTHOR_NAME='Synthetic fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',
            GIT_COMMITTER_NAME='Synthetic fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid')
        return subprocess.run(['git','-C',str(self.repo),'-c','commit.gpgsign=false',*args],
            check=True,capture_output=True,env=env).stdout

    def commit(self,message):
        self.git('add','.')
        self.git('commit','-qm',message)
        return self.git('rev-parse','HEAD').decode().strip()

    def identity_at(self,commit,path):
        raw=self.git('show',commit+':'+path)
        return dict(repository=CHECKER.REPOSITORY,commit=commit,path=path,
            git_blob=self.git('rev-parse',commit+':'+path).decode().strip(),
            bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

    def test_raw_reader_preserves_final_newlines_and_ignores_worktree(self):
        (self.repo/'source.txt').write_bytes(b'changed worktree')
        self.assertEqual(CHECKER.verify_file_identity(self.identity,self.repo),self.raw)

    def test_raw_reader_ignores_replacement_and_ambient_routing(self):
        (self.repo/'source.txt').write_bytes(b'replacement')
        changed=self.commit('changed')
        self.git('replace',self.source_commit,changed)
        with mock.patch.dict(os.environ,{'GIT_DIR':'/nonexistent','GIT_WORK_TREE':'/nonexistent','GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'core.bare','GIT_CONFIG_VALUE_0':'true'}):
            self.assertEqual(CHECKER.verify_file_identity(self.identity,self.repo),self.raw)

    def test_all_object_reads_disable_lazy_fetch_and_replacements(self):
        original=subprocess.run
        with mock.patch.object(CHECKER.subprocess,'run',wraps=original) as calls:
            CHECKER.verify_file_identity(self.identity,self.repo)
        self.assertGreaterEqual(len(calls.call_args_list),3)
        for call in calls.call_args_list:
            self.assertIn('--no-lazy-fetch',call.args[0])
            self.assertIn('--no-replace-objects',call.args[0])
            self.assertEqual(call.kwargs['env']['GIT_NO_LAZY_FETCH'],'1')

    def test_backend_capability_failure_is_unavailable(self):
        with mock.patch.object(CHECKER._retrofit,'_git_blob',side_effect=CHECKER._retrofit._GitBackendError('no flag')):
            with self.assertRaises(CHECKER.ContractError) as error:
                CHECKER.verify_file_identity(self.identity,self.repo)
        self.assertEqual(error.exception.reason,'INPUT_UNAVAILABLE')

    def test_missing_promisor_blob_does_not_fetch_or_write(self):
        self.git('config','extensions.partialClone','origin')
        self.git('config','remote.origin.promisor','true')
        self.git('config','remote.origin.url','file:///nonexistent-proof-slice-remote')
        oid=self.identity['git_blob']
        (self.repo/'.git/objects'/oid[:2]/oid[2:]).unlink()
        before={str(p.relative_to(self.repo)):p.read_bytes() for p in (self.repo/'.git').rglob('*') if p.is_file()}
        with self.assertRaises(CHECKER.ContractError) as error:
            CHECKER.verify_file_identity(self.identity,self.repo)
        self.assertEqual(error.exception.reason,'INPUT_UNAVAILABLE')
        after={str(p.relative_to(self.repo)):p.read_bytes() for p in (self.repo/'.git').rglob('*') if p.is_file()}
        self.assertEqual(before,after)

    def test_false_blob_identity_and_foreign_repository_refuse(self):
        forged={**self.identity,'git_blob':'a'*40}
        with self.assertRaises(CHECKER.ContractError) as error:
            CHECKER.verify_file_identity(forged,self.repo)
        self.assertEqual(error.exception.reason,'IDENTITY_MISMATCH')
        with self.assertRaises(CHECKER.ContractError) as error:
            CHECKER.verify_file_identity({**self.identity,'repository':'other/repository'},self.repo)
        self.assertEqual(error.exception.reason,'INPUT_UNAVAILABLE')

    def prepare_pair(self):
        f=copy.deepcopy(FIXTURE)
        (self.repo/'synthetic').mkdir()
        (self.repo/'synthetic/proof.md').write_text(f['source_text'])
        source=self.commit('synthetic proof')
        actual=self.identity_at(source,'synthetic/proof.md')
        def replace(obj):
            if isinstance(obj,dict):
                if set(obj)==set(CHECKER.FILE_KEYS) and obj.get('path')=='synthetic/proof.md':
                    obj.clear();obj.update(actual)
                else:
                    for v in obj.values():replace(v)
            elif isinstance(obj,list):
                for v in obj:replace(v)
        replace(f['expected']);replace(f['companion'])
        self.write('synthetic/EXPECTED_INVENTORY.json',f['expected'])
        for record in f['expected']['records']:
            name=CHECKER.snapshot_path('synthetic/EXPECTED_INVENTORY.json',record['identity'])
            self.write(name,f['snapshots'][record['id']])
        a=self.commit('inventory A')
        f['companion']['inventory_binding']['expected_inventory']=self.identity_at(a,'synthetic/EXPECTED_INVENTORY.json')
        self.write('synthetic/PROOF_SLICE.json',f['companion'])
        b=self.commit('companion B')
        return f,a,b

    def write(self,path,value):
        p=self.repo/path;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

    def cli(self,*args):
        flags=['-B','-S']
        if sys.flags.optimize:flags.insert(1,'-O')
        env={k:v for k,v in os.environ.items() if k!='PYTHONOPTIMIZE'}
        result=subprocess.run([sys.executable,*flags,str(ROOT/'tools/proof_slice_check.py'),'--repo',str(self.repo),*args],capture_output=True,text=True,env=env)
        try:parsed=json.loads(result.stdout)
        except ValueError:self.fail('CLI did not return its structured report: '+repr(result.stdout)+' '+result.stderr)
        return result.returncode,parsed

    def test_actual_cli_inventory_and_descendant_pair_ignore_worktree(self):
        f,a,b=self.prepare_pair()
        code,r=self.cli('--inventory-commit',a,'--inventory-path','synthetic/EXPECTED_INVENTORY.json')
        self.assertEqual(code,0,r);self.assertEqual(r['phase'],'inventory-only')
        (self.repo/'synthetic/PROOF_SLICE.json').write_text('not committed')
        code,r=self.cli('--expected-commit',a,'--expected-path','synthetic/EXPECTED_INVENTORY.json','--companion-commit',b,'--companion-path','synthetic/PROOF_SLICE.json')
        self.assertEqual(code,0,r);self.assertEqual(r['phase'],'paired')
        self.assertEqual(r['inputs']['companion']['commit'],b)
        self.assertIn('checker',r['tools']);self.assertIn('retrofit',r['tools'])

    def test_cli_refuses_modified_expected_file_in_descendant(self):
        f,a,b=self.prepare_pair()
        (self.repo/'synthetic/EXPECTED_INVENTORY.json').write_text('{}\n')
        later=self.commit('changed expected denominator')
        code,r=self.cli('--expected-commit',a,'--expected-path','synthetic/EXPECTED_INVENTORY.json','--companion-commit',later,'--companion-path','synthetic/PROOF_SLICE.json')
        self.assertEqual(code,2,r);self.assertEqual(r['reason'],'EXPECTED_INVENTORY_MISMATCH')

    def test_cli_authenticates_captures_at_each_artifact_commit(self):
        f,a,b=self.prepare_pair()
        record=f['expected']['records'][0]
        capture=copy.deepcopy(f['snapshots']['R11']);capture['body']+='tampered'
        self.write(CHECKER.snapshot_path('synthetic/PROOF_SLICE.json',record['identity']),capture)
        later=self.commit('tampered companion evidence')
        code,r=self.cli('--expected-commit',a,'--expected-path','synthetic/EXPECTED_INVENTORY.json','--companion-commit',later,'--companion-path','synthetic/PROOF_SLICE.json')
        self.assertEqual(code,2,r);self.assertEqual(r['reason'],'IDENTITY_MISMATCH')
        code,r=self.cli('--inventory-commit',a,'--inventory-path','synthetic/EXPECTED_INVENTORY.json')
        self.assertEqual(code,0,r)

    def test_cli_incomplete_arguments_refuse_structurally(self):
        code,r=self.cli('--inventory-commit',self.source_commit)
        self.assertEqual(code,2,r);self.assertEqual(r['reason'],'CONTRACT_SHAPE')

    def paired_cli(self,a,b):
        return self.cli('--expected-commit',a,'--expected-path','synthetic/EXPECTED_INVENTORY.json',
                        '--companion-commit',b,'--companion-path','synthetic/PROOF_SLICE.json')

    def test_cli_duplicate_inventory_precedes_malformed_companion(self):
        f,a,b=self.prepare_pair()
        f['expected']['expected_units'].append(copy.deepcopy(f['expected']['expected_units'][0]))
        self.write('synthetic/EXPECTED_INVENTORY.json',f['expected'])
        a=self.commit('Inventory with duplicate row')
        f['companion']['inventory_binding']['expected_inventory']=self.identity_at(a,'synthetic/EXPECTED_INVENTORY.json')
        del f['companion']['id']
        self.write('synthetic/PROOF_SLICE.json',f['companion'])
        b=self.commit('Malformed companion after independently fixed duplicate inventory')
        code,r=self.paired_cli(a,b)
        self.assertEqual(code,2,r);self.assertEqual(r['reason'],'CONTRACT_SHAPE',r)
        self.assertEqual(r['failed_input'],'inventory',r)

    def test_cli_duplicate_history_precedes_wrong_pin(self):
        f,a,b=self.prepare_pair()
        f['companion']['history']*=2
        f['companion']['inventory_binding']['expected_inventory']['commit']='4'*40
        self.write('synthetic/PROOF_SLICE.json',f['companion']);b=self.commit('Duplicate history and wrong pin')
        code,r=self.paired_cli(a,b)
        self.assertEqual(code,2,r);self.assertEqual(r['reason'],'CONTRACT_SHAPE',r)
        self.assertEqual(r['failed_input'],'companion',r)

    def test_cli_duplicate_history_precedes_missing_capture(self):
        f,a,b=self.prepare_pair()
        f['companion']['history']*=2
        self.write('synthetic/PROOF_SLICE.json',f['companion'])
        capture=CHECKER.snapshot_path('synthetic/PROOF_SLICE.json',f['companion']['records'][0]['identity'])
        (self.repo/capture).unlink();b=self.commit('Duplicate history and missing current capture')
        code,r=self.paired_cli(a,b)
        self.assertEqual(code,2,r);self.assertEqual(r['reason'],'CONTRACT_SHAPE',r)
        self.assertEqual(r['failed_input'],'companion',r)

    def test_cli_mixed_alias_exclusions_and_positive_control(self):
        f,a,b=self.prepare_pair()
        c=f['companion'];c['sources'].append({'id':'P_ALIAS','identity':copy.deepcopy(c['sources'][0]['identity'])})
        use=c['units'][0]['uses'][0]
        selection={'source_id':'P_ALIAS','lines':[90,90],'locator':'CLI mixed-alias selection','precision':'exact_lines'}
        use['binding']['source_reading']=[{'boundary_id':'RB','supplier_ids':[],'applies_to':[selection],
                                        'explanation':copy.deepcopy(use['binding']['context'])}]
        self.write('synthetic/PROOF_SLICE.json',c);valid=self.commit('Permitted mixed-alias reading')
        code,r=self.paired_cli(a,valid);self.assertEqual(code,0,r)
        selection['lines']=[30,40]
        self.write('synthetic/PROOF_SLICE.json',c);invalid=self.commit('Excluded mixed-alias reading')
        code,r=self.paired_cli(a,invalid)
        self.assertEqual(code,2,r);self.assertEqual(r['reason'],'CONTRACT_SHAPE',r)


class WorkflowTests(unittest.TestCase):
    def test_required_downstream_job_runs_both_modes_and_real_inventory(self):
        workflow=(ROOT/'.github/workflows/downstream-gate.yml').read_text()
        start=workflow.index('      - name: P-C inventory A source-bound conformance')
        end=workflow.index('      - name:',start+1)
        step=workflow[start:end]
        for mode in ('-B -S','-B -O -S'):
            self.assertIn('python3 '+mode+' -m unittest discover -s tests -p test_proof_slice_check.py -v',step)
            self.assertIn('python3 '+mode+' tools/proof_slice_check.py',step)
        self.assertIn('--inventory-commit "$GITHUB_SHA"',step)
        self.assertIn('--inventory-path reviews/proof_dependencies_20261008/P_C/EXPECTED_INVENTORY.json',step)
        self.assertIn('--no-replace-objects --no-lazy-fetch',step)
        self.assertIn('9fd261135b41daf1e377f9ef2db193fee6ec36be^{commit}',step)
        self.assertIn('rev-parse HEAD)',step)
        self.assertIn('rev-parse --is-shallow-repository)',step)
        self.assertIn('downstream-gate-results',step)
        self.assertNotIn('if:',step)
        self.assertNotIn('continue-on-error',step)
        self.assertIn('needs: [checks, formal]',workflow)
        self.assertIn("report['distinct_tests'] != 71",workflow)


if __name__ == '__main__':
    unittest.main()
