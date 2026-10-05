# Exact all-direction envelope for the conditional cubic jet variance

Object: PERIODIC-TAU-ENVELOPE-20261005. Author: OpenAI / GPT-6 Astra Pro,
`periodic-tau-envelope-20261005`, continuing `lean-custody-round6-20261005`.
Dylan Roy — delegated AI work. Scientific effect: **NONE**.
Author-side mathematical contribution; nonauthor review pending at publication.
This is not a Lean certificate or an independent re-audit of the input packet.

## 1. Input and the specific gap addressed

Math-#297 computes exact-periodic covariance tensors, then samples directions.
Its corrected source at `d8be92076dae46f9504d279b286da0432d01e088` uses the product
spectral cumulants to compute `tau2 = Var(t_u) - c_tG Cov(G)^{-1} c_Gt`.
The moment/sign reconstruction in #297 comment6001649072 gives

    tau(u)^2 = 6 a^3 + 9 a b sum_i u_i^4 + (c - b^2/a) sum_i u_i^6,       (1)

where a=kappa_2>0, b=kappa_4, c=kappa_6, and sum_i u_i^2=1.
Here tau(u)^2 denotes a variance, not its square root. The notation `b` in this
report is a spectral cumulant, not the research program's birth-level mark.

The result below makes the all-direction extrema of this ONE invariant exact:
only d scalar values need be considered. It does not bound the other invariants
in #297's maximum, the coefficient quadrature, or the error in numerical cumulants.
The separate Frobenius-trace correction PJ-A-001 is not reopened here.

## 2. Algebraic extremum theorem

**Theorem T1.** Let d>=1 be an integer and A,B arbitrary real numbers. On the
closed simplex Delta_d={x_i>=0, sum_i x_i=1}, define

    F(x) = A sum_i x_i^2 + B sum_i x_i^3.

Then

    min_Delta F = min_{1<=m<=d} (A/m + B/m^2),
    max_Delta F = max_{1<=m<=d} (A/m + B/m^2).                         (2)

Every listed value is attained: choose m coordinates equal to 1/m and the
remaining coordinates zero. Thus (2) is an exact range endpoint formula, not
merely a bound. There may also be nonuniform maximizers/minimizers in degenerate
cases; the theorem does not claim to enumerate every extremizing vector.

### Proof, including boundary and degenerate cases

F is continuous on the compact simplex, so it has a minimum and maximum. Take
any one of these points and restrict to the face formed by its positive
coordinates. It is a relative-interior extremum of that face. Let m be its
support size. For m=1 the claimed value is A+B. For m>=2, tangent first
variations give one common number lambda with

    2 A x_i + 3 B x_i^2 = lambda                                     (3)

for every positive coordinate. Tangent second variations of the diagonal
Hessian diag(2A+6Bx_i) must be nonpositive at a maximum and nonnegative at a
minimum. Variations used below are supported on the positive coordinates and
have sum zero, so both signs of sufficiently small displacement stay in the face.

If A=B=0 the statement is immediate. If B=0 and A!=0, (3) forces all positive
coordinates equal, hence x_i=1/m. Now suppose B!=0. Equation (3) is quadratic:
there can be at most two distinct positive values. One value again means 1/m.
For two distinct values s<t, subtract (3) to obtain

    2A+3B(s+t)=0.

The two corresponding Hessian entries are

    h_s=3B(s-t),  h_t=3B(t-s)=-h_s.                                 (4)

They are opposite nonzero numbers, of equal magnitude h>0.

At a local MAXIMUM the group with Hessian entry +h cannot contain two
coordinates: varying these two by +epsilon and -epsilon gives positive second
variation 2h. Therefore that group has exactly one coordinate. If the support
has m>=3, the other group has n=m-1>=2 coordinates, all with entry -h. Use the
tangent vector whose single +h coordinate is -n and whose n other coordinates
are all +1. Its second variation is

    h n^2 - h n = h n(n-1) > 0,

again impossible at a maximum. At a local MINIMUM the group with entry -h must
have one coordinate; the analogous tangent vector has second variation
-h n(n-1)<0, likewise impossible. This argument handles either sign of B.

The remaining unequal two-value case is m=2. Then s+t=1, so 2A+3B=0, and on
that entire edge

    A(s^2+t^2)+B(s^3+t^3) = A+B-(2A+3B)st = A+B.

Its value is also attained at a vertex and at the equal two-support point.
Thus an extremal value is always one of the d equal-support values. Since each
listed value actually occurs in the simplex, both equalities in (2) follow.
No hypothesis on the signs or nonvanishing of A and B was suppressed. QED.

## 3. Conditional variance corollary and its input derivation

Assume the centered stationary Gaussian field's spectral law has independent,
identically distributed symmetric coordinates with finite sixth moment. Write
a>0 for their variance and b,c for fourth and sixth cumulants. At a fixed point,
let G be the full gradient and t_u the third directional derivative. All
assertions here concern this displayed covariance structure; no construction of
a particular Gaussian field or Palm law is being supplied.

