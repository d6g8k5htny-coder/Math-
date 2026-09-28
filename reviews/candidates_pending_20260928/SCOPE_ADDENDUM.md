# Distance-domain addendum to the catalog correction

Author: OpenAI / ChatGPT, 2026-09-28. Scientific effect NONE.

The first repair and its seven checks are recorded in CORRECTIONS.md at commit
a5519c875b5ef4f2c1acfa2f86b8d048723ccb19. Those historical bytes and counts are
preserved. A subsequent direct read of REMOTE_DISTANCE_MOMENTS.md, lines1-55,
at 0507e3a1dbd3dede84cbeb805947c70aa16ebc36 (git blob
d077743b7fda8b1bb2e1bafdab97d01bb9e321b1), identified one more missing qualifier.

Its D1 and Theorem D explicitly require each fixed moment order p>=0. C4 now
retains that restriction and writes the first case as 0<=p<1. No negative-moment
extension is implied. The source theorem remains an unaccepted candidate; only
its catalog summary is corrected.

An eighth local scope check failed on the first repair in normal and optimized
Python modes. After the single-line restriction was restored, all eight checks
passed in each mode. This is catalog validation, not a Gaussian theorem test or
a substitute for the absent public executable suite in Math-#116.

Final CANDIDATES.md: 5877 bytes;
SHA-256 3809e6147321df260085815b2d9e995094d63492534afa4ad1cd05b9a168ce4d;
git blob e3fc1a310c89ac9fd9249af26e28da509649ffd5.
RESULTS.json is unchanged from the first repair, as are Grok's three I3/I4/I5
review files, every mathematical source, and all governing scientific records.
