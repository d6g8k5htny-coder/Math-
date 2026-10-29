"""Replay saved native request/export/receipt bindings; no Lean is launched."""
import argparse
import json
from pathlib import Path
import sys
from runtime_support import HERE,ROOT,rt,require
sys.path.insert(0,str(ROOT/'integration/engine_audit'))
import catalog


def load(path): return json.loads(Path(path).read_text())
def equal(a,b): return catalog.canonical_json(a)==catalog.canonical_json(b)
def worker(path,controller_source_root=ROOT):
    events=[json.loads(line) for line in (path/'events.jsonl').read_text().splitlines()]
    starts=[e for e in events if e['event']=='request_started']
    done=[e for e in events if e['event']=='request_completed']
    require(not any(e['event']=='request_failed' for e in events),'passing worker has failed request')
    ids=[e['id'] for e in starts]
    require(ids==list(range(1,len(ids)+1)) and [e['id'] for e in done]==ids,'request journal coverage/order mismatch')
    require(all(type(e['id']) is int for e in starts+done),'noninteger request id')
    requests={e['id']:e['request'] for e in starts};responses={e['id']:e['response'] for e in done}
    raw=(path/'stdout.bin').read_bytes();receipt=load(path/'receipt.json')
    require(receipt['stdout_truncated'] is False and len(raw)==receipt['stdout_bytes'],'saved stdout incomplete')
    wire=[json.loads(row) for row in raw.splitlines()]
    require(wire[0]['event']=='ready' and equal(wire[1:],[e['response'] for e in done]),'journal responses differ from actual native stdout')
    require(equal({k:v for k,v in events[-1].items() if k!='event'},receipt)
            and events[-1]['event']=='worker_stopped','worker receipt differs from final journal event')
    require(receipt['reason']=='closed' and responses[ids[-1]]['status']=='stopped'
            and requests[ids[-1]]['op']=='shutdown','worker lacks acknowledged bounded shutdown')
    require(receipt['returncode']==0 and receipt['shutdown_acknowledged'] is True
            and receipt['forced_termination'] is False,'final native campaign has degraded teardown')
    require(events[0]['metadata']['new_transport_sha256']==rt._hash(controller_source_root/'integration/engine_audit/ul_engine/worker.py')
            and events[0]['metadata']['new_search_sha256']==rt._hash(controller_source_root/'integration/engine_audit/ul_engine/search.py'),'worker used different audited transport/search')
    active=set()
    for i in ids:
        req,res=requests[i],responses[i]
        require(req['id']==res['id']==i and req['session']==res['session']==receipt['session'],'session/id mismatch')
        if res['ok'] is True and req['op'] in ('open','attempt') and 'state' in res: active.add(res['state'])
        if res['ok'] is True and req['op']=='drop' and res['status']=='dropped':
            require(req['state'] in active,'drop without owned state');active.remove(req['state'])
    require(not active,'successful campaign left active handles')
    return requests,responses,receipt


