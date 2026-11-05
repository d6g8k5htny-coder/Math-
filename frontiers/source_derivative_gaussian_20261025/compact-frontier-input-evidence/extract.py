import pathlib, subprocess, hashlib, json, datetime
repo=pathlib.Path('/workspace/Math-curvature-20261026')
s=pathlib.Path('/workspace/scratch/reused-compact-frontier')
p=repo/'frontiers/source_derivative_gaussian_20261025'
pin='5f49444d13b9c322f5214e11bc3936b2271b615f'
rel='frontiers/cap_first_exit_lean_20261002/CapFirstExit.lean'
old=subprocess.check_output(['git','show',f'{pin}:{rel}'],cwd=repo)
assert old==(repo/rel).read_bytes()
start=old.index(b'/-- Frontier of a compact image.')
end=old.index(b'\nnamespace CapHyp',start)
extract=old[start:end]
statement_start=extract.index(b'theorem frontier_image_subset')
statement=extract[statement_start:]
proof=statement.split(b' := by\n',1)[1]
header=f'''/-
Reused compact-image frontier support. No new mathematical target.
Exact accepted origin: commit {pin}
path {rel}, lines 357-369.
Original namespace and implicit context are retained. Only this theorem is extracted;
Mathlib's umbrella import is replaced by one finite topology import.
Accepted proof bytes and source custody: /workspace/scratch/reused-compact-frontier/BINDINGS.json.
-/
import Mathlib.Topology.Separation.Hausdorff

open Set

namespace CapFirstExit

variable {{X : Type*}} [TopologicalSpace X]

'''.encode()
new=header+extract+b'\nend CapFirstExit\n'
target=p/'inputs/elder/ReusedCompactFrontier.lean'
assert not target.exists()
target.write_bytes(new)
(s/'accepted_theorem.lean.txt').write_bytes(extract)
(s/'accepted_proof_body.txt').write_bytes(proof)
sha=lambda b:hashlib.sha256(b).hexdigest()
newextract=new[new.index(b'/-- Frontier of a compact image.'):new.index(b'\nend CapFirstExit')]
assert extract==newextract
body={
 'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'origin_commit':pin,'origin_path':rel,
 'origin_blob_sha1':subprocess.check_output(['git','rev-parse',f'{pin}:{rel}'],cwd=repo,text=True).strip(),
 'origin_last_change_commit':subprocess.check_output(['git','log','-1','--format=%H',pin,'--',rel],cwd=repo,text=True).strip(),
 'origin_file_sha256':sha(old),'origin_file_bytes':len(old),
 'origin_worktree_equals_pinned_blob':True,
 'origin_declaration_lines':[359,369],
 'origin_exact_name':'CapFirstExit.frontier_image_subset',
 'origin_surrounding_context':['open Set unitInterval','namespace CapFirstExit','variable {X : Type*} [TopologicalSpace X]'],
 'successor_context_delta':'Dropped unused open unitInterval only; open Set, namespace and implicit variables retained exactly.',
 'extracted_documented_declaration_sha256':sha(extract),'extracted_documented_declaration_bytes':len(extract),
 'statement_and_proof_sha256':sha(statement),'proof_body_sha256':sha(proof),
 'exact_documented_declaration_comparison':extract==newextract,
 'source':str(target),'source_sha256':sha(new),'source_bytes':len(new),
 'old_imports':['Mathlib'],'new_imports':['Mathlib.Topology.Separation.Hausdorff'],
 'old_mathematical_evidence_reused':True,'new_research_target_credit':0,
 'new_obligation':'Strict compilation of extracted unchanged theorem in finite narrow-import environment only.',
 'binding_spec_commit':pin,
 'binding_spec_path':'frontiers/source_derivative_gaussian_20261025/SOURCE_ACTUAL_FOLD_TORUS.md',
 'binding_spec_sha256':sha((p/'SOURCE_ACTUAL_FOLD_TORUS.md').read_bytes()),
 'preflight_path':'/workspace/scratch/actual-fold-torus-elder-preflight/REPORT.md',
 'preflight_sha256':sha(pathlib.Path('/workspace/scratch/actual-fold-torus-elder-preflight/REPORT.md').read_bytes())}
(s/'BINDINGS.json').write_text(json.dumps(body,indent=2)+'\n')
print(json.dumps(body,indent=2))
