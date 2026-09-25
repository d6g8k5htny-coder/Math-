# Downstream hard gate — fail-closed promotion control

**Object:** DOWNSTREAM-HARD-GATE-20260925-v1  
**Author:** Cursor (Cloud Agent). **Disposition:** engineering integrity control for [main #90](https://github.com/d6g8k5htny-coder/main/issues/90) / [main #86](https://github.com/d6g8k5htny-coder/main/issues/86). **Scientific effect: NONE.**

[Research home](https://github.com/d6g8k5htny-coder/main) · [Math index](../../README.md) · [Scope note](SCOPE.md) · [Machine graph](GRAPH.json)

## What this is

A machine-checked dependency graph over the Math- candidate surfaces and the historical RN walls they interact with. It enforces:

1. **No CONTROLLING promotion** unless every *required* transitive dependency is terminally classified as `PROVED_REVIEWED`, `SUPERSEDED_NONBLOCKING`, `REFUTED`, or `BLOCKED_ABSENT`.
2. Any required `BLOCKED_ABSENT` dependency forces the dependent node to **HOLD**.
3. A fingerprint or classification change on a dependency marks transitive dependents `REVALIDATION_REQUIRED`.
4. Green CI, hashes, architectural admission, numerical experiments, same-author review, and navigation success are **non-discharge** tokens and cannot alone authorize promotion.

This package also records the **D4 region complement**: the fixed-remote candidate covers only `dist>=rho` with the between-pin height window; mesoscopic scaled annulus, pin-collision, intermediate `r<<|x|<<rho`, and witness-collision regions remain open.

## What this is not

- Not analytic review of #63/#65/#67/#74/#76.
- Not a replacement for main PR87's hardening-branch crosswalk text.
- Not a flip of `lemma_closed`, `certified_C_H`, or any prize/premise register.
- Not permission to mutate the Drive `99_DO_NOT_OPEN` vault (#91 sole-auditor freeze).

## Run

```sh
python -B -S hard_gate.py
python -B -S -m unittest -v test_hard_gate
python -B -O -S -m unittest -v test_hard_gate
python -B -S run_validation.py --output /tmp/downstream-gate-new-run
```

Choose a new output directory outside this source tree. The suite has 31 distinct tests and ten semantic mutations. Required REFUTED premises block; reverse impact uses the union of old and new edges so edge deletion cannot erase revalidation.

See also the [D0 CI unblock recipe](D0_CI_UNBLOCK.md) (portable patch for main PR87) and the [selector×region inventory](SELECTOR_REGION.json).