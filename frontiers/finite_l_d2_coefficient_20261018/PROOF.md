# Original finite-L d2 collision expression: rational enclosure

Actual implementer: OpenAI/Codex `/root/d2_coefficient_implementation`.
Pickup Math193/6244794852 activates offer6244787399. Root and the source
group supplied mathematical design/sixth-power advice; this is disclosed
assistance, not final independent implementation review. Source exposure,
organizational/provider/blind/human independence credit: zero.

## Exact object and algebra

This package evaluates only the explicit original collision expression
C_alg(2,24), with physical derivatives, the complete infinite lattice
spectrum and the common full normalizer including the zero mode. It does
not evaluate a cutoff field, remove the spatial mean, condition on common
height or add a volume or pair-count factor. The original source hash is
f38c085ab5b15368e6989a1fd6298490f3b671f5a6c3a01bcdc81b516022bc33.
The accepted in-principle METHOD_V2 is 32593 bytes, SHA256
8bdea4b42e9efd2d846cd1aa73691e8194fa26cd937ac02b79991334f88204f6,
published Math193/6243041893. The independent d2 algebra precheck is at
the end of Math193/6243050857. Those sources are referenced, not republished
as a competing durable method package.

Let a=mu2, b=mu4, c=mu6. With t=e1^2 e2^2 in [0,1/4], the d2 precheck gives
D(t)=a^2*b+(b-3a^2)(b+a^2)t and
V(t)=c-b^2/a+3(b^2/a+3ab-3a^3-c)t. The conditional transverse Gaussian
has variance a^2(b^2-a^4)/D(t); its squared negative half-axis moment is
half that variance. The original full sphere is the full physical angle
of area2pi, not an average or hemisphere.

Set beta=b-a^2 and nu3=c-b^2/a. The affine endpoint values are
D0=a^2*b, Dq=beta*(b+3a^2)/4, V0=nu3,
Vq=(nu3+9a*beta)/4. Exact outward rational interval arithmetic computes
these values from independently verified moment intervals. Every moment,
beta, nu3 and D/V hull must have a strictly positive lower endpoint.
Failure means HOLD, never a midpoint positivity inference. Each true affine
value lies within the separate endpoint hull for every angle.

Separate hulls are essential: a=1,b=4,c=20 gives D=4+5t,V=4+15t.
The logarithmic derivative of V^4/D^9 vanishes at t=4/25 and changes
from positive to negative there. This interior maximum exceeds both ratio
endpoints. Endpoint ratios alone do not bound the angular integral.

The exact reduction before bounding is

    C_alg = Gamma(7/6)*a*(b^2-a^4)
            /(8*24^(1/3)*pi^(5/2))
            * integral_0^(2pi) V(t(theta))^(2/3)/D(t(theta))^(3/2) dtheta.

For every angle, independent positive D and V hulls bound the ratio by
V_lo^(2/3)/D_hi^(3/2) and V_hi^(2/3)/D_lo^(3/2). Integrating multiplies
by the full2pi. H=beta*(b+a^2)=b^2-a^4 is positive. Thus positive interval
endpoints can be raised to the sixth power using

    C_bound^6 = Gamma^6*a^6*H^6*V_bound^4
                /(4^6*24^2*pi^9*D_bound^9).

Use all lower positive numerator endpoints and upper denominator endpoints
for the lower bound, and conversely for the upper bound. This bounds the
whole angular integral; it is not a claim that the angular integrand is
constant. The final unit is physical length^-2 as in the original M1.

## Gamma and root witnesses

Substitution t=s^6 in the defining Gamma integral gives
Gamma(7/6)=6 integral_0^infinity s^6 exp(-s^6) ds. For g(s)=s^6 exp(-s^6),
g'(s)=6s^5 exp(-s^6)(1-s^6). Therefore g increases on[0,1] and decreases
on[1,2]. The frozen4096 equal cells have endpoints j/2048; endpoint2048
is exactly1. Both extremal endpoints of each cell are enclosed using the
unchanged exponential primitive at the exact rational (j/2048)^6. With
4097 shared endpoint witnesses, the new layer uses fewer than8192 calls.
Positive Darboux sums multiply by6/2048. No uncertain extremum or floating
quadrature is used.

