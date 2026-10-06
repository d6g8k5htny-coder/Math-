# D2: a sharper scalar lower floor without moment upper inputs

Object: D2-SHARP-SCALAR-PARTB-PUBLICATION-20261006-R5.
Scientific effect: NONE. Publication source review: PENDING.

Dylan Roy — delegated AI work. Publication and regression author: OpenAI /
GPT-6 Astra Pro, `canonical-r5-partb-source-publication-20261006`;
pickup Math-#328/6016272882. The original mathematical observation is by
OpenAI / GPT-6 Astra Pro, `round17-continuation-audit-20261005`, Part B of
[comment 6008747995](https://github.com/d6g8k5htny-coder/Math-/pull/328#issuecomment-6008747995),
created/updated 2026-10-06T03:29:55Z. This is its separate source publication,
not a new independent discovery or an amendment to either original packet.

The comment received a separate [PASS_SCOPED review 6016072968](https://github.com/d6g8k5htny-coder/Math-/pull/328#issuecomment-6016072968)
from OpenAI / GPT-6 Astra Pro, `canonical-r4-partb-scalar-review-20261006`,
on 2026-10-06T12:18:58Z. That review covers the exact comment argument,
not this new publication or regression file. The same conversation now
assembles this packet; no self-review or organizational independence is
claimed. A separate source-bound publication review is required.

## 1. Sources and non-duplication

Source A is #328's NOTE.md at commit
`31f7a6b5a36045be7795a6461da067a8ada96343`, path
`reviews/d2_two_atom_floors_20261006/NOTE.md`, blob
`cedbb44a237d1a158111dca81c30983f7efd37f1`, specifically section 5,
formula (5.1), its positive lower-input interface, and section 6's example.

Source B is `formal/ResearchFormalCoreR1/D2Schur.lean` at commit
`2f8b6f372be383d752e9dd30d38234faa977243c`, blob
`b95460c0d263a32ea274b347079cca6aaab3d2e9`. Its scalar definitions,
`d2_schur_ratio`, and `d2_det_interpolation` provide the correspondence.
All formulas used below are stated explicitly; no running import, pending
PR merge, or older CI outcome is a proof premise.

#326 remains the primary source for the common three moment floors under
its broader squared-radius mass premise. #328 is the individual-atom
companion with its original conservative upper-moment-free Schur bound.
The common moment floors and determinant/tau consequences are not counted
again. Neither source is replaced, edited, or globally superseded here.
The canonical crosswalk remains [6009510800](https://github.com/d6g8k5htny-coder/Math-/pull/328#issuecomment-6009510800).

## 2. Exact scalar proposition

Let x >= x0 > 0, g >= g0 > 0 and 0 <= t <= 1/4. Define

    D0 = x(g+x),       D1 = g(g+4x)/4,
    N = xg(g+2x),      D(t) = (1-4t)D0 + 4tD1,
    S(t) = N/D(t).

Then D(t)>0 and

    S(t) >= H(x0,g0)
         := min{g0(g0+2x0)/(g0+x0), 4x0(g0+2x0)/(g0+4x0)}
          >= min{g0, 2x0}.                                      (1)

For the original moment application use x=s^2 and x0=s0^2, with
s>=s0>0. In source B the substitution is m2=s, m4=g+s^2 and q=t.
Thus its numerator equals N and its determinant equals D(t); its Schur
ratio identity applies because the determinant has just been proved
positive. No moment upper bounds or probabilistic independence are used.
This proposition takes lower inputs as premises; it does not re-prove
or broaden the atom-integral argument supplying those inputs.

## 3. Proof with denominator and monotonicity directions explicit

Both D0 and D1 are positive. The interpolation weights are nonnegative
and sum to one, including at t=0 and t=1/4. Consequently

    0 < D(t) <= max(D0,D1),
    S(t) >= N/max(D0,D1) = min{F0(x,g),F1(x,g)},
    F0(x,g) = g(g+2x)/(g+x),
    F1(x,g) = 4x(g+2x)/(g+4x).

For X>=x>0 and G>=g>0, clearing the positive denominators gives

    F0(X,g)-F0(x,g) = g^2(X-x)/((g+X)(g+x)),
    F0(x,G)-F0(x,g) = (G-g)+x^2(G-g)/((G+x)(g+x)),
    F1(X,g)-F1(x,g) = 2(X-x)+2g^2(X-x)/((g+4X)(g+4x)),
    F1(x,G)-F1(x,g) = 8x^2(G-g)/((G+4x)(g+4x)).          (2)

Every denominator is positive and each increment is nonnegative.
Apply (2) one coordinate at a time to obtain Fi(x,g)>=Fi(x0,g0)
for i=0,1. Taking the minimum proves the first inequality in (1).
Finally,

    F0(x0,g0)-g0 = g0*x0/(g0+x0) > 0,
    F1(x0,g0)-2x0 = 2*x0*g0/(g0+4*x0) > 0,

which proves the last inequality in (1). At no point is an uncontrolled
quotient denominator replaced by a lower bound. This proof requires
neither joint attainment of the moment floors nor a new normalizer.

## 4. Example and scope limits

Source A's example gives s0=5/4, x0=25/16 and g0=9/8. Direct calculation
produces F0(x0,g0)=153/86 and F1(x0,g0)=425/118. Hence H=153/86,
with H/(9/8)=68/43. The example's actual g is 43/16, not g0. The
comparison uses lower inputs; the original conservative floor 9/8
remains correct.

The direction interval is essential. For (x,g,t)=(1,1,-1) or (1,4,1),
D(t)>0 but the asserted endpoint lower floor fails. Such directions are
outside the proposition. Strict positivity of x0,g0 is also retained.
No extension to singular inputs through total division is asserted.

The endpoint reduction is exact for fixed positive x,g. This packet
does NOT claim global sharpness over the original constrained moment
laws, a concrete periodic/Gaussian/Palm identification, a numerical field
certificate, an elder/capture/persistence consequence, or a family-uniform
positive floor without uniform caller inputs. It adds no Lean declaration,
kernel execution, independent statement alignment, or scientific acceptance.

## 5. Reproduction and source-review boundary

From the repository root:

```sh
python -B -S reviews/d2_sharp_scalar_floor_20261006/check_partb.py
python -B -O -S reviews/d2_sharp_scalar_floor_20261006/check_partb.py
python -B -S -m unittest discover -s tests -p test_d2_sharp_scalar_floor.py -v
python -B -O -S -m unittest discover -s tests -p test_d2_sharp_scalar_floor.py -v
```

The checker is byte-identical to the previous reviewer control script,
SHA256 `64047e54a8525cd890fcc0f400cd529a357537a901a5de792b49afb71cd669da`.
Here "independent" means no import from either original packet helper;
it does not mean an independent organization or a new review of this code.
Its ten exact polynomial coefficient identities and finite rational cases
supplement the continuum proof in section 3, not replace it.

The new five-method regression authenticates the note, checker and itself
against SOURCES.json; requires exact successful baseline bytes; checks all
six named wrong-formula reports, exact exit codes and empty stderr; and
separately checks invalid CLI calls. Invalid-argument tests check the usage
prefix and one of two exact error suffix spellings (plain or quoted choices),
not every intermediate usage-layout byte.
The six variants are explicit checker formula variants, not source edits
to either original packet. A hash establishes identity, not trust by itself.

Tests were first executed before the publication files existed and failed
with ten intended missing-checker/manifest assertions, zero test errors.
One initial assembled test falsely expected quoted argparse choices; actual
3.13.5 printed plain choices. Only the test presentation contract was corrected
to those two explicit spellings; the original failure is retained.
After assembly, local results and exact hosted outcomes are recorded on
the PR; this static source does not claim a future green run. Direct local
GitHub access failed DNS, so local checks use an authenticated file subset,
not a complete repository checkout or a local Lean build. Existing CI must
supply its own current-candidate results; no older receipt is rebound.

Any publication amendment, implementation, consolidation or changed
hypothesis must expose its exact source delta and applicable review.
The comment-level PASS is not automatically a PASS of these four files.
SOURCES.json preserves the original pending publication-review annotation;
subsequent reviews belong in source-bound PR records, not silent flag edits.
