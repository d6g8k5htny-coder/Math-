import pathlib
import json
import subprocess
import sys
import tempfile
import unittest


class HardDirectionWorkflowContract(unittest.TestCase):
    @staticmethod
    def guarded_run(block, root):
        # Record the actual traceback while it is live, before unittest formats it.
        driver = '''import json,math,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1])
source=sys.stdin.read()
try:
 exec(compile(source, '<workflow-guard>', 'exec'))
except BaseException as exc:
 tb=exc.__traceback__
 frames=[]
 while tb is not None:
  code=tb.tb_frame.f_code
  if code.co_filename == '<workflow-guard>':
   frames.append([code.co_name,tb.tb_lineno])
  tb=tb.tb_next
 print(json.dumps({'exception':type(exc).__name__,'message':str(exc),'frames':frames}))
 sys.exit(42)
'''
        result = subprocess.run([sys.executable, '-B', '-S', '-c', driver, str(root)],
                                input=block.encode(), capture_output=True, timeout=120)
        return result

    def test_traceback_records_unrelated_same_message_origin(self):
        block = "raise RuntimeError('unexpected child exit or stderr')\n"
        child = self.guarded_run(block, '.')
        self.assertEqual(child.returncode, 42, child.stderr.decode())
        event = json.loads(child.stdout)
        self.assertEqual(event['exception'], 'RuntimeError')
        self.assertEqual(event['message'], 'unexpected child exit or stderr')
        # Same text is insufficient: this originated at the module body, not decode.
        self.assertEqual(event['frames'], [['<module>', 1]])

    def test_baseline_child_failures_are_not_admitted(self):
        workflow = pathlib.Path('.github/workflows/c6-hard-direction-factorization.yml').read_text()
        start = workflow.index("          script = str(root / 'factorization.py')")
        end = workflow.index("          print(json.dumps({'scientific_effect'", start)
        block = '\n'.join(line[10:] for line in workflow[start:end].splitlines())
        bad_programs = {
            'exit': 'raise SystemExit(1)',
            'stderr': "import sys; print('error', file=sys.stderr)",
            'wrong_schema': "print('{}')",
            'nonfinite': "print('{\\\"check\\\":\\\"ok\\\",\\\"R_3_0\\\":NaN,\\\"closed_form\\\":1,\\\"mutant\\\":null}')",
        }
        for case, program in bad_programs.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                pathlib.Path(tmp, 'factorization.py').write_text(program + '\n')
                child = self.guarded_run(block, tmp)
                self.assertEqual(child.returncode, 42, child.stderr.decode())
                event = json.loads(child.stdout)
                function, line = event['frames'][-1]
                source_line = block.splitlines()[line - 1]
                if case in ('exit', 'stderr'):
                    self.assertEqual((event['exception'], function), ('RuntimeError', 'decode'))
                    self.assertIn('unexpected child exit or stderr', source_line)
                elif case == 'wrong_schema':
                    self.assertEqual((event['exception'], function), ('RuntimeError', '<module>'))
                    self.assertIn('unexpected baseline result', source_line)
                else:
                    self.assertEqual(event['exception'], 'ValueError')
                    self.assertEqual(function, '<genexpr>')
                    self.assertIn('parse_constant=lambda value:', source_line)

    def test_adverse_child_outcomes_are_rejected(self):
        workflow = pathlib.Path('.github/workflows/c6-hard-direction-factorization.yml').read_text()
        start = workflow.index("          script = str(root / 'factorization.py')")
        end = workflow.index("          print(json.dumps({'scientific_effect'", start)
        block = '\n'.join(line[10:] for line in workflow[start:end].splitlines())
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
                child = self.guarded_run(block, tmp)
                self.assertEqual(child.returncode, 42, child.stderr.decode())
                event = json.loads(child.stdout)
                expected_type = {'silent':'JSONDecodeError', 'invalid_json':'JSONDecodeError', 'duplicate':'ValueError'}.get(failure, 'RuntimeError')
                self.assertEqual(event['exception'], expected_type)
                function, line = event['frames'][-1]
                source_line = block.splitlines()[line - 1].strip()
                if failure in ('silent', 'invalid_json'):
                    self.assertEqual((function, source_line), ('decode', 'return json.loads(out.stdout, object_pairs_hook=pairs,'))
                elif failure == 'duplicate':
                    self.assertEqual(function, 'pairs')
                    self.assertIn("raise ValueError('duplicate JSON key:", source_line)
                elif failure == 'stderr':
                    self.assertEqual(function, 'decode')
                    self.assertIn("raise RuntimeError('unexpected child exit or stderr')", source_line)
                else:
                    self.assertEqual(function, '<module>')
                    self.assertIn("raise RuntimeError('mutant ' + m + ' not rejected')", source_line)

    def test_optimized_child_failure_is_exercised(self):
        workflow = pathlib.Path('.github/workflows/c6-hard-direction-factorization.yml').read_text()
        start = workflow.index("          script = str(root / 'factorization.py')")
        end = workflow.index("          print(json.dumps({'scientific_effect'", start)
        block = '\n'.join(line[10:] for line in workflow[start:end].splitlines())
        with tempfile.TemporaryDirectory() as tmp:
            pathlib.Path(tmp, 'factorization.py').write_text(
                "import json,sys\n"
                "if sys.flags.optimize: raise RuntimeError('optimized child failure')\n"
                "reasons={'drop-vandermonde':'m_(3,0) = (7 - 4 sqrt2)/2','hard-power-two':'N_3(0) = 2 sqrt2','drop-spectral-constant':'c_1 = 1, c_2 = pi'}\n"
                "if '--mutant' in sys.argv:\n"
                " m=sys.argv[-1]; print(json.dumps({'check':'FAIL','what':reasons[m],'mutant':m})); sys.exit(1)\n"
                "print(json.dumps({'check':'ok','R_3_0':1.0,'closed_form':1.0,'mutant':None}))\n"
            )
            child = self.guarded_run(block, tmp)
            self.assertEqual(child.returncode, 42, child.stderr.decode())
            event = json.loads(child.stdout)
            function, line = event['frames'][-1]
            self.assertEqual((event['exception'], function), ('RuntimeError', 'decode'))
            self.assertIn("raise RuntimeError('unexpected child exit or stderr')", block.splitlines()[line - 1])

    def test_normal_child_failure_is_exercised(self):
        workflow = pathlib.Path('.github/workflows/c6-hard-direction-factorization.yml').read_text()
        start = workflow.index("          script = str(root / 'factorization.py')")
        end = workflow.index("          print(json.dumps({'scientific_effect'", start)
        block = '\n'.join(line[10:] for line in workflow[start:end].splitlines())
        with tempfile.TemporaryDirectory() as tmp:
            pathlib.Path(tmp, 'factorization.py').write_text(
                "import json,sys\n"
                "if not sys.flags.optimize: raise RuntimeError('normal child failure')\n"
                "reasons={'drop-vandermonde':'m_(3,0) = (7 - 4 sqrt2)/2','hard-power-two':'N_3(0) = 2 sqrt2','drop-spectral-constant':'c_1 = 1, c_2 = pi'}\n"
                "if '--mutant' in sys.argv:\n"
                " m=sys.argv[-1]; print(json.dumps({'check':'FAIL','what':reasons[m],'mutant':m})); sys.exit(1)\n"
                "print(json.dumps({'check':'ok','R_3_0':1.0,'closed_form':1.0,'mutant':None}))\n"
            )
            child = self.guarded_run(block, tmp)
            self.assertEqual(child.returncode, 42, child.stderr.decode())
            event = json.loads(child.stdout)
            function, line = event['frames'][-1]
            self.assertEqual((event['exception'], function), ('RuntimeError', 'decode'))
            self.assertIn("raise RuntimeError('unexpected child exit or stderr')", block.splitlines()[line - 1])

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
            child = self.guarded_run(block, tmp)
            self.assertEqual(child.returncode, 42, child.stderr.decode())
            event = json.loads(child.stdout)
            function, line = event['frames'][-1]
            self.assertEqual((event['exception'], function), ('RuntimeError', 'decode'))
            self.assertIn("raise RuntimeError('unexpected child exit or stderr')", block.splitlines()[line - 1])


if __name__ == '__main__':
    unittest.main()
