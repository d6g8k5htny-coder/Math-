"""Interactive controller; only native.py should launch it under the global lock."""
import argparse
import copy
import json
from pathlib import Path
import sys

from runtime_support import HERE,ROOT,validate_build,environment,require,rt
sys.path.insert(0,str(ROOT/'integration/engine_audit'))
from ul_engine.worker import LeanWorker
from ul_engine.search import CheckpointSearch


def write(path,value): path.write_text(json.dumps(value,indent=2)+'\n')
def name(value):
    answer=None
    for part in value.split('.'): answer={'str':[answer,part]}
    return answer

def worker(build,receipt_dir,*,max_requests=256):
    cfg,identities,manifest=validate_build(build)
    command=[sys.executable,'-B',str(HERE/'exec_guard.py'),*cfg.command()]
    return LeanWorker(command,receipt_dir=receipt_dir,timeout=20,startup_timeout=75,
                      max_lifetime=110,max_requests=max_requests,
                      env=environment(build,manifest['formal_cache']),
                      metadata={'runtime':identities,'guard_sha256':rt._hash(HERE/'exec_guard.py'),
                                'new_transport_sha256':rt._hash(ROOT/'integration/engine_audit/ul_engine/worker.py'),
                                'new_search_sha256':rt._hash(ROOT/'integration/engine_audit/ul_engine/search.py'),
                                'source_exposed':True,'training_eligible':False})

def accepted(response):
    require(response.get('ok') is True and response.get('status')=='accepted','independent verify rejected')

def produce(build,output,tasks):
    records=[]
    with worker(build,output/'worker') as w:
        require(set(t['id'] for t in tasks)<=set(w.ready['tasks']),'worker missing trusted endpoint')
        require(len(w.ready['tasks'])==57,'old8 or new49 task table incomplete')
        require(set(t['id'] for t in tasks)==set(w.ready['source_exposed_tasks'])
                and w.ready['training_eligible'] is False,'exposure metadata mismatch')
        for t in tasks:
            opened=w.request('open',task=t['id'])
            require(opened['ok'] is True and opened['status']=='opened','endpoint open failed')
            state=opened['state']
            closed=w.request('attempt',state=state,action=t['action'],heartbeat_limit=20000)
            require(closed['ok'] is True and closed['status']=='closed','endpoint fixed reuse action did not close: '+t['id'])
            cert=closed['certificate']
            require(cert['schema']=='ul-closed-proof-certificate-v2' and cert['task']==t['id'],'certificate target/schema mismatch')
            checked=w.request('verify',task=t['id'],certificate=cert);accepted(checked)
            dropped=w.request('drop',state=state)
            require(dropped['ok'] is True and dropped['status']=='dropped' and w.active_state_count==0,'endpoint cleanup failed')
            filename=t['id']+'.certificate.json';write(output/filename,cert)
            records.append({'task':t['id'],'action':t['action'],'certificate':filename,
                            'certificate_sha256':rt._hash(output/filename),
                            'open_id':opened['id'],'closed_id':closed['id'],'verify_id':checked['id'],'drop_id':dropped['id'],
                            'source_exposed':True,'training_eligible':False})
        requests_before_shutdown=256-w.remaining_requests
    return {'records':records,'certificates':len(records),'requests_before_shutdown':requests_before_shutdown,
            'cleanup_complete':True,'training_eligible':False}

