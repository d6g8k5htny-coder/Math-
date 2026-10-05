# Scope erratum: the normalized cap bound is a compact-mark statement

**Object:** C7-NORMALIZED-SCOPE-ERRATUM-20261005-v1.  
**Date:** 2026-10-05. **Scientific effect: NONE** — no theorem promotion or
scientific-register change.  
**Actual author:** OpenAI / GPT-6 Astra Pro, session
`github-rules-and-closure-round3-20261005`, acting for Dylan Roy as delegated AI
work. This erratum does not change the attribution of the original Claude proof
or the independent audit. Organizational-independence credit: 0.

## Reading rule and exact source

Read [the retained original PROOF.md](PROOF.md) together with this erratum when
using its Section 3 **Remark (normalized form)**, lines 134–136 at the source
identified below. The original file remains byte-for-byte unchanged. Its
unrestricted-positive-`k` normalized reading is withdrawn by this correction;
the replacement is the compact-mark statement in the next section.

Source snapshot: Math- commit
`8fb6d41d201c7695cc23cfdd235f420be204a0c7`.

| Source at that commit | Git blob identity | Consumed slice |
|---|---|---|
| `frontiers/c7_total_bounded_20260929/PROOF.md` | `28748b086ec6761ef467dc67cba475fbdf8b7455` | Theorem K2; Section 3 normalized remark; Section 4's unnormalized assembly |
| `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `dfed3b8d318a3ab1950957f393307733a4bef3f2` | P Section 1, (5.4)–(5.5), and the cap implication in Sections 7–8 |
| `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` | `213594d6ca6a86fb938110f4d166d9ce275a02d0` | The existing mandatory reading correction for P Section 5 |

These are Git blob identifiers, not SHA-256 digests or proof certificates. The
parent's Section 5 is consumed **with its existing congruence erratum**, not with
the uncorrected displayed scaling factor.

## Exact replacement for the normalized remark

> **Remark (normalized form, compact marks only).** Fix `d >= 2`, `L > 0`, a
> nonempty compact birth set `B` in the real line, and a fixed gap interval
> `K = [k_-, k_+]` with `0 < k_- <= k_+ < infinity`. There are constants
> `r_* > 0` and `C_{B,K,d,L} < infinity`, which may depend on all these fixed
> choices, such that, for every `b in B`, every `k in K`, every orthogonal
> frame, and every `0 < r <= r_*`,
>
>     0 <= 1 - p_r <= Q_r^W(G_r^c) <= C_{B,K,d,L} (r/k)^3.
>
> Here `Q_r^W = (W_r/Z_r) Q_r` and `Z_r = E_Q W_r` are the actual typed
> weighted law and its full normalizer. This follows from K2 and the
> compact-parameter lower bound P (5.5), as detailed below. It does not assert
> a constant or radius uniform as `k_-` tends to zero or `k_+` tends to
> infinity. The condition `r <= c k` alone does not replace these compact-mark
> restrictions. Corollary T does not use this normalized remark.

## Derivation and all constant dependencies

Retain K2, with its original constants `C_K`, `N_K` and radius `r_0`, depending
on `d,L` only:

    E_Q[(W_r/r^2) 1_{G_r^c}]
        <= C_K (r^3/k) (1 + |b| + k)^{N_K},
        when 0 < r <= min(k, r_0).

By P (5.4)–(5.5), on the fixed compact set of birth marks, gap marks and frames
there are `z_* > 0` and `r_Z > 0` such that

    E_Q[W_r/r^2] = Z_r/r^2 >= z_*  for 0 < r <= r_Z.

This is a compact-set lower bound, **not** a globally uniform relative error
estimate. Its justification uses the continuity and strict positivity of the
contact cone moment, compactness of the parameters, and the parent's uniform
convergence on that compact set. The qualitative convergence supplies a radius;
no numerical value of that radius is claimed here.

Let `P_* = 1 + max_{b in B}|b| + k_+`, and choose

    r_* = min(r_0, r_Z, k_-, 1).

For every parameter in the replacement statement, K2 and the normalizer floor
both apply. Consequently

    Q_r^W(G_r^c)
      = E_Q[(W_r/r^2) 1_{G_r^c}] / E_Q[W_r/r^2]
      <= (C_K P_*^{N_K}/z_*) r^3/k
      =  (C_K P_*^{N_K}/z_*) k^2 (r/k)^3
      <= (C_K P_*^{N_K} k_+^2/z_*) (r/k)^3.

Thus one may take `C_{B,K,d,L} = C_K P_*^{N_K} k_+^2/z_*`. The lower-normalizer
direction and the upper-gap dependence are explicit. On the parent's generic
typed support the deterministic cap implies elder pairing, so
`1 - p_r <= Q_r^W(G_r^c)`. This uses the existing cap/mark interface; it is not a
new proof of that interface. No independence between `W_r` and `G_r` is assumed.

## Why the former unrestricted reading must not be used

[Audit IBA2-001 in main#259](https://github.com/d6g8k5htny-coder/main/issues/259)
identifies the false quantifier extension. Its exact-periodic example has
`d=2`, axial orientation, `b=0`, and `k(r)=r^(-2)`: the cap-failure probability
under the typed weighted law tends to one, whereas `(r/k)^3=r^9` tends to zero.
That analytic counterexample is the audit's work, not a new execution or
independent reconstruction claimed by this erratum. This erratum supplies the
replacement statement and the compact-window derivation above.

In particular, `z_0=(6k)^2 E[det(A_0)^2 1_{A_0<0}]` does not make the entire
coefficient independent of the marks or extend compact-parameter convergence
to an unbounded moving sequence of gap targets. Nor does a derivative identity
alone control the normalized expectation uniformly on such a sequence.

Cap failure is the failure of a **sufficient criterion**. It is not the same as
failure of elder pairing. The audit's counterexample does not assert that
`1-p_r` tends to one.

## Preserved results and review boundary

The all-mark **unnormalized** K1/K2 statements and their proofs are unchanged.
Corollary T's Section 4 continues to use the pin density multiplied by the
weighted numerator, K1/K2 with their target-growth factors, the actual lower
integration cutoff, and the near/far split. It does not divide by a uniform
all-mark normalizer. No new review or acceptance of that complete argument is
claimed here.

`PROOF.md`, `SOURCE_FILES.json`, `RESULTS.json`, `exponent_check.py`, all original
source pins, and every workflow and formal package file are retained unchanged.
The new README is a reading guide, not another scientific-status register.

Nonauthor review of this correction must check the compact quantifiers, the
normalizer division, the `k_+^2` factor and the original-source preservation.
Review and integration dispositions belong to the source-bound PR record;
this file itself does not award acceptance. The broader audit coverage items
in main#259 remain separate from the correction of IBA2-001.
