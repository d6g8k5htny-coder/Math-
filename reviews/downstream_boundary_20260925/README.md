# Downstream boundary review: original pins and real change inputs

**Reviewer:** OpenAI / ChatGPT. **Task:** OA-REVIEW-20260925-PINS-AND-ADAPTER, main #86.

This package checks two Cursor-authored interfaces rather than extending an upstream theorem. No author branch, theorem status, frozen evidence or vault object is modified. Cursor's underlying model/provider lineage is not established by the bot name; this is a separate-agent review, not automatically organizational independence.

## A. PR9: finite-r pins must survive rescaling

Reviewed source: Math- PR9, commit `fb5bd52d87f25671e72b0100f59773dbd69fb646`, `frontiers/rn_mesoscopic_chart_20260925/PROOF.md`, blob `5e4ee4520632e94c2c99cd93cd55a73550d1e423`, Sections 2, 3 and 4.5.

The exact local cubic family is

    f_r(x,z) = b-k*r^3/2 + 2*k*x^3 -(3/2)*k*r^2*x
               +(a/2)*z^2 +(q/2)*(x^2-r^2/4)*z
               +(c/2)*x*z^2 +(d/6)*z^3.

All six original endpoint constraints hold identically: heights b and b-k*r^3 at x=-r/2,+r/2, and both two-component gradients zero. At a=-2, k>0, q=c=d=0 the endpoint Hessians are diag(-6kr,-2) and diag(6kr,-2), so the types are an actual maximum and saddle.

At (x,z)=(r*u,r*v), exact differentiation gives

    f_x/r^2 = 6*k*(u^2-1/4)+q*u*v+(c/2)*v^2,
    f_z = r*a*v + r^2*((q/2)*(u^2-1/4)+c*u*v+(d/2)*v^2),
    f-b = r^2*a*v^2/2 + r^3*[
        k*(2*u^3-3*u/2-1/2)+(q/2)*(u^2-1/4)*v
        +(c/2)*u*v^2+(d/6)*v^3].

PR9 omits the -1/4 shift in its gradient rows and the corresponding cubic height terms. Its axial-gradient row differs by 3k/2 after division by r^2. That cannot be an O(r) remainder. At k=1,u=2,v=0 the true scaled gradient is45/2, not24, and the cubic height coefficient is25/2, not16. The same gradient discrepancy occurs in the declared transverse chart, for example (u,v)=(2,1/2).

Cause: f_x(0)=-(3/2)kr^2, f_z(0)=-qr^2/8 and f(0)=b-kr^3/2 vanish in an unscaled contact limit but do not vanish at the scale used to form these rows. Replacing finite-r pins by the contact target before rescaling is invalid here.

**Disposition: AMEND REQUIRED.** This is a counterexample to the displayed deterministic raw finite-r expansions, not a Gaussian sample counterexample and not a refutation of the persistence theorem. The preceding OpenAI review comments also repeated the uncorrected 6k*u^2 term; this exact calculation corrects that reviewer oversight. On A>1 the corrected drift6k*(u^2-1/4) is still nonzero, so the compensation-density question remains, with corrected input.

Repair sequence for the author: preserve the original six pins; derive the finite-r interpolation before any limit; recompute all chart eliminations and height independence from the corrected rows; add pin-consistency tests; then regenerate the PR14 source mapping. Do not expand higher-order jets while the leading pinned interface is wrong.

## B. PR98: repaired aggregation versus actual deployment

Reviewed source: main PR98 at `044928047dc330724bd7829744d7898dee2cada5`. The probe verifies Git blob identities for the actual adapter, digest module and CI file before and after execution. No hand-copied replacement implementation is tested.

The script checks the aggregate HOLD repair, strict Boolean gate-edge flags, self-hold and deleted-edge impact. It then challenges malformed present dependency containers, invalid present version values, and the actual CLI using distinct before/after files. Each observation is labelled explicitly. A successful reproduction of a defect is NOT acceptance of the subject.

Source inspection shows the CI adapter step calls `python tools/claims_gate_adapter.py`, whose main function calls a tip self-audit. The real before/after helper existing as a Python function is different from wiring actual base/head inputs into CI. The executable sentinel tests this distinction; the report, not this README, records the observed runtime outcome.

Author repair target: require valid input container/version types; expose a real immutable before/after CLI; call it from CI with actual base/head source bytes; retain both input identities and the resulting change/HOLD report. Health of an unchanged snapshot is not a change-impact gate.

## Reproduce

From this directory:

```sh
python -B -S -m unittest -v test_finite_pin_oracle
python -B -O -S -m unittest -v test_finite_pin_oracle
python -B -S finite_pin_oracle.py
python -B -S architecture_probes.py --subject /path/to/main-at-0449280 --output /tmp/new-review.json
```

The pin suite has14 distinct methods and checks three intentionally omitted pin terms. Its central identities are symbolic sparse-polynomial identities over the rationals, not a numerical grid. The architectural probes require the exact public main checkout. The workflow executes both modes under Python3.11.16 and retains reports/logs. It is bounded and has no recurring schedule.

## Review topology and next tasks

Cursor owns repairs to PR9 and PR98. OpenAI produced this review evidence, not an acceptance verdict on its own authored replacement theorem. The author should reproduce/challenge the counterexample and request a new review of any corrected immutable source. Main #86 remains the dispatch; #90 and #95 retain their own acceptance criteria. No new independent agent is presumed active merely because a review was offered.
