"""Real whole-shell controls for the equal-height execution wrapper.

Fixed reports are independent captures of original checker 92ba3cde; synthetic
children do not run quadrature or import production validation. Source controls,
ordered stage traces, and final Git cleanliness are exercised by the real shell.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/equal-height-mass.yml"
PACKET = "frontiers/equal_height_mass_value_20261001"
STAGES = ("baseline", "M1", "M2", "M3", "M9")
REPORTS = {'baseline': '{\n "checks": {\n  "Q1_conditional_hessian_law": {\n   "info": "scaled GOE: Var f_ii = 2, Var f_ij = 1, all other pairs 0; E[f_ii | f = b] = -b",\n   "passed": true\n  },\n  "Q2_scaled_GOE_normalisation": {\n   "info": {\n    "2": 20.0530262,\n    "3": 213.258381\n   },\n   "passed": true\n  },\n  "Q3_total_densities_closed_forms": {\n   "info": {\n    "2": {\n     "n_max": 0.09188814923,\n     "n_max_closed": 0.09188814924,\n     "n_sad": 0.1837762985,\n     "n_sad_closed": 0.1837762985\n    },\n    "3": {\n     "n_max": 0.03486240891,\n     "n_max_closed": 0.03486240894,\n     "n_sad": 0.106507305,\n     "n_sad_closed": 0.106507305\n    }\n   },\n   "passed": true\n  },\n  "Q4_beta_two_resolutions": {\n   "info": {\n    "24^3 beta_3": 10.23061,\n    "beta_2": 0.003122769186,\n    "beta_3": 0.0007400614572\n   },\n   "passed": true\n  }\n },\n "mutant": null,\n "object": "CL-EQUAL-HEIGHT-MASS-20261001-v1",\n "passed": true,\n "scientific_effect": "NONE"\n}\n', 'M1': '{\n "checks": {\n  "Q1_conditional_hessian_law": {\n   "info": "scaled GOE: Var f_ii = 2, Var f_ij = 1, all other pairs 0; E[f_ii | f = b] = -b",\n   "passed": true\n  },\n  "Q2_scaled_GOE_normalisation": {\n   "info": {\n    "2": 36.83976148,\n    "3": 719.7470357\n   },\n   "passed": false\n  },\n  "Q3_total_densities_closed_forms": {\n   "info": {\n    "2": {\n     "n_max": 0.1064044144,\n     "n_max_closed": 0.09188814924,\n     "n_sad": 0.2923863004,\n     "n_sad_closed": 0.1837762985\n    },\n    "3": {\n     "n_max": 0.0370511896,\n     "n_max_closed": 0.03486240894,\n     "n_sad": 0.1972540471,\n     "n_sad_closed": 0.106507305\n    }\n   },\n   "passed": false\n  },\n  "Q4_beta_two_resolutions": {\n   "info": {\n    "24^3 beta_3": 21.824481,\n    "beta_2": 0.006405517566,\n    "beta_3": 0.001578738502\n   },\n   "passed": true\n  }\n },\n "mutant": "M1",\n "object": "CL-EQUAL-HEIGHT-MASS-20261001-v1",\n "passed": false,\n "scientific_effect": "NONE"\n}\n', 'M2': '{\n "checks": {\n  "Q1_conditional_hessian_law": {\n   "info": "scaled GOE: Var f_ii = 2, Var f_ij = 1, all other pairs 0; E[f_ii | f = b] = -b",\n   "passed": true\n  },\n  "Q2_scaled_GOE_normalisation": {\n   "info": {\n    "2": 12.56637061,\n    "3": 44.54662398\n   },\n   "passed": false\n  },\n  "Q3_total_densities_closed_forms": {\n   "info": {\n    "2": {\n     "n_max": 0.1200418013,\n     "n_max_closed": 0.09188814924,\n     "n_sad": 0.08092865947,\n     "n_sad_closed": 0.1837762985\n    },\n    "3": {\n     "n_max": 0.06896003859,\n     "n_max_closed": 0.03486240894,\n     "n_sad": 0.03138667793,\n     "n_sad_closed": 0.106507305\n    }\n   },\n   "passed": false\n  },\n  "Q4_beta_two_resolutions": {\n   "info": {\n    "24^3 beta_3": 6.5702789,\n    "beta_2": 0.001937897205,\n    "beta_3": 0.0004752805934\n   },\n   "passed": false\n  }\n },\n "mutant": "M2",\n "object": "CL-EQUAL-HEIGHT-MASS-20261001-v1",\n "passed": false,\n "scientific_effect": "NONE"\n}\n', 'M3': '{\n "checks": {\n  "Q1_conditional_hessian_law": {\n   "info": "scaled GOE: Var f_ii = 2, Var f_ij = 1, all other pairs 0; E[f_ii | f = b] = -b",\n   "passed": true\n  },\n  "Q2_scaled_GOE_normalisation": {\n   "info": {\n    "2": 20.0530262,\n    "3": 213.258381\n   },\n   "passed": true\n  },\n  "Q3_total_densities_closed_forms": {\n   "info": {\n    "2": {\n     "n_max": 0.09188814923,\n     "n_max_closed": 0.09188814924,\n     "n_sad": 0.09188814923,\n     "n_sad_closed": 0.1837762985\n    },\n    "3": {\n     "n_max": 0.03486240891,\n     "n_max_closed": 0.03486240894,\n     "n_sad": 0.03486240891,\n     "n_sad_closed": 0.106507305\n    }\n   },\n   "passed": false\n  },\n  "Q4_beta_two_resolutions": {\n   "info": {\n    "24^3 beta_3": 5.9884942,\n    "beta_2": 0.002847545995,\n    "beta_3": 0.0004331954693\n   },\n   "passed": true\n  }\n },\n "mutant": "M3",\n "object": "CL-EQUAL-HEIGHT-MASS-20261001-v1",\n "passed": false,\n "scientific_effect": "NONE"\n}\n'}

CHILD = r"""
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
stage = "baseline" if not args else args[1]
if args and (len(args) != 2 or args[0] != "--mutant"):
    raise RuntimeError("bad synthetic command")
