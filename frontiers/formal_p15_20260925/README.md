# P15 algebraic formal-verification pilot

**Object:** P15-ALGEBRA-SMT-PILOT-20260925-v1. Author-side translation by OpenAI / ChatGPT. Scientific effect **NONE**. Independent translation review, parent analytic review, and proof-assistant verification remain open. This supplies a small executable pilot for main #95 / downstream D6, not acceptance of P15 or the Gaussian program.

## Exact source and scope

Parent: `d6g8k5htny-coder/Math-`, commit `baca69c394ab42130c61771bee74e808703f1ce7`, `frontiers/full_price_20260924/PROOF.md`.

- Git blob: `582180e41dca0ad815ad0f18574df42040912149`
- SHA-256: `87521901ca8e5405b4d1e47f1deb1cd0326affbd6f5967b53c4178590da993f9`
- Bytes: 11352

The runner checks these three identities before evaluating a sublemma. It writes only a new evidence directory. The parent proof and scientific registers are unchanged. Seven statements are translated into quantifier-free nonlinear real arithmetic by asking whether their hypotheses AND the negation of their conclusion are satisfiable. All exact statements, domains, and rational witnesses are in `SPEC.json`.

| Source | Checked algebraic content | Imported / not checked here |
|---|---|---|
| F4-F5 | For a,b>=0, a+b>0, x>0, d=a+bx: d>0; if d^2 c=-abx, then c<=0 | x=exp(-t); differentiation; c actually equals the displayed second derivative |
| F10 | From (1-p)n=pm, the identity (1-p)^2 n-p^2 m=p(1-2p)m | Construction and normalization of binomial masses |
| F10 | Strict negativity for 1/2<p<1, m>0, n>=0; nonpositivity on the closed interval with m,n>=0 | Positivity of the particular binomial mass in the interior; induction across capacities |
| F11 | Real e>2 implies 0<3e-2<e^2 | e is Euler's number; exponential/logarithm monotonicity |
| Section 6 | Exact rational identities and positivity for 11/23520 and 26081/933120 | Exponential series tail bounds and the deduction about rho_star |

The seven checks do not formalize separate-concavity interpolation, continuum probabilities, cover construction, cross-block independence, the full sharp constant, or the parent theorem. Algebraic variables may range over a larger domain than their application: x>0 is enough for the curvature sign without encoding exp(-t). This is not substitution of a stronger hypothesis into the parent theorem.

## Explicit domain clarification

The strict '<0' in the source's F10 requires interior p<1 and a positive mass. At p=1 and a>=1, m=P(S=a)=0 and n=P(S=a+1)=0, so both sides are zero. `F10_STRICT_INTERIOR` and `F10_CLOSED_NONPOSITIVE` separate the two correct scopes; `M_STRICT_AT_P_ONE` records the false endpoint strengthening. The source application p_star=1-exp(-1) is interior, so this does not refute the full-price theorem. It is an additive precision note, not a silent edit to the frozen source.

## False variants and anti-vacuity controls

Six deliberate false variants drop a>=0, drop b>=0, replace nonpositive curvature by strict negativity, reverse the recurrence sign, demand strictness at p=1, or omit the mass relation. Each has an explicit rational counterexample checked independently with Python Fraction and a solver SAT result for the negated false claim. Every positive statement also has an explicit rational premise witness and an additional SAT query, preventing acceptance solely from inconsistent hypotheses.

One run contains 26 solver queries: seven UNSAT negation checks, six SAT counterexample searches, and thirteen SAT premise-witness checks. The 24 unit tests exercise the wrapper, source identity, exact witnesses, solver-result handling, and rejection of malformed expressions; they are not 24 additional mathematical theorems.

## Reproduce

Python standard library only; the native Z3 shared library is a separate explicit runtime requirement. There is no pip dependency. On Debian/Ubuntu the native package is `libz3-4`. A different operating system can provide a compatible library using `--library /path/to/libz3`. The report records actual Python/Z3 versions and the loaded library's SHA-256 when the file can be located. The observed local run used Z3 4.13.3.0; no untested platform is certified by this note.

From the Math repository root, choose NEW output directories:

```sh
python -B -S frontiers/formal_p15_20260925/verify.py --output /tmp/p15-smt-normal
python -B -O -S frontiers/formal_p15_20260925/verify.py --output /tmp/p15-smt-optimized
python -B -S -m unittest discover -s frontiers/formal_p15_20260925 -p 'test_*.py' -v
python -B -O -S -m unittest discover -s frontiers/formal_p15_20260925 -p 'test_*.py' -v
```

Outside the repository, pass `--source-proof /path/to/the/exact/parent/PROOF.md`. Outputs include every `.smt2` query, solver transcript/proof export, exact source hashes, and `REPORT.json`. Existing output directories are never overwritten. Unknown solver results, API errors, wrong result polarity, absent proof exports, bad source identity, and unavailable runtime fail closed. Each query has a solver timeout.

## Trust boundary and next review

The universal algebraic results trust Z3 and the correctness of this translation/runner. Proof objects are exported, but **not independently checked by another proof kernel**. No Lean/Coq/Isabelle build has occurred. Exact-rational witness checks validate individual examples, not universal conclusions. The source-hash check establishes identity, not truth.

A nonauthor reviewer should check the seven formula translations against the cited source, confirm the import boundaries, replay both modes, and examine the six false variants. A future proof-assistant translation can reduce solver trust; it must still address the mathematical-source-to-formal-statement correspondence. Verification evidence and scientific acceptance remain separate fields. Neither this directory nor its workflow can promote a claim or close #74/#90/#94/#95.
