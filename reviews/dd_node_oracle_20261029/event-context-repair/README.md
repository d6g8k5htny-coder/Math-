# Failure-event context identity (finite engineering controls)

Parent: `94a78d8bd95f0cafae85bd6b202407e418fafc2b`.
Review: https://github.com/d6g8k5htny-coder/Math-/pull/541#pullrequestreview-5706017963

The review's two genuine failing subtests are legitimate: one selected method
may emit multiple distinct contexts. Repeated parent IDs or identical subtest
labels do not constitute duplicate event identity. The positive regression
explicitly permits two different contexts bearing identical labels.

A separate regression replays the exact same `(test, subtest, err)` callback
twice while the selected body is active. Before repair this was admitted; the
retained RED log records the failing refusal assertion. The result now retains
actual test/context references and compares with `is`; duplicate context
callbacks fail closed. No integer object ID or label equality authorizes this
gate. Ordinary failure context is the selected case object. Existing origin,
lifecycle, exact-code-identity, clean-state and method-accounting gates remain.

Pinned CPython3.11.16 commands from repository root:

```
python3.11 -B -S -m unittest discover -s tests -p test_lifetime_dd_node_oracle.py -v
python3.11 -B -O -S -m unittest discover -s tests -p test_lifetime_dd_node_oracle.py -v
```

Each mode runs25 methods (all23 prior methods preserved plus2 additive
regressions), original16 wrapper mutants, and7 effective grader mutants plus
2 deliberately redundant omissions recorded as non-kills. The new source mutant
removes the identity admission gate; the pristine outer grader authenticates
the resulting intended regression assertion. Source tests are finite evidence,
not mathematical certification or a proof against hostile in-process mutation.
No historical finite kill, production output, certificate, or theorem is
invalidated. Historical receipts remain unchanged; hosted evidence for the new
composition remains pending.
