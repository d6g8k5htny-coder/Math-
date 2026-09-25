"""Run source-pinned adversarial probes against the real PR98 checkout.

A passed review probe can CONFIRM A DEFECT: see each recorded observation.
No source mutation, permission change, or mathematical promotion occurs.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SUBJECT_COMMIT='044928047dc330724bd7829744d7898dee2cada5'
BLOBS={
    'tools/claims_gate_adapter.py':'fbf376a15a862daf71b4b51fe14e234088c10b39',
    'tools/semantic_digest.py':'94f790288d7b00cf1b5ab2ac28bda0d0941bf89f',
    '.github/workflows/ci.yml':'61dce153618d08c3288d9ac1554b685f76ca0872',
}


def verify_sources(root):
    result={}
    for path, expected in BLOBS.items():
        p=root/path
        if p.is_symlink():
            raise RuntimeError('symlinked review subject')
        data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if actual!=expected:
            raise RuntimeError('wrong source identity: '+path)
        result[path]={'bytes':len(data),'git_blob_sha1':actual,'sha256':hashlib.sha256(data).hexdigest()}
    return result


def fixture():
    return {
        'as_of':'2026-09-25',
        'premises':{'P':{'status_frozen_v2_2':'OPEN','statement':'unreviewed premise'}},
        'claims':{'T':{'grade':'CANDIDATE','statement':'dependent claim','depends_on':['P']}},
    }


def run(root):
    before=verify_sources(root)
    spec=importlib.util.spec_from_file_location('reviewed_adapter',root/'tools/claims_gate_adapter.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('cannot load reviewed adapter')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    observations=[]
    def record(name, observation, passed, detail):
        observations.append({'case':name,'observation':observation,'review_probe_passed':bool(passed),'detail':detail})

    base=fixture()
    for status in ('OPEN','CLOSED'):
        doc=copy.deepcopy(base); doc['premises']['P']['status_frozen_v2_2']=status
        result=module.compare_claims_files(doc,copy.deepcopy(doc))
        record('aggregate_'+status,'REPAIR_CONFIRMED',
               'T' in result['hold_proposals'] and result['promotion_permission'] is False,
               {'hold_nodes':sorted(result['hold_proposals'])})

    graph=module.claims_to_gate_graph(base)
    strict=True
    for value in (0,1,'false',None):
        bad=copy.deepcopy(graph);bad['edges'][0]['required']=value
        try:
            module.validate_graph_fail_closed(bad)
        except module.AdapterError:
            pass
        else:
            strict=False
    record('strict_required_bool','REPAIR_CONFIRMED',strict,'invalid gate-edge flags refused')

    changed=copy.deepcopy(base);changed['claims']['T']['statement']='amended scientific content'
    result=module.compare_claims_files(base,changed)
    record('changed_node_self_hold','REPAIR_CONFIRMED',
           'T' in result['reverse_impact']['impacted'],result['reverse_impact']['impacted'])

    changed=copy.deepcopy(base);changed['claims']['T']['depends_on']=[]
    result=module.compare_claims_files(base,changed)
    record('deleted_dependency_edge','REPAIR_CONFIRMED',
           'T' in result['reverse_impact']['impacted'],result['reverse_impact']['impacted'])

    # These are malformed PRESENT fields, not an omitted optional field.
    accepted=[]
    for field in ('depends_on','sub_obligations'):
        for value in (False,0,'',{},None):
            doc=copy.deepcopy(base)
            doc['claims']['T'].pop('depends_on',None)
            doc['claims']['T'][field]=value
            try:
                projected=module.claims_to_gate_graph(doc)
            except Exception as exc:
                accepted.append({'field':field,'value':value,'rejected':type(exc).__name__})
            else:
                accepted.append({'field':field,'value':value,'accepted':True,
                                 'edge_count':len(projected['edges']),
                                 'hold_nodes':sorted(module.aggregate_hold_proposals(projected))})
    record('malformed_dependency_containers','DEFECT_REPRODUCED',
           any(row.get('accepted') and row.get('edge_count')==0 for row in accepted),accepted)

    accepted_versions=[]
    for value in (None,'',False,0):
        doc=copy.deepcopy(base);doc['as_of']=value
        try:
            module.claims_to_gate_graph(doc)
        except Exception as exc:
            accepted_versions.append({'value':value,'rejected':type(exc).__name__})
        else:
            accepted_versions.append({'value':value,'accepted':True})
    record('invalid_present_version','DEFECT_REPRODUCED',
           any(row.get('accepted') for row in accepted_versions),accepted_versions)

    # An executable end-to-end sentinel, not a simulation of the entry point.
    with tempfile.TemporaryDirectory(prefix='oa-pr98-review-') as temp:
        temp=Path(temp)
        old_path=temp/'before.json';new_path=temp/'after.json'
        old_path.write_text(json.dumps(base))
        altered=copy.deepcopy(base);altered['premises']['P']['statement']='different premise'
        new_path.write_text(json.dumps(altered))
        expected=module.compare_claims_files(base,altered)['reverse_impact']['impacted']
        proc=subprocess.run([sys.executable,'-B','-S',str(root/'tools/claims_gate_adapter.py'),
                             '--before',str(old_path),'--after',str(new_path)],
                            cwd=root,capture_output=True,text=True,timeout=30)
        try:
            actual=json.loads(proc.stdout)
        except json.JSONDecodeError:
            actual={}
        record('actual_cli_before_after_sentinel','DEPLOYMENT_GAP_REPRODUCED',
               proc.returncode==0 and actual.get('identity_impacted')==[] and bool(expected),
               {'returncode':proc.returncode,'expected_impacted':expected,
                'reported_identity_impacted':actual.get('identity_impacted'),
                'reported_meaning':actual.get('meaning'),
                'stderr':proc.stderr})

    workflow=(root/'.github/workflows/ci.yml').read_text()
    record('workflow_entrypoint','DEPLOYMENT_GAP_CONFIRMED_BY_SOURCE',
           'run: python tools/claims_gate_adapter.py' in workflow
           and '--before' not in workflow and '--after' not in workflow,
           'The explicit adapter step is a tip self-audit; no actual base/head arguments are passed.')
    after=verify_sources(root)
    if before!=after:
        raise RuntimeError('subject changed during review')
    return {'object':'OA-PR98-EXECUTABLE-REVIEW-20260925-v1','subject_commit':SUBJECT_COMMIT,
            'runtime':sys.version,'sources':before,'sources_unchanged':True,
            'all_review_probes_passed':all(x['review_probe_passed'] for x in observations),
            'observations':observations,'scientific_promotion':False,
            'meaning':'Confirmed repairs and reproduced remaining defects; passing probes are NOT subject acceptance.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--subject',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    root=args.subject.resolve();out=args.output.resolve()
    if out.exists() or out.is_relative_to(root):
        raise SystemExit('new output outside reviewed checkout required')
    report=run(root)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))
    raise SystemExit(0 if report['all_review_probes_passed'] else 1)
