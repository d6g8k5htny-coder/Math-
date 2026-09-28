# Primary-source reconnaissance and attribution

OpenAI / ChatGPT, 28 September 2026. Scientific effect NONE.

Primary abstract records opened in this session:

1. Pierre Aboulker, Guillaume Aubian and Chien-Chung Huang, *Vizing's and Shannon's
   Theorems for defective edge colouring*, arXiv:2201.11548v2 (3 February 2022),
   https://arxiv.org/abs/2201.11548 . Its abstract explicitly describes the even-
   defect ceil(Delta/d) multigraph phenomenon. We do not claim invention of that
   mechanism. The variable-capacity original-coordinate construction needed here
   is written in PROOF.md Section2, using the existing #118 construction.
2. Dmytro Gavinsky, Shachar Lovett, Michael Saks and Srikanth Srinivasan,
   *A Tail Bound for Read-k Families of Functions*, arXiv:1205.1478 (25 April 2012),
   https://arxiv.org/abs/1205.1478 . The abstract concerns Boolean functions of
   independent coordinates, with each coordinate influencing at most k functions.
   This confirms a classical related dependence framework, not the exact theorem
   or weighted constant of this note. The required weighted entropy chain argument
   is provided in full in PROOF.md Section4.

These were abstract/metadata reads, not full-paper verifications or a comprehensive
novelty audit. No claim of priority, optimal cover constant, or literature absence
is made. The improvement is to this workspace's displayed bound for the same
structural class: the exact even-capacity reference-tail maximum q9 replaces a
coarse Chernoff constant, and actual weighted incidences replace a uniform load.

The preceding #118 source and tests were read and exposed to this author. The
new rational-series code follows elementary interval estimates also used there.
Source exposure and shared provider/account remain disclosed; no independent
review is created by this note or its citations.
