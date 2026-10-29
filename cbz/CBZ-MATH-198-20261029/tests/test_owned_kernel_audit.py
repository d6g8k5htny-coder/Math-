"""Fail-closed evidence controls for the all-owned kernel audit, without launching Lean."""
import copy
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / "tools/owned_kernel_audit.py"
INVENTORY = """OWN_MODULE|s41|2|1
OWN_CONST|s41|s41/s74|theorem|user|body|0|safe|total|primary
OWN_CONST|s41|s5f70726976617465/s41/n0/s68656c706572|def|aux|body|0|safe|total|primary
OWN_DEP|s41::s41/s74|s5f70726976617465/s41/n0/s68656c706572
OWN_DEP|s41::s5f70726976617465/s41/n0/s68656c706572|
OWN_EXTRA|s41|s41/s6972|ir_only
OWN_INVENTORY_COMPLETE|1|2|1
"""
CHECK = """OWN_CHECK|s41|s41/s74|theorem|checked|checked|checked|0
OWN_CHECK|s41|s5f70726976617465/s41/n0/s68656c706572|def|checked|checked|checked|0
OWN_AXIOMS|s70726f70657874,s436c6173736963616c/s63686f696365
OWN_CLOSURE|17
OWN_AUDIT_COMPLETE|2
"""


