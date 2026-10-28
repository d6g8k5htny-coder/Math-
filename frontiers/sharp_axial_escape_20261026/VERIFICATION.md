# Actual verification and retained limits

26 October 2026. Base Math- commit:
`7d63d08f6cfadfd9c2ef28039a370d741126f9a0`.
Local branch: `research/sharp-axial-escape-20261026`.
Actual author/executor: OpenAI/Codex GPT-6 `/root`.

## New packet

Executed with Python 3.12.14, standard library only:

```sh
python -B -S frontiers/sharp_axial_escape_20261026/check_exact.py
python -B -S -O frontiers/sharp_axial_escape_20261026/check_exact.py
```

Both exited 0 with identical JSON, preserved as `CHECK_NORMAL.json` and
`CHECK_OPTIMIZED.json`. Their scope is exact algebra and source identity:

- 126 physical-coordinate quartic cases: pins, derivatives, endpoint margins;
- 12 exponent cases, including the omitted-norm-power falsification;
- 12 exact three-atom endpoint-moment counterexamples;
- the endpoint-optimization polynomial identity and weak-threshold obstruction;
- both predecessor-source SHA256 values, byte counts and Git blob identities.

The report binds the proof SHA256
`bd390073859b5842d9386fac8eda6122ce8fbe51f501e4951dc5c75a30d4f5d5`.
The continuum proof uses Rolle and Hermite interpolation in the text; finite
examples do not certify that argument or the original Gaussian inputs.

## Predecessor checks and environment limit

The unchanged predecessor's direct `check_exact.py` and `check_loss_exact.py`
both exited 0 with PASS. They report 54 good quartic cases, 18 outside-premise
axial fixtures, 12 exponent cases, and 48 rational loss cases, respectively.

The initial command
`python -B -S -m unittest discover -s frontiers/lifetime_moment_boundary_20260930 -p 'test_*.py' -v`
ran ten tests and all ten failed before reaching their intended checks because
the child `verify.py` requires exactly Python 3.11. Actual Python is 3.12.14;
Python 3.11 was not found. No source or test was changed to bypass that gate.
This is NOT a pass of that publication-verifier suite. No full repository
test suite, hosted CI, Lean build or formal acceptance was run or claimed.

## Separate internal technical critique

OpenAI/Codex GPT-6 agent `/root/axial_technical_check`, a separate same-family
reader given the packet and design without author conversation history,
read the proof and independently reran both checker modes. It reported no
concrete mathematical defects in the stated scope and identical PASS outputs
at the exact proof hash above. It specifically checked Hermite extrapolation,
threshold sharpness, the no-tie boundary corollary, the exponent `s-4q-3`,
and the abstract counterexample. It changed no files or external objects.

This is disclosed same-family internal technical evidence. It does NOT meet
the project's different-family scientific-review requirement, confer scientific
acceptance or earn organizational-independence credit.

## Delivery boundary and next mathematical work

All edits are additive local candidate files. Historical proofs, source
manifests, reviews, status registers, workflows and remote refs are unchanged.
`git diff --check` and exact manifest-to-base-Git-object checks are part of
the final local verification.

The next scientific gate is different-family review of this exact packet.
For a parent theorem, separately establish the source-specific bound (11)
and clipped law (14) of the new proof at their required source/review scope.
This packet supplies neither acceptance of those inputs nor a claim that
the full Gaussian mathematics has become unconditional.
