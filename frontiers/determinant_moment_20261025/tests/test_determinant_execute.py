#!/usr/bin/env python3
"""Bounded integration probes. All external process observations are SYNTHETIC.

This script never executes Lean. Receipt files exist only in disposable test packages;
none is retained or presented as actual kernel evidence. Production files are untouched.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from types import ModuleType
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
INPUT = HERE
FIXTURE = HERE
ADAPTER_SHA256 = hashlib.sha256((INPUT/'determinant_inventory.py').read_bytes()).hexdigest()
VERSION = 'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)'
MANIFEST = json.loads((FIXTURE/'tests/fixtures/actual_manifest_v2_fields.json').read_text())
INVENTORY = (FIXTURE/'tests/fixtures/actual_inventory_4ccc.log').read_text()


def ensure(condition, message):
    if not condition:
        raise AssertionError(message)


def emit(kind, **fields):
    return dict(check=kind, **fields)  # All process responses remain synthetic.


def enc(name):
    return '/'.join('n'+str(x) if type(x) is int else 's'+x.encode().hex() for x in name)


def load_gate():
    raw=(INPUT/'gate.py').read_bytes()
    gate=ModuleType('bounded_integration_gate')
    gate.__file__=str(INPUT/'gate.py')
    exec(compile(raw,gate.__file__,'exec'),gate.__dict__)
    return gate


def injected_inventory(module,label,unrelated=False):
    if label=='compiled_admission':
        name=('_private',*module,0,'ResearchFormalCoreR1','compiledAdmission')
        row=('theorem','user',module,name)
    else:
        row=('theorem','aux',module,('ResearchFormalCoreR1','ec005_fold_gap','_proof_999'))
    prefix='MODULE|'+enc(module)+'|false|'
    lines=INVENTORY.splitlines()
    matches=[i for i,line in enumerate(lines) if line.startswith(prefix)]
    ensure(len(matches)==1,'module table not unique in fixture')
    i=matches[0];parts=lines[i].split('|');parts[3]=str(int(parts[3])+1);lines[i]='|'.join(parts)
    lines.append('INV|'+'|'.join((row[0],row[1],enc(row[2]),enc(row[3]))))
    result='\n'.join(lines)+'\n'
    if label=='compiled_admission':
        result=result.replace('AXIOMS|','AXIOMS|'+enc(('sorryAx',))+',')
    if unrelated:
        target='MODULE|'+enc(('ResearchFormalCoreR1','DeterminantMoment'))+'|false|20|6'
        ensure(target in result,'IR drift fixture anchor changed')
        result=result.replace(target,target[:-1]+'7')
    return result


def execute_scenario(scenario):
    gate=load_gate()
    with tempfile.TemporaryDirectory(prefix=scenario+'-') as directory:
        package=Path(directory)/'package';package.mkdir()
        for name in ('compiled_inventory.py','determinant_inventory.py'):
            shutil.copyfile(INPUT/name,package/name)
        m=json.loads(json.dumps(MANIFEST))
        m['files']={'determinant_inventory.py':ADAPTER_SHA256}
        m['dependency_revisions']={'mathlib':'1'*40}
        for name in [*m['source_modules'],'ResearchFormalCoreR1.lean']:
            dest=package/name;dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(FIXTURE/name,dest)
        (package/'.lake/packages').mkdir(parents=True)
        (package/'.lake/build').mkdir()
        active=package/'.lake/formal-evidence/receipt.json'
        active.parent.mkdir();active.write_text('SYNTHETIC stale active receipt\n')
        archive=package/'.lake/formal-evidence/historical-marker.txt'
        archive.write_text('preserve historical evidence\n')
        gate.ROOT=package;gate._compiled=None;gate._determinant=None
        digest='d'*64
        module=tuple(m['source_modules'][0][:-5].replace('/','.').split('.'))
        calls=[];postchecks=[];source_observations=[]
        source_identity=dict(checked_commit='a'*40, checked_tree='b'*40, manifest_sha256=digest,
                             scope='SYNTHETIC_ORCHESTRATION_ONLY_NO_GIT_EVIDENCE')

        def qualify_source(manifest, observed_digest, *, previous=None):
            ensure(manifest==m and observed_digest==digest, 'source endpoint received wrong inputs')
            phase='preflight' if previous is None else 'final'
            source_observations.append(phase)
            if scenario=='pre_git_failure' and phase=='preflight':
                raise ValueError('SYNTHETIC preflight Git refusal')
            if scenario=='post_git_failure' and phase=='final':
                raise ValueError('SYNTHETIC final Git refusal')
            if previous is not None:
                ensure(previous==source_identity, 'final endpoint lost the exact preflight identity')
            return json.loads(json.dumps(source_identity))

        def clone_label(cwd):
            body=(Path(cwd)/m['source_modules'][0]).read_text()
            if 'private theorem compiledAdmission' in body:
                return 'compiled_admission'
            if 'Lean.addDecl' in body:
                return 'compiled_metaprogram'
            return 'compiled_baseline'

        def fake_run(command,cwd=None,**kwargs):
            ensure(not active.exists(),'stale receipt visible during a process stage')
            cwd=Path(cwd);in_clone=cwd!=package
            returncode=0
            if command==['lake','build']:
                stage=clone_label(cwd)+'_build' if in_clone else 'build'
                (cwd/'.lake/build').mkdir(parents=True,exist_ok=True)
                result='SYNTHETIC successful build response; no Lean executed\n'
                if scenario=='injection_prerequisite_failure' and stage=='compiled_admission_build':
                    returncode=1;result='SYNTHETIC intended prerequisite failure\n'
            elif command[:3]==['lake','env','leanchecker']:
                stage=clone_label(cwd)+'_leanchecker' if in_clone else 'leanchecker'
                result='SYNTHETIC checker success; no checker executed\n'
            elif command[-1]=='--version':
                stage='version-preflight' if not any(c[0]=='version-preflight' for c in calls) else 'version'
                result=VERSION
                if scenario=='final_runtime_failure' and stage=='version':
                    result=result.replace('4.34.1','4.34.2')
            else:
                path=Path(command[-1]);name=path.name
                if name=='Audit.lean':
                    stage=clone_label(cwd)+'_axioms' if in_clone else 'axioms'
                    result='\n'.join("'"+n+"' does not depend on any axioms" for n in m['targets'])
                elif name=='Types.lean':
                    stage='elaborated-types';result='SYNTHETIC type response\n'
                elif name=='Inventory.lean':
                    stage=clone_label(cwd) if in_clone else 'inventory'
                    result=INVENTORY if stage in ('compiled_baseline','inventory') else injected_inventory(
                        module,stage,unrelated=scenario=='unrelated_injection_failure')
                    if scenario=='hidden_positive_axiom' and stage=='inventory':
                        result=result.replace('AXIOMS|','AXIOMS|'+enc(('Hidden','unapproved'))+',')
                elif path.stem in ('false_fold','false_power'):
                    stage=path.stem;returncode=1;result='SYNTHETIC Lean response: unsolved goals\n'
                elif path.stem in ('sorry','custom_imported','native'):
                    stage=path.stem
                    axiom={'sorry':'sorryAx','custom_imported':'hiddenPremise','native':'Lean.ofReduceBool'}[stage]
                    result="'injected' depends on axioms: ["+axiom+']\n'
                else:
                    raise RuntimeError('unexpected external command: '+repr(command))
            calls.append((stage,list(command),in_clone,returncode))
            return subprocess.CompletedProcess(command,returncode,stdout=result)

        def post_source(**kwargs):
            ensure(kwargs=={'expected_manifest_sha256':digest}, 'post-source guard lost expected manifest digest')
            postchecks.append('source')
            if scenario=='post_source_failure':
                raise ValueError('SYNTHETIC post-execution source mismatch')
            return m,digest

        expected_failures={
            'injection_prerequisite_failure':'unexpected process outcome: compiled_admission_build',
            'unrelated_injection_failure':'unexpected reason',
            'hidden_positive_axiom':'forbidden_axiom',
            'final_runtime_failure':'unexpected running Lean version',
            'post_source_failure':'post-execution source mismatch',
            'pre_git_failure':'preflight Git refusal',
            'post_git_failure':'final Git refusal',
        }
        captured=io.StringIO()
        # A late unqualified lookup must differ from the authenticated endpoint,
        # so replacing the receipt label with that lookup is observable.
        with patch.object(gate.subprocess,'run',side_effect=fake_run), \
             patch.object(gate.subprocess,'check_output',return_value='c'*40+'\n'), \
             patch.object(gate,'dependency_state',return_value=m['dependency_revisions']), \
             patch.object(gate,'source_check',side_effect=post_source), \
             patch.object(gate,'source_qualification',side_effect=qualify_source), \
             contextlib.redirect_stdout(captured):
            try:
                receipt=gate.execute(m,digest)
            except ValueError as error:
                ensure(scenario in expected_failures,'success scenario failed: '+str(error))
                ensure(expected_failures[scenario] in str(error),'wrong failure: '+str(error))
                ensure(not active.exists(),'failed execution retained or wrote active receipt')
                outcome='EXPECTED_FAILURE_WITHOUT_ACTIVE_RECEIPT'
            else:
                ensure(scenario=='success','failure scenario accepted')
                ensure(active.is_file(),'successful synthetic execution did not reach receipt write')
                ensure(receipt['inventory']['kernel_or_cbz_status']=='NOT_AWARDED','policy credit changed')
                ensure(set(receipt['inventory']['compiled_admission']['injections'])=={'compiled_admission','compiled_metaprogram'},'missing V2 control')
                ensure(set(receipt['negative_controls'])=={'false_fold','false_power','sorry','custom_imported','native'},'missing existing control')
                ensure(receipt['observations']['preflight']==receipt['observations']['final'],'runtime observation gap')
                ensure(source_observations==['preflight','final'],'missing source endpoint observation')
                ensure(receipt['source_identity']=={'preflight':source_identity,'final':source_identity},'source identity gap')
                ensure(receipt['checked_commit']==source_identity['checked_commit'] and
                       receipt['checked_tree']==source_identity['checked_tree'],'receipt uses an unqualified late identity')
                outcome='SYNTHETIC_V2_BRANCH_REACHED_ALL_SEVEN_CONTROLS'
        ensure(archive.read_text()=='preserve historical evidence\n','historical evidence changed')
        ensure(not (package/'.lake/determinant-compiled-admission').exists(),'disposable admission work leaked')
        if scenario=='injection_prerequisite_failure':
            ensure('SYNTHETIC intended prerequisite failure' in (active.parent/'compiled_admission_build.log').read_text(),'failure log lost')
        emit(scenario,outcome=outcome,stages=[c[0] for c in calls],logs_preserved=len(list(active.parent.glob('*.log'))),
             post_source_checked=bool(postchecks),external_responses='SYNTHETIC',lean_execution='NOT_RUN',
             persistent_receipt='NONE_DISPOSABLE_TEST_PACKAGE_ONLY')


def outer_adapter_revalidation():
    gate=load_gate()
    with tempfile.TemporaryDirectory(prefix='adapter-loader-') as directory:
        package=Path(directory)
        shutil.copyfile(INPUT/'determinant_inventory.py',package/'determinant_inventory.py')
        gate.ROOT=package
        m={'files':{'determinant_inventory.py':ADAPTER_SHA256}}
        loaded=gate.determinant_implementation(m)
        ensure(loaded.SCOPE=='DETERMINANT_ADMISSION_POLICY_ONLY_NOT_KERNEL_OR_CBZ_SUCCESS','adapter did not load')
        marker=package/'unauthenticated-executed'
        (package/'determinant_inventory.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+").write_text('executed')\n")
        try:
            gate.determinant_implementation(m)
        except ValueError as error:
            ensure('determinant adapter source hash mismatch' in str(error),'wrong adapter revalidation error')
        else:
            raise RuntimeError('cached adapter hid source mutation')
        ensure(not marker.exists(),'changed adapter executed before hash rejection')
        emit('outer_adapter_revalidation',source_change_refused=True,source_executed=False)


class V2ExecutionTests(unittest.TestCase):
    def test_v2_execution_reaches_both_compiled_and_five_proof_controls(self):
        execute_scenario('success')

    def test_v2_execution_failures_preserve_logs_without_active_receipt(self):
        for scenario in ('injection_prerequisite_failure', 'unrelated_injection_failure',
                         'hidden_positive_axiom', 'final_runtime_failure', 'post_source_failure',
                         'pre_git_failure', 'post_git_failure'):
            with self.subTest(scenario=scenario):
                execute_scenario(scenario)

    def test_adapter_loader_revalidates_after_a_source_change(self):
        outer_adapter_revalidation()


if __name__ == '__main__':
    unittest.main()