class OwnedKernelAuditTests(unittest.TestCase):
    def tool(self):
        self.assertTrue(TOOL.is_file(), "owned kernel auditor not implemented")
        spec = importlib.util.spec_from_file_location("owned_kernel_audit_tested", TOOL)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def inventory(self):
        return self.tool().parse_inventory(INVENTORY, ["A"], ["A.t"])

    def test_lossless_names_distinguish_private_numeric_and_quoted_components(self):
        tool = self.tool()
        for parts, encoded in [(["A", "t"], "s41/s74"),
                               (["_private", "A", 0, "helper"], "s5f70726976617465/s41/n0/s68656c706572"),
                               (["A.B"], "s412e42"), (["α"], "sceb1")]:
            self.assertEqual(tool.encode_name(parts), encoded)
            self.assertEqual(tool.decode_name(encoded), parts)
        for bad in ("", "sGG", "s61/n01", "sff", "s61//s62", "n-1"):
            with self.subTest(bad=bad), self.assertRaises(ValueError): tool.decode_name(bad)
        with self.assertRaises(ValueError): tool.encode_name([True])

    def test_inventory_includes_private_helper_and_ir_boundary(self):
        result = self.inventory()
        self.assertEqual(len(result["constants"]), 2)
        self.assertEqual(result["constants"][1]["origin"], "aux")
        self.assertEqual(result["extras"][0]["status"], "ir_only")

    def test_logical_extra_is_checked_not_assumed_ir_only(self):
        tool = self.tool()
        for status in ("logical_added", "logical_existing"):
            text = INVENTORY.replace("OWN_MODULE|s41|2|1", "OWN_MODULE|s41|1|2" if status == "logical_added" else "OWN_MODULE|s41|2|2")
            name = "s5f70726976617465/s41/n0/s68656c706572" if status == "logical_added" else "s41/s74"
            if status == "logical_added": text = text.replace("|def|aux|body|0|safe|total|primary", "|def|aux|body|0|safe|total|extra")
            text = text.replace("OWN_INVENTORY_COMPLETE|1|2|1", "OWN_EXTRA|s41|" + name + "|" + status + "\nOWN_INVENTORY_COMPLETE|1|2|2")
            result = tool.parse_inventory(text, ["A"], ["A.t"])
            self.assertEqual(len(result["constants"]), 2)
            bad = text.replace("|" + status + "\n", "|ir_only\n")
            with self.assertRaises(ValueError): tool.parse_inventory(bad, ["A"], ["A.t"])

    def test_omitted_module_constant_completion_or_dependency_cannot_pass(self):
        tool = self.tool()
        variants = [INVENTORY.replace("OWN_MODULE|s41|2|1\n", ""),
                    INVENTORY.replace("OWN_CONST|s41|s5f70726976617465/s41/n0/s68656c706572|def|aux|body|0|safe|total|primary\n", ""),
                    INVENTORY.replace("OWN_INVENTORY_COMPLETE|1|2|1\n", ""),
                    INVENTORY.replace("OWN_DEP|s41::s5f70726976617465/s41/n0/s68656c706572|\n", "")]
        for text in variants:
            with self.subTest(text=text), self.assertRaises(ValueError): tool.parse_inventory(text, ["A"], ["A.t"])

    def test_duplicate_foreign_unsafe_partial_axiom_or_missing_explicit_target_rejects(self):
        tool = self.tool()
        variants = [INVENTORY.replace("|theorem|user|", "|axiom|user|"),
                    INVENTORY.replace("|safe|total|", "|unsafe|total|", 1),
                    INVENTORY.replace("|safe|total|", "|safe|partial|", 1),
                    INVENTORY.replace("OWN_MODULE|s41|2|1", "OWN_MODULE|s42|2|1"),
                    INVENTORY + "OWN_MODULE|s41|2|1\n"]
        for text in variants:
            with self.subTest(text=text), self.assertRaises(ValueError): tool.parse_inventory(text, ["A"], ["A.t"])
        with self.assertRaises(ValueError): tool.parse_inventory(INVENTORY, ["A"], ["A.missing"])

    def test_self_and_mutual_body_cycles_are_rejected(self):
        tool = self.tool()
        direct = INVENTORY.replace("OWN_DEP|s41::s41/s74|s5f70726976617465/s41/n0/s68656c706572", "OWN_DEP|s41::s41/s74|s41/s74")
        mutual = INVENTORY.replace("OWN_DEP|s41::s5f70726976617465/s41/n0/s68656c706572|\n", "OWN_DEP|s41::s5f70726976617465/s41/n0/s68656c706572|s41/s74\n")
        for text in (direct, mutual):
            with self.assertRaisesRegex(ValueError, "cycle"): tool.parse_inventory(text, ["A"], ["A.t"])

    def test_actual_body_type_declaration_and_axiom_rows_are_required(self):
        tool = self.tool(); inventory = self.inventory()
        names = [x["id"] for x in inventory["constants"]]
        result = tool.parse_checks(CHECK, inventory, names)
        self.assertEqual(len(result["checked"]), 2)
        self.assertEqual(result["closure_size"], 17)
        for text in (CHECK.replace("|checked|checked|checked|", "|checked|missing|checked|", 1),
                     CHECK.replace("OWN_AUDIT_COMPLETE|2", "OWN_AUDIT_COMPLETE|1"),
                     CHECK.replace("OWN_AUDIT_COMPLETE|2\n", ""),
                     CHECK.replace("s70726f70657874", "s736f7272794178"),
                     CHECK.replace("OWN_AXIOMS|", "BROKEN|", 1)):
            with self.subTest(text=text), self.assertRaises(ValueError): tool.parse_checks(text, inventory, names)

    def test_primitive_rules_receive_their_own_checked_counts(self):
        tool = self.tool()
        inv = INVENTORY.replace("|def|aux|body|0|", "|rec|aux|primitive|2|")
        checked = CHECK.replace("|def|checked|checked|checked|0", "|rec|checked|absent|primitive|2")
        inventory = tool.parse_inventory(inv, ["A"], ["A.t"])
        names = [x["id"] for x in inventory["constants"]]
        self.assertEqual(len(tool.parse_checks(checked, inventory, names)["checked"]), 2)
        with self.assertRaises(ValueError): tool.parse_checks(checked.replace("|primitive|2", "|primitive|1"), inventory, names)

    def test_generator_rejects_injected_modules_and_names(self):
        tool = self.tool()
        for modules in (["A\naxiom bad : False"], ["A", "A"], []):
            with self.assertRaises(ValueError): tool.render_support(modules, ["A.t"])
        with self.assertRaises(ValueError): tool.render_chunk(["szz"])
        with self.assertRaises(ValueError): tool.render_chunk([])

    def test_duplicate_logical_name_instances_are_both_required_and_checked(self):
        tool=self.tool()
        inventory=INVENTORY.replace("OWN_MODULE|s41|2|1", "OWN_MODULE|s41|2|1\nOWN_MODULE|s42|1|0")
        inventory=inventory.replace("OWN_DEP|s41::s41/s74|", "OWN_CONST|s42|s41/s74|theorem|aux|body|0|safe|total|primary\nOWN_DEP|s42::s41/s74|\nOWN_DEP|s41::s41/s74|")
        inventory=inventory.replace("OWN_INVENTORY_COMPLETE|1|2|1", "OWN_INVENTORY_COMPLETE|2|3|1")
        result=tool.parse_inventory(inventory,["A","B"],["A.t"])
        self.assertEqual(len(result["constants"]),3)
        self.assertEqual(len({x["name"] for x in result["constants"]}),2)
        checked=CHECK.replace("OWN_AXIOMS|", "OWN_CHECK|s42|s41/s74|theorem|checked|checked|checked|0\nOWN_AXIOMS|")
        checked=checked.replace("OWN_AUDIT_COMPLETE|2", "OWN_AUDIT_COMPLETE|3")
        self.assertEqual(len(tool.parse_checks(checked,result,[x["id"] for x in result["constants"]])["checked"]),3)

    def test_parent_lock_identity_is_checked_not_merely_an_environment_flag(self):
        tool = self.tool()
        with tempfile.TemporaryDirectory() as temp:
            lock = Path(temp)/"lock"; lock.touch()
            with self.assertRaises(ValueError): tool.require_parent_lock(lock)

    def test_parent_lock_can_be_held_by_a_verified_ancestor_supervisor(self):
        self.tool()
        with tempfile.TemporaryDirectory() as temp:
            lock = Path(temp)/"lock"
            grandchild = "import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); import owned_kernel_audit as m; m.require_parent_lock(Path(sys.argv[2])); print('locked')"
            child = "import subprocess,sys; r=subprocess.run([sys.executable,'-B','-c',sys.argv[1],sys.argv[2],sys.argv[3]],capture_output=True,text=True);print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr);raise SystemExit(r.returncode)"
            with lock.open("a") as stream:
                fcntl.flock(stream, fcntl.LOCK_EX)
                result = subprocess.run([sys.executable,"-B","-c",child,grandchild,str(TOOL.parent),str(lock)],capture_output=True,text=True,timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "locked\n")

    def test_complete_cache_staging_does_not_shadow_missing_sibling_modules(self):
        tool = self.tool()
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); source=root/"cache"; (source/"Closure").mkdir(parents=True)
            (source/"Closure/Assembly.olean").write_bytes(b"assembly")
            (source/"General.olean").write_bytes(b"general")
            expected={"Closure/Assembly.olean":hashlib.sha256(b"assembly").hexdigest(),"General.olean":hashlib.sha256(b"general").hexdigest()}
            staged=root/"staged"; staged.mkdir()
            tool.stage_cache(source,staged,expected)
            self.assertEqual((staged/"Closure/Assembly.olean").read_bytes(),b"assembly")
            self.assertEqual((source/"General.olean").read_bytes(),b"general")
            (source/"extra.olean").write_bytes(b"unlisted")
            with self.assertRaises(ValueError): tool.stage_cache(source,root/"other",expected)

    def test_source_snapshot_freezes_all_lean_files_without_touching_them(self):
        tool = self.tool()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = root/"source"; (source/"formal/A").mkdir(parents=True)
            (source/"formal/A/B.lean").write_text("theorem t : True := True.intro\n")
            (source/"audit_targets.json").write_text(json.dumps({"names":["A.t"]}))
            output = root/"snapshot"
            result = tool.freeze_sources(source, output)
            self.assertEqual(result["modules"], ["A.B"])
            self.assertEqual((output/"formal/A/B.lean").read_bytes(), (source/"formal/A/B.lean").read_bytes())
            (source/"formal/A/B.lean").write_text("changed\n")
            with self.assertRaises(ValueError): tool.check_source_snapshot(source, result)

    def test_prior_cache_sources_order_and_records_are_exact_not_a_subset(self):
        tool = self.tool()
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); source=root/"source"; cache=root/"cache"; evidence=root/"evidence"
            (source/"formal").mkdir(parents=True);cache.mkdir();evidence.mkdir()
            targets=["A.t"+str(n) for n in range(198)]
            snapshot={"modules":["A","B","Legacy"],"explicit_targets":targets,"sources":{}}
            sources={}; outputs={}; records=[]
            empty=hashlib.sha256(b"").hexdigest()
            for module in ("A","B","Legacy"):
                relative="formal/"+module+".lean"; data=("def "+module+" : Nat := 1\n").encode()
                (source/relative).write_bytes(data);snapshot["sources"][relative]=hashlib.sha256(data).hexdigest()
                if module=="Legacy":continue
                sources[relative]=snapshot["sources"][relative]
                leaf=evidence/module;leaf.mkdir()
                log=("".join("P15_AUDIT|"+n+"|closed|kernel|declaration|\n" for n in targets)+"P15_AUDIT_COMPLETE|198\n").encode() if module=="B" else b""
                (leaf/"stdout.txt").write_bytes(log);(leaf/"stderr.txt").write_bytes(b"")
                receipt={"succeeded":True,"returncode":0,"failure":None,"timed_out":False,"output_limit_exceeded":False,
                         "streams":{"stdout.txt":{"sha256":hashlib.sha256(log).hexdigest(),"bytes":len(log)},"stderr.txt":{"sha256":empty,"bytes":0}}}
                (leaf/"receipt.json").write_text(json.dumps(receipt))
                records.append({"module":module,"source_sha256":sources[relative],"receipt":module+"/receipt.json",**receipt})
                (cache/(module+".olean")).write_bytes(module.encode());outputs[module+".olean"]=hashlib.sha256(module.encode()).hexdigest()
            result={"status":"PASS","cache_was_fresh":True,"old_project_cache_on_lean_path":False,
                    "sources":sources,"outputs":outputs,"order":["A","B"],"records":records,
                    "audited_theorems":[{"name":n,"axioms":[]} for n in targets]}
            (evidence/"results.json").write_text(json.dumps(result))
            tool.verify_prior(source,cache,evidence,snapshot)
            variants=[]
            missing=copy.deepcopy(result);del missing["sources"]["formal/B.lean"];variants.append(missing)
            duplicate=copy.deepcopy(result);duplicate["order"]=["A","A"];variants.append(duplicate)
            omitted=copy.deepcopy(result);omitted["records"].pop();variants.append(omitted)
            wrong=copy.deepcopy(result);wrong["records"][0]["source_sha256"]="0"*64;variants.append(wrong)
            for value in variants:
                (evidence/"results.json").write_text(json.dumps(value))
                with self.subTest(value=value),self.assertRaises(ValueError): tool.verify_prior(source,cache,evidence,snapshot)
            for change in ("streams", "returncode"):
                value=copy.deepcopy(result);receipt=json.loads((evidence/"B/receipt.json").read_text())
                receipt[change]={} if change=="streams" else False
                value["records"][-1][change]=receipt[change]
                (evidence/"B/receipt.json").write_text(json.dumps(receipt));(evidence/"results.json").write_text(json.dumps(value))
                with self.subTest(change=change),self.assertRaises(ValueError): tool.verify_prior(source,cache,evidence,snapshot)
                (evidence/"B/receipt.json").write_text(json.dumps({k:v for k,v in result["records"][-1].items() if k not in {"module","source_sha256","receipt"}}))
            value=copy.deepcopy(result); log=b"P15_AUDIT_COMPLETE|198\n"; (evidence/"B/stdout.txt").write_bytes(log)
            receipt=json.loads((evidence/"B/receipt.json").read_text());receipt["streams"]["stdout.txt"]={"bytes":len(log),"sha256":hashlib.sha256(log).hexdigest()}
            value["records"][-1]["streams"]=receipt["streams"]
            (evidence/"B/receipt.json").write_text(json.dumps(receipt));(evidence/"results.json").write_text(json.dumps(value))
            with self.assertRaises(ValueError):tool.verify_prior(source,cache,evidence,snapshot)


if __name__ == "__main__": unittest.main()