mode = sys.flags.optimize
with open(os.environ["EH_TRACE"], "a") as stream:
    stream.write(json.dumps([mode, stage]) + "\n")
data = json.loads(Path(__file__).with_name("reports.json").read_text())
out = b"" if stage == "M9" else data[stage].encode()
err = b"unknown mutant label\n" if stage == "M9" else b""
code = 0 if stage == "baseline" else 2 if stage == "M9" else 1
case = os.environ["EH_CASE"]
if case == "dirty":
    Path(os.environ["EH_RESULTS"]).write_text("changed after preflight\n")
if stage == os.environ["EH_STAGE"] and mode == int(os.environ["EH_MODE"]):
    if case == "crash": raise RuntimeError("unrelated synthetic error")
    if case == "silent": out = b""; err = b""
    elif case == "garbage": out = b"unrelated\n"
    elif case == "stderr": err += b"unexpected\n"
    elif case == "trailing": out += b"{}\n"
    elif case == "prefix": out = b"prefix\n" + out
    elif case == "format": out = b"\n" + out
    elif case == "same-size": out = out.replace(b'scaled GOE', b'scaled BAD', 1)
    elif case == "nested-null": out = out.replace(b'"passed": true', b'"passed": null', 1)
    elif case == "wrong-label": out = data["M2" if stage == "M1" else "M1"].encode()
    elif case == "wrong-exit": code = 0 if stage != "baseline" else 1
    elif case == "unknown-stdout": out = b"unexpected\n"
    elif case == "unknown-reason": err = b"unrelated failure\n"