The omitted Gamma tail is integral_64^infinity t^(1/6) exp(-t) dt.
Since t^(1/6)<=t there, integration gives at most65 exp(-64). This is
already the Gamma tail after substitution; it is added once, without an
extra factor6. The lower omitted tail is0. The final endpoint witness
at s=2 is also the exp(-64) witness.

Each positive sixth root uses absolute dyadic mesh2^-96. Producer integer
bisection finds n with n^6<=floor(x*2^576)<(n+1)^6. Hence n/2^96 is a
lower root endpoint and either the same exact root or(n+1)/2^96 is an
upper endpoint. The checker independently checks nonnegative dyadic
endpoints, width<=2^-96 and the exact rational sixth-power inequalities.
No library floating root or special function is trusted.

## Trusted computation and custody

The two unchanged moment files have their published full hashes in
SOURCE_MAP.json and contract.py. Their checker validates physical h=2pi/L,
full-spectrum moment tails on integer cutoffs and the shared full
normalizer. The frozen request retains its existing
UNASSIGNED_PARAMETER_INPUT semantics: no scientific target is assigned by
the kernel. The external task binds those general valid intervals to the
explicit fixed C_alg expression. That does not change the kernel schema.

New producer coefficient.py imports moment_kernel. New verifier
verify_coefficient.py never imports or executes coefficient.py. It uses
the unchanged verify_certificate module to verify the moment subcertificate
and exponential witnesses, and independently reconstructs Gamma sums,
scalar bounds, sixth-power bounds, roots and final width. contract.py is
shared trusted parsing, fixed configuration, custody and resource logic;
it contains no scalar/Gamma/root enclosure calculation. The programs share
the mathematical specification; this is software separation, not
organizational independence or a proof of Python/checker correctness.
The trusted base includes Python integer/Fraction semantics, bounded JSON,
the stated elementary identities and these actual checker sources.

The certificate carries SHA256 identities of the exact source/request/docs
files and the frozen source commit. Source hashes prove identity, not that
the recorded commit executed; original command receipts record that join.
The CLI checker requires the external expected source commit. It reads
the producer file only to hash it, never to import or execute it.

Certificate parsing is bounded to8MiB and forbids duplicate keys/nonfinite
constants. Rational strings are canonical and bounded3000characters/8192bits.
Every moment subcertificate is separately bounded2MiB and replayed within
the old checker caps. Original exponential calls preserve their3s,
100000work,8192bit and16squaring caps; no old cap is raised. Fresh old-checker
instances check each Gamma primitive, while a separate outer180s budget
and8192call cap govern the complete new invocation. Internal clocks are
cooperative checks between calls, not preemptive OS resource isolation.
Original receipts additionally invoke each complete command with an
external180s subprocess timeout. Bounded JSON parsing and Python integer
operations remain trusted stages, not a hostile-service real-time claim.

## Acceptance boundary

The frozen engineering goal is positive bounds with relative width at
most1/100, verified by exact rational comparison. A valid wider interval
is HOLD_TARGET_UNMET. The checker can accept valid bounds with that HOLD;
it never equates successful checking with meeting the target. Recorded
Gamma call count certifies witness cardinality, not execution history.

This deterministic enclosure has scientific_acceptance=false. It supplies
no ordinary-bar identification, G1–G4 closure, M31 effective remainder,
finite-lifetime window, count tail, sampler/input law, source-row closure,
power/confidence or resource admission. Original14+113 failures, all
scientific HOLDs, TA/TRIG and other owner scopes remain. No scientific
field, driver, sampler, Lean, CI/manual workflow or experiment runs here.
Final substantive nonauthor mathematical/code/certificate review remains
separate from author replay and from the earlier design advice.
