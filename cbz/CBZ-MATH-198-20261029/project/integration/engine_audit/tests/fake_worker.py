import json, os, sys, time
mode, session = sys.argv[1:]
def send(x):
    print(json.dumps(x), flush=True)
if mode == 'slowready': time.sleep(3)
if mode == 'badready':
    print('bad ready', flush=True); sys.exit(1)
send({'event':'ready','protocol':'ul-closed-proof-v1','session':session,'max_states':64,'tasks':[],'actions':[]})
if mode == 'blocked':
    time.sleep(10)
for line in sys.stdin:
    req = json.loads(line)
    if mode == 'latefault':
        if req['op'] == 'verify':
            result = {'protocol':'ul-closed-proof-v1','session':session,'id':req['id'],'ok':True,'status':'verified','padding':'x'*500}
            os.write(2, b'e'*500)
            send(result); continue
        os.write(2, b'late stderr marker')
        sys.stdout.write('{\"late fault marker\":'); sys.stdout.flush(); time.sleep(10)
    if mode == 'checktimeout' and 'timeout' in req:
        raise RuntimeError('timeout leaked to protocol')
    if mode == 'eof': break
    if mode == 'timeout':
        sys.stdout.write('{"partial":'); sys.stdout.flush(); time.sleep(10)
    if mode == 'malformed':
        print('not json', flush=True); continue
    if mode == 'oversize':
        print('x'*3000, flush=True); continue
    if mode == 'stderr':
        os.write(2, b'e'*200000)
    result = {'protocol':'ul-closed-proof-v1','session':session,'id':req['id'],'ok':True,'status':req['op']}
    if mode == 'wrongid': result['id'] += 1
    if mode == 'wrongsession': result['session'] = 'other'
    if req['op'] == 'open': result.update(status='opened',state='one' if mode == 'stringstate' else 1)
    if req['op'] == 'attempt': result.update(status='progress',state=2)
    if req['op'] == 'drop': result['status']='dropped'
    if req['op'] == 'shutdown': result['status'] = 'stopped'
    send(result)
    if req['op'] == 'shutdown':
        if mode == 'delayedexit': time.sleep(0.5)
        if mode == 'stubbornexit': time.sleep(10)
        break
