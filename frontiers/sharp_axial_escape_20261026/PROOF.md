# Sharp axial escape and a single sufficient lifetime moment

26 October 2026. Author: OpenAI/Codex, GPT-6, `/root`. Additive author-side
mathematical candidate; no independent scientific review or status promotion.
Source identities and consumption rules are in [SOURCES.json](SOURCES.json).

The predecessor's §2 proves escape under `rH<=3k`. Here the exact strict
threshold is `rH<24k`. The result is deterministic and needs no stochastic
conjecture. Its lifetime-moment application remains conditional on explicitly
listed source-law and clipped-moment inputs. Historical proofs are unchanged.

## 1. Deterministic theorem

Let `r,k>0`, `a=-r/2`, `c=r/2`, `e=3r/2`, and let `g` be real C4 on `[a,e]`.
Suppose

    g(a)=b, g(c)=b-kr^3, g'(a)=g'(c)=0.
    H=sup_[a,e] |g''''|, rho=rH/(24k).

If `rho<1`, the segment from `a` to `e` ends strictly above `b`, and its
minimum is exactly `g(c)`, attained only at `c`. More precisely, for
`t=(x-a)/r` in `[0,2]`,

    g(x)-g(c) >= kr^3 (t-1)^2 [1+2t-rho t^2],            (1)
    g(e)-b >= 4kr^3(1-rho)>0.                           (2)

For `rho<=1`, the bracket in (1) is at least 1 on `[0,2]`.

**Proof.** In the normalized coordinate the cubic Hermite interpolant is

    p(a+rt)=b+kr^3(2t^3-3t^2).

For any `x` distinct from the two pins, the fourth-order Hermite remainder
gives

    g(x)-p(x)=g''''(xi_x)(x-a)^2(x-c)^2/24               (3)

for some `xi_x` between the extreme nodes among `a,c,x`. This includes
extrapolation to `x>c`: subtract the appropriate multiple of
`(u-a)^2(u-c)^2` from `g(u)-p(u)`, which leaves double zeros at `a,c` and a
zero at `x`; repeated Rolle yields a zero of its fourth derivative.
At the pins the resulting bound holds by equality. All involved nodes lie
in `[a,e]`, so (3) implies

    g(a+rt) >= b+kr^3[2t^3-3t^2-rho t^2(t-1)^2].       (4)

Subtract `g(c)=b-kr^3` and factor to obtain (1). For `rho<=1`,

    1+2t-rho t^2 >= 1+2t-t^2 = 2-(t-1)^2 >= 1.

Thus `c` is the unique minimum even at the boundary `rho=1`.
Putting `t=2` in (4) gives (2), with strict escape when `rho<1`. QED.

## 2. Sharpness and the importance of strictness

Consider the actual polynomial

    g_rho(a+rt)=b+kr^3[2t^3-3t^2-rho t^2(t-1)^2].       (5)

It has the exact four pins, `rH=24rho k`, and physical second derivatives

    g_rho''(a)=-2kr(3+rho),
    g_rho''(c)=2kr(3-rho).

Hence both axial types are strict for `1<=rho<3`: maximum at `a`, minimum
at `c`. At `rho=1`,

    g_1(a+rt)=b-kr^3 t^2(t-2)^2 <= b                    (6)

for every real `t`. There is no strictly higher axial endpoint, even if
the allowed segment is extended. Thus `rH<=24k` cannot guarantee escape.
For `rho>1`, completing the square gives

    g_rho(a+rt)-b
      =-kr^3 t^2[rho(t-1-1/rho)^2+1-1/rho]<0           (7)

for every `t!=0`. This gives a unique global axial maximum at `a`, while
retaining both strict axial types when `rho<3`. For every proposed threshold
`C>24`, choose `1<rho<min(3,C/24)`; then `rH<Ck` but escape fails.
This proves optimality of 24 for this class of four-pin C4 data.

Adding `-eta|y|^2`, `eta>0`, supplies a local multidimensional maximum at
the first pin and an index `d-1` saddle at the second. This is a scalar/local
sharpness fixture, not a periodic Gaussian realization or a statement about
the probability of a field event. The existing fold-isolation proposal has
a different quartic saturating an endpoint cubic estimate at `24k/r`;
that example is prior related mathematics, not the proof of (1)-(7).

Why doubling the pin separation is optimal for this endpoint comparison:
at `t=T>3/2`, (4) certifies `g>b` if

    rho < (2T-3)/(T-1)^2
         = 1-(T-2)^2/(T-1)^2 <= 1.                    (8)

The maximum is exactly 1 at `T=2`. This observation does not replace the
counterexample, which rules out other arguments based only on these data.

### Boundary corollary when critical heights cannot tie

There is a useful distinction for an actual smooth field. Suppose the axial
segment is embedded, `M` is a critical point at height `b`, and no OTHER
critical point of the field has height `b`. Then `rH<=24k` suffices for a
path to a strictly older endpoint with minimum `f(S)`, allowing that path
to leave the axis after `e`.

Indeed (1)-(2) give the axial minimum and `f(e)>=b`. If `f(e)>b`, stop there.
If `f(e)=b`, the distinct point `e` cannot be critical. In a local chart a
direction with positive directional derivative gives a short segment from
`e` on which the value increases strictly above `b`. Append it to the axial
path; its values are at least `b`, so the minimum remains `f(S)`. No global
Morse lemma or stochastic assumption is needed for this argument. The scalar
counterexample (6) cannot disprove this corollary: it has two equal-height
critical maxima. This does not make the axial-only strict inequality weak,
or prove that the no-tie property holds under a particular conditioned law.