sys.stdout.buffer.write(out)
sys.stderr.buffer.write(err)
sys.exit(code)
"""


def shell_text(text):
    marker = "      - name: Verify sources, replay both modes, reject mutants\n"
    if text.count(marker) != 1:
        raise ValueError("ambiguous replay step")
    lines = text.split(marker, 1)[1].split("        run: |\n", 1)[1].splitlines()
    result = []
    for line in lines:
        if line and not line.startswith("          "):
            break
        result.append(line[10:] if line else "")
    if not result or result[0] != "set -euo pipefail":
        raise ValueError("strict shell missing")
    return "\n".join(result) + "\n"


def entry(path, data):
    return {"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


class EqualHeightWorkflowTests(unittest.TestCase):
    def fixture(self, case="valid", stage="baseline", mode=0, guard=None):
        with tempfile.TemporaryDirectory(prefix="equal-height-fixture-") as temporary:
            home = Path(temporary)
            repo = home / "repo"
            packet = repo / PACKET
            packet.mkdir(parents=True)
            (packet / "equal_height_mass.py").write_text(CHILD)
            (packet / "RESULTS.json").write_text(REPORTS["baseline"])
            (packet / "reports.json").write_text(json.dumps(REPORTS))
            manifest = {"files": [entry(p.name, p.read_bytes()) for p in sorted(packet.iterdir())],
                        "mutants": ["M1", "M2", "M3"], "consumed": [], "cited_only": []}
            for kind in ("consumed", "cited_only"):
                data = ("nonempty fixed " + kind + "\n").encode()
                (repo / (kind + ".txt")).write_bytes(data)
                manifest[kind] = [entry(kind + ".txt", data)]
            (packet / "SOURCES.json").write_text(json.dumps(manifest))
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update(HOME=str(home), GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                       GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                       PYTHONDONTWRITEBYTECODE="1", EH_TRACE=str(home/"trace"),
                       EH_RESULTS=str(packet/"RESULTS.json"), EH_CASE=case,
                       EH_STAGE=stage, EH_MODE=str(mode))
            env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
            def git(*args):
                return subprocess.run(["git", *args], cwd=repo, env=env, check=True,
                                      capture_output=True, timeout=15)
            git("init", "-q")
            git("config", "core.hooksPath", os.devnull)
            git("add", ".")
            git("-c", "commit.gpgsign=false", "-c", "maintenance.auto=false", "commit", "-qm", "fixture")
            if guard == "source":
                with (packet/"equal_height_mass.py").open("a") as stream:
                    stream.write("\n# changed source\n")
            elif guard in ("consumed", "cited_only"):
                (repo/(guard+".txt")).write_bytes(b"changed pin\n")
            elif guard == "extra":
                (packet/"extra").write_text("unexpected")
            elif guard == "missing":
                (packet/"RESULTS.json").unlink()
            elif guard == "symlink":
                (home/"original").write_text(REPORTS["baseline"])
                (packet/"RESULTS.json").unlink()
                (packet/"RESULTS.json").symlink_to(home/"original")
            elif guard == "unmerged":
                manifest["consumed_unmerged"] = [{"path": "missing"}]
            elif guard and guard.startswith("inventory-"):
                manifest["mutants"] = {
                    "inventory-empty": [],
                    "inventory-missing": ["M1", "M2"],
                    "inventory-reverse": ["M3", "M2", "M1"],
                    "inventory-duplicate": ["M1", "M1", "M3"],
                    "inventory-mapping": {"M1": "Q2", "M2": "Q2", "M3": "Q3"},
                }[guard]
            if guard == "unmerged" or (guard and guard.startswith("inventory-")):
                (packet/"SOURCES.json").write_text(json.dumps(manifest))
                git("add", ".")
                git("-c", "commit.gpgsign=false", "-c", "maintenance.auto=false", "commit", "-qm", "inventory fixture")
            result = subprocess.run(["bash", "--noprofile", "--norc", "-c", shell_text(WORKFLOW.read_text())],
                                    cwd=repo, env=env, capture_output=True, timeout=30)
            calls = [json.loads(line) for line in (home/"trace").read_text().splitlines()] if (home/"trace").exists() else []
            if os.environ.get("EH_SAVE"):
                dest = Path(os.environ["EH_SAVE"]) / f"{case}-{stage}-{mode}-{guard}"
                dest.mkdir(parents=True, exist_ok=True)
                (dest/"stdout").write_bytes(result.stdout)
                (dest/"stderr").write_bytes(result.stderr)
                (dest/"record.json").write_text(json.dumps({"case": case, "stage": stage, "mode": mode,
                    "guard": guard, "returncode": result.returncode, "calls": calls}, sort_keys=True)+"\n")
            return result, calls

    def reject(self, case, stage, mode):
        result, calls = self.fixture(case, stage, mode)
        order = [[m, s] for m in (0, 1) for s in STAGES]
        self.assertIn([mode, stage], calls, "target was never reached")
        self.assertNotEqual(result.returncode, 0, "invalid protocol admitted")
        self.assertEqual(calls, order[:order.index([mode, stage])+1], "wrong stopping stage")

    def test_valid_inventory(self):
        result, calls = self.fixture()
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        self.assertEqual(calls, [[m, s] for m in (0, 1) for s in STAGES])

    def test_mutant_full_reports(self):
        for case in ("silent", "crash", "garbage", "stderr", "trailing", "prefix", "format", "same-size", "nested-null", "wrong-label", "wrong-exit"):
            for stage in ("M1", "M2", "M3"):
                for mode in (0, 1):
                    with self.subTest(case=case, stage=stage, mode=mode):
                        self.reject(case, stage, mode)

    def test_baseline_contract(self):
        for case in ("stderr", "silent", "garbage", "wrong-exit"):
            for mode in (0, 1):
                with self.subTest(case=case, mode=mode):
                    self.reject(case, "baseline", mode)

    def test_unknown_contract(self):
        for case in ("silent", "unknown-reason", "unknown-stdout", "wrong-exit"):
            for mode in (0, 1):
                with self.subTest(case=case, mode=mode):
                    self.reject(case, "M9", mode)

    def test_source_guards(self):
        reasons = {"source": b"packet file identity mismatch", "consumed": b"merged source drifted",
                   "cited_only": b"merged source drifted", "extra": b"packet tree differs",
                   "missing": b"packet tree differs", "symlink": b"symlink:",
                   "unmerged": b"this packet declares no unmerged dependency"}
        for guard, reason in reasons.items():
            with self.subTest(guard=guard):
                result, calls = self.fixture(guard=guard)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(calls, [])
                self.assertIn(reason, result.stderr)

    def test_inventory_guard(self):
        for guard in ("inventory-empty", "inventory-missing", "inventory-reverse", "inventory-duplicate", "inventory-mapping"):
            with self.subTest(guard=guard):
                result, calls = self.fixture(guard=guard)
                self.assertNotEqual(result.returncode, 0, "invalid inventory admitted")
                self.assertEqual(calls, [])

    def test_final_clean_tree_guard(self):
        result, calls = self.fixture(case="dirty")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(calls, [[m, s] for m in (0, 1) for s in STAGES])
        self.assertIn(b"changed after preflight", result.stdout)

    def test_workflow_test_wiring(self):
        text = WORKFLOW.read_text()
        self.assertIn("- 'tests/test_equal_height_workflow.py'", text)
        for flags in ("-B -S", "-B -O -S"):
            self.assertIn("python "+flags+" -m unittest discover -s tests -p test_equal_height_workflow.py -v", text)


if __name__ == "__main__":
    unittest.main()
