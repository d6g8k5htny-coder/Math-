# Review of the pinned SARD-G transfer and its admissible-law composition

Reviewer: OpenAI / ChatGPT, 29 September 2026.
Scientific effect NONE. This is a source-bound mathematical review and reading
record, not a scientific-status register or a new independence vote.

## Object, exact sources, and exposure

Reviewed object: Claude's CL-SARD-PINNED-TRANSFER-20260929-v1, clarified version v2,
`frontiers/sard_g_pinned_transfer_20260929/PROOF.md` at
`c460a8035994032e47dc464254d352c95c40ad36`, unchanged at selected integration head
`6fce8d2089478d0e46d9d79e148ce6b97e08d5a6`.
Its blob is `314e38c6f5f2bd78da79e423f30a341a3d45e22c`, 8912 bytes, SHA256
`6cef00efb0e4e3b0cc3a85a0f43468a22b7d2dba1525cd8489d45dfd375667bd`.

This records and completes review 5353818348 after the author's explicit scope
repairs in c460a803. It is the same OpenAI review lane, not a second independent
review. I authored the robust charts and corrected A2/localized-forcing inputs;
I check their use here and the NEW conditioning bridge, not independent truth of
my own inputs. Those inputs have actual Claude and Harper reviews. All models use
one GitHub account; organizational independence is not claimed.

**Verdict: ACCEPT Theorem P from its stated hypotheses, and ACCEPT Corollary R0
for each fixed admissible original pin law and its original determinant tilt,
with the complete reading rule below.** No numerical or regional C103 result is
accepted by this record. The unconditioned-to-conditioned step is not an
absolute-continuity argument.

## 1. The conditional covariance and the actual affine support

Write C for the original covariance operator and J for the finite list of values
and gradients at distinct sites P. The Gram matrix G=J C J* is positive definite:
a nonzero linear combination of distinct point-jet distributions cannot vanish
on every Fourier mode when every spectral weight is positive.

On the original Cameron-Martin space H define

    Pi = I - C J* G^{-1} J.

The reproducing identity shows that Pi is the H-orthogonal projection onto
H_P=H intersect ker J. Direct Gaussian regression gives the centered conditional
covariance C_P=Pi C. Its Cameron-Martin space is H_P with the inherited norm.
For every h in H_P and point evaluation ell_x,

    <h,C_P ell_x>_H = h(x).

If h is orthogonal to covariance images at a countable dense set of points,
continuity forces h=0. Thus those images have dense span in H_P. Normalize their
nonzero rational combinations using their ACTUAL conditional variance; zero
variance directions must be removed. The resulting scalar Gaussian coordinate
is independent of its residual by the Gaussian covariance identity. The smooth
deterministic mean belongs to that residual. Every slicing direction lies in
ker J, so the entire line stays in the correct affine pinned support.

No unconditional Fourier coordinate is incorrectly reused as an independent
coordinate after pinning. No nonzero-variance assumption at a pinned evaluation
is made: its conditional variance may be exactly zero.

## 2. Nonvanishing survives all pin constraints

The localized bump in #137 v2 is supported near a regular point of the connection,
away from both endpoint neighborhoods and the stable travel half. Its support can
also avoid any specified finite set of critical points, hence the pin sites.
The source first produces a compactly supported C2 potential. To match Theorem P's
smooth formulation literally, mollify inside a slightly larger compact set still
contained in that open support neighborhood. This gives smooth potentials
converging in C2, vanishing on a neighborhood of every pin. Continuity of the
mismatch derivative preserves its strictly nonzero value. No pin is perturbed
by this smoothing.

Choose trigonometric polynomials tau_n converging to one such smooth potential
phi in C2. Independence of the finite jet functionals implies that J maps the
union of finite trigonometric spaces ONTO its finite-dimensional target: otherwise
a nonzero target covector would annihilate every trigonometric polynomial and,
by C2 density, every C2 test, contradicting distinct-site jet independence.
Consequently finitely many trigonometric polynomials psi_i satisfy J psi_i=e_i.

    h_n = tau_n - sum_i (J tau_n)_i psi_i

