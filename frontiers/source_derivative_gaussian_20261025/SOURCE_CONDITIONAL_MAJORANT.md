# Actual uniform whole-field derivative majorants and cutoff tails

Frozen before code,25October2026. OpenAI/Codex root and
/root/dm2_landed_composition. Scientific effect NONE.

Sole new SourceConditionalMajorant.lean. Use the actual posteriorSample and
sourceSmoothKernel. Let Gamma_k(omega)=sum' m,orderModeBound k 2 L m*abs(omega_m)
and A_m=confluentModeMajorant L m. Derive actual inverse-entry bounds K and
prescribed-value bounds D uniformly on one small positive-radius interval,
using completed actual covariance/inverse limits, not an assumed bound.
With B_w=sum' m,w_m*A_m, prove the actual deterministic inequality

  Gamma_w(posteriorSample d_r omega)
    <= Gamma_w(omega)+36*K*B_w*(D+Gamma_A(omega)).

Supply the per-sample summability and all infinite-sum interchanges; a real
tsum identity is not proof of summability. Preserve arbitrary fixed height b
and the posterior drift. The source weights are nonnegative and summable;
posterior Gaussian coordinates are not replaced by centered standard ones.

Use GaussianWeightedMajorants under the unchanged NOISE law and the proved
kernel pushforward to derive, for every natural moment order, a uniform
conditional Gamma_5 moment bound without a moment premise. Derive the global
pointwise bound norm(D^5 smoothSourceField(omega)(x))<=Gamma_5(omega) from
actual termwise derivatives. The same may be done for any fixed order k.
Do not silently assume measurability of an uncountable derivative supremum;
use the literal measurable Gamma cutoff, which certifies the field bound.

Derive uniform polynomial cutoff tails for each requested order. If the
separately proved exponential majorant theorem is available, recombine the
bound as drift+Gamma_(w+constant*A) and derive its Gaussian upper tail with
explicit retained drift; do not infer this from bare moments. Transfer the
actual measurable carrier events to the constructed whole-carrier weighted
law only after SourceSmoothPalm supplies its proved event formula/bounds.
No inherited LM007/LM009 scientific review or stronger historical scope is
transferred. Literal historical nine-jet normalization and geometric/parent
joins still require their own proofs within the original research goal.

Only new code receives new checks; reuse14baseline/23input/kernel evidence.
No completed source edits, custom axioms, assumed realizations or desired
conclusions as premises. Root owns integration and distinct-family review.