def check(output=HERE/'evidence/session04', *, controller_source_root=ROOT):
    # This root is an explicit operator-trusted input, never inferred from the
    # campaign. Default checks bind current code and reject historical drift.
    controller_source_root=Path(controller_source_root).resolve()
    output=Path(output);campaign=load(output/'results.json')
    require(campaign['status']=='PASS' and campaign['training_eligible'] is False,'native campaign not passing/ineligible')
    for name,digest in campaign['controller_transport_sources_sha256'].items():
        require(rt._hash(catalog.file_at(controller_source_root,name))==digest,'controller/transport source drift')
    entries=catalog.verify_catalog()['endpoints'];wanted={e['id']:e for e in entries}
    tasks=load(HERE/'endpoint_tasks.json')['tasks']
    require(len(tasks)==len(wanted)==49 and {t['id'] for t in tasks}==set(wanted),'trusted endpoint coverage mismatch')
    for t in tasks:
        e=wanted[t['id']];short=e['target'].rsplit('.',1)[1]
        require(t['original_target']==e['target'] and t['original_theorem']==e['theorem']
                and t['wrapper']=='ClosedProof.Endpoints.reuse_'+short
                and t['task_constant']=='ClosedProof.Endpoints.'+short
                and t['generic'] is ('{X : Type}' in e['statement'])
                and t['action']=='reuse_'+short and t['training_eligible'] is False
                and t['source_exposed'] is True,'trusted task mapping drift')
    require(rt._hash(ROOT/'formal/Integration/EndpointTasks.lean')==load(HERE/'endpoint_tasks.json')['formal_source_sha256']
            ==rt._hash(HERE/'lean/Integration/EndpointTasks.lean'),'wrapper source binding drift')
    for r in campaign['records']:
        path=output/(r['mode']+'-controller')/'receipt.json';receipt=load(path)
        require(equal(r['receipt'],receipt) and receipt['succeeded'] is True,'controller receipt mismatch/failure')
        for stream,info in receipt['streams'].items():
            file=path.parent/stream
            require(file.stat().st_size==info['bytes'] and rt._hash(file)==info['sha256'],'controller stream drift')
    production=load(output/'produce/results.json');fresh=load(output/'recheck/results.json')
    require(production['status']==fresh['status']=='PASS','endpoint sessions not passing')
    require(len(production['records'])==len(fresh['records'])==49,'incomplete49 endpoint replay')
    produce_req,produce_res,produce_receipt=worker(output/'produce/worker',controller_source_root)
    verify_req,verify_res,verify_receipt=worker(output/'recheck/worker',controller_source_root)
    require(len(produce_req)==197 and len(verify_req)==53,'unexpected native request coverage')
    emitted={};seen=set()
    for row in production['records']:
        task=row['task'];require(task in wanted and task not in seen,'duplicate/unknown production task');seen.add(task)
        certificate=load(catalog.file_at(output/'produce',row['certificate']))
        require(rt._hash(output/'produce'/row['certificate'])==row['certificate_sha256'],'export certificate hash drift')
        opened=produce_req[row['open_id']];state=produce_res[row['open_id']]['state']
        attempted=produce_req[row['closed_id']];checked=produce_req[row['verify_id']];dropped=produce_req[row['drop_id']]
        require(opened['op']=='open' and opened['task']==task and attempted['op']=='attempt'
                and attempted['state']==state and attempted['action']==row['action']=='reuse_'+wanted[task]['target'].rsplit('.',1)[1],'wrong task/action/parent binding')
        require(produce_res[row['closed_id']]['status']=='closed' and equal(produce_res[row['closed_id']]['certificate'],certificate),'export differs from native closed certificate')
        require(checked['op']=='verify' and checked['task']==task and equal(checked['certificate'],certificate)
                and produce_res[row['verify_id']]['status']=='accepted','in-session verify payload mismatch')
        require(dropped['op']=='drop' and dropped['state']==state and produce_res[row['drop_id']]['status']=='dropped','missing state release')
        emitted[task]=certificate
    seen=set()
    for row in fresh['records']:
        task=row['task'];require(task in emitted and task not in seen,'duplicate/unknown fresh replay');seen.add(task)
        req=verify_req[row['request_id']];res=verify_res[row['request_id']]
        require(req['op']=='verify' and req['task']==task and equal(req['certificate'],emitted[task])
                and res['ok'] is True and res['status']=='accepted','fresh verify requested payload mismatch')
    require(seen==set(wanted),'fresh target coverage incomplete')
    require(set(fresh['negative_controls'])=={'wrong_target','open_forged_term','forbidden_axiom'},'negative control coverage incomplete')
    require({r['id'] for r in fresh['negative_controls'].values()}=={50,51,52},'negative controls reused or omitted actual requests')
    for label,response in fresh['negative_controls'].items():
        require(equal(response,verify_res[response['id']]) and response['ok'] is False
                and response['status']=='rejected','negative control not rejected')
        if label=='forbidden_axiom': require(response.get('reason')=='forbidden axiom','axiom control failed wrong gate')
    wrong=verify_req[fresh['negative_controls']['wrong_target']['id']]
    opened=verify_req[fresh['negative_controls']['open_forged_term']['id']]
    forbidden=verify_req[fresh['negative_controls']['forbidden_axiom']['id']]
    first,second=tasks[:2]
    require(wrong['task']==second['id'] and wrong['certificate']['task']==second['id']
            and equal(wrong['certificate']['type'],emitted[second['id']]['type'])
            and equal(wrong['certificate']['proof'],emitted[first['id']]['proof']),'wrong-target control payload mismatch')
    require(opened['task']==first['id'] and equal(opened['certificate']['proof'],
            {'schema':'ul-expr-dag-v1','nodes':[{'bvar':0}],'root':0}),'forged open-term control payload mismatch')
    require(forbidden['task']==first['id'] and forbidden['certificate']['axioms']==['sorryAx']
            and forbidden['certificate']['proof']['nodes'][0]['const']=={'str':[None,'sorryAx']},'forbidden-axiom control payload mismatch')
    budget=load(output/'budget/results.json');budget_req,budget_res,budget_receipt=worker(output/'budget/worker',controller_source_root)
    fresh_req,fresh_res,_=worker(output/'budget/fresh-worker',controller_source_root)
    require(budget['status']=='PASS' and budget['accepted_searches']==3
            and budget['stop_reason']=='request_capacity' and budget['remaining_before_shutdown']>=1,'budget phase missing successful cutoff')
    budget_coverage=set()
    require(sum(s['solved'] is True for s in budget['searches'])==budget['accepted_searches'],'budget accepted count differs from searches')
    for search in budget['searches']:
        require(search['cleanup_complete'] is True and search['unreleased_states']==[]
                and search['resources_after_cleanup']['worker_active_state_count']==0,'budget cleanup not confirmed')
        for event in search['journal']:
            if event['op']=='search': continue
            response=event.get('response',{});i=response.get('id')
            require(i not in budget_coverage,'budget request counted twice');budget_coverage.add(i)
            require(i in budget_req and equal(response,budget_res[i])
                    and all(equal(budget_req[i].get(k),v) for k,v in event['request'].items()),'budget journal differs from actual request/response')
    require(budget_coverage==set(budget_req)-{max(budget_req)},'budget journal omitted actual native requests')
    last=budget['searches'][-1]
    require(last['status']=='resource_exhausted' and last['termination_reason']=='request_capacity'
            and last['solved'] is False,'budget termination mislabeled')
    accepted_cert=next(s['certificate'] for s in reversed(budget['searches']) if s['solved'])
    require(equal(fresh_req[1]['certificate'],accepted_cert) and fresh_req[1]['task']=='logic_identity'
            and fresh_res[1]['status']=='accepted','budget proof not independently rechecked')
    return {'status':'PASS','native_endpoint_certificates':49,'fresh_endpoint_rechecks':49,
            'negative_controls':3,'live_request_capacity_guard':True,'kernel_executed_by_this_verifier':False,
            'training_eligible':False,'budget_worker_returncode':budget_receipt['returncode'],
            'controller_source_root':str(controller_source_root),
            'scope':'Saved request/stdout/export/receipt/source bindings; native acceptance evidence was produced earlier.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--campaign',type=Path,default=HERE/'evidence/session04')
    p.add_argument('--controller-source-root',type=Path,default=ROOT,
                   help='Operator-trusted source root for campaign controller pins; defaults to current code, not historical fallback')
    args=p.parse_args()
    print(json.dumps(check(args.campaign,controller_source_root=args.controller_source_root),indent=2))
