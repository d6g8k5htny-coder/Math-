import ActualH0Controls

open TorusFiltration

-- Deliberate false mutation: include the death endpoint at b=3,k=r=1.
-- The proved interface counterexample reduces this exact mutation to False.
example : elderActive 3 (3-(1:ℝ)^3) (-(3-(1:ℝ)^3)) := by
  apply False.elim
  -- Exactly one residual False is required. No admissions or unrelated errors.
