Frozen full proof identity: **7657 UTF-8 bytes**, SHA256 `7198ff636e330749428ded6938776dad612f6bdb51ad62359b445f016df13a7a`, final newline included. Native pickup: [5965119121](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965119121).

# Designated maximin level equals the ordinary-superlevel H0 death

Object: C96-DESIGNATED-MAXIMIN-TO-H0-20261003-v1.
Author: OpenAI/Codex coordinating `/root` session, acting for Dylan Roy —
delegated AI work. Disposition: source-exposed author-side composition and
verified reproduction; nonauthor review pending. Personal reading PENDING;
organizational independence 0; scientific effect NONE.

This note supplies the explicit event-identification step deliberately left
outside C95. It proves the deterministic statement directly and then applies
it to C95's actual determinant-weighted event. The deterministic content is
already asserted in the pinned parent and public pairing-gap record; it is not
claimed as a new theorem.

## 0. Exact inputs and scope

- C95 proof: main issue 229 comment 5964938563, 16185 UTF-8 bytes,
  SHA256 `c0d9ee72352fafe91f96a8b6187c978f09ee3c187d5f4c7c2462c0187750d2e1`.
  Its G13--G18 define the actual maximin event and prove the weighted bounds.
- C95 fresh review: comment 5965062739. Its scoped PASS leaves this H0
  identification outside the reviewed C95 object.
- Parent [P]: `imports/lifetime_parent_20260925/
  UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, git blob
  `dfed3b8d318a3ab1950957f393307733a4bef3f2`, especially section 8.
  Its source-bound review is blob
  `bc11369c41ebc76de5700df3f931939ccfc88b9b`; the chain reconciliation is
  blob `75da2597971510f843f8d90c743950cb8c177342`. Both bind the same parent
  bytes, and the review records section 8 as previously accepted.
- Public cross-check: `incoming/grok-session-20260926-replay/
  PAIRING_IMPLICATION_GAP.md`, blob
  `47a71054ebe72588c2f9405292e575dababa84e4`, at main
  `3a896badf5404f7e9c98486af3859ee5d6c829d1`.

The parent already states that, on the Morse/distinct-critical-value locus,
its maximin equality expresses ordinary elder death. The proof below exposes
that implication in full at the exact convention consumed here. It does not
identify a gradient branch, require Morse--Smale transversality, prove an
all-bars/local-witness converse, or change any parent disposition.

## 1. Deterministic lemma

Let X be a compact connected smooth manifold and let f:X->R be Morse with
distinct critical values. For a local maximum M define

    d_f(M)=sup_{gamma(0)=M, f(gamma(1))>f(M)} min_t f(gamma(t)),       (D1)

where paths are continuous and the supremum of the empty family is minus
infinity. Let S be an index-(dim X-1) critical point with
f(S)<f(M). Then the following are equivalent:

1. d_f(M)=f(S).
2. In ordinary superlevel H0 persistence with the elder rule, the finite
   class born at M dies at S.

In either case M is not the global maximum, the bar endpoints are
`(f(S),f(M))`, and its lifetime is `f(M)-f(S)`. The statement concerns the
designated pair (M,S); it says nothing about gradient-flow adjacency.

### Proof

For a real level a write X_a={x:f(x)>=a}. Two points lie in the same path
component of X_a exactly when a path joining them has minimum at least a.
Consequently (D1) is the largest level, in the supremal sense, at which the
component issued from M can meet a point born strictly earlier, i.e. a point
x with f(x)>f(M).

Assume first d_f(M)=c:=f(S). For every a>c there is no path in X_a from M
to a point higher than M: such a path would make d_f(M)>=a. For every a<c,
the definition of the supremum supplies a path from M to some x with
f(x)>f(M) whose minimum is greater than a (otherwise c could not be the
supremum). Thus, while the superlevel decreases, the component born at M is
separate from every older component above c and is joined to an older
component immediately below c.

The superlevel component partition is locally constant on intervals that
contain no critical value. Hence c is a critical value at which that merge
occurs. Critical values are distinct, and S is the unique critical point at
level c. Therefore the merge occurs at S. Equivalently, for -f the
index-one handle attached there joins two previously distinct components;
it cannot be a handle whose ends lie in one component, because the preceding
component change is forced. The newly joined component contains a point of
height strictly greater than f(M), so its elder was born above M. The elder
rule therefore kills the class born at M, rather than the older class, at S.
The path family is nonempty because its supremum is the finite number c, so
M is not the global maximum and the class is finite.

Conversely, suppose the class born at M dies at S and put c=f(S). Before
the death, at every regular level a>c sufficiently close to c, the component
of M contains no older component. Hence no path from M to a point higher
than M can have minimum greater than c; otherwise the two components would
already have met above the declared death level. Thus d_f(M)<=c. Immediately
below c the merging component contains an older maximum, so for every regular
a<c sufficiently close to c there is a path in X_a from M to a point whose
height exceeds f(M). Therefore d_f(M)>=a for all such a, and letting a
increase to c gives d_f(M)>=c. Hence d_f(M)=f(S).

Using open superlevels instead of closed superlevels changes only endpoint
decoration. The numerical birth and death critical values, and therefore the
lifetime, are unchanged. QED.

## 2. Actual weighted C95 corollary

Use exactly the fixed planar finite-torus setting, pins, law Q_r, determinant
weight W_r, full normalizer Z_r and weighted law Q_r^W of C95. Let

    A_r={D_f(M_r)=f(S_r)}

be C95 G16's actual maximin event, and let

    H_r={the finite ordinary-superlevel H0 class born at M_r dies at S_r}.

On the support of Q_r^W, W_r>0 almost surely; hence M_r is a nondegenerate
maximum and S_r is a nondegenerate index-one saddle. Parent [P] section 8
proves that at each fixed r the pinned field is Q_r-almost surely Morse with
distinct critical values. Since Q_r^W is absolutely continuous with respect
to Q_r and 0<Z_r<infinity, the same locus has full Q_r^W measure.

On that locus the deterministic lemma applies. The higher-endpoint condition
is exactly the one built into C95 G13; if A_r holds then its path family is
nonempty because f(S_r) is finite. Thus

    1_{A_r}=1_{H_r}                 Q_r^W-almost surely.             (D2)

No branch-adjacency event is inserted into (D2). In particular no
Morse--Smale or no-saddle-connection hypothesis is needed.

Let E, m_E and z_0 be exactly C95's fixed bounded-soft-coordinate sector and
leading quantities. Substituting (D2) into C95 G16--G18 gives, uniformly in
the fixed compact birth heights and frames and for sufficiently small r,

    Q_r^W(E minus H_r) <= C r^(7/2),                               (D3)
    Q_r^W(E intersect H_r)=r^3 m_E/z_0+O(r^(7/2)),                 (D4)
    Q_r^W(H_r | E)=1-O(sqrt(r)).                                  (D5)

These are actual full-normalizer statements for the designated finite bar.
They are not an unconditional probability tending to one: E itself has mass
of order r^3. The constants retain C95's fixed-Lambda dependence.

## 3. Exact boundary

This closes only the deterministic/event-measurable translation of C95's
designated maximin pair into the corresponding finite ordinary-superlevel H0
bar. It does not prove that every small bar lies in E, the all-bars converse,
the rejected-side/chord estimate, shrinking multiple-witness collision,
intermediate/coarea composition, unbounded Lambda, all marks, another
dimension, or the global density/remainder theorem. The essential class is
excluded because D1 requires a strictly higher endpoint. Tests, source
identity and this publication do not supply human or organizationally
independent acceptance.
