from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import cbz_source514_hosted as subject

class SourceBindingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(["git","init","-q",str(self.root)],check=True)
        subprocess.run(["git","-C",str(self.root),"config","user.email","fixture@example.invalid"],check=True)
        subprocess.run(["git","-C",str(self.root),"config","user.name","Finite fixture"],check=True)
        (self.root/"Proof.lean").write_text("theorem exactFixture : True := True.intro\n")
        subprocess.run(["git","-C",str(self.root),"add","Proof.lean"],check=True)
        subprocess.run(["git","-C",str(self.root),"commit","-qm","finite fixture"],check=True)
        self.previous_head=subject.git(self.root,"rev-parse","HEAD").decode().strip()
        (self.root/"Metadata.txt").write_text("second commit; unchanged proof blob\n")
        subprocess.run(["git","-C",str(self.root),"add","Metadata.txt"],check=True)
        subprocess.run(["git","-C",str(self.root),"commit","-qm","metadata successor"],check=True)
        self.head=subject.git(self.root,"rev-parse","HEAD").decode().strip()

    def test_exact_source_is_bound(self):
        result=subject.bind(self.root,self.head,["Proof.lean"])
        self.assertEqual(result["commit"],self.head)
        self.assertEqual(result["files"]["Proof.lean"]["sha256"],subject.sha((self.root/"Proof.lean").read_bytes()))

    def test_wrong_head_rejected(self):
        with self.assertRaisesRegex(ValueError,"source HEAD differs"):
            subject.bind(self.root,self.previous_head,["Proof.lean"])

    def test_dirty_bytes_rejected_even_assume_unchanged(self):
        subprocess.run(["git","-C",str(self.root),"update-index","--assume-unchanged","Proof.lean"],check=True)
        (self.root/"Proof.lean").write_text("theorem changedFixture : True := True.intro\n")
        with self.assertRaisesRegex(ValueError,"source bytes differ"):
            subject.bind(self.root,self.head,["Proof.lean"])

    def test_unsafe_relative_path_rejected(self):
        with self.assertRaisesRegex(ValueError,"unsafe bound source path"):
            subject.bind(self.root,self.head,["../Proof.lean"])

    def test_symlink_rejected(self):
        (self.root/"Link.lean").symlink_to("Proof.lean")
        with self.assertRaisesRegex(ValueError,"symlinked bound source"):
            subject.bind(self.root,self.head,["Link.lean"])

