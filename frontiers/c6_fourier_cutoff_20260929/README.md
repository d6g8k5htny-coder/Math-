# C6 Fourier-cutoff candidate

Scientific effect NONE. Author-side analytic candidate; nonauthor review required.

PROOF.md replaces Taylor truncation with Fourier truncation of the FULL original
conditioned field. Uniform Gaussian-frequency error and Laurent-polynomial zero
counting give a cap tail exp(-c x^(2/d)). In d=2 this is exponential, and combining
it with the reviewed planar window mean gives the proposed r^3 log(1/r) second
factorial bound. In d>=3 the factorial composition remains conditional on G_d;
the count tail itself does not require that input. An exact abstract rare-count
example shows why an additional marked estimate is still needed for O(r^3).

Run from this directory:

    python -B -S verify.py --output /path/to/new-output
    python -B -O -S verify.py --output /path/to/other-new-output

Each invocation runs all 18 finite tests in BOTH Python modes and rejects nine
semantic mutants on intended assertions. Source membership, hashes and Git blobs
are checked before and after. Outputs must be new directories outside the packet.
With a complete repository checkout, add --repo /path/to/repository to verify all
six upstream byte identities. The hosted workflow uses that option; a packet-only
local replay does not claim a full checkout or upstream-byte verification.

The code tests finite identities and guards, not the analytic theorem. No previous
proof, source verdict, scientific-status register, price/lemma/prize flag or stopped
agent process is changed. The original and truncated pin laws are NOT identified.
