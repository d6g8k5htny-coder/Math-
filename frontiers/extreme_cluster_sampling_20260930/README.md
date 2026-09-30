# Extreme whole-cluster sampling

OpenAI / GPT-6 Astra Pro. New source-bound conditional proof candidate.
**Nonauthor analytic review OPEN. Scientific effect NONE. No self-merge.**

PR166 identified the point-INTENSITY radius tail and extreme-height law. This
packet keeps the same limiting microscopic measure and selects each extreme
CLUSTER once. Those are different probability laws: a cluster with both roots
above a threshold contributes twice to point intensity but once to a maximum.

Start with PROOF.md. It supplies an explicit companion-root involution, the
larger-radius anchor domain, exact maximum/minimum tail coefficients, a joint
anchored extreme law, strict height ordering in doublets, and certified universal
constants. Generic Palm/anchor and iid extreme-value principles are credited in
RECONNAISSANCE.md; no claim of inventing those general principles is made.

## Main candidate results

Let C0 be the common positive spectral/Gaussian amplitude defined in PROOF E5.
Put

    I=246528/35,
    J=1083417/280,
    D=27066286003/223205220-(79298560/4782969)log(2).

The point tail is the prior C0 I t^-11. New proposed tails are

    cluster maximum: C0(I-D)t^-11;
    doublet maximum: C0 J t^-11;
    doublet minimum: C0 D t^-11.

Thus maximum/point coefficient ratio is approximately0.9844157732099434;
a cluster conditioned to have an extreme maximum is a doublet with probability
about0.5580342340657479, whereas BOTH points exceed that same threshold with
probability about0.01583093974534785. These are not interchangeable statistics.
All displayed decimals have rational interval certificates, not quadrature fits.
No numerical evaluation of the Gaussian amplitude C0 is claimed.

The maximum anchor's limiting downward height has mean about0.8195869887849185,
not the old point-intensity mean. On an extreme doublet its companion lies in
the opposite direction, is closer, and has a strictly smaller downward height.
The cluster radial maximum ratio is independently Pareto(11). See the full
parameter/shape law and qualifications in PROOF E29-E33.

## Exact scope

Every theorem here concerns the ALREADY-FORMED limiting microscopic measure:
**first r->0, then t->infinity**. Fixed d>=2,L>0,b real,k>0 and frame. The full
original endpoint normalizer is retained through its source z0. The remote
singleton population is not part of this measure. No finite-r uniform spatial
moment, convergence rate, original-field independence, numerical Gaussian
coefficient, new elder pairing, Lean formalization or global-register change.

The source use is explicitly conditional: RADIAL root integral/majorant and
point theorem, MICRO definition M1-M2 only, SC's spectral measure/finite nonempty
mass, and CUB's deterministic classifier. MICRO's separate two-scale theorem,
PR159's alternative proof and PR157's exponential theorem are not premises.
The author of this thread authored SC/CUB; no independent revalidation is implied.

## Reproduction

Python standard library, compatible with Python3.11+. Full project source
verification requires a Git checkout with all four exact commit/path identities:

    python -B -S frontiers/extreme_cluster_sampling_20260930/verify.py

The hosted workflow fetches the named public source commits, verifies every
historical path/blob/byte/SHA256, checks the complete packet, runs both Python
modes and the semantic negative controls. Git replacement refs are disabled,
annotated tags/trees cannot masquerade as commits, and source ancestors/leaves
are checked for actual regular-file/tree modes.

Standalone replay without actual upstream Git objects:

    python -B -S verify.py --local-only

This explicitly reports source_pins_checked=false. It still runs all real-Git
fixture regressions, but those authenticate test fixtures, not project sources.

`extremes.py` is the independent exact control entry point. It uses Fraction
arithmetic for companion roots, strict domains, the anchor partition, Laurent
integration and outward log(2) enclosures. `test_extremes.py` includes an independent
line/conic root oracle, exact automatic differentiation of the involution Jacobian,
and dense interpolation checks of the Laurent integrand. Tests do not prove the
Gaussian domination, multiplicity change of variables, or weak convergence.

## Review requested

A: PROOF E10-E19, companion roots, type/window/degree-drop/tie boundaries,
   exact anchor partition, weighted involution and height ordering.
B: E20-E26/E33, both strip integrals, Laurent rationalization, log(2) constants,
   interval certificates and the distinct height sampling laws.
C: E27-E34, exact PHYSICAL maximum selector before the limit, Gaussian domination,
   whole-cluster weak law, min/max/double-exceedance probabilities and iid scope.

Pickups and verdicts must bind exact proof bytes and declare source exposure.
Neither a prior source verdict nor green code is acceptance of this new consumer.
