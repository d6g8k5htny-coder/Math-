# DD exact process contracts — reconstructed candidate

## Scope and source

Base: `95eb8daaa02e89be1f816bc7f58eac812dd1b469` of Math-. Original wrapper blob: `9b01189115f9abd1b57dba581628e52be71453ae`. This is an engineering repair, not a theorem closure or a new mathematical bound. All stored notes, numerical algorithms, certificate inputs/results, bounds and SOURCES.json remain unchanged.

The earlier unpublished candidate `fb20f42` and its dirty extension, raw logs and review were lost when the execution workspace was replaced. They are historical reports only, not authenticated evidence for this new candidate. A surviving transformation script was inspected but not applied as recovery of missing bytes. This candidate was reconstructed from public source, with new actual specimens and fresh failing tests before production edits. No prior review is transferred.

## Contracts and meaning

The original changed-node predicate accepted any result except successful unchanged stdout, including unrelated crashes. The fixed deterministic perturbation of nodes_3.json must instead match `(0, CHANGED_NODE_STDOUT, b'')`. This runs with `--no-recheck --no-sample` and tests **output sensitivity**, not rejection of mathematical invalidity. The perturbation, Decimal precision and underlying arithmetic are unchanged. Its altered output must not be cited as a certified new bound.

The original missing-node predicate accepted exit1 and a diagnostic substring, ignoring stdout and the complete error. Omitting nodes_11.json must match `(1, b'', expected_missing)`. The expected complete CPython3.11.16 traceback names dd_exact.py:95, dd_exact.py:37 and ddcore.py:23, ending exactly `AssertionError: incomplete node values: 2194 of 2393 cells`. The omitted shard represents199cells. This is **input-completeness rejection**, not proof that supplied numerical values are mathematically correct.

Only the known certificate directory is substituted into the expected missing-node template. Actual streams are never stripped, normalized or searched by substring. Source/runtime traceback drift deliberately fails closed and requires renewed observation/review, not relaxation of the contract. Success markers distinguish `output_sensitivity_verified` from `input_completeness_rejection_verified`.

## New specimens and reproducibility

New actual normal/optimized runs used the official Astral python-build-standalone CPython3.11.16 release20260929. Its install-only x86_64 Linux archive SHA256 was checked against release metadata: `fbbfd0f2253996486455f44a28c09ac7e2df534b8a4835408d17c99d185b80ec`. No global installation is needed; hosted workflow remains pinned to3.11.16.

Both modes produced identical stream pairs: changed-node exit0, empty stderr and989bytes stdout SHA256 `1e547fee84313e3fd62d822c97f9c76b08335112bcd71337e00bc06ea4a31bf8`; missing-node exit1, empty stdout and the full path-dependent traceback. The path-neutral574byte template SHA256 is `74c9a35ac855ac1abba7c48a3eb1f25333b277738fd75da47fa8c73fe402833b`. Fixtures are retained independently of production literals.

Run with CPython3.11.16:

```sh
python -B -S -m unittest discover -s tests -p 'test_lifetime_dd*.py' -v
python -B -O -S -m unittest discover -s tests -p 'test_lifetime_dd*.py' -v
python -B -S -m unittest discover -s tests -p test_full_suite_routing.py -v
python -B -O -S -m unittest discover -s tests -p test_full_suite_routing.py -v
```

The focused population is36methods:26 unchanged protocol/evidence tests and10 new oracle tests. Fifteen changed-node and16 missing-node adverse tuples cover unrelated failures, wrong exits/signals, empty streams, stderr/stdout contamination, truncation, prefix/suffix/duplicate/newline changes, numeric/frame/exception/path differences. Exact positive tuples and actual bounded children prevent unconditional rejection. Sixteen source mutants (eight per predicate) must each cause assertion failures with zero runner errors; threshold16/16. Finite mutation coverage is not a proof of universal auditor soundness. Fresh RED on original source ran10methods with33assertion failures and no errors.

The dedicated workflow runs and retains the new tests and both fixtures before its existing full replay. Original tests, actual full replay, runtime/action pins and permissions remain enabled and unchanged.

## Remaining boundaries and tool registry

The new bounded controls do not run the approximately45-minute-per-mode complete certificate replay. No complete repository regression, current hosted gate pass, Lean verification or federation CBZ-0 completion is claimed by this local artifact. The full assembly's existing boundary is all2393cell remainders and24sampled nodes, not all38288nodes; no analytic theorem is formalized here.

Tool: existing packet `replay.py`, strengthened process predicates. Purpose: reject unrelated subprocess outcomes instead of calling them successful controls. Usage: packet README; self-verification: commands above and assertion-only mutation threshold. Maintenance: self-contained, no ongoing owner; intentional input/runtime changes require independent recharacterization. CBZ criteria served:4,5,7,9,10; none is established federation-wide by this scoped repair. Canonical GOVERNANCE/TOOLING/STATUS registration remains with the federation coordinator; this is not a competing scientific-status register.
