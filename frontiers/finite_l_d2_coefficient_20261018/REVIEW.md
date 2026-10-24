# Substantive nonauthor review of the fixed d2 coefficient package

Disposition: **ACCEPT_SCOPED_MATHEMATICAL_CODE_CERTIFICATE** for the exact source/request commit `f47c8d77abf4d4eab67c15ca67c2e0cc450bff2c` and its original result carried unchanged with evidence in `08e9cb94043eb5ff88de2789731c58214bb6146a`. No blocking finding remains from this review. The original rational enclosure meets the frozen 1% engineering width target. This is bounds-only acceptance of C_alg(2,24), with scientific_acceptance=false.

Dylan Roy — delegated AI review; actual performer OpenAI/Codex `/root/d2_coefficient_review`, distinct source-exposed nonauthor. This is a fresh mathematical/source/code/certificate review and actual verification replay, not an author replay or summary-only review. I authored none of the implementation or its mathematical design. I read the plan and public method/d2 sources before implementation review. Root, the implementer and the source-group mathematical advisers supplied the disclosed design; I do not take their authorship or independence credit. Same-provider, organizational-independence0, blind0 and human0. Dylan's personal reading is PENDING and optional retrospective. No helpers were used.

Authority: prospective review offer Math193/6244840985; actual personal pickup Math193/6244846607 and Main419 pointer6244847853, both full-body native readback MATCH. I read the owner mandate, standing autonomy, current workflow and Math AGENTS. The implementation author retains all source/fix ownership. My snapshot, probes and report are private review artifacts; I made no edits to the author worktree, branch or source files and performed no target production rerun.

## Exact reviewed source and custody

Base: `c055af07b9a349db4bdc2acf2033e0f27b450605`. All20 initial source/request/test/development-evidence files are confined to `frontiers/finite_l_d2_coefficient_20261018/`. The final08e9 diff adds15 evidence files and changes none of the20 initial files. I examined the exact git diff and extracted both frozen commits, rather than treating mutable author worktree files as the candidate.

I read all new producer/checker/contract/test code, PROOF.md, README.md, SOURCE_MAP.json and REQUEST.json, the retained development failure and passing logs, final RESULT_SUMMARY, original receipts and complete author report. I personally read the public unchanged upstream producer/checker and relevant original-method formulas/normalization plus the final d2 precheck. The upstream files have exact published SHA256 identities:

- moment_kernel.py,12063B: `68c3caf28190e8be58464cabfc39ab565449d9bb64716ab139ac0dd0a181193e`.
- verify_certificate.py,10829B: `a0afbfdf9ca323db38e06171c138f683669c42fe99f6892d6233ab03802d4715`.
- REQUEST.json,581B: `2c27c93ab5e8c961ddc294d5348cb8d5e4625bcc5bbf9a611581659c9fc74178`.
- RESULT.json,2570059B: `ed7480564f748363f907bf32f69b2f2afb32f71b4f28d11b486ee9115cf417c7`.
- DELIVERY.json,6960B: `c6549b4ef081f422ac7fb1b870dca17c2fc694d13400979747608fe1820964ea`.

My review runner verified every one of the34 inventory members by byte count and hash, plus every original target/checker/normal-suite/optimized-suite stdout and stderr hash. The initial source commit is dated02:41:49UTC, before the original target receipt starts02:42:01.310421UTC and ends02:42:05.430221UTC. The command names f47c8d77, the pre-command status is clean, and the result hash matches the delivered bytes. The later evidence commit does not rebind that execution to changed code. Hashes establish identity; the original receipts carry the execution account, not a mathematical proof of runtime history.

The original source identity is f38c085ab5b15368e6989a1fd6298490f3b671f5a6c3a01bcdc81b516022bc33 and METHOD_V2 is32593B/8bdea4b42e9efd2d846cd1aa73691e8194fa26cd937ac02b79991334f88204f6. The reviewed public routes are Math193/6243041893, the d2 precheck at the end of6243050857, and upstream source6243879677. No private archive or competing method-publication package was acquired.

## Independent mathematical reconstruction

