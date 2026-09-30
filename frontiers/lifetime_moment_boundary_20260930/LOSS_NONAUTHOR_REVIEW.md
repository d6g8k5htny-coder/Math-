# Nonauthor review of the additive lifetime-loss consequence

Reviewer: OpenAI / Codex subagent `/root/workflow_bottleneck_audit`, 30 September 2026. No drafting or amendment of this consequence was performed by the reviewer. Same-provider/source exposure and shared-account work grant zero organizational-independence credit.

**VERDICT: ACCEPT (L1)–(L3) of `LOSS_COROLLARY.md`, SHA256 `8d202bf2adbf25cb10ba7b114024e7772f2e6839746dc744e1494027a25a178c`, as conditional consequences of the separately reviewed frozen C28 proof and its original actual-elder event definition. No blocking amendment found.**

The source check is substantive: MARK_D §1 defines F_r as failure of the actual ordinary elder partner to equal S and identifies finite death with that partner's height on the full-probability Morse/distinct-value locus. MARK_2 uses the same event and expressly equates success with d_f(M)=f(S). Since f(S)=b-kr³, success implies finite death and X_r=1 exactly. No witness-count event is substituted.

The finite numerator decomposes exactly into Q^W(F_r complement) plus the finite-death failure moment. Substituting Q^W(F_r)=a r³+o(r³) and the frozen proof's failure moment m_q r³+o(r³) gives 1-(a-m_q)r³+o(r³). The essential mass e_r is o(r³), so division by 1-e_r leaves this coefficient unchanged. Positivity and strict upper bound of c_q=a-m_q follow from positive failure mass and limiting fractions strictly between zero and one.

For the clipped formula, success contributes one and essential deaths also have clipped value one; subtracting its expectation from one leaves the bounded nonnegative loss. For the finite signed deficit the exact identity is Q^W(finite)-E[X_r^q;finite]=(1-e_r)-E[X_r^q;finite]. The candidate correctly distinguishes it from a pointwise nonnegative loss: it is negative on finite X_r>1. The frozen axial-tail bound makes the expectation of this discrepancy negligible at r³ scale. Neither formula silently treats infinity times an indicator as an ordinary finite moment.

Multiplication by the deterministic positive factor (kr³)^q yields the physical-lifetime expansion at fixed q,k. Both essential-inclusive positive moments remain infinite. These remain weighted pair-Palm expectations, not counts or intensities of distinct replacement bars, and there is no extra failure normalization.

The additive file leaves frozen `PROOF.md` SHA256 `3c69e20a332457211b8b1182a4819ce9b1dda824801f3a90157751f41b8fedf8` unchanged. The separate exact control was inspected and replayed once with `python3 -B -S`; its 48 rational probability-bookkeeping cases passed. The fixture retains separate success, ordinary failure, rare finite long lifetime, and essential atoms, so it checks the conditioning denominator and the distinction between signed and clipped loss. It does not prove any Gaussian-model premise. File identities and the observed receipt are in `LOSS_IDENTITY_AND_CONTROL_OBSERVATIONS.json`.
