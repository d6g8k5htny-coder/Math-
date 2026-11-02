# C297 hosted coercion-classifier amendment review

**`PASS_SCOPED_ENGINEERING_AMENDMENT` — the minimal classifier correction is appropriate.** Run 1 remains **HOLD**; this does not replace the required successful hosted run.

Actual reviewer: OpenAI Codex `/root/c292_geometry_review`, delegated work for Dylan Roy. This is same-provider, source-exposed nonauthor review, with organizational independence 0 and human review 0. Exposure includes the prior C297 mathematical/source reviews, topology/control advice, the hosted verifier review and multiline-parser finding, and the actual run-1 negative diagnostics. The reviewer did not author this classifier change or its regression test.

`$C297_ROOT` denotes the C297 working/evidence root without disclosing a machine-specific path. This amendment review supplements the frozen prior hosted engineering review; it does not rewrite that historical review or the run-1 evidence.

## Actual diagnostic and artifact binding

I read both actual negative diagnostics and receipts under `$C297_ROOT/hosted-run1/`, and verified their extracted bytes against the corresponding members of `$C297_ROOT/C297_RUN1_39418891714.zip`:

- ZIP: **323,718 bytes**, SHA-256 `edb500e87ab5c6880a32ffdf3950c186728bec24c8f758d3d9170f091fd81157`.
- `negative-WithoutRegularOrInterior.stdout`: **449 bytes**, SHA-256 `a723a09d113b51625b2f1ea3be658adf97077c1b545b65c63d021ee186efbeae`.
- `negative-WithoutCoordinateIdentity.stdout`: **438 bytes**, SHA-256 `5968ca1e824c98dc0c3871735efa6ea0c451f59d51473eb493cd706e29d707a2`.

Both are the intended missing-premise type mismatches, with rc 1, no timeout, empty stderr, and unchanged local objects. The precise mismatch in the old classifier was the displayed **`↑p` coercion**: `.1` was already accepted alongside `.fst`.

The coordinate diagnostic shows the actual invocation

```text
TorusRegularSuperlevel.closed_superlevel_basis_of_chart a x p hx
```

with type

```text
(∀ y ∈ p.source, (↑p y).1 = g y) →
  (𝓝 x).HasBasis (fun V => V ∈ 𝓝 x ∧ IsPathConnected V) id
```

where the requested type is the basis proposition itself. The regular-or-interior diagnostic analogously shows the remaining explicit premise

```text
a < g ↑x ∨ ¬IsCriticalPoint d g ↑x
```

before the basis conclusion. Neither diagnostic is a syntax, import, setup, or resource failure.

The reviewed coordinate receipt is 2,426 bytes, SHA-256 `cb9341f2223afb18b0756f90effaa529ce083e1a5e9204b3bb4b61b8e1ce3436`; the regular-or-interior receipt is 2,470 bytes, SHA-256 `b0652e343a1f50a7dc8510f7439bf00ce0fcd214366997af2882c7770c33327e`. Both receipts, both stdout/stderr pairs, and the aggregate `RESULT.json` matched their actual ZIP-member bytes.

## Exact source delta

The only production-code change is:

```text
\(p y\)\.(?:fst|1)\s*=\s*g y
→
\(↑?p y\)\.(?:fst|1)\s*=\s*g y
```

It accepts the observed spelling without relaxing the required chart, coordinate identity, function, source, invocation, or failure-kind checks. The added regression uses the actual diagnostic form and checks rejection after removing or changing those essential elements.

I compared the amended verifier and test module with the exact support files retained in the run-1 source snapshot. The verifier difference is the one regex change above. The test difference adds the actual coercion diagnostic and rejection mutations for missing identity, wrong chart, wrong function, missing source condition, unrelated invocation, and an import error.

Final reviewed identities:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `c297_hosted_verify.py` | 25,485 | `18985d363f3a0b0529e88c9c69dd07c626e6b5f82a251c19c7d820117b7d47c1` |
| `test_c297_hosted_verify.py` | 12,196 | `0d1d8d18a11334364151d16f7640af2730e38f17d8240ddf0244decc2f8376cd` |
| Unchanged `c297-regular-superlevel.yml` | 3,129 | `03b3d8fb4ca95316247b93ad3937ea2d56f0509040c819534873be1bb341eab3` |

The reviewed staged support files are under `$C297_ROOT/hosted/`. This review concerns this exact amendment; it neither authorizes a change to the frozen Lean sources nor treats the amended classifier as a new proof.

## Retained engineering control evidence

I read the retained regression failure and subsequent **10/10 normal and optimized** test results:

| Retained log under `$C297_ROOT/hosted/` | Bytes | SHA-256 |
|---|---:|---|
| `TEST_COERCION_RED.stderr` | 2,742 | `0045daa87111a04665923f19287703530e31e0ab4f54dc99dcd4c046850863af` |
| `TEST_COERCION_GREEN.stderr` | 1,774 | `08ab1b1edfbc8dad4238f37b4c15fcb733de877108132cf3335c8e4e3f643df2` |
| `TEST_COERCION_OPTIMIZED.stderr` | 1,774 | `10c767efdf08964c67741e1669944bea761fabcb88dd76a6b53beb29dfa8634e` |

The failing regression reports the actual-diagnostic rejection before the one-line fix. The subsequent normal and optimized results report all ten controls passing. These are the verifier author's engineering executions, not this reviewer's executions and not new Lean runs.

## Preserved outcome and acceptance boundary

Run 1's aggregate correctly records `HOLD_NOT_COMPLETED`, lacks `completed_at`, and lacks the second negative's semantic-acceptance flag. Its `RESULT.json` is 45,173 bytes, SHA-256 `55d8cac09bb7a96265de7f3c18bf75ae2aba1ee5d6a3138b96f6f705080e3bc3`. Those records must remain unchanged. The phase-level `PASS` on the coordinate process records the expected exit/object outcome; it is not a completed semantic classification.

Full artifact acceptance will bind the next hosted run and these amended support identities. It must still establish the exact source bindings, five builds, four standard named-module kernel replays, complete four-module census, both intended missing-premise rejections, and the final source/object stability checks.

C296-N1 remains with the peer reviewer and source owner. This narrowly reviewed C297 classifier change neither supplies blanket approval of the peer workflow nor duplicates its repair.

I ran no tests, Lean, or hosted verification and made no remote action. I edited no implementation or Lean source. The only write was this authorized amendment-review record. Same-provider exposed nonauthor review, **org0/human0**. Scientific effect: **NONE**.
