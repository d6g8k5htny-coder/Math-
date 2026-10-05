# Digest erratum to the retained scoped moment-generality review

Date: 2026-10-05. Scientific effect: **NONE**.

Dylan Roy — delegated AI engineering. Actual performer: OpenAI / GPT-6 Astra Pro, ChatGPT session `github-rules-and-closure-20261005`. This is a documentary correction, not a new mathematical review or an alignment acceptance. Organizational-independence credit: **0**.

## Retained original and reading order

Read [the original review](REVIEW.md) together with this erratum. The original first-person execution statements, authorship, scoped PASS, exposure limits, and missing independence remain the original reviewer's statements; this erratum does not claim to rerun them.

The retained `REVIEW.md` is byte-for-byte Git blob `fa25c742e0cf27d2b02baeb69556ca7d9afc663a` from Math-#280 head `4551c3321943bcbbc679fb34a990523361734290`. Its recorded SHA-256 is `fce6067fcc9c7edfe08e7f7e67b8275223e9b315c37832fdacea6661ecee1523`. Copying that exact blob preserves the historical failure rather than silently rewriting another reviewer's account.

The original is a scoped review of Math-#279 source `f6672c1a77d67b6257c43acaf5a4481b28fd87e0`. The source and its acceptance state are separate from custody of this review. In particular, this successor imports no #279 implementation files and does not change the withheld #281 alignment disposition.

## Exact correction

Agent14's [required finding](https://github.com/d6g8k5htny-coder/Math-/pull/280#issuecomment-5998491524) identifies the digest in original `REVIEW.md` line105.

The original token is:

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b855
```

It contains59 hexadecimal characters, not64. The exact replacement token is:

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Consequently the corrected reading of that original line is:

> - `leanchecker.log` is empty. Its digest is the empty-file SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The hosted gate accepted that exit. This session did not re-run `leanchecker`.

Here “This session” continues to refer to the original xAI/Grok reviewer, not the erratum author. No other sentence, verdict, proof, hypothesis, receipt, or status is amended.

## Reproduction and limits

The erratum author independently executed this standard-library calculation:

```python
import hashlib
old = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b855"
correct = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
if len(old) != 59 or len(correct) != 64:
    raise SystemExit("unexpected token length")
if hashlib.sha256(b"").hexdigest() != correct or old == correct:
    raise SystemExit("digest correction failed")
print("EMPTY_DIGEST_CORRECTION_PASS")
```

This proves the replacement is the SHA-256 of empty bytes. It does **not** independently establish that a particular downloaded execution log was empty. No receipt or workflow artifact was downloaded anew for this erratum; no Lean build or `leanchecker` replay is claimed. The original review and original run retain their own execution evidence and limitations.

The isolated custody successor starts from Math main `0cdc19fcf857b441cee92e0201b6c4f5a9dba072` and adds only the unchanged original review plus this erratum. It does not merge the implementation or evidence branches through their ancestry. Review of this correction and any later integration must be recorded separately at the actual successor head.
