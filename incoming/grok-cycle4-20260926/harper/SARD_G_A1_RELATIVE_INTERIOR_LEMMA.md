# SARD-G A1 — relative-interior first-hit predicate

Date: 2026-09-26
Author-side packet: Harper cycle-4 (E)
Scientific effect: NONE.
This file freezes a standalone lemma that an external reviewer can apply to the existing author source. It does not edit the author source, does not flip A1 off AMEND, and does not accept A6.

Cited review (source of the AMEND, not replaced here):
`main/reviews/sard_g_successor_a1_a6_20260926/REVIEW.md` (2026-09-26).
Successor chart conditions as recorded there:

- Condition 1: `m_K(f) := min_K |grad f| > eta` (strict).
- Condition 2: declared local branches meet their local sections uniquely and transversely.
- Condition 3: branches remain inside the tube until their unique first crossing of `Sigma`.
- Condition 4: strict speed, angle, and travel-time inequalities.

The review records that neither condition 2 nor condition 3 states that the hit lies in the relative interior of the finite section, or assigns positive distance from its endpoints. Under the parent manuscript’s closed-section reading, a chart may contain a transverse endpoint hit and fail to be open.

## Lemma RI (robust first interior hit)

Let `Sigma = [a, b] := { (1-u) a + u b : 0 <= u <= 1 } subset R^2`, `a != b`, be a compact nondegenerate line segment (“finite section”). Write `partial Sigma := {a, b}` for its **endpoint set** (this is the boundary of `Sigma` relative to the line through `a` and `b`, not the topological boundary of `Sigma` in `R^2`, which would be all of `Sigma`), and `relint(Sigma) := Sigma \ {a, b} = { (1-u) a + u b : 0 < u < 1 }` for its relative interior. Let `n_Sigma` be a fixed unit normal to `Sigma`.
Let `T` be an open tubular neighborhood of an arc that contains `Sigma`.
Let `gamma : [0, t_max] -> R^2` be a `C^1` embedded arc (“branch”) with launch point `gamma(0) notin Sigma`.

A time `t_* in (0, t_max)` and point `x_* = gamma(t_*)` form a *robust first interior hit* of `Sigma` by `gamma` if all four hold:

**(RI1) Relative interior.** `x_* in relint(Sigma)`. Equivalently `dist(x_*, {a, b}) > 0`.

**(RI2) First contact with the closed segment, with terminal-time slack.**
`t_* = inf{ t in [0, t_max] : gamma(t) in Sigma }` and `t_* < t_max`.
In particular there is no earlier intersection with `Sigma`, no earlier tangent contact, and no earlier endpoint contact. The strict inequality `t_* < t_max` is needed for robustness: if the hit sat at the terminal time, a small perturbation could push the transverse crossing past `t_max` and leave no hit in `[0, t_max]`. If the branch is defined only up to its first hit, extend it by a positive time margin and state that margin.

**(RI3) Open-tube clearance of the compact travelled arc.**
The compact set `gamma([0, t_*])`, including launch and terminal points, lies in `T`. Compactness gives `dist(gamma([0, t_*]), partial T) > 0`. If a closed tube is used instead, the same strict positive clearance must be imposed as a hypothesis.

**(RI4) Transverse local uniqueness.** The normal speed at the hit is nonzero, `< gamma'(t_*), n_Sigma > != 0` (Euclidean inner product of the velocity with the unit normal `n_Sigma`), and `x_*` is the unique intersection of `gamma` with `Sigma` in some time neighborhood of `t_*`.

The same four items are required of every branch-label section used to name the chart, not only of the central section `Sigma`.

## Lemma OPEN (openness of a chart that uses only robust hits)

Let `U_chi` be the set of `C^2` fields (on the compact domain of the successor argument) for which a labeled chart `chi` is assembled from branches and sections that satisfy Condition 1, Condition 4, and Lemma RI at every declared hit, including branch-label sections.

Then `U_chi` is open in the `C^2` topology.

### Proof sketch (for the reviewer; not a substitute for writing it into the author source)

All four RI predicates are strict. In `C^1`, the flow of `grad f / |grad f|^2` (or the successor’s chosen unit-speed / gradient-ascent parametrization) depends continuously on `f` on any compact set where `min |grad f| > eta`.
Arrival time at a transverse interior point of a fixed segment is a `C^1` function of the field by the implicit-function theorem, because RI4 supplies a nonvanishing normal speed. Relative-interior distance, first-contact slack, terminal-time slack `t_* < t_max`, and tube clearance persist under small `C^1` perturbations. Condition 1 and Condition 4 are already strict and persist under small `C^2` perturbations. Hence a `C^2`-ball about any `f in U_chi` remains in `U_chi`.

## What the author source does not yet give

Applying Lemma OPEN to the written successor predicate requires the reviewer to check that Conditions 2–3 imply RI1–RI2. They do not, as written:

- “Unique first crossing of `Sigma`” can be read as a first hit of the closed segment at an endpoint.
- Unique transverse meeting of a local section can likewise be an endpoint meeting.
- Speed, angle, and travel-time bounds do not force positive distance to `partial Sigma`.

Until the author source states RI1–RI4 (or an equivalent open-section convention that also excludes earlier contact with the closed boundary), A1 remains AMEND. This file does not perform that edit.

## Analytic witness that the gap is not verbal

The review’s counterexample on the unit torus remains the external check:

```
F(x,y) = sin(2 pi x) (2 - cos(2 pi y)),
Sigma = {(1,y) : 0 <= y <= 1/200},
```

with vertical closed local sections of height `1/50` at `x in {73/100, 77/100, 123/100, 127/100}`.
Both tracked ascending branches first hit `Sigma` at the endpoint `(1,0)`, while Condition 1 and Condition 4 hold with slack. The vertical translate `F_eps(x,y) = F(x, y+eps)` converges to `F` in `C^2` and misses `Sigma`. Thus `F in U_chi` and `F_eps notin U_chi` under the closed-section reading of the written predicate, so that reading does not define an open chart.

Lemma RI excludes this `F` because RI1 fails. After the exclusion, the implicit-function argument of Lemma OPEN applies to the remaining fields.

## A6 boundary (recorded, not repaired)

The successor A6 slicing argument is conditionally valid on an open chart: once `U_chi` is open, `D_chi` is `C^1`, and `d D_chi[h_j] != 0` on the regular zero set, the scalar-section Tonelli argument produces a completed-measure zero set. That argument does not itself open `U_chi`. A6 therefore remains AMEND in its source application until A1 supplies an open-chart premise. No claim about A2–A5 is made here.

## Reviewer checklist

An external reviewer can close A1 by checking, against the author source and not against this note:

1. Every chart member’s first hit of its finite section is required to lie in the relative interior.
2. That hit is required to be the first contact with the *closed* section.
3. The same two items hold for branch-label sections.
4. Compact travelled arcs, including endpoints, lie in the open tube (or a closed tube with a written positive clearance).
5. The reference branch starts off the section and has positive finite travel time, with the first hit strictly before the terminal time of the declared branch interval.
6. With those predicates in the source, openness of `U_chi` follows by Lemma OPEN.

If any of 1–5 is still only inferred from speed/angle/time bounds, A1 stays AMEND.
