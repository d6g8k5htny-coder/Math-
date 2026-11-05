"""Harness orchestration tests with SYNTHETIC external build/checker/Lean responses.

Source copying, injected source text, frozen bindings, policy checks and cleanup are real.
No test here executes Lean or writes a native qualification receipt.
"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
CORE=Path(os.environ.get('DETERMINANT_CORE_PATH',str(ROOT/'compiled_inventory.py' if (ROOT/'compiled_inventory.py').exists() else ROOT.parent/'cbz_hosted_determinant_census/native_successor/frontiers/determinant_moment_20261025/compiled_inventory.py')))
spec=importlib.util.spec_from_file_location('determinant_harness_under_test',ROOT/'determinant_inventory.py')
adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
MODULE=('ResearchFormalCoreR1','AlgebraV2')


def enc(n):return '/'.join('n'+str(x) if type(x)is int else 's'+x.encode().hex() for x in n)


class AdmissionHarnessTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(getattr(adapter,'compiled_admission',None)), 'adapter compiled-admission harness is missing')
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT);self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.package=self.base/'package';self.output=self.base/'logs';self.output.mkdir()
        (self.package/'.lake/build').mkdir(parents=True);(self.package/'.lake/build/synthetic-marker').write_text('not a real build')
        (self.package/'.lake/packages').mkdir()
        self.source='namespace ResearchFormalCoreR1\ntheorem ec005_fold_gap : True := True.intro\nend ResearchFormalCoreR1\n'
        (self.package/'ResearchFormalCoreR1').mkdir();(self.package/'ResearchFormalCoreR1/AlgebraV2.lean').write_text(self.source)
        self.text=(ROOT/'tests/fixtures/actual_inventory_4ccc.log').read_text()
        self.manifest=json.loads((ROOT/'tests/fixtures/actual_manifest_v2_fields.json').read_text())
        self.baseline=adapter.audit_inventory(self.text,self.manifest,core_path=CORE)
        self.core=adapter.load_core(CORE);self.calls=[];self.seen_injected_sources={}

    def injected_text(self,label,*,unrelated=False,omit=False):
        if omit:return self.text
        if label=='compiled_admission':
            row=('theorem','user',MODULE,('_private',*MODULE,0,'ResearchFormalCoreR1','compiledAdmission'))
        else:
            row=('theorem','aux',MODULE,('ResearchFormalCoreR1','ec005_fold_gap','_proof_999'))
        text=self.text.replace('MODULE|'+enc(MODULE)+'|false|8|0','MODULE|'+enc(MODULE)+'|false|9|0')
        text+='INV|'+'|'.join((row[0],row[1],enc(row[2]),enc(row[3])))+'\n'
        if label=='compiled_admission':text=text.replace('AXIOMS|','AXIOMS|'+enc(('sorryAx',))+',')
        if unrelated:
            text=text.replace('MODULE|'+enc(('ResearchFormalCoreR1','DeterminantMoment'))+'|false|20|6','MODULE|'+enc(('ResearchFormalCoreR1','DeterminantMoment'))+'|false|20|7')
        return text

    def runner(self,*,fail=None,unrelated=False,omit=False):
        def run(command,label,out,expect_success=True,cwd=None):
            self.calls.append(label)
            if label==fail:raise ValueError('synthetic prerequisite failure: '+label)
            if label=='compiled_baseline':return self.text
            if label.endswith('_build'):
                body=(Path(cwd)/'ResearchFormalCoreR1/AlgebraV2.lean').read_text()
                self.seen_injected_sources[label]=body
                return 'SYNTHETIC BUILD RESPONSE; NO LEAN EXECUTED\n'
            if label.endswith('_leanchecker'):return 'SYNTHETIC CHECKER RESPONSE\n'
            if label.endswith('_axioms'):
                return '\n'.join("'"+name+"' does not depend on any axioms" for name in self.manifest['targets'])
            return self.injected_text(label,unrelated=unrelated,omit=omit)
        return run

    def invoke(self,**kwargs):
        return adapter.compiled_admission(self.manifest,self.baseline,self.output,
            package_root=self.package,core_path=CORE,runner=self.runner(**kwargs))

    def test_both_original_payloads_run_after_clean_adapter_baseline(self):
        result=self.invoke()
        self.assertEqual(set(result['injections']),{'compiled_admission','compiled_metaprogram'})
        self.assertEqual([r['outcome'] for r in result['injections'].values()],['REJECTED_FOR_EXPECTED_REASON']*2)
        self.assertEqual(self.calls,['compiled_baseline','compiled_admission_build','compiled_admission_leanchecker','compiled_admission_axioms','compiled_admission','compiled_metaprogram_build','compiled_metaprogram_leanchecker','compiled_metaprogram_axioms','compiled_metaprogram'])
        self.assertIn('private theorem compiledAdmission',self.seen_injected_sources['compiled_admission_build'])
        self.assertIn('Lean.addDecl',self.seen_injected_sources['compiled_metaprogram_build'])
        self.assertEqual((self.package/'ResearchFormalCoreR1/AlgebraV2.lean').read_text(),self.source)
        self.assertFalse((self.package/'.lake/determinant-compiled-admission').exists())
        self.assertEqual(result['kernel_or_cbz_status'],'NOT_AWARDED')

    def test_prerequisite_failure_is_not_counted_as_an_admission_rejection(self):
        for label in ['compiled_admission_build','compiled_admission_leanchecker','compiled_admission_axioms']:
            with self.subTest(label=label),self.assertRaisesRegex(ValueError,'synthetic prerequisite failure'):
                self.invoke(fail=label)
            self.assertFalse((self.package/'.lake/determinant-compiled-admission').exists())

    def test_unrelated_IR_drift_fails_exact_reason_check(self):
        with self.assertRaisesRegex(ValueError,'unexpected reason'):
            self.invoke(unrelated=True)

    def test_missing_injection_cannot_satisfy_the_control(self):
        with self.assertRaisesRegex(ValueError,'exactly one'):
            self.invoke(omit=True)

    def test_changed_positive_baseline_digest_refuses_before_injection(self):
        self.baseline['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'baseline.*digest|baseline.*inventory'):
            self.invoke()
        self.assertEqual(self.calls,['compiled_baseline'])

    def test_clean_or_wrong_reason_output_is_not_a_rejection(self):
        text=self.injected_text('compiled_metaprogram');m=copy.deepcopy(self.manifest)
        typed=lambda n:[['n',x] if type(x)is int else ['s',x] for x in n]
        m['compiled_inventory'].append(['theorem','aux',typed(MODULE),typed(('ResearchFormalCoreR1','ec005_fold_gap','_proof_999'))])
        with self.assertRaisesRegex(ValueError,'unexpected reason'):
            adapter.check_admission(text,'control',('theorem','aux',('ResearchFormalCoreR1','ec005_fold_gap','_proof_999'),False,MODULE),{('unregistered_constant',('ResearchFormalCoreR1','ec005_fold_gap','_proof_999'),False)},m,core_path=CORE)

    def test_output_symlink_and_ancestor_are_refused_before_cleanup(self):
        for ancestor in (False,True):
            with self.subTest(ancestor=ancestor):
                work=self.package/'.lake/determinant-compiled-admission';work.mkdir(parents=True,exist_ok=True)
                sentinel=work/'retained-evidence.log';sentinel.write_text('preserve this evidence')
                alias=self.base/('linked-parent' if ancestor else 'linked-output')
                alias.symlink_to(work,target_is_directory=True)
                output=alias/'logs' if ancestor else alias
                original_runner=self.runner()
                def logged(command,label,out,**kwargs):
                    result=original_runner(command,label,out,**kwargs)
                    Path(out).mkdir(parents=True,exist_ok=True)
                    (Path(out)/(label+'.log')).write_text(result)
                    return result
                with self.assertRaisesRegex(ValueError,'symlink|contain|outside'):
                    adapter.compiled_admission(self.manifest,self.baseline,output,
                        package_root=self.package,core_path=CORE,runner=logged)
                self.assertEqual(sentinel.read_text(),'preserve this evidence')
                self.assertEqual(self.calls,[],'unsafe path must refuse before external stages or cleanup')

    def test_resolved_dotdot_output_containment_refuses_before_cleanup(self):
        work=self.package/'.lake/determinant-compiled-admission';work.mkdir(parents=True)
        sentinel=work/'retained-evidence.log';sentinel.write_text('preserve canonical-path evidence')
        bridge=self.package/'.lake/bridge';bridge.mkdir()
        output=bridge/'..'/'determinant-compiled-admission'/'logs'
        original_runner=self.runner()
        def logged(command,label,out,**kwargs):
            result=original_runner(command,label,out,**kwargs)
            Path(out).mkdir(parents=True,exist_ok=True)
            (Path(out)/(label+'.log')).write_text(result)
            return result
        with self.assertRaisesRegex(ValueError,'contain|outside|disposable'):
            adapter.compiled_admission(self.manifest,self.baseline,output,
                package_root=self.package,core_path=CORE,runner=logged)
        self.assertEqual(sentinel.read_text(),'preserve canonical-path evidence')
        self.assertEqual(self.calls,[])

    def test_output_symlink_outside_work_is_also_refused(self):
        retained=self.base/'retained';retained.mkdir()
        for ancestor in (False,True):
            with self.subTest(ancestor=ancestor):
                alias=self.base/('external-parent' if ancestor else 'external-output')
                alias.symlink_to(retained,target_is_directory=True)
                output=alias/'logs' if ancestor else alias
                with self.assertRaisesRegex(ValueError,'symlink'):
                    adapter.compiled_admission(self.manifest,self.baseline,output,
                        package_root=self.package,core_path=CORE,runner=self.runner())
                self.assertEqual(self.calls,[])

    def test_external_logs_survive_work_cleanup_on_success_and_failures(self):
        for scenario in ('success','prerequisite_failure','unexpected_rejection'):
            with self.subTest(scenario=scenario):
                output=self.base/scenario;output.mkdir()
                run=self.runner(fail='compiled_admission_build' if scenario=='prerequisite_failure' else None,
                                unrelated=scenario=='unexpected_rejection')
                def logged(command,label,out,**kwargs):
                    (Path(out)/(label+'.log')).write_text('SYNTHETIC EXTERNAL RESPONSE; NO LEAN EXECUTED\n')
                    return run(command,label,out,**kwargs)
                if scenario=='success':
                    adapter.compiled_admission(self.manifest,self.baseline,output,
                        package_root=self.package,core_path=CORE,runner=logged)
                else:
                    with self.assertRaisesRegex(ValueError,'synthetic prerequisite failure|unexpected reason'):
                        adapter.compiled_admission(self.manifest,self.baseline,output,
                            package_root=self.package,core_path=CORE,runner=logged)
                self.assertTrue((output/'compiled_baseline.log').is_file())
                self.assertTrue((output/'compiled_admission_build.log').is_file())
                self.assertFalse((self.package/'.lake/determinant-compiled-admission').exists())


if __name__=='__main__':unittest.main()