def recheck(build,output,tasks,certificates):
    prior=json.loads((certificates/'results.json').read_text())
    require(prior['status']=='PASS' and len(prior['records'])==49,'missing production campaign')
    by_task={r['task']:r for r in prior['records']}
    require(set(by_task)==set(t['id'] for t in tasks),'production task coverage mismatch')
    certs={}
    records=[]
    with worker(build,output/'worker') as w:
        for t in tasks:
            row=by_task[t['id']];path=certificates/row['certificate']
            require(path.resolve().is_relative_to(certificates.resolve()) and rt._hash(path)==row['certificate_sha256'],'certificate export drift')
            cert=json.loads(path.read_text());certs[t['id']]=cert
            response=w.request('verify',task=t['id'],certificate=cert);accepted(response)
            records.append({'task':t['id'],'request_id':response['id'],'certificate_sha256':rt._hash(path),'accepted':True})
        first,second=tasks[:2]
        forged=copy.deepcopy(certs[first['id']]);forged['task']=second['id'];forged['type']=certs[second['id']]['type']
        wrong=w.request('verify',task=second['id'],certificate=forged)
        require(wrong['ok'] is False and wrong['status']=='rejected','wrong target proof admitted')
        forged=copy.deepcopy(certs[first['id']]);forged['proof']={'schema':'ul-expr-dag-v1','nodes':[{'bvar':0}],'root':0}
        opened=w.request('verify',task=first['id'],certificate=forged)
        require(opened['ok'] is False and opened['status']=='rejected','open forged proof admitted')
        forged=copy.deepcopy(certs[first['id']])
        forged['proof']={'schema':'ul-expr-dag-v1','nodes':[
            {'const':name('sorryAx'),'levels':[{'zero':None}]},copy.deepcopy(forged['type']),
            {'app':[0,1]},{'const':name('Bool.false'),'levels':[]},{'app':[2,3]}],'root':4}
        forged['axioms']=['sorryAx']
        forbidden=w.request('verify',task=first['id'],certificate=forged)
        require(forbidden['ok'] is False and forbidden['status']=='rejected'
                and forbidden.get('reason')=='forbidden axiom','forbidden sorryAx proof did not reach and fail axiom gate')
    return {'records':records,'fresh_rechecked':len(records),'negative_controls':{'wrong_target':wrong,'open_forged_term':opened,'forbidden_axiom':forbidden},'training_eligible':False}

def budget(build,output):
    results=[];last=None
    with worker(build,output/'worker',max_requests=32) as w:
        for _ in range(32):
            value=CheckpointSearch(w).solve('logic_identity',actions=['intro_all','all_assumption'],max_attempts=8,wall_budget=20)
            results.append(value)
            require(value['cleanup_complete'] is True and w.active_state_count==0,'budget search left unconfirmed handles')
            if value['status']=='resource_exhausted':
                require(value['termination_reason']=='request_capacity' and w.remaining_requests>=1,'request budget did not reserve shutdown')
                break
            require(value['solved'] is True and value['status']=='accepted','budget search failed before resource cutoff')
            last=value['certificate']
        else: raise ValueError('request capacity was not reached')
        remaining=w.remaining_requests
    require(last is not None,'budget campaign had no accepted certificate')
    with worker(build,output/'fresh-worker') as fresh:
        checked=fresh.request('verify',task='logic_identity',certificate=last);accepted(checked)
    return {'searches':results,'accepted_searches':sum(r['solved'] for r in results),
            'stop_reason':'request_capacity','remaining_before_shutdown':remaining,
            'cleanup_complete':True,'fresh_recheck':checked,'training_eligible':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['produce','recheck','budget'])
    p.add_argument('--build-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--certificates',type=Path)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    result={'schema':'ul-native-endpoint-session-v1','mode':a.mode,'status':'RUNNING','source_exposed':True,'training_eligible':False}
    tasks=json.loads((HERE/'endpoint_tasks.json').read_text())['tasks']
    try:
        data=produce(a.build_dir,a.output,tasks) if a.mode=='produce' else recheck(a.build_dir,a.output,tasks,a.certificates) if a.mode=='recheck' else budget(a.build_dir,a.output)
        result.update(data,status='PASS')
    except BaseException as exc:
        result.update(status='FAILED',error={'type':type(exc).__name__,'reason':str(exc)})
        raise
    finally: write(a.output/'results.json',result)
    print(json.dumps({'status':result['status'],'mode':a.mode}))

if __name__=='__main__': main()