For Y=sum_i u_i xi_i and a unit vector u, the even-block moment expansion gives

    E[Y^6] = 15a^3 + 15ab sum_i u_i^4 + c sum_i u_i^6,
    E[Y^3 xi_i] = 3a^2 u_i + b u_i^3.

The gradient covariance is aI. The stationary derivative sign makes Cov(t_u,G_i)
the negative of the second expression, but the sign disappears on squaring.
Consequently the Schur subtraction is

    (1/a) sum_i (3a^2 u_i + b u_i^3)^2
      = 9a^3 + 6ab sum_i u_i^4 + (b^2/a) sum_i u_i^6.

Subtracting proves (1). For jointly Gaussian derivatives this Schur complement
is the conditional variance given G=0; it conditions on the FULL gradient,
not just its component parallel to u.

**Corollary T2.** Under these input conditions, put

    v_m = 6a^3 + 9ab/m + (c-b^2/a)/m^2,     1<=m<=d.

Then min over unit u of tau(u)^2 is min_m v_m, and max is max_m v_m.
Indeed x_i=u_i^2 maps the unit sphere ONTO Delta_d, and T1 applies. Each value
v_m occurs at a direction with m nonzero coordinates of magnitude 1/sqrt(m),
with arbitrary signs and coordinate permutations. This is exact for the actual
real cumulants, not a declaration that rounded input values equal those cumulants.

When v_1>0, the maximum absolute relative deviation from the axis value is

    max_m |v_m/v_1 - 1|.                                            (5)

Thus the direction sets listed by #297 for d=2,3,4 already contain a representative
of every needed support size for THIS invariant. No angular grid refinement is
needed to maximize tau(u)^2 under the product-cumulant model. One must still
control numerical parameter error before reporting a certified numerical bound.

The support sequence also has the exact adjacent-difference identity, with
A=9ab and B=c-b^2/a:

    v_m-v_{m+1} = [A m(m+1)+B(2m+1)]/[m^2(m+1)^2].                  (6)

Do not compare only the axis and full diagonal: with d=3, A=1, B=-1, the maximum
is 1/4 at support m=2, larger than the axis value 0 and full-diagonal value 2/9.
This polynomial example is a control, not an assertion of Gaussian realization.

## 4. Verification and falsification controls

`envelope_check.py` evaluates (2) and T2 exactly on rational inputs, rejecting
floats rather than silently treating a binary approximation as a certified input.
A rational or decimal string means its exact encoded value only. The arbitrary
real theorem is proved above, not established by finite sampling.

`test_envelope.py` has 14 tests, including 17,850 rational simplex-grid comparisons
(d=2..5), equal-support attainment, all two-level stationary candidates on its
finite coefficient grid, the flat two-coordinate edge, equal-multiplicity
stationary degeneracy, d=1, vanishing coefficients, sign/permutation invariance,
and invalid inputs. A distinct finite product-spectrum oracle computes
E[Y^6]-sum E[Y^3 xi_i]^2/a by direct atom enumeration on six rational unit
directions, independent of the cumulant formula. The test spectrum is uniform
on {-2,-1,1,2} in each coordinate; it is not the periodic infinite spectrum.

Four intentionally wrong formulas must fail named controls:
- M1 removes intermediate support sizes from (2).
- M2 drops the conditional-regression term b^2/a.
- M3 substitutes 15 for 9 in the fourth-cumulant coefficient after conditioning.
- M4 replaces 1/m^2 by 1/m in the cubic support contribution.

Run from this packet directory:

```sh
python3 -B -S -m unittest test_envelope -v
python3 -B -O -S -m unittest test_envelope -v
python3 -B -S envelope_check.py
python3 -B -O -S envelope_check.py
python3 -B -S envelope_check.py --mutant M1  # expected exit 1, likewise M2--M4
python3 -B -S envelope_check.py --mutant BAD # expected exit 2
```

Test-first observation: both initial runs failed all14 tests at the explicit
missing-implementation assertion. After implementation, both runs passed14/14.
The CLI baseline passes and the four named mutants reject; invalid label exits2.
The CI of the containing repository is separate and does not automatically run
this new standalone script. No local or hosted Lean execution of T1/T2 is claimed.

## 5. Limits and source custody

This is an additive authored result, not a new scientific-status register.
It neither edits #297 nor replaces its three slice reviews. In particular it
makes no all-direction bound for det(V), det(A|V), or the Frobenius covariance
trace. That tau drove the sampled combined maximum does not prove that it drives
the combined maximum over all directions. Other invariants require their own
analysis. No numerical coefficient enclosure, positivity theorem for arbitrary
input cumulants, lifetime theorem, persistence-pairing result, IBA1/IBA2 closure,
or complete formal alignment is asserted.

The exact input source identities and locally recomputed payload identities are
in SOURCES.json. The #297 source hash there is from its pinned manifest, with
native Git blob identity read back; only the stated sections were consumed.
The new extremum proof and diagnostic have OpenAI authorship. Independent review
must be of these new bytes, not inferred from the earlier covariance review.