class DependencyCustodyTests(SourceBindingTests):
    def package(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        package=Path(temporary.name)
        (package/".lake/packages").mkdir(parents=True)
        (package/".lake/packages/Fixture").symlink_to(self.root,target_is_directory=True)
        lock={"packages":[{"name":"Fixture","type":"git","rev":self.head}]}
        return package,lock

    def test_dependency_hidden_dirty_bytes_rejected(self):
        subprocess.run(["git","-C",str(self.root),"update-index","--assume-unchanged","Proof.lean"],check=True)
        (self.root/"Proof.lean").write_text("theorem changedFixture : True := True.intro\n")
        with self.assertRaisesRegex(ValueError,"source bytes differ"):
            subject.bind_dependency(self.root,self.head)

    def test_dependency_changed_index_rejected_with_original_working_bytes(self):
        original=(self.root/"Proof.lean").read_bytes()
        (self.root/"Proof.lean").write_text("theorem changedFixture : True := True.intro\n")
        subprocess.run(["git","-C",str(self.root),"add","Proof.lean"],check=True)
        (self.root/"Proof.lean").write_bytes(original)
        with self.assertRaisesRegex(ValueError,"index differs"):
            subject.bind_dependency(self.root,self.head)

    def test_dependency_ignored_lean_shadow_rejected(self):
        (self.root/".git/info/exclude").write_text("Shadow.lean\n")
        (self.root/"Shadow.lean").write_text("theorem shadowFixture : True := True.intro\n")
        with self.assertRaisesRegex(ValueError,"untracked Lean shadow"):
            subject.bind_dependency(self.root,self.head)

    def test_dependency_change_during_actual_phase_rejected(self):
        package,lock=self.package()
        with self.assertRaisesRegex(ValueError,"source bytes differ"):
            with subject.frozen_dependencies(package,lock):
                subprocess.run(["git","-C",str(self.root),"update-index","--assume-unchanged","Metadata.txt"],check=True)
                (self.root/"Metadata.txt").write_text("actual phase mutated a dependency\n")

    def test_git_replacement_cannot_relabel_a_new_tree_as_the_frozen_commit(self):
        frozen=self.head
        (self.root/"Proof.lean").write_text("theorem replacementFixture : True := True.intro\n")
        subprocess.run(["git","-C",str(self.root),"add","Proof.lean"],check=True)
        subprocess.run(["git","-C",str(self.root),"commit","-qm","replacement tree"],check=True)
        replacement=subject.git(self.root,"rev-parse","HEAD").decode().strip()
        subprocess.run(["git","-C",str(self.root),"replace",frozen,replacement],check=True)
        subprocess.run(["git","-C",str(self.root),"update-ref","HEAD",frozen],check=True)
        with self.assertRaisesRegex(ValueError,"index differs"):
            subject.bind_dependency(self.root,frozen)

    def test_inherited_git_directory_cannot_redirect_dependency_identity(self):
        with mock.patch.dict(os.environ,{"GIT_DIR":str(self.root/"missing-git"),"GIT_WORK_TREE":str(self.root/"missing-worktree")}):
            bound=subject.bind_dependency(self.root,self.head)
        self.assertEqual(bound["commit"],self.head)

class CompiledObjectCustodyTests(unittest.TestCase):
    def test_dependency_object_change_rejected_while_owned_object_is_stable(self):
        with tempfile.TemporaryDirectory() as temporary:
            package=Path(temporary)
            owned=package/".lake/build/lib/lean/Owned.olean"
            dependency=package/".lake/packages/Fixture/.lake/build/lib/lean/Dependency.olean.private"
            owned.parent.mkdir(parents=True)
            dependency.parent.mkdir(parents=True)
            owned.write_bytes(b"owned fixture object")
            dependency.write_bytes(b"dependency fixture object")
            with self.assertRaisesRegex(ValueError,"compiled objects changed"):
                with subject.frozen_objects(package,["Fixture"]):
                    dependency.write_bytes(b"changed dependency fixture object")
            self.assertEqual(owned.read_bytes(),b"owned fixture object")

    def test_unused_dependency_object_root_absence_is_explicit(self):
        with tempfile.TemporaryDirectory() as temporary:
            package=Path(temporary)
            owned=package/".lake/build/lib/lean/Owned.olean"
            owned.parent.mkdir(parents=True)
            owned.write_bytes(b"owned fixture object")
            snapshot=subject.object_snapshot(package,["Unused"])
            self.assertFalse(snapshot["root_presence"][".lake/packages/Unused/.lake/build"])
            self.assertTrue(snapshot["root_presence"][".lake/build"])

    def test_symlinked_build_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            package=Path(temporary)/"package"
            outside=Path(temporary)/"outside"
            package.joinpath(".lake").mkdir(parents=True)
            outside.mkdir()
            (outside/"hidden.olean").write_bytes(b"object")
            package.joinpath(".lake","build").symlink_to(outside,target_is_directory=True)
            with self.assertRaisesRegex(ValueError,"symlink"):
                subject.object_snapshot(package,[])

    def test_symlinked_nested_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            package=Path(temporary)/"package"
            outside=Path(temporary)/"outside"
            build=package/".lake/build/lib/lean"
            build.mkdir(parents=True)
            outside.mkdir()
            (build/"Owned.olean").write_bytes(b"owned")
            (outside/"hidden.olean").write_bytes(b"hidden")
            (build/"Shadow").symlink_to(outside,target_is_directory=True)
            with self.assertRaisesRegex(ValueError,"symlink"):
                subject.object_snapshot(package,[])

    def test_dependency_object_root_appearance_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            package=Path(temporary)
            owned=package/".lake/build/lib/lean/Owned.olean"
            owned.parent.mkdir(parents=True)
            owned.write_bytes(b"owned fixture object")
            with self.assertRaisesRegex(ValueError,"compiled objects changed"):
                with subject.frozen_objects(package,["Unused"]):
                    (package/".lake/packages/Unused/.lake/build").mkdir(parents=True)

class LoadedCodeTests(unittest.TestCase):
    def test_changed_loaded_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/"loaded.py"
            path.write_text("value = 7\n")
            with self.assertRaisesRegex(ValueError,"loaded code differs"):
                subject.load("finite_loaded",path,subject.sha(b"value = 8\n"))
    def test_immutable_loaded_bytes_are_the_recorded_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/"loaded.py"
            data=b"value = 7\n"
            path.write_bytes(data)
            module=subject.load("finite_loaded",path,subject.sha(data))
            self.assertEqual(module.value,7)
            self.assertEqual(module.__source_sha256__,subject.sha(data))

class ExecutionInputCustodyTests(SourceBindingTests):
    def prepare(self):
        tool=self.root/"tools/cbz_source514_hosted.py"
        plan=self.root/"cbz/source514-hosted/domain.json"
        tool.parent.mkdir()
        plan.parent.mkdir(parents=True)
        tool.write_bytes(b"value = 7\n")
        plan.write_text('{"frozen": 7}\n')
        subprocess.run(["git","-C",str(self.root),"add","tools","cbz"],check=True)
        subprocess.run(["git","-C",str(self.root),"commit","-qm","execution input fixture"],check=True)
        self.head=subject.git(self.root,"rev-parse","HEAD").decode().strip()
        return tool,plan

    def test_loaded_launcher_then_restored_file_is_rejected(self):
        tool,plan=self.prepare()
        tool.write_bytes(b"value = 8\n")
        loaded=subject.load("changed_launcher",tool,subject.sha(tool.read_bytes()))
        tool.write_bytes(b"value = 7\n")
        self.assertEqual(loaded.value,8)
        with self.assertRaisesRegex(ValueError,"loaded launcher differs"):
            subject.execution_inputs(self.root,self.head,loaded.__source_sha256__,plan)

    def test_plan_mutation_after_parse_is_rejected(self):
        tool,plan=self.prepare()
        loaded_sha=subject.sha(tool.read_bytes())
        parsed,binding=subject.execution_inputs(self.root,self.head,loaded_sha,plan)
        self.assertEqual(parsed,{"frozen":7})
        plan.write_text('{"frozen": 8}\n')
        with self.assertRaisesRegex(ValueError,"source bytes differ"):
            subject.execution_inputs(self.root,self.head,loaded_sha,plan)

class RegisteredDomainTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name)
        self.production=["Production"+str(i) for i in range(67)]
        self.support=["Support"+str(i) for i in range(25)]
        self.elder=["SuperlevelBar","ElderClearance","ReusedCompactFrontier","ClosedSuperlevel","OrdinaryH0","ElderInterval","ElderBridge"]
        self.plan={"production":self.production,"support":self.support,"elder":self.elder,"schema":"cbz-source514-exact-domain-v1","source_commit":subject.SOURCE_COMMIT}
        (self.root/"inputs").mkdir()
        for name in self.production:
            (self.root/(name+".lean")).write_text("-- finite source fixture\n")
        for name in self.support:
            (self.root/"inputs"/(name+".lean")).write_text("-- finite input fixture\n")
        (self.root/"inputs"/"elder").mkdir()
        for name in self.elder:
            (self.root/"inputs"/"elder"/(name+".lean")).write_text("-- consumed elder input fixture\n")
        for name in ["lake-manifest.json","lean-toolchain"]:
            (self.root/name).write_text("finite configuration fixture\n")
        self.write_configuration()

    def write_configuration(self):
        (self.root/"lakefile.toml").write_text("defaultTargets = "+json.dumps(self.production)+"\n[[lean_lib]]\nname = \"SourceDerivativeInputs\"\nroots = "+json.dumps(self.support)+"\n[[lean_lib]]\nname = \"SourceElderInputs\"\nsrcDir = \"inputs/elder\"\nroots = "+json.dumps(self.elder)+"\n")

    def test_complete_registered_domain(self):
        modules,sources=subject.checked_domain(self.root,self.plan)
        self.assertEqual(len(modules),99)
        self.assertEqual(len(set(modules)),99)
        self.assertEqual(len(sources),102)
        for name in self.elder:
            self.assertIn("inputs/elder/"+name+".lean",sources)

    def test_omitted_registered_elder_root_rejected(self):
        plan = dict(self.plan, elder=self.elder[:-1])
        with self.assertRaisesRegex(ValueError, "domain differs"):
            subject.checked_domain(self.root, plan)

    def test_missing_imported_elder_source_rejected(self):
        (self.root/(self.production[0]+".lean")).write_text("import "+self.elder[-1]+"\n")
        (self.root/"inputs"/"elder"/(self.elder[-1]+".lean")).unlink()
        with self.assertRaisesRegex(ValueError,"registered source is absent"):
            subject.checked_domain(self.root,self.plan)

    def test_plan_and_configuration_cannot_jointly_omit_elder_root(self):
        self.elder.pop()
        self.write_configuration()
        with self.assertRaisesRegex(ValueError,"expected exactly"):
            subject.checked_domain(self.root,self.plan)

    def test_reordered_domain_rejected(self):
        plan=dict(self.plan,production=self.production[::-1])
        with self.assertRaisesRegex(ValueError,"domain differs"):
            subject.checked_domain(self.root,plan)

    def test_duplicate_modules_rejected(self):
        self.production[-1]=self.support[0]
        self.write_configuration()
        with self.assertRaisesRegex(ValueError,"unique support modules"):
            subject.checked_domain(self.root,self.plan)

    def test_missing_source_rejected(self):
        (self.root/(self.production[0]+".lean")).unlink()
        with self.assertRaisesRegex(ValueError,"registered source is absent"):
            subject.checked_domain(self.root,self.plan)

