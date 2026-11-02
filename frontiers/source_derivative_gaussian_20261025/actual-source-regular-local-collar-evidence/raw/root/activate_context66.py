"""Root initial context-only GO; exact adopted control copy reuses existing identity."""
import json
from datetime import datetime, timezone
from pathlib import Path
U=Path('/workspace/scratch/actual-source-regular-local-collar-publication')
P=Path('/workspace/scratch/actual-source-regular-local-collar-construct')
R=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
P.mkdir(exist_ok=True)
def put(p,x):
    with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
now=datetime.now(timezone.utc).isoformat()
docs=json.loads((U/'PRECODE66_IDENTITIES.json').read_text())['documents']
control=next(x for x in docs if Path(x['path']).name=='SOURCE_ACTUAL_REGULAR_LOCAL_COLLAR_CONTROLS.md')
raw=(R/'SOURCE_ACTUAL_REGULAR_LOCAL_COLLAR_CONTROLS.md').read_bytes()
assert len(raw)==control['bytes']==14724
with (P/'CONTROL_CONTRACT.md').open('xb') as f:f.write(raw)
put(U/'ROOT_CONTROL_CONTRACT66_COPY.json',{'status':'FULL_ADOPTED_CONTROLS66_EXACT_COPY_WITH_REUSED_FIRST_ID','observed_utc':now,'source':str(R/'SOURCE_ACTUAL_REGULAR_LOCAL_COLLAR_CONTROLS.md'),'destination':str(P/'CONTROL_CONTRACT.md'),'bytes':control['bytes'],'sha256':control['sha256'],'hashes_here':0,'old_mathematical_checks':0})
go={'status':'ROOT_GO66_INITIAL_RUNNER_AND_FULL_LITERAL_CONTEXT_ONLY','observed_utc':now,
    'creator':6482857252,'creator_native_utc':'2026-10-28T22:57:35Z','creator_full_body_match':True,
    'published_precode_head':'263b9d4329043e6debd299a8c27327ee515670d7',
    'postclaim_reconciliation':'Actual Math514/Main619 comment deltas contain only own claim/result/mirror; no new contender. Fresh Mathmain8151 and22openPR scope retained; new523 actual8paths disjoint. No duplicate old mathematical verification.',
    'producer':'/root/regular_collar_prospective','producer_personal_full_ten_doc_ACK':'2026-10-28T22:40:10Z',
    'allowed':'Only initial dedicated runner/outer/entry scripts and documentary bootstrap to freeze complete literal imports/instances/common definitions/typed physical and quotient interfaces/public theorem/ALL actual positive consumers/ordinary closed mutation and independent counterproof contract. Preserve initial originals and prospective full worker+outer+entry captures from FIRST important documentary invocation; cache necessary NEW IDs once and known-copy IDs reuse.',
    'proof_text_or_math_execution_allowed':False,
    'text_release_gate':'Root must personally FULL-read/accept complete literal context. Each optional helper must personally FULL-ACK that effective complete context before separate explicit TEXT release. No helper candidate/proof/fixture/ordinary/harness body or Lean/probe/check until authorized applicable gate.',
    'helper_max':1,'helper_scope_if_later_released':'ONE complete PRIVATE actual physical scalar-submersion adapter TEXT, zero executions/hashes/probes/objects. Producer owns quotient/O/inverse-ball/geometry/public assembly/ALL fixtures/ordinary/counterproof/amendments/executions; no extra ordinary author.',
    'controls_copy':str(U/'ROOT_CONTROL_CONTRACT66_COPY.json'),
    'mathematical_reuse':'Qualified earlier public interfaces and completed65 evidence reusable; no64/65 mathematical dependency and no private-body/fixture/ordinary copy or old object/check/hash campaigns.',
    'root_only':'Shared metadata/cache/Git/external/eligible own placement after actualcut. Producer only own new source/scratch when later released; all old/helper/ordinary/further objects SKIP.',
    'checkpoint':'2026-10-28T23:20:00Z','hard_terminal':'2026-10-29T03:30:00Z or invocationend whicheverfirst/noautoextension',
    'process':'OpenDraft/noReady/noMerge/samefamily0/scienceNONE/provider process separate/014KMath403STOP/no denial workaround/no foreign or Main seat',
    'global_goal':'ACTIVE_UNMET; continue beyond this unit'}
put(U/'ROOT_GO66_INITIAL_CONTEXT_ONLY.json',go)
print(json.dumps({'status':go['status'],'creator':go['creator'],'controls_bytes':len(raw),'control_copy_hashes':0,'observed_utc':now}))
