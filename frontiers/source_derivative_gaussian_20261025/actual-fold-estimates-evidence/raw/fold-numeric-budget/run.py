import subprocess,time,pathlib,json,sys,shutil,hashlib
p=pathlib.Path('/workspace/scratch/fold-numeric-budget'); name=sys.argv[1]; s=p/'runs'/name; s.mkdir()
src=p/'NumericBudget.lean'; shutil.copy2(src,s/src.name)
cmd=['lake','env','lean','-DwarningAsError=true',str(src)]
(s/'command.json').write_text(json.dumps({'cwd':'/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025','argv':cmd})); t=time.monotonic(); r=subprocess.run(cmd,cwd='/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025',text=True,capture_output=True); (s/'stdout').write_text(r.stdout); (s/'stderr').write_text(r.stderr); (s/'result.json').write_text(json.dumps({'exit':r.returncode,'seconds':time.monotonic()-t,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})); print(r.stdout,r.stderr); print((s/'result.json').read_text()); sys.exit(r.returncode)