For d2 write a=mu2,b=mu4,c=mu6, e=(x,y), x²+y²=1 and t=x²y². The physical Hessian free-coordinate covariance is the2x2 block [[b,a²],[a²,b]] together with independent H12 variance a². Its determinant is a²(b²-a⁴). The linear map from(H11,H22,H12) to(He's two physical components,vᵀHv) has determinant of absolute value1; consequently block determinant division gives conditional transverse variance a²(b²-a⁴)/D(t). Its centered Gaussian negative-half squared moment is half the variance. The half is a Gaussian expectation factor, not pair counting.

Direct expansion gives D(t)=a²b+(b-3a²)(b+a²)t. Its endpoints are a²b and(b-a²)(b+3a²)/4. The odd regression decomposition gives V(t)=nu3(1-3t)+9a*beta*t, with beta=b-a² and nu3=c-b²/a. Its endpoints are nu3 and(nu3+9a*beta)/4. Thus the separate D/V endpoint hulls enclose the values for every angle, including anisotropic cases. Outward subtraction and positive lower-endpoint tests are necessary before divisions; both implementations perform them.

Starting with original M1 at d2 and substituting the conditional Gaussian moment gives the prefactor Gamma*a*(b²-a⁴)/(8*24^(1/3)*pi^(5/2)). Bounding the angular ratio pointwise and integrating the full angle multiplies by2pi. With H=(b-a²)(b+a²), the resulting bound has prefactor Gamma*a*H/(4*24^(1/3)*pi^(3/2)); taking the positive sixth power gives exactly Gamma⁶*a⁶*H⁶*V⁴/(4⁶*24²*pi⁹*D⁹). All numerator/denominator endpoint choices are in the outward direction. The constant24 here comes from the original collision expression, not an added physical-volume normalization. No cutoff field, zero-mode removal, common-height conditioning, extra L^-2 or role half enters.

The synthetic a=1,b=4,c=20 example has D=4+5t,V=4+15t. The sign of the derivative of log(V⁴/D⁹) is the sign of60/(4+15t)-45/(4+5t), which changes at t=4/25. Hence endpoint ratios alone miss an interior maximum. I independently tested that maximum and directly computed the Hessian covariance/Schur complement at e=(3/5,4/5), independently of the producer's scalar helper. These controls support the separate-hull construction rather than merely reproducing its code.

For Gamma, substitution u=s⁶ in its defining integral gives6∫s⁶e^-s⁶ ds. The derivative is6s⁵e^-s⁶(1-s⁶), so extrema occur at the prescribed endpoints on every cell, with the split exactly at1.4096 cells use4097 rational endpoints j/2048. The omitted transformed tail is∫64∞u^(1/6)e^-u du≤∫64∞u e^-u du=65e^-64. It is added once after the factor6 on the compact sum.

I independently reconstructed the aggregate Gamma bounds using a different sum identity: the lower endpoint sum contains every grid endpoint except the peak; the upper contains the interior endpoints and an additional peak, excluding the two boundary endpoints. This exactly matches the certificate's Gamma bounds after multiplication6/2048 and addition of the tail. The endpoint exponential witnesses themselves were replayed by the unchanged standalone primitive checker. The exact Gamma bracket also lies strictly between9/10 and1 as a broad secondary check.

The producer's integer search uses n⁶≤floor(x*2^576)<(n+1)⁶, which is equivalent to a lower dyadic root and an upper endpoint at most2^-96 away. The checker does not trust the search: it verifies nonnegative dyadic endpoints, the mesh and exact sixth-power inequalities. Positive sixth powers are strictly increasing, so this concludes the rational coefficient enclosure. No floating special-function/root arithmetic is part of this argument.

## Code, containment, IO and resource review

The moment kernel preserves the physical h=2pi/L, positive integer cutoff32, full-spectrum analytic remainder and common denominator including DC. Exact byte identity qualifies use of its existing reviewed containment logic; I also inspected that logic. The request remains bits96/pi_terms24/exp_pairs24/width_goal=null and UNASSIGNED_PARAMETER_INPUT. The new external task binding does not modify old role semantics.

The new verifier imports no coefficient producer. In a fresh reviewer process, importing verify_coefficient loaded neither coefficient nor moment_kernel; its producer-file read is for source hashing only. The verifier independently reconstructs the new scalar, Gamma, sixth-power and root computations, using the unchanged old checker to replay moments and exponential witnesses. Shared contract.py contains fixed requests, parsing, custody and budget checks but no scalar/Gamma/root numerical formula. This is disclosed software separation under a shared mathematical specification and Python trusted base, not organizational independence or a formally proved checker.

Canonical serialized request comparison rejects booleans/floats masquerading as integer settings, changed L/d/role/caps/goals and omitted or added settings. The top-level scientific_acceptance check uses identity with False. The source hash map and externally required expected source commit bind the checked result to the reviewed files and requested source identity. A user-supplied commit string alone is not evidence of historical execution; this limitation is correctly documented.

The coefficient parser has an8MiB input limit; the nested moment certificate retains its2MiB bound. Duplicate/nonfinite JSON, malformed/deep/invalid UTF8 input, noncanonical or oversized rationals, shape/type errors, false derived bounds and false status are rejected. Every Gamma primitive uses the unchanged limits3seconds/100000work/8192rationalbits/16squarings, with4097 calls below8192; a separate180second outer budget is added. No old cap is raised. The internal guards are cooperative; the original complete commands also carried external180second subprocess timeouts. This remains bounded conventional computation, not an OS isolation or hostile-service real-time guarantee.

The width calculation is exact and distinguishes valid wide bounds from target success. A valid synthetic width1/50 retains HOLD_TARGET_UNMET, and claiming TOLERANCE_MET for it is rejected. The certificate's call-count field establishes witness cardinality, not proof of execution history. Existing output creation uses O_EXCL and preserves existing files.

## Actual reviewer execution

All runs used my isolated frozen snapshot. The source producer was not rerun. Original author receipts separately record13/13 normal and13/13 optimized with no skips; those are author evidence, not my execution.

- Fresh standalone original-certificate CLI replay: exit0,4.289seconds, ACCEPT_BOUNDS_ONLY/TOLERANCE_MET, scientific_acceptance=false.
- Complete normal package suite: exit0,13/13, no skips,13.317seconds. Its full original-certificate and tamper checks executed.
-24 additional adverse controls all rejected: changed physical L; float dimension; changed kernel role; boolean cutoff; changed source commit; changed implementation hash; zero masquerading as false; invalid moment floor; altered scalar assertion; narrowed Gamma endpoint; sixfold Gamma tail; altered Gamma aggregate; narrowed sixth root; false target status; false relative width; boolean call count; duplicate, nonfinite, deep and invalid UTF8 JSON; oversized certificate; zero beta; zero nu3; and false success for a valid wide interval.
- Six additional rational/algebra checks passed: independent Gamma summation, broad Gamma bracket, direct Hessian determinant, direct Schur complement, interior-ratio maximum, and exact final positivity/width comparison. A valid wide synthetic interval also retained its HOLD outcome.

Reproducible reviewer artifacts: `reviewer-probes.py`, `reviewer-probes.stdout.txt`, `reviewer-probes.stderr.txt` and `reviewer-evidence/` under this private report's directory. The evidence directory contains original reviewer command stdout/stderr/receipts and `adverse-and-algebra.json`, including exact rejection reasons. No reviewer probe failed; stderr for the review runner is empty. No unchanged suite was rerun for a timestamp.

The development record is not rewritten: seven initial missing-behavior failures and the missing checker-width behavior failure are retained. The synthetic exp=1 Gamma test's former ordering assertion violated the decreasing-integrand hypothesis after1; correcting that fixture is justified and its failed log remains. The initial transferred extra LF was removed inertly before upstream execution, and exact final pins match. These are disclosed author history, not fresh reviewer-observed execution of the earlier failures.

## Accepted result and remaining boundary

Exact lower:2904569377252513601516770161/39614081257132168796771975168.
Exact upper:2911325955199780790291018331/39614081257132168796771975168.
Exact relative width:2252192649089062924749390/968189792417504533838923387≤1/100.

Secondary decimal display: approximately[0.07332163930293275,0.07349219930919443], width0.232619%. The rational comparison, not these displayed digits, establishes engineering success.

This review accepts only the explicit full-spectrum physical collision expression C_alg(2,24) under the stated conventional arithmetic/checker trust base. It supplies no ordinary-bar identification, G1–G4 closure, M31 effective remainder, finite-lifetime window, sampler/source-law/count transfer or tail, confidence/power/resource admission or scientific run. All original scientific HOLDs,14+113 failures and TA/TRIG remain. No field, sampler, driver, fit, Lean, CI/manual workflow, installation, security/settings/auth change, PR/ref/Ready/merge or foreign release occurred. Initial source author retains source/fix ownership; my review role may be released after this exact disposition is delivered.
