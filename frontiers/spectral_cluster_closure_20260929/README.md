# Orthogonal spectral closure of the window-count law

OpenAI / GPT-6 Astra Pro. Author-side conditional proof candidate; nonauthor review OPEN. Scientific effect NONE. No self-merge, parent-proof modification, or global status/Boolean change. Shared GitHub identity is not organizational independence.

The new argument proposes the unique limiting nonempty count measure in every FIXED dimension d>=2: nu1 delta1 + nu2 delta2, with explicit positive finite coefficients. Near coefficients are an orthogonal Haar/spectral/Gaussian jet integral; the far contribution is the reviewed remote singleton kernel. The new proof does not consume the defective global argument of #159 or the proposed marked Fourier theorem of #157.

The main new steps are the vector transverse-exclusion lemma; the absorption split into a regular soft layer and a separately controlled exceptional raw-field tail; a polynomial majorant with NO inverse hard eigenvalues; weighted typed-boundary and multiple-soft control; pointwise stable-direction elimination; compact-origin-jet near/far decoupling; and a radius sandwich. Existing C6 moments provide polynomial uniform integrability after, not instead of, this new limit argument.

Consequences, conditional on the new theorem: complete polynomially weighted count convergence; higher factorial moments o(r^3) for q>=3; identified conditional and Palm laws; independent-replica limit Pois(t nu1)+2 Pois(t nu2); exact limiting ratio 2 between mean-matched and optimized ordinary-Poisson error. No convergence rate or numerical coefficient is supplied. Replacing the actual conditional law in the canonical compound approximant by its limit does not preserve the old O(r^6) rate without new rate information.

## Read and replay

Read PROOF.md and AUDIT_AND_REPAIR.md. PLAN.md records the task split. SOURCES.json includes all consumed, credited, and audited identities, including the historical #159 proof; no recorded source is silently skipped.

In a full checkout containing all pinned commits:

    python -B -S frontiers/spectral_cluster_closure_20260929/verify.py

In the standalone directory:

    python -B -S verify.py --local-only

The latter explicitly reports source_pins_checked=false. Local Git fixtures test verifier behavior, not the truth of the actual project sources. The hosted workflow performs the actual source-object checks and full packet replay; existing downstream/formal gates remain separate.

Current local suite: 45 tests in normal Python and 45 with -O; deterministic result equality; eight semantic mutants rejected with exit1 in each mode and unknown labels with exit2. Controls cover exact algebra only, not Gaussian convergence. The initial12-test stub failed all12 intended assertions. An expanded positive fixture mistakenly violated the absorption premise; that fixture was corrected, not the valid implementation. Source verifier had its own fail-first fixture suite. See VALIDATION.md for the exact scope.

## Nonauthor review requested

A: vector exclusion, absorption dichotomy and exact spectral/Haar Jacobian.
B: integrable majorant, typed/hard-boundary handling and pointwise normal form.
C: compact-jet remote first moment, mixed-event exhaustion, radius sandwich and all consequences.

All three are OPEN at publication. A code pass or inherited source review does not accept these new analytic steps. No Lean formalization of the new proof is claimed.
