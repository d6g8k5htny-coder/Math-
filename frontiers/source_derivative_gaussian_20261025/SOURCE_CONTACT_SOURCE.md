# Instantiate the contact covariance for the literal Fourier field

Frozen before code, 25 October 2026. OpenAI/Codex root and
/root/uniform_jet_moment_sources; scientific effect NONE.

Sole new SourceContactCovariance.lean module, using the immutable inputs and
SourceDerivativeGaussian. Define the actual seven derivative observations at
the origin of smoothSourceField 2 L in order
(f,fx,fy,fxx,fxy,fxxx,fyy), by orders (0,1,1,2,2,3,2) and coordinate direction
lists. This is the same concrete source and common smooth carrier as before.
For L!=0, prove their joint Gaussianity and identify each covariance with the
Gram sum of the actual differentiated Fourier coefficients using the already
proved derivative covariance formula.

Prove the seven selected coefficient columns are EXACTLY the polynomial
columns in SOURCE_CONTACT_GRAM.md, with c=sourceC L=2*pi/L and the actual
positive source amplitudes. Use canonical source modes, preserving the
half-lattice convention and false=cos/true=sin tags. Prove mode membership,
nonzero frequency and amplitude positivity; do not assume these selected
columns or a finite-mode source replacement. Use the generic seven-mode Gram
certificate from ContactJetCovariance to conclude positive definiteness of
the literal seven-observation covariance. No PosDef/invertible pin covariance
or conditional reference variance may be assumed in this instantiation.

The six-pin contact covariance is its principal block. A positive reference
Schur variance follows once the 6+1 algebra is supplied. This is a contact
claim only: do not infer finite-r confluent invertibility or uniform parameter
bounds without proving the needed covariance convergence.

All input and SourceDerivativeGaussian verification already completed is
reusable. Compile/check only this new affected module/closure as necessary.
Retain commands/exits, initial failures and meaningful controls. Root owns
Lake/source inventory/evidence and different-family review routing. No edits
to the landed source or completed derivative theorem are needed.
