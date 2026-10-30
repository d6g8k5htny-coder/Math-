"""Named Cap auditor mutations; generic errors, zero tests and foreign failures never kill."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

import gate

HERE=Path(__file__).resolve().parent
MUTATIONS=[
 ('owned_axiom',"        if kind == 'axiom':",'        if False:', 'test_owned_axiom_is_forbidden_even_if_approved_name_and_bound'),
 ('extra_constant','            if row not in bound:','            if False:', 'test_compiler_shaped_added_theorem_is_not_automatically_admitted'),
 ('hidden_user_theorem',"        if origin == 'user' and kind == 'theorem' and relation_map.get(name, (None,))[0] != 'projection':",'        if False:', 'test_hidden_private_user_theorem_rejects_even_if_manifest_lists_it'),
 ('hidden_user_definition',"        if origin == 'user' and kind in ('def','inductive','opaque') and name not in relation_map:",'        if False:', 'test_user_definition_cannot_be_laundered_as_structure_support'),
 ('axiom_closure','    for axiom in axioms - {dotted(a) for a in ALLOWED}:','    for axiom in ():', 'test_unused_sorry_and_custom_axiom_closure_refuse'),
 ('module_count','    if MODULE_NAME in module_counts and actual_count != module_counts[MODULE_NAME]:','    if False:', 'test_duplicate_names_and_module_counts_refuse'),
 ('missing_binding','    for row in bound - observed:','    for row in ():', 'test_missing_or_changed_support_record_refuses'),
 ('codegen_extras',"        if extra != sum(owner==module for owner,name in inventory['extras']):",'        if False:', 'test_module_system_and_codegen_extras_fail_closed'),
 ('codegen_binding',"    for module,name in set(inventory['extras']) ^ codegen:",'    for module,name in ():', 'test_codegen_extras_are_exactly_bound_not_ignored'),
 ('unsafe_partial',"        if safety != 'safe':",'        if False:', 'test_unsafe_or_partial_constant_refuses_even_if_bound'),
 ('unsupported_kind',"        if kind in ('opaque','quot'):",'        if False:', 'test_owned_opaque_and_quot_never_self_admit'),
]


def execute(command,cwd,out,label,timeout=900):
    """Retain every completed/expired process before refusing a timeout."""
    process=gate.run_process(command,cwd=cwd,timeout=timeout)
    process.stdout=process.stdout.encode() if isinstance(process.stdout,str) else process.stdout
    process.stderr=process.stderr.encode() if isinstance(process.stderr,str) else process.stderr
    (out/(label+'.stdout')).write_bytes(process.stdout)
    (out/(label+'.stderr')).write_bytes(process.stderr)
    (out/(label+'.exit')).write_text(str(process.returncode)+'\n')
    (out/(label+'.process.json')).write_text(json.dumps({
        'command':[str(part) for part in command], 'cwd':str(cwd), 'exit':process.returncode,
        'timed_out':getattr(process,'timed_out',False),
        'cleanup_signals':getattr(process,'cleanup_signals',[])},indent=2)+'\n')
    if getattr(process,'timed_out',False):
        raise RuntimeError('process timed out; retained streams and metadata: '+label)
    return process


def intended_failure(process, method, marker=None):
    expected=('FAIL: '+method+' (').encode()
    semantic=(re.search(rb'^AssertionError: ValueError not raised\r?$',process.stderr,re.M) is not None
              if marker is None else marker in process.stderr)
    return bool(process.returncode==1 and expected in process.stderr and b'ERROR:' not in process.stderr
                and re.search(rb'^Ran 1 test in [0-9]+(?:\.[0-9]+)?s$',process.stderr,re.M)
                and re.search(rb'^FAILED \(failures=1\)$',process.stderr,re.M)
                and semantic and not getattr(process,'timed_out',False))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--lean',required=True,type=Path,help='verified exact Lean4.34.1 binary for the actual exporter guard control')
    args=parser.parse_args()
    args.output=args.output.expanduser().resolve()
    args.lean=args.lean.expanduser().resolve(strict=True)
    args.output.mkdir(parents=True,exist_ok=False)
    original=(HERE/'compiled_inventory.py').read_text()
    identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file()}
    results=[]
    with tempfile.TemporaryDirectory(prefix='cap-auditor-mutants-') as temporary:
        base=Path(temporary)
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            copied=base/mode;copied.mkdir()
            for name in ('compiled_inventory.py','test_compiled_inventory.py','gate.py','lean_opaque_control.py','run_cbz_mutations.py'):
                shutil.copy2(HERE/name,copied/name)
            baseline=execute([sys.executable,'-B','-S']+flags+['-m','unittest','-v','test_compiled_inventory'],copied,args.output,mode+'-baseline')
            if baseline.returncode!=0 or not re.search(rb'Ran [1-9][0-9]* tests',baseline.stderr) or b'\nOK\n' not in baseline.stderr:
                raise RuntimeError('selected unchanged baseline is not green: '+mode)
            for label,old,new,method in MUTATIONS:
                if original.count(old)!=1:raise RuntimeError('nonunique mutant anchor: '+label)
                (copied/'compiled_inventory.py').write_text(original.replace(old,new,1))
                process=execute([sys.executable,'-B','-S']+flags+['-m','unittest','-v','test_compiled_inventory.CompiledInventory.'+method],copied,args.output,mode+'-'+label)
                killed=intended_failure(process,method)
                results.append({'mode':mode,'mutation':label,'expected_test':method,'exit':process.returncode,'killed':bool(killed)})
                if not killed:raise RuntimeError('mutation not killed by intended assertion: '+mode+'/'+label)
            (copied/'compiled_inventory.py').write_text(original)
            positive=execute([sys.executable,'-B','-S']+flags+['lean_opaque_control.py','--lean',str(args.lean),'--output',str(args.output/(mode+'-opaque-positive'))],copied,args.output,mode+'-opaque-positive-observer')
            if positive.returncode!=0:raise RuntimeError('actual unchanged opaque exporter control failed: '+mode)
            anchor='  if ci.isUnsafe then "unsafe" else'
            if original.count(anchor)!=1:raise RuntimeError('nonunique actual Lean mutation anchor')
            (copied/'compiled_inventory.py').write_text(original.replace(anchor,'  if false then "unsafe" else',1))
            mutant=execute([sys.executable,'-B','-S']+flags+['lean_opaque_control.py','--lean',str(args.lean),'--output',str(args.output/(mode+'-opaque-mutant'))],copied,args.output,mode+'-opaque-mutant-observer')
            killed=intended_failure(mutant,'runTest',b'ACTUAL_UNSAFE_OPAQUE_EXPORT_MISMATCH')
            results.append({'mode':mode,'mutation':'actual_opaque_export','exit':mutant.returncode,'killed':bool(killed)})
            if not killed:raise RuntimeError('actual exporter mutation did not reach the intended safety assertion: '+mode)
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file()}
    if after!=identities:raise RuntimeError('production source changed during source mutations')
    report={'schema':'cap.auditor-mutations.v1','threshold':'all12 named mutations in each Python mode',
            'source_sha256':identities,'mutations':results,'source_preserved':True}
    (args.output/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'mutations':len(results),'all_killed':all(r['killed'] for r in results),'source_preserved':True}))


if __name__=='__main__':main()
