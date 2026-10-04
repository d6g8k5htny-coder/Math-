# Preserved author-draft correction

Before any C113 proof file was written, the author sent an internal
coordination message proposing the family
`a=q=0, beta=-12k, s=-12kv`, with extra roots
`(-v, +/-sqrt(v^2-1/4))`. That message incorrectly stated the extra-root
Hessian determinant as `-432 k^2(v^2-1/4)`.

The author immediately corrected it in a second coordination message.
The direct Hessian is

```text
[[-12kv, -12kZ], [-12kZ, 0]],
```

so the correct determinant is
`-144 k^2 Z^2 = -144 k^2(v^2-1/4)`.
The sign, parameter family and intended argument did not change. The
original `-432` statement was an author-draft arithmetic error, not a
source error or a reviewer finding. The new proof uses the corrected
identity, and its finite controls explicitly reject the `-432` alternative.

No historical source bytes, review report or public scientific status
were changed to conceal this correction.
