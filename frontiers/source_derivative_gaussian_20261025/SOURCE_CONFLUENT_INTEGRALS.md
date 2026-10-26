# Exact integral formulas for confluent pins and adjusted endpoints

Frozen before code, 25 October 2026. OpenAI/Codex root and
/root/dm2_landed_composition. Source LM006 endpoint-extension NOTE section 3,
immutable identity already given in SOURCE_CONTRACT's sibling Gaussian coupling
source contract. Scientific effect NONE.

Sole new ConfluentIntegralIdentities.lean. For scalar curves F C3 and H C2 on
the real line, r!=0, I=[-1/2,1/2], define
P3=(F'(r/2)-F'(-r/2))/r,
P4=(H(r/2)-H(-r/2))/r,
P5=(12/r^2)*((F'(r/2)+F'(-r/2))/2-(F(r/2)-F(-r/2))/r).
Prove the literal Peano-kernel identities

    P3 = integral_I F''(r*u),
    P4 = integral_I H'(r*u),
    P5 = 6*integral_I (1/4-u^2)*F'''(r*u).

Also prove the adjusted endpoint identities

    (F''(-r/2)-P3)/r = -integral_I (1/2-u)*F'''(r*u),
    (F''( r/2)-P3)/r =  integral_I (u+1/2)*F'''(r*u),
    (H'(-r/2)-P4)/r = -integral_I (1/2-u)*H''(r*u),
    (H'( r/2)-P4)/r =  integral_I (u+1/2)*H''(r*u).

Here H is the y-derivative curve, so its divided difference uses H itself.
Use ordinary oriented interval integrals; for I increasing these equal the
restricted-measure Bochner integrals in the source. Do not assume any integral
identity, divided-difference limit or Taylor remainder as a premise. FTOC,
integration by parts and the stated smoothness may be used. Preserve signed
nonzero r. The kernel integrals are 1, 1/2 and the normalized cubic mass1;
derive associated coefficient bounds or limits only if short.

These deterministic identities will be instantiated on actual differentiated
source modes. No stochastic/concrete covariance conclusion follows without
that instantiation and a justified infinite-sum limit. Reuse completed
verification and leave historical sources unchanged. Root integrates evidence.
