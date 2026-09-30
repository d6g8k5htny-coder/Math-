# Actual weighted-Palm lifetime loss

30 September 2026. Additive author-side corollary proposed by the root OpenAI agent and checked by reader_first_independent_review. Zero organizational-independence credit; scientific effect NONE. The frozen [PROOF.md](PROOF.md), SHA256 `3c69e20a332457211b8b1182a4819ce9b1dda824801f3a90157751f41b8fedf8`, remains unchanged. Its hypotheses, original weight, full normalizer, source identities, and reading rules are retained.

The success event is exact. Source #175 §1 defines F_r as failure of S to be the actual ordinary elder partner, and identifies finite death with that partner's height on the almost-sure Morse distinct-value locus. Source #170 §§1,8.1 gives the same definition and explicitly writes p_r=Q_r^W{d_f(M)=f(S)}. Both have f(S)=b-kr^3. Thus, Q_r^W-almost surely,

    F_r^c implies finite death and X_r=(b-d_f(M))/(kr^3)=1.

The essential event E_r is contained in F_r. These are the exact sources MARK_D and MARK_2 in [SOURCES.json](SOURCES.json), not a count-defined replacement event.

Fix q>0 and the fixed model parameters. Using the notation of PROOF.md, define

    m_q=integral lambda(theta)^q dmu_fail(theta),
    c_q=a-m_q=integral [1-lambda(theta)^q] dmu_fail(theta).

Because a>0 and 0<lambda<1 almost everywhere, 0<c_q<a. Expectations below use the original Q_r^W; no conditional-on-failure normalization is inserted.

The finite-death moment and its conditional version have the expansions

    E_QW[X_r^q;finite] = 1-c_q r^3+o(r^3),
    E_QW[X_r^q | finite] = 1-c_q r^3+o(r^3).           (L1)

The genuine bounded loss, with min(infinity,1)=1, and the finite signed deficit satisfy

    E_QW[1-min(X_r,1)^q] = c_q r^3+o(r^3),
    E_QW[(1-X_r^q);finite] = c_q r^3+o(r^3).           (L2)

The first integrand is nonnegative. The second can be negative when a finite X_r exceeds 1; it is not a bounded nonnegative loss at finite r. The tail estimate in PROOF.md makes that discrepancy negligible at this scale.

Consequently the actual lifetime power, with essential deaths excluded, satisfies

    E_QW[(b-d_f(M))^q;finite]
      = (kr^3)^q [1-c_q r^3+o(r^3)],                   (L3)

and the same expansion holds conditional on finite death. The essential-inclusive positive moments remain infinite; (L1) and (L3) cannot be written without their finite-death convention.

Proof. The exact success identity and PROOF.md (MOM) give

    E_QW[X_r^q;finite]
      = Q_r^W(F_r^c)+E_QW[X_r^q;F_r,finite]
      = 1-a r^3+m_q r^3+o(r^3).

By PROOF.md (U3), e_r=Q_r^W(E_r)=o(r^3), so division by 1-e_r preserves this expansion. Likewise PROOF.md (B1), with the success contribution equal to one, gives E[min(X_r,1)^q]=1-c_q r^3+o(r^3). Subtracting from 1 proves the first loss formula. The finite signed deficit equals (1-e_r)-E[X_r^q;finite], proving the second. Finally multiply by the deterministic factor (kr^3)^q, with fixed k>0. QED.

This is a pair-Palm expectation under the existing marked-law premises. It is not a new Kac–Rice intensity, an unrestricted parameter statement, or an acceptance of those premises. No existing weak-limit scope was defective. The separate rational control checks finite probability bookkeeping, the finite-conditioning denominator, and the difference between clipped loss and signed deficit; it is not a Gaussian-model simulation or a proof of the analytic premises.
