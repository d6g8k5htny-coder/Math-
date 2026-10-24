# Logarithmic cap transfer — IBA2-012

This additive conditional proof uses FR's finite-radius multi-soft event bound,
SH's quantitative original-law critical-count cap tail and P's moments/full
normalizer to obtain full soft power with a logarithmic penalty:

    E[K^a N_R^s; S] <= C r^3 Xi [log(1/r)/loglog(1/r)]^(d s).

This is NOT O(r^3Xi) with a uniform constant. An explicit dyadic abstract family
satisfies the numerical tail/event/moment bounds and attains this logarithmic
order. It is not an actual Gaussian-field counterexample. Read NOTE.md before
using the formulas. Existing #319 count transfer and #324 input-reduction work
are credited and unchanged.

## Reproduce finite controls

Python3.11+ standard library only, from this directory:

```sh
python3 -B -S test_log_cap.py
python3 -B -O -S test_log_cap.py
python3 -B -S test_log_cap.py --mutant M1
python3 -B -S test_log_cap.py --mutant M2
python3 -B -S test_log_cap.py --mutant M3
python3 -B -S test_log_cap.py --mutant M4
python3 -B -S test_log_cap.py --mutant M5
```

The baseline reports12 methods with empty errors/failures and exit0. Repeat the
mutants under -O: each must exit1 with its intended assertion failures and no
errors. Invalid labels exit2. Unittest writes diagnostics to stderr; empty
baseline stderr is NOT required. Deterministic JSON stdout is the comparison
surface. A crash or permission failure is never a successful negative control.
These are finite exact controls, not a simulation, Lean replay or proof of the
arbitrary-law/analytic inputs. Existing general CI does not automatically discover
this packet's standalone tests.

## Scope and offline agents

SOURCES.json binds complete directly quoted sources. Preserve original files and
save outputs into a new outbox, not inside a sealed packet. The accompanying
private chat delivery includes these source texts and the source/execution audit;
it is a supplement, not a new complete repository or laptop backup. Existing
large archives and the corrected R5 installer stay unchanged. No laptop install,
local inference or toolchain-cache completeness is implied.

Nonauthor mathematical review and separate eligible integration remain distinct
from these tests and current-candidate required checks. No scientific status,
parent theorem, formal target, workflow, or historical review is promoted.
