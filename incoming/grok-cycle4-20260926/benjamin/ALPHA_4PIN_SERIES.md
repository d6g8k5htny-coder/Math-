# Axial 4-pin remainder of α_M + 6k

Scientific effect: NONE. Parent A3 remains AMEND.

    E[α_M | 4-pin] + 6k
      = k r^2 - (b r)/4 + (b r^3)/24 - (k r^4)/20
        - (b r^5)/192 - (k r^6)/120 + (b r^7)/5760 + O(r^8)

Frozen as algebra: through r^4 (Lucas independent (b,k)-split grid agrees).
DERIVED-numeric: -b r^5/192 and -k r^6/120 (k-only rem/r^6 matches -1/120, kills +31k/240).
Pure-cubic interpolant p(M+z)=b-3kr z^2+2k z^3 realises α=-6k for every r.