## 3. Lifetime-tail implication with one finite norm moment

Keep the predecessor's actual original pinned law `Q_r`, typed nonnegative
weight `W_r`, full normalizer `Z_r=E_Q W_r>0`, and law
`P_r=(W_r/Z_r)Q_r`. Keep `k>0`, dimension and geometry fixed. The segment
must be embedded in the source chart. Let `K=1+||f||_C4>=1`, with a fixed
coordinate-norm constant `D>0` such that every axial fourth derivative is
bounded by `D K`. Put

    A=24k/D, B_r={K>=A/r}.

Define the actual extended lifetime `X_r=(b-d_f(M))/(kr^3)`, the essential
event `E_r={d_f(M)=-infinity}`, and `C_r=min(X_r,1)`, with `C_r=1` on `E_r`.
The source's death definition is the supremum of path minima to strictly
older endpoints. Outside `B_r` the theorem supplies such a path with minimum
`f(S)`, hence

    E_r subset B_r,
    {finite death, X_r>1} subset B_r.                  (9)

This does not identify S as the actual elder partner. For finite deaths the
connected compact source domain supplies the original bound

    0<=X_r<=2K/(kr^3).                                (10)

Assume, for ONE finite exponent `s>0` and all sufficiently small `r`,

    Z_r/r^2 >= z_*>0,
    E_Q[(W_r/r^2) K^s] <= M_s<infinity.                (11)

Then `E_Pr K^s<=M_s/z_*=:L_s`. Weighted Markov, using the SAME weight
and full normalizer, gives

    P_r(E_r)<=L_s A^(-s) r^s.                         (12)

For `q>0` and `s>=q`, (9)-(11) give the explicit tail bound

    r^-3 E_Pr[X_r^q; finite death, X_r>1]
      <= (2/k)^q L_s A^(q-s) r^(s-4q-3).             (13)

Indeed on `B_r`, `K^q<=K^s(r/A)^(s-q)`; multiply this by the factor
`(2/k)^q r^(-3q-3)` from (10). No independence of the weight and norm is
used. Equation (13) is the complete calculation, including the extra `q`
lost in controlling the finite-death height by `K`.

Consequently `s>4q+3` is sufficient to make this tail `o(1)` and essential
mass `o(r^3)`. The all-order premise in the predecessor is unnecessary for
ONE fixed `q`; it remains useful to cover every `q` and every desired power
of remainder decay. In particular (13) gives `O(r^N)` if (11) is available
at `s>=4q+3+N`. At equality `s=4q+3`, it gives only `O(1)`.

## 4. Precisely what this removes from a moment-convergence argument

Let `F_r` denote actual pairing failure, with `E_r subset F_r`. Suppose
the original source's clipped-moment conclusions are available:

    r^-3 P_r(F_r)->a>0,
    r^-3 E_Pr[C_r^q;F_r]->m_q.                        (14)

For example these follow from the predecessor's specified marked-law
premises. If (11) holds for some `s>4q+3`, then

    r^-3 E_Pr[X_r^q;F_r,finite death]->m_q,
    E_Pr[X_r^q | F_r,finite death]->m_q/a.             (15)

The difference between the two unnormalized moment numerators is exactly

    E_Pr[X_r^q-1;F_r,finite death,X_r>1]-P_r(E_r).

After multiplication by `r^-3`, (12)-(13) make both terms vanish. Also
`r^-3 P_r(F_r,finite death)->a`, proving the conditional ratio.

This removes an independent uniform-integrability assumption, provided (11)
has actually been proved for the same source. It does NOT prove (11) or
(14), a failure coefficient, global elder identification, or an unconditional
Gaussian parent theorem. Essential-inclusive positive moments remain infinite
whenever the source's positive-probability essential event holds. Their
divergence cannot be repaired by an improved escape constant.

## 5. The finite-moment threshold cannot be weakened from these bounds alone

Fix any `q>0` and write `s_*=4q+3`. For sufficiently small `r`, take three
atoms under `P_r`:

| Atom | Probability | K | X | F |
|---|---|---|---|---|
| ordinary | `1-r^3-r^(s_*)` | 1 | 1 | false |
| regular failure | `r^3` | 1 | 1/2 | true |
| exceptional finite failure | `r^(s_*)` | `B/r` | `r^-4` | true |

Choose a fixed `B>=max(A,k/2,1)`. There is no essential atom. For small `r`,
(9)-(10) hold and `sup_r E K^s<=1+B^s` for every `0<s<=s_*`.
Set `Q_r=P_r`, `W_r=r^2`, `Z_r=r^2` to realize (11) literally.
Yet

    r^-3 P_r(F_r)=1+r^(4q)->1,
    r^-3 E[C_r^q;F_r]=2^(-q)+r^(4q)->2^(-q),
    r^-3 E[X_r^q;F_r]=2^(-q)+1.                       (16)

Thus even the endpoint moment `s=s_*` does not imply (15). The scaled
failure mark also converges weakly to mass one at `1/2`: the escaping atom
has scaled mass `r^(4q)->0`, so every bounded test has the same limit.
This is an ABSTRACT sharpness example for the listed probabilistic bounds,
not a Gaussian-field counterexample and not a necessity theorem for the
original source, which has additional structure and higher moments.

## 6. Remaining work

The deterministic theorem and the probabilistic implications above are full
author-side proofs. Finite exact controls support their algebra, not the
general C4 argument or scientific acceptance. Before project adoption the
packet needs scientific review by a different model family. Any parent
promotion additionally needs its exact source moment bounds, marked-law
inputs and controlling acceptance evidence. No `lemma_closed`, premise,
prize, register, historical review or source file is changed here.
