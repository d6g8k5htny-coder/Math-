# Marked-Fourier sector transfer — conditional publication candidate

Dylan Roy — delegated AI work. Author OpenAI / GPT-6 Astra Pro,
`iba2-marked-sector-publication-20261006-r9`, continuing the R8 local proposal.
Read NOTE.md and SOURCES.json. No existing proof, workflow, scientific status or
formal manifest changes. Nonauthor review and separate integration are required.

For fixed d>=3, torus side, observation radius, compact birth heights and strictly
positive compact gap marks, the proposed consequence is

    E[K^a N_R^s;S] <= C r^3 Xi [log(e/Xi)]^(d*s/2).

It combines the existing #157 MF1 marked stretched-exponential moment with #306's
finite-radius event bounds. It does not re-prove the Fourier theorem, replace
#319/#324/#327, or claim growing-order control. Every admissible Xi->0 gives
o(r^3) for each fixed count power. Sharpness is only for the numerical interfaces,
not a Gaussian-field lower result or a field-realization construction.

Run with existing Python3.11+ from this directory:

```sh
python3 -B -S test_marked_entropy.py
python3 -B -O -S test_marked_entropy.py
```

Baseline:15 methods, exit0, JSON empty failures/errors. Ordinary unittest stderr
is expected. M1–M5 via --mutant intentionally exit1 with nonempty intended assertion
failures and no errors; UNKNOWN exits2. Source/test identities and actual stdout,
stderr and returncodes are retained in the R9 delivery. The same fifteen methods
were developed/tested in R8; fresh publication replay is not fifteen new methods.
Existing general CI does not automatically discover this standalone test file.

Publication changes only the local-only metadata of NOTE/README/SOURCES. NOTE
sections2–5 and both Python files are unchanged from the retained R8 proposal.
SOURCES binds both direct quantitative inputs and every non-self payload.
The complete input texts, original failures and earlier execution evidence remain
in Marked_Sector_Transfer_R8_20261006.zip (401470 bytes), SHA256
b7416404ec7a1627251f902ea99da493a376ced40390b4204675100b5dbb8ee3.
The original ZIP stays unchanged; new evidence is a separate supplement.

No lower local/factorial normalizer, all-mark or growing-radius theorem,
full spatial limit, elder/lifetime matching, independent alignment or physical
laptop installation is supplied. Keep output outside sealed deliveries.
