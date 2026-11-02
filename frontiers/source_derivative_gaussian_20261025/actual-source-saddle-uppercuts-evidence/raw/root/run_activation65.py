from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,hashlib,sys,traceback
p=Path(__file__).resolve().parent
t0=datetime.now(timezone.utc).isoformat()
cmd=["python3",str(p/"root_activate65.py")]
ids=[]
for name in ["ROOT_GO65_TEMPLATE.json","root_activate65.py","run_activation65.py"]:
 q=p/name;data=q.read_bytes();ids.append({"path":str(q),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"origin":"FIRSTnewactivationtemplate/scriptIDoncebeforeworker; nooldpayloadhash"})
(p/"GO65_RUNTIME_FIRST_IDS.json").write_text(json.dumps(ids,indent=2)+"\n")
workerstart=datetime.now(timezone.utc).isoformat()
r=subprocess.run(cmd,cwd="/workspace",capture_output=True)
workerend=datetime.now(timezone.utc).isoformat()
(p/"GO65_WORKER_001.stdout.txt").write_bytes(r.stdout)
(p/"GO65_WORKER_001.stderr.txt").write_bytes(r.stderr)
rec={"command":cmd,"cwd":"/workspace","started_utc":workerstart,"ended_utc":workerend,"exit_code":r.returncode,"stdout":str(p/"GO65_WORKER_001.stdout.txt"),"stderr":str(p/"GO65_WORKER_001.stderr.txt"),"scope":"Nonmathroot65completecontrols-copy/GOactivation; no Lean/probe/check"}
(p/"GO65_WORKER_001.json").write_text(json.dumps(rec,indent=2)+"\n")
print(r.stdout.decode(),end="");print(r.stderr.decode(),end="",file=sys.stderr)
outer={"command":["python3",str(Path(__file__).resolve())],"cwd":"/workspace","started_utc_observed_inside_process":t0,"ended_utc_observed_inside_process":datetime.now(timezone.utc).isoformat(),"exit_code":r.returncode,"worker_receipt":str(p/"GO65_WORKER_001.json"),"stdout":str(p/"GO65_OUTER_001.stdout.txt"),"stderr":str(p/"GO65_OUTER_001.stderr.txt"),"capture":"ProspectiveoriginalWORKERsplit plus OUTERdirectentryredirection; parentexternaltoolUTCnotclaimed"}
(p/"GO65_OUTER_001.json").write_text(json.dumps(outer,indent=2)+"\n")
sys.exit(r.returncode)