class IndependentCensusTests(unittest.TestCase):
    def row(self,module="Fixture",name="Fixture.witness"):
        return dict(module=module,name=name,kind="theorem",type="True",user_written=True,user_name=name)
    def stream(self,rows):
        return "".join("SOURCE514_CENSUS "+json.dumps(r)+"\n" for r in rows)
    def test_exact_census(self):
        expected,rows=subject.parse_census(self.stream([self.row()]),["Fixture"])
        self.assertEqual(expected,{"module_counts":{"Fixture":1},"module_declarations":{"Fixture":["Fixture.witness"]}})
        self.assertEqual(len(rows),1)
    def test_duplicate_names_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate census"):
            subject.parse_census(self.stream([self.row(),self.row()]),["Fixture"])
    def test_omitted_registered_module_rejected(self):
        with self.assertRaisesRegex(ValueError,"omitted a registered"):
            subject.parse_census(self.stream([self.row()]),["Fixture","Other"])
    def test_unrecognized_output_rejected(self):
        with self.assertRaisesRegex(ValueError,"unrecognized"):
            subject.parse_census("PASS\n",["Fixture"])
    def test_empty_literal_type_rejected(self):
        row=self.row();row["type"]=""
        with self.assertRaisesRegex(ValueError,"literal type"):
            subject.parse_census(self.stream([row]),["Fixture"])
    def test_non_boolean_origin_rejected(self):
        row=self.row();row["user_written"]=1
        with self.assertRaisesRegex(ValueError,"literal type/origin"):
            subject.parse_census(self.stream([row]),["Fixture"])
    def test_unknown_fields_rejected(self):
        row=self.row();row["ignored"]={}
        with self.assertRaisesRegex(ValueError,"record fields"):
            subject.parse_census(self.stream([row]),["Fixture"])
    def test_duplicate_json_keys_rejected(self):
        line=self.stream([self.row()]).replace('"name": "Fixture.witness"','"name": "other", "name": "Fixture.witness"')
        with self.assertRaisesRegex(ValueError,"duplicate census JSON"):
            subject.parse_census(line,["Fixture"])
    def test_unsupported_kind_rejected(self):
        row=self.row();row["kind"]="ignored"
        with self.assertRaisesRegex(ValueError,"unsupported census"):
            subject.parse_census(self.stream([row]),["Fixture"])
    def test_empty_user_name_rejected(self):
        row=self.row();row["user_name"]=""
        with self.assertRaisesRegex(ValueError,"user name"):
            subject.parse_census(self.stream([row]),["Fixture"])
    def test_non_kernel_codegen_names_are_explicitly_recorded(self):
        metadata={"module":"Fixture","name":"Fixture.witness._boxed","classification":"NON_KERNEL_CODE_GENERATOR_OWNERSHIP"}
        stream="SOURCE514_CODEGEN_METADATA "+json.dumps(metadata)+"\n"+self.stream([self.row()])
        expected,rows=subject.parse_census(stream,["Fixture"])
        self.assertEqual(expected["non_kernel_codegen_ownership"],[metadata])
        self.assertEqual(expected["module_declarations"],{"Fixture":["Fixture.witness"]})
        self.assertEqual(len(rows),1)
    def test_codegen_metadata_cannot_hide_a_kernel_declaration(self):
        metadata={"module":"Fixture","name":"Fixture.witness","classification":"NON_KERNEL_CODE_GENERATOR_OWNERSHIP"}
        stream="SOURCE514_CODEGEN_METADATA "+json.dumps(metadata)+"\n"+self.stream([self.row()])
        with self.assertRaisesRegex(ValueError,"overlaps kernel census"):
            subject.parse_census(stream,["Fixture"])
    def test_generated_census_uses_exact_table_and_all_modules(self):
        program=subject.census_program(["Fixture","Other"])
        self.assertIn("let names := data.constNames.qsort Name.lt",program)
        self.assertIn("for extraName in data.extraConstNames",program)
        self.assertIn("code-generator metadata unexpectedly has a kernel declaration",program)
        self.assertIn("#["+chr(96)+"Fixture, "+chr(96)+"Other]",program)
        self.assertIn("missing independent census module",program)
        self.assertNotIn("MODLITERAL",program)

if __name__=="__main__":
    unittest.main()