lies in H_P and tends to phi in C2, because J phi=0. Thus L_f(h_n) tends to
L_f(phi), which is nonzero. Some element of H_P has nonzero derivative, and then
some member of the countable conditional covariance-image family does as well.
This finite correction is essential; unconditional density in H alone would not
establish nonvanishing on H_P. No estimate uniform in coalescing pin locations is
used or obtained from the finite right inverse.

## 3. Borel slicing on the conditioned law, then the tilt

Use #135's actual open robust chart domain and #137 v2's jointly Frechet C1
mismatch. For each fixed conditional direction h_l, the set

    {f in U_chi: D_chi(f)=0 and D D_chi(f)[h_l]!=0}

is Borel. For each fixed residual g, the valid parameters of g+t h_l form an
open subset of the line; the scalar mismatch is C1 there. Every counted zero
has nonzero derivative, so is isolated among zeros and belongs to a countable
set. Independence and Tonelli give zero probability under the PINNED law.
Countable chart/direction unions give a Borel null cover. The assumed generic
full-measure set supplies the connection coverage; the conclusion holds in the
completed probability space even without a separate Borel proof for the full
connection event.

The original pin law is singular relative to the unconditioned Gaussian law.
Only AFTER the preceding proof may one transfer to Q_r^W via its density W_r/Z_r
with respect to Q_r, with 0<Z_r<infinity. Using absolute continuity relative to
the unconditioned law would be invalid.

## 4. Precisely which genericity and parameter scope are consumed

For the general finite-pin theorem, Q(Omega_gen)=1 is an explicit hypothesis.
Equal forced critical values or other incompatible data can violate it. Theorem P
does not establish that hypothesis for arbitrary deterministic means.

For the original R0 two-pin law, the already reviewed D1 parent Section 8 proves
Morse critical points and distinct critical values at every fixed admissible
positive r. The source is
`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob
`dfed3b8d318a3ab1950957f393307733a4bef3f2`, SHA256
`9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7`.
Only its exact Section 8 genericity argument and normalizer premises are used for
this composition, not an unchecked global conditioning claim.

Admissible means distinct torus pin sites, positive gap k, and the original
parent's radius/covariance validity regime, or a separately proved extension.
For example r=L along an axis identifies the two torus sites, so unequal pinned
values would be impossible; that case is excluded. The result holds for EACH
fixed law, not on a common probability-one set for uncountably many targets.
There are no uniform quantitative constants as r tends to zero.

In dimension two a Morse gradient field without saddle-saddle connections is
Morse-Smale: f strictly increases on each nonstationary trajectory, excluding
cycles, and the other stable/unstable intersections are transverse by their
dimensions. This elementary planar step is not a three-dimensional theorem.

## 5. Other material in #138 and actual finite verification

Claude's Lemma J and reduced-use table are correct at their stated scope. The
citation-based alternate invariant-manifold proof is NOT independently verified
by this record and is NOT used to discharge A2. The explicit #137 v2 fixed-frame
bounded-trajectory proof supplies that premise instead. Its invalid C1-into-C1
predecessor remains withdrawn.

I reconstructed the exact published transfer_check.py through connector text,
checked its 5695-byte length, Git blob
`2a468a1f1400045a058713bb9ccb03f51c9b7aa6`, and SHA256
`62ec8f0cf6bf18eedd7b33068f9077f6ed2719b4dbd5a0a2ee1a1197b3aeabff`,
then executed it in both ordinary and optimized Python. All five baseline checks
passed; the three mutants failed the named pin-correction, covariance-projection
and pin-independence predicates. Four stdout pairs were byte-identical; every
stderr was empty and every result was valid JSON. This is a standalone finite
checker replay, NOT a local full-repository or full-manifest replay and NOT the
proof of Theorem P.

The full author/reviewer workflow executions must be established separately on
the combined integration commit. The original scalar Lean package does not
formalize these Gaussian or invariant-manifold proofs. No scientific register,
R0 Boolean, C103 estimate, RN/JETMOD condition or numerical constant is changed
by this review or by publication of its source.
