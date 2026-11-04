import datetime,difflib,hashlib,json,pathlib,shutil
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
path=BASE/'CONTEXT.md'; old=path.read_text()
new=old+'''
## Amendment004: sole closed assertion harness, no assumed mutation

The sole importing-only negative is a CLOSED assertion of the ordinary PUBLIC nonnegativeUpperMutation with NO mutation hypothesis, axiom, parameter, local assumed proof or supplied certificate. The independently passed negation rewrites the asserted proposition to the intended ONE unsolved False. Its COMPLETE planned literal text is:

```lean
import SaddleUppercutsControls

example : ActualSaddleUppercutsControls.nonnegativeUpperMutation := by
  rw [show ActualSaddleUppercutsControls.nonnegativeUpperMutation ↔ False from
    ⟨ActualSaddleUppercutsControls.nonnegativeUpperMutation_false, fun h => h.elim⟩]
```

The actual complete harness, FIRST identity and pre-run immutable snapshot are frozen BEFORE its exactly ONE invocation, AFTER ordinary strict PASS and its separate ALL-owned-ID/std3 inventory PASS. Expected exit1, ONE unsolved False, empty stderr. Earlier001 prose about applying negation to a false mutation premise is superseded by this exact no-premise assertion; all historical bytes remain immutable. No B geometry/header/interface, production theorem, mutation, positive/counterproof or verification-count change. No further speculative context changes.
'''
(BASE/'context/context-004.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='CONTEXT.003.md',tofile='CONTEXT.004.md')))
path.write_text(new); cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text()); st=path.stat()
row={'path':str(path),'bytes':st.st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'marker':[st.st_size,st.st_mtime_ns],'first_observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'origin':'new actual context004 identity calculated once'}
cache[str(path)]=row; dst=BASE/'context/CONTEXT.004.md'; shutil.copyfile(path,dst); st=dst.stat()
copied={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
 'origin':'known exact byte-copy identity reused','copied_from':str(path)}
cache[str(dst)]=copied
(BASE/'context/FIRST_ID.004.json').write_text(json.dumps({'context':row,'immutable_snapshot':copied,
 'patch':str(BASE/'context/context-004.patch'),'reason':'root/reviewer precise sole closed no-premise assertion harness binding'},indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n'); print(json.dumps(row))
