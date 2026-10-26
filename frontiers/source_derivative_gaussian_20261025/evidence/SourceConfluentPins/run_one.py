import hashlib,json,pathlib,subprocess,sys,time
p=pathlib.Path(__file__).parent
label=sys.argv[1]
source=pathlib.Path("SourceConfluentPins.lean")
sha=hashlib.sha256(source.read_bytes()).hexdigest()
if label=="kernel":
    cmd=["lake","env","leanchecker","SourceConfluentPins"]
else:
    cmd=["lake","env","lean",str(p/{"axioms":"AxiomAudit.lean","positive":"PositiveControls.lean","false-zero-inverse":"FalseZeroInverse.lean","false-zero-cubic":"FalseZeroCubicPin.lean"}[label])]
start=time.time()
r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(p/(label+".log")).write_bytes(r.stdout)
meta={"cwd":str(pathlib.Path.cwd()),"command":cmd,"exit_code":r.returncode,"duration_seconds":time.time()-start,"source_sha256_before":sha,"source_sha256_after":hashlib.sha256(source.read_bytes()).hexdigest()}
(p/(label+".json")).write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(meta))
print(r.stdout.decode(),end="")
raise SystemExit(r.returncode)
