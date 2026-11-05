"""Actual census policy regressions; harness process responses are explicitly synthetic.

The positive fixture is authenticated hosted Lean output, not a fabricated clean transcript.
These tests execute Python policy/file logic only and cannot award a repaired kernel receipt.
"""
import copy
import importlib.util
import json
import os
import py_compile
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORE = Path(os.environ.get('DETERMINANT_CORE_PATH', str(
    ROOT / 'compiled_inventory.py' if (ROOT / 'compiled_inventory.py').exists() else
    ROOT.parent / 'cbz_hosted_determinant_census/native_successor/frontiers/determinant_moment_20261025/compiled_inventory.py')))
SPEC = importlib.util.spec_from_file_location('determinant_adapter_under_test', ROOT / 'determinant_inventory.py')
adapter = importlib.util.module_from_spec(SPEC) if (ROOT / 'determinant_inventory.py').exists() else None
if adapter is not None:
    SPEC.loader.exec_module(adapter)


def enc(name):
    return '/'.join('n'+str(x) if type(x) is int else 's'+x.encode().hex() for x in name)


class DeterminantPolicyTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(adapter, 'determinant-specific adapter has not been implemented')
        self.text = (ROOT / 'tests/fixtures/actual_inventory_4ccc.log').read_text()
        self.manifest = json.loads((ROOT / 'tests/fixtures/actual_manifest_v2_fields.json').read_text())
        self.core = adapter.load_core(CORE)
        self.parsed = self.core.parse_inventory(self.text)
        self.private = next(r for r in self.parsed['constants'] if r[0:2] == ('theorem','user') and r[3][0] == '_private')
        self.instance = next(r for r in self.parsed['constants'] if r[3] == ('ResearchFormalCoreR1','regressionKernel_isMarkov'))

    def audit(self, text=None, manifest=None, reported=None):
        return adapter.audit_inventory(self.text if text is None else text,
            self.manifest if manifest is None else manifest, reported_axioms=reported, core_path=CORE)

    def rejected(self, text=None, manifest=None, reported=None):
        with self.assertRaises(adapter.InventoryRejected) as caught:
            self.audit(text, manifest, reported)
        return {code for code, name, note in caught.exception.violations}

    def change(self, old=None, new=None):
        lines = self.text.splitlines(); delta = {}
        if old is not None:
            oldline='INV|'+'|'.join((old[0],old[1],enc(old[2]),enc(old[3])))
            self.assertEqual(lines.count(oldline),1);lines.remove(oldline);delta[old[2]]=-1
        if new is not None:
            lines.append('INV|'+'|'.join((new[0],new[1],enc(new[2]),enc(new[3]))))
            delta[new[2]]=delta.get(new[2],0)+1
        for i,line in enumerate(lines):
            if line.startswith('MODULE|'):
                parts=line.split('|');module=self.core.decode(parts[1]);parts[3]=str(int(parts[3])+delta.get(module,0));lines[i]='|'.join(parts)
        return '\n'.join(lines)+'\n'

    def test_actual_census_accepts_all157_constants_without_changing_core(self):
        try:
            report=self.audit()
        except adapter.InventoryRejected as error:
            self.fail('authenticated actual census must satisfy the policy: '+str(error))
        self.assertEqual(report['declarations'],157)
        self.assertEqual(len(report['public_theorems']),66)
        self.assertEqual(report['internal_user_proofs'],20)
        self.assertEqual(report['auxiliary_theorems'],51)
        self.assertEqual(report['ir_extra_total'],41)
        self.assertEqual(report['closure'],58421)
        self.assertEqual(report['axioms'],['Classical.choice','Quot.sound','propext'])
        self.assertEqual(report['kernel_or_cbz_status'],'NOT_AWARDED')

    def test_missing_registered_private_proof_rejects_with_adjusted_module_count(self):
        self.assertIn('missing_internal_proof',self.rejected(self.change(self.private)))

    def test_new_axiom_free_private_proof_is_not_blanket_allowed(self):
        module=('ResearchFormalCoreR1','AlgebraV2')
        new=('theorem','user',module,('_private',*module,0,'ResearchFormalCoreR1','newUnregisteredProof'))
        self.assertIn('extra_theorem',self.rejected(self.change(new=new)))

    def test_moved_private_proof_rejects_even_when_counts_match(self):
        new=(*self.private[:2],('ResearchFormalCoreR1','AlgebraV2'),self.private[3])
        self.assertTrue({'extra_theorem','missing_internal_proof'} <= self.rejected(self.change(self.private,new)))

    def test_missing_proof_valued_instance_rejects(self):
        self.assertIn('missing_internal_proof',self.rejected(self.change(self.instance)))

    def test_moved_proof_valued_instance_rejects(self):
        new=(*self.instance[:2],('ResearchFormalCoreR1','AlgebraV2'),self.instance[3])
        self.assertTrue({'extra_theorem','missing_internal_proof'} <= self.rejected(self.change(self.instance,new)))

    def test_numeric_zero_is_not_string_zero_in_private_name(self):
        record=next(r for r in self.manifest['compiled_inventory'] if any(c==['n',0] for c in r[3]))
        numeric=record[3].index(['n',0]);record[3][numeric]=['s','0']
        self.assertTrue({'extra_theorem','missing_internal_proof'} <= self.rejected(manifest=self.manifest))

    def test_changed_private_kind_or_provenance_rejects(self):
        for kind,origin in [('def','user'),('theorem','aux')]:
            with self.subTest(kind=kind,origin=origin):
                self.assertIn('missing_internal_proof',self.rejected(self.change(self.private,(kind,origin,*self.private[2:]))))

    def test_duplicate_private_name_is_preserved_as_violation(self):
        self.assertIn('duplicate_name',self.rejected(self.change(new=self.private)))

    def test_changed_IR_extra_count_rejects_and_is_not_an_allowlist(self):
        needle='MODULE|'+enc(('ResearchFormalCoreR1','DeterminantMoment'))+'|false|20|6'
        self.assertIn('ir_extra_count_mismatch',self.rejected(self.text.replace(needle,needle[:-1]+'7')))
        self.assertIn('ir_extra_count_mismatch',self.rejected(self.text.replace(needle,needle[:-1]+'0')))

    def test_missing_or_duplicate_module_still_rejects(self):
        line=next(l for l in self.text.splitlines() if l.startswith('MODULE|') and enc(('ResearchFormalCoreR1','AlgebraV2'))+'|' in l)
        self.assertIn('missing_module',self.rejected(self.text.replace(line+'\n','')))
        self.assertIn('duplicate_module',self.rejected(self.text+line+'\n'))

    def test_forbidden_axiom_behind_non_target_cannot_be_filtered(self):
        text=self.text.replace('AXIOMS|','AXIOMS|'+enc(('Hidden','behindDefinition'))+',')
        self.assertIn('forbidden_axiom',self.rejected(text))

    def test_package_axiom_cannot_be_bound_or_hidden(self):
        new=('axiom','user',('ResearchFormalCoreR1','AlgebraV2'),('ResearchFormalCoreR1','unlistedPremise'))
        self.assertIn('package_axiom',self.rejected(self.change(new=new)))
        self.manifest['compiled_inventory'].append(['axiom','user',[['s','ResearchFormalCoreR1'],['s','AlgebraV2']],[['s','ResearchFormalCoreR1'],['s','unlistedPremise']]])
        with self.assertRaisesRegex(ValueError,'bound.*axiom|invalid.*kind'):
            self.audit(manifest=self.manifest)

    def test_unbound_compiler_shaped_auxiliary_is_rejected(self):
        new=('theorem','aux',('ResearchFormalCoreR1','AlgebraV2'),('ResearchFormalCoreR1','ec005_fold_gap','_proof_999'))
        self.assertIn('unregistered_constant',self.rejected(self.change(new=new)))

    def test_unbound_auxiliary_parent_rule_remains_active(self):
        new=('theorem','aux',('ResearchFormalCoreR1','AlgebraV2'),('ResearchFormalCoreR1','noUserParent','_proof_1'))
        self.assertIn('unbound_auxiliary',self.rejected(self.change(new=new)))

    def test_missing_bound_definition_and_public_target_reject(self):
        definition=next(r for r in self.parsed['constants'] if r[0:2]==('def','user'))
        self.assertIn('missing_constant',self.rejected(self.change(definition)))
        target=next(r for r in self.parsed['constants'] if r[3]==('ResearchFormalCoreR1','ec005_fold_gap'))
        self.assertIn('missing_theorem',self.rejected(self.change(target)))

    def test_count_closure_and_reported_axiom_guards_remain(self):
        self.assertIn('impossible_closure',self.rejected(self.text.replace('CLOSURE|58421','CLOSURE|1')))
        self.assertIn('reported_axiom_omitted',self.rejected(reported={'p':['Hidden.unreported']}))
        line=next(l for l in self.text.splitlines() if l.startswith('MODULE|') and '|false|8|0' in l)
        self.assertIn('count_mismatch',self.rejected(self.text.replace(line,line.replace('|8|0','|9|0'))))

    def test_manifest_cannot_duplicate_or_shadow_public_target(self):
        self.manifest['compiled_inventory'].append(copy.deepcopy(self.manifest['compiled_inventory'][0]))
        with self.assertRaisesRegex(ValueError,'duplicate'):
            self.audit()
        m=json.loads((ROOT/'tests/fixtures/actual_manifest_v2_fields.json').read_text())
        m['compiled_inventory'][0][3]=[['s','ResearchFormalCoreR1'],['s','ec005_fold_gap']]
        with self.assertRaisesRegex(ValueError,'target.*shadow|shadow.*target'):
            self.audit(manifest=m)

    def test_typed_name_and_IR_schema_reject_bool_and_missing_keys(self):
        m=copy.deepcopy(self.manifest);m['compiled_inventory'][0][3][0]=['n',True]
        with self.assertRaisesRegex(ValueError,'component'):
            self.audit(manifest=m)
        m=copy.deepcopy(self.manifest);m['ir_extra_counts'].pop()
        with self.assertRaisesRegex(ValueError,'IR.*module|module.*IR'):
            self.audit(manifest=m)

    def test_empty_or_malformed_protocol_never_passes(self):
        for text in ['',self.text.replace('AXIOMS|','BADAXIOMS|')]:
            with self.subTest(text=text[:10]),self.assertRaises(ValueError):self.audit(text)

    def test_core_hash_guard_refuses_modified_helper_before_import(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            path=Path(d)/'compiled_inventory.py';path.write_text("raise RuntimeError('must not import')\n")
            with self.assertRaisesRegex(ValueError,'core.*hash'):
                adapter.audit_inventory(self.text,self.manifest,core_path=path)

    def test_stale_timestamp_pyc_cannot_replace_verified_core_bytes(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            path=Path(d)/'compiled_inventory.py';authentic=CORE.read_bytes()
            malicious=b'REVIEW_STALE_CACHE_EXECUTED = True\n'
            malicious+=b'#'*(len(authentic)-len(malicious))
            self.assertEqual(len(malicious),len(authentic))
            timestamp=1_700_000_000
            path.write_bytes(malicious);os.utime(path,(timestamp,timestamp))
            py_compile.compile(str(path),doraise=True,invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
            path.write_bytes(authentic);os.utime(path,(timestamp,timestamp))
            loaded=adapter.load_core(path)
            self.assertFalse(getattr(loaded,'REVIEW_STALE_CACHE_EXECUTED',False),'stale cache executed instead of authenticated source bytes')
            self.assertTrue(callable(getattr(loaded,'inventory_violations',None)))

    def test_missing_exact_auxiliary_compatibility_binding_refuses(self):
        self.manifest.pop('auxiliary_compatibility')
        with self.assertRaisesRegex(ValueError,'compatibility'):
            self.audit()

    def test_auxiliary_compatibility_record_must_already_be_frozen_bound(self):
        self.manifest['auxiliary_compatibility'][0]['record'][3][-1]=['s','_proof_999']
        with self.assertRaisesRegex(ValueError,'already.*bound|bound.*compatibility'):
            self.audit()

    def test_auxiliary_compatibility_wrong_parent_or_owner_refuses(self):
        self.manifest['auxiliary_compatibility'][0]['parent'][2]=[['s','ResearchFormalCoreR1'],['s','AlgebraV2']]
        with self.assertRaisesRegex(ValueError,'compatibility parent'):
            self.audit()

    def test_missing_or_moved_compatibility_auxiliary_is_not_silently_discharged(self):
        record=next(r for r in self.parsed['constants'] if r[3]==('ResearchFormalCoreR1','dm2Radius','eq_1'))
        self.assertIn('missing_constant',self.rejected(self.change(record)))
        moved=(record[0],record[1],('ResearchFormalCoreR1','AlgebraV2'),record[3])
        self.assertIn('unbound_auxiliary',self.rejected(self.change(record,moved)))

    def test_missing_cross_module_compatibility_parent_refuses(self):
        parent=next(r for r in self.parsed['constants'] if r[3]==('ResearchFormalCoreR1','dm2Radius'))
        self.assertIn('auxiliary_compatibility_parent_mismatch',self.rejected(self.change(parent)))

    def test_compatibility_name_lookalike_is_not_an_exception(self):
        new=('theorem','aux',('ResearchFormalCoreR1','GaussianJetMoments'),('ResearchFormalCoreR1','dm2Radius','eq_999'))
        codes=self.rejected(self.change(new=new))
        self.assertTrue({'unbound_auxiliary','unregistered_constant'}<=codes)

    def test_even_bound_unknown_auxiliary_cannot_bypass_parent_rule(self):
        new=('theorem','aux',('ResearchFormalCoreR1','AlgebraV2'),('ResearchFormalCoreR1','noUserParent','_proof_1'))
        typed=lambda n:[['n',v] if type(v)is int else ['s',v] for v in n]
        self.manifest['compiled_inventory'].append([new[0],new[1],typed(new[2]),typed(new[3])])
        self.assertIn('unbound_auxiliary',self.rejected(self.change(new=new)))


if __name__=='__main__':unittest.main()
