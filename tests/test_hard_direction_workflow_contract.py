import pathlib
import subprocess
import sys
import tempfile
import unittest


class HardDirectionWorkflowContract(unittest.TestCase):
    def test_adverse_child_outcomes_are_rejected(self):
        workflow = pathlib.Path('.github/workflows/c6-hard-direction-factorization.yml').read_text()
        start = workflow.index("          script = str(root / 'factorization.py')")
        end = workflow.index("          print(json.dumps({'scientific_effect'", start)
        block = '\n'.join(line[10:] for line in workflow[start:end].splitlines())
        harness = 'import pathlib,subprocess,sys,json,math\nroot=pathlib.Path(sys.argv[1])\n' + block
        for failure in ('silent', 'wrong_reason', 'wrong_label', 'stderr', 'duplicate', 'invalid_json'):
          for target in ('drop-vandermonde', 'hard-power-two', 'drop-spectral-constant'):
            with self.subTest(failure=failure, target=target), tempfile.TemporaryDirectory() as tmp:
                program = """import json,sys
mode = %r
target = %r
if '--mutant' not in sys.argv:
 print(json.dumps({'check':'ok','R_3_0':1.0,'closed_form':1.0,'mutant':None})); sys.exit(0)
mutant=sys.argv[-1]
reasons={'drop-vandermonde':'m_(3,0) = (7 - 4 sqrt2)/2','hard-power-two':'N_3(0) = 2 sqrt2','drop-spectral-constant':'c_1 = 1, c_2 = pi'}
if mutant != target:
 print(json.dumps({'check':'FAIL','what':reasons[mutant],'mutant':mutant})); sys.exit(1)
if mode == 'silent': sys.exit(1)
if mode == 'invalid_json': print('not json'); sys.exit(1)
if mode == 'duplicate': print('{"check":"FAIL","check":"FAIL"}'); sys.exit(1)
if mode == 'stderr': print('unexpected',file=sys.stderr)
print(json.dumps({'check':'FAIL','what': 'wrong' if mode == 'wrong_reason' else reasons[mutant], 'mutant': 'wrong' if mode == 'wrong_label' else mutant}))
sys.exit(1)
""" % (failure, target)
                pathlib.Path(tmp, 'factorization.py').write_text(program)
                child = subprocess.run([sys.executable, '-B', '-S', '-c', harness, tmp], capture_output=True)
                self.assertNotEqual(child.returncode, 0, failure)

    def test_actual_checker_and_all_mutants(self):
        workflow = pathlib.Path('.github/workflows/c6-hard-direction-factorization.yml').read_text()
        start = workflow.index("          script = str(root / 'factorization.py')")
        end = workflow.index("          print(json.dumps({'scientific_effect'", start)
        block = '\n'.join(line[10:] for line in workflow[start:end].splitlines())
        root = pathlib.Path('frontiers/c6_hard_direction_factorization_20260930').resolve()
        harness = 'import pathlib,subprocess,sys,json,math\nroot=pathlib.Path(sys.argv[1])\n' + block
        child = subprocess.run([sys.executable, '-B', '-S', '-c', harness, str(root)], capture_output=True, timeout=120)
        self.assertEqual(child.returncode, 0, child.stderr.decode())

    def test_unrelated_child_crash_is_not_a_mutant_kill(self):
        workflow = pathlib.Path('.github/workflows/c6-hard-direction-factorization.yml').read_text()
        start = workflow.index("          script = str(root / 'factorization.py')")
        end = workflow.index("          print(json.dumps({'scientific_effect'", start)
        block = '\n'.join(line[10:] for line in workflow[start:end].splitlines())
        with tempfile.TemporaryDirectory() as tmp:
            pathlib.Path(tmp, 'factorization.py').write_text(
                "import json,sys\n"
                "if '--mutant' in sys.argv: raise RuntimeError('unrelated failure')\n"
                "print(json.dumps({'check':'ok','R_3_0':4.211645867438038,'closed_form':4.2116458674380395,'mutant':None}))\n"
            )
            harness = 'import pathlib,subprocess,sys,json,math\nroot=pathlib.Path(sys.argv[1])\n' + block
            child = subprocess.run([sys.executable, '-B', '-S', '-c', harness, tmp], capture_output=True)
            self.assertNotEqual(child.returncode, 0, child.stdout.decode())


if __name__ == '__main__':
    unittest.main()
