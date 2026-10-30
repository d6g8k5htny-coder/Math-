"""Actual pinned-Lean emitter control; invoked explicitly, never skipped by discovery."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import unittest

from run_cbz_mutations import execute


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output=args.output.expanduser().resolve()
    args.lean=args.lean.expanduser().resolve(strict=True)
    args.output.mkdir(parents=True, exist_ok=False)
    implementation = Path(__file__).resolve().with_name('compiled_inventory.py')
    spec = importlib.util.spec_from_file_location('cap_actual_safety_exporter', implementation)
    api = importlib.util.module_from_spec(spec); spec.loader.exec_module(api)
    work = args.output
    (work/'CapFirstExit.lean').write_text('namespace CapFirstExit\nunsafe opaque opaqueHazard : Nat := 0\n'
                                       'theorem visible : True := by trivial\nend CapFirstExit\n')
    (work/'Inventory.lean').write_text(api.inventory_source())
    records = []

    def retained(command, label, timeout=600):
        try:
            return execute(command,work,work,label,timeout=timeout)
        finally:
            metadata=work/(label+'.process.json')
            if metadata.is_file():
                records.append(dict(label=label,**json.loads(metadata.read_text())))

    class ActualLeanSafety(unittest.TestCase):
        def runTest(self):
            version = retained([str(args.lean),'--version'],'version')
            self.assertEqual(version.returncode, 0)
            self.assertEqual(version.stderr, b'')
            self.assertRegex(version.stdout.decode(), r'^Lean \(version 4\.34\.1, [^\n]+, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release\)\n$')
            for label, command in [('compile',[str(args.lean),'-j2','-o','CapFirstExit.olean','CapFirstExit.lean']),
                                   ('export',[str(args.lean),'-j2','Inventory.lean'])]:
                env_program=shutil.which('env')
                self.assertIsNotNone(env_program, 'POSIX env executable unavailable for isolated fixture')
                process = retained([env_program,'LEAN_PATH='+str(work),'LEAN_NUM_THREADS=2']+command,label)
                self.assertEqual(process.returncode,0, 'actual fixture process failed before the safety assertion: '+label)
                self.assertEqual(process.stderr,b'', 'actual fixture stderr before the safety assertion: '+label)
            inventory=api.parse_inventory((work/'export.stdout').read_text())
            hazards=[row for row in inventory['constants'] if row[3]==('CapFirstExit','opaqueHazard')]
            self.assertEqual(len(hazards),1)
            self.assertEqual(hazards[0][4],'unsafe','ACTUAL_UNSAFE_OPAQUE_EXPORT_MISMATCH')
    result=unittest.TextTestRunner(verbosity=2).run(ActualLeanSafety())
    report={'schema':'cap.actual-opaque-export-control.v1','runs':records,
            'success':result.wasSuccessful(),'tests':result.testsRun,
            'implementation_sha256':hashlib.sha256(implementation.read_bytes()).hexdigest(),
            'program_sha256':hashlib.sha256((work/'Inventory.lean').read_bytes()).hexdigest(),
            'failures':len(result.failures),'errors':len(result.errors)}
    (work/'RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    return 0 if result.wasSuccessful() else 1


if __name__=='__main__':
    raise SystemExit(main())
