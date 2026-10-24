#!/usr/bin/env python3
"""Verify the stored QS A3-A3.11 records and replay their published author controls (standard library only).

Every file in this packet except replay.py, README.md and SOURCES.json is one of two things:
  - an exact copy of a public comment body on main#229 (a note, claim, controls comment, review, readback,
    erratum, successor text or author response);
  - a control script or its stdout, extracted verbatim from a stored controls comment by the extraction rule that
    comment states (the rule of main#229 comment 5971055189); A3.10's ledger script and its stdout are extracted the
    same way from the stored note itself (its section 4), the stdout from a ```text fence.
SOURCES.json pins each file by byte count and SHA-256 and lists each replay. This script performs four checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned
     identity.
  2. Every extracted script and stdout equals the fenced payload inside its stored source comment, under the
     extraction rule (the stdout fence language follows the stored stdout's suffix: .json for ```json, .txt for ```text).
  3. Every control script runs under the current interpreter's -O/-S flags and reproduces its published stdout byte
     for byte (none prints an interpreter version), with empty stderr. Every listed mutant or invalid invocation
     must reproduce its exact source-bound rejection on BOTH captured streams, not merely exit 1 or 2.
  4. Negative controls must be rejected:
     - a one-byte change to a stored note (A3_6/PROOF.md);
     - a control script with one changed constant (A3.6's hard-gap integral coefficient 5/4 replaced by 1/4).

Reproducibility only. The analytic notes and their reads carry the mathematics. These finite checks support
algebra, as the reads say. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/qs_d3_soft_layer_chain_20261005/replay.py   (exit 0 iff every check passes)
Optional QS_REPLAY_EVIDENCE_DIR (outside the checkout) retains raw child streams and process records.
Each invocation gets a new directory; records describe execution, never mathematical acceptance.
Required evidence I/O fails the run; a timeout/spawn error remains the primary exception.
"""
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
OWN = {'README.md', 'SOURCES.json', 'replay.py'}

# Exact rejection fingerprints from the UNCHANGED source packet at b157df1b57da41d2d75d6515b5e795b234ee7d34 (A3-A3.6)
# and, for A3.7, from its extracted author control a37_exact.py (main#229 comment 6004629351), computed under both
# interpreter modes at incorporation and found identical; likewise for A3.8 (a38_exact.py, comment 6007706590),
# A3.10 (pd3_ledger.py, published inside the note 6008550120) and A3.11 (a311_exact.py, comment 6009957866).
# Each key is (script path, complete argv tail); each value is (exit, stdout SHA256,
# stderr SHA256, readable reason). References are frozen independently of this run.
# All 94 mutants and 24 invalid invocations were executed and their named reasons
# checked against their source. Different checkers intentionally use different
# streams/formats. Exact fingerprints enforce those full contracts, including
# JSON structure/types, labels, counts, usage text, and empty/nonempty streams.
# No current failing output, generic exit code or broad regex creates a reference.
# Any source/runtime output drift fails closed and requires a reviewed amendment.
REJECTION_CONTRACTS = {
    ('A3/author_controls.py', ('--mutant', 'Z2')):
        (1, 'e04b2610f0b94857f65265e92fc2ef03f5d26c90e9bc76c87b0e60c3fe73bbe0', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'Z2-gain'),
    ('A3/author_controls.py', ('--mutant', 'Z3')):
        (1, '15364c942daeecd42584fc0cd28568908542950e96d8905c94a8fe387080d22f', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'Z3-drop'),
    ('A3/author_controls.py', ('--mutant', 'Z4')):
        (1, '5425d23fdf3ae54af74001f1d56f06b4cf9942d4d9258f9b26f84fcc52b2cfb3', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'Z4'),
    ('A3/author_controls.py', ('--bogus',)):
        (2, '034489f97f641cc1afed3ce1cbcd4e992ee86bd1ecb35605d27149c59e7f37c9', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '{"error": "unknown arguments"}'),
    ('A3_1/author_controls.py', ('--mutant', 'N1')):
        (1, 'bdae332b611455aadc8065ec8651cb09bb49f06a60eab73839052e6fcea5d757', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'N1'),
    ('A3_1/author_controls.py', ('--mutant', 'F1')):
        (1, '8f637a031d7176b4859ff503e98c661c0ed11c344637d4b9f043b3d75ca9148e', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'F1-linear'),
    ('A3_1/author_controls.py', ('--mutant', 'R1')):
        (1, '94f45519c4c9b5ed2f891377e7b4780e6fdacddf16544251b0a426baf2538d15', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'R1'),
    ('A3_1/author_controls.py', ('--mutant', 'C1')):
        (1, 'ab8c4393467bd87b70446711b78122408a74cf8954c3e3dd16b3f33fefab95b9', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'C1'),
    ('A3_1/author_controls.py', ('--mutant', 'H1')):
        (1, '15d71c1992177a1f8334ac678726414f9fe8bf50851f42f2b547e0935415aa20', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'H1; H1-global'),
    ('A3_1/author_controls.py', ('--bogus',)):
        (2, '034489f97f641cc1afed3ce1cbcd4e992ee86bd1ecb35605d27149c59e7f37c9', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '{"error": "unknown arguments"}'),
    ('A3_2/author_controls.py', ('--mutant', 'W1')):
        (1, '62a9beb4f697c0f2d86151c91a93c8f1de3056ea2bb22c178b30c69672ddd1e3', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W1-det'),
    ('A3_2/author_controls.py', ('--mutant', 'W3')):
        (1, 'fbea0daa327d6d93570ef86cea6365cd3a6ff27130c5eae4307c9d54ecc83f9b', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W3-psi-c'),
    ('A3_2/author_controls.py', ('--mutant', 'W4')):
        (1, '5dd21eff08c0b14b4f413c743f7ba3ef8e44e85ae496550d3271f39df6fedff8', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W4-hard'),
    ('A3_2/author_controls.py', ('--mutant', 'W4r')):
        (1, '3d62fdc97b4db41e301926538b642d03131dd2a7097a731a4c53fb02023f6da9', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W4-extreme'),
    ('A3_2/author_controls.py', ('--bogus',)):
        (2, '034489f97f641cc1afed3ce1cbcd4e992ee86bd1ecb35605d27149c59e7f37c9', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '{"error": "unknown arguments"}'),
    ('A3_3/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '1d40f29decb2fb7edc239f430921c1826267f40b1ea902ec4569d6b2526761e7', 'K1 BD(a) violated on the explicit instance (ratio 13225/6664)'),
    ('A3_3/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ab5b2910401dd46dcd01f5b8217bb506cdcf47956c01b4785ae9f02ce3d05a49', 'K2 BD(b) violated: n1=1 j=2 lhs=1 |c|=1'),
    ('A3_3/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '43a8d1f30540704886973e7bd777cafcbc0b8ca21e013f939eb0e026ecf2ff1d', 'K4 s^1 part is not the mixed block at entry (0,2)'),
    ('A3_3/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '0f33e6d22f652eb410cf4dfc6328cd166fa3de09babbf28e127bb86a587e29f6', 'K5 W3 bound violated: r=1/100 lam2=1 ratio=1380122500/60162641'),
    ('A3_3/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '3ae2328a110d8870008d319e30b02ed13bcd3602f027c5ba1c04bfa0f24a2645', 'K3 index additivity fails: (2,1) j=1'),
    ('A3_3/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '727a88582d0e4605f5fafcfc233dc55111bde6af3c12aaf17e1a9f65f697cf4a', 'usage: a33_exact.py [--mutant M1|M2|M3|M4|M5]'),
    ('A3_3/addendum_control_k5o.py', ('author_controls.py', '--mutant', 'W1')):
        (1, '0f36d669163dbaf123b5b862b84258e6c03385e1b5f05cda49948a409d1c7ca3', '5ad81e75571085c09eed3eac956968afe62463ca2352b4f2e3d8580e7c20e7bb', 'O2: W_r/r^4; O2: pin Hessians'),
    ('A3_3/addendum_control_k5o.py', ('author_controls.py', '--mutant', 'W2')):
        (1, '0f36d669163dbaf123b5b862b84258e6c03385e1b5f05cda49948a409d1c7ca3', 'cba682aa71052ef54aec90f0f7571579b0dd273762c2cf231fcf0982b08ad5d9', 'O2: W_r/r^4; O2: not ordered with lambda2 < 0; O2: pin Hessians'),
    ('A3_3/addendum_control_k5o.py', ('author_controls.py', '--mutant', 'W3')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '26eac1668d0a95fd54a36c92aeff13007a4a145dc3a3667f6ec836bec0cc6cd1', 'usage: a33_k5o.py PATH/a33_exact.py [--mutant W1|W2]'),
    ('A3_3/addendum_control_k5o.py', ()):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '26eac1668d0a95fd54a36c92aeff13007a4a145dc3a3667f6ec836bec0cc6cd1', 'usage: a33_k5o.py PATH/a33_exact.py [--mutant W1|W2]'),
    ('A3_4/author_controls.py', ('--mutant', 'N1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '8acd4b89cd7fac49fea480c701c5d79c6291bdea9558e66955ed5996c8eb8a1d', 'S1 spectral Jacobian fails: mu1=0 mu2=14/11 tau=-2/13'),
    ('A3_4/author_controls.py', ('--mutant', 'N2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '0d1941b2b1e8f1fcfd676bda8df6cf7bebb065c0b7dc94decc20fa6d516dfac6', 'S2 the monomial matrix at the lattice points is singular'),
    ('A3_4/author_controls.py', ('--mutant', 'N3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'b811a904b49d6d2ddc91698c011856f53acd1b41b97f36df308f8d8d5079cbab', 'S3 eigenframe jet formulas fail'),
    ('A3_4/author_controls.py', ('--mutant', 'N4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '66faa6cea9d23e2908f8f8bbbf4eda251cf8eb1c949d1edf5e152cdc4d3d9da4', 'S4 a_M + a_S != 12 lt'),
    ('A3_4/author_controls.py', ('--mutant', 'N5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '42645b1d864dde35dbed7465deea3ee17db948fd64e8dca32d882d89c2215258', 'S5 the strip integral is not of order delta^2: Lam=1/2 delta=1/2 ratio=397/144'),
    ('A3_4/author_controls.py', ('--mutant', 'N6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '75e7a9077ee5beed85ef3eec5a6b998f08a5596525a95dbf7a60a2e0b3ed3d4c', 'S2 the 20 contact functionals are not the distinct multi-indices of order <= 3'),
    ('A3_4/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ff172c1663e868f7cbd25928d384be3d46dd2f959d924bac2192c13f67b6aac2', 'usage: a34_exact.py [--mutant N1|N2|N3|N4|N5|N6]'),
    ('A3_4/author_controls.py', ('--mutant', 'N7')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ff172c1663e868f7cbd25928d384be3d46dd2f959d924bac2192c13f67b6aac2', 'usage: a34_exact.py [--mutant N1|N2|N3|N4|N5|N6]'),
    ('A3_4/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ff172c1663e868f7cbd25928d384be3d46dd2f959d924bac2192c13f67b6aac2', 'usage: a34_exact.py [--mutant N1|N2|N3|N4|N5|N6]'),
    ('A3_5/author_controls.py', ('--mutant', 'M1')):
        (1, '2c6ab7d931ca3a040117e5359616b63defd5ff7e3e95b2336fcc881c400962dc', 'fb7bdb03d16f56f9d947d8380e3d2416c56cb23f5f84a7cd52fbca5f3d732e6a', 'F2_FW2'),
    ('A3_5/author_controls.py', ('--mutant', 'M2')):
        (1, '44e0e82e0d69a2d424b1ca74a13dcc3647a1b0f3a4f6be5320ebe98eddce8bb7', '6c6ecda028a985c503ae735ff1520195c2efbec40573b4922117840e81594216', 'F2_FW1'),
    ('A3_5/author_controls.py', ('--mutant', 'M3')):
        (1, '925de071af2eeb04f9f62ccd73ca83b13c5bc31a3b8ff573b8d66b45115f3f9d', '6067508640a48e55fe45b1686c0a3053b4df05049beac6bb341729e3c2447cc9', 'D1_prop_D3'),
    ('A3_5/author_controls.py', ('--mutant', 'M4')):
        (1, '1a7ca14805737057103daa5c0045ee36459ddb40837b029fce6102d187b25115', 'cc4c2e10e6d1992b1f4c6245f225282029e3e8bcc8ce17e4933cb25d48d611e6', 'T1_frobenius'),
    ('A3_5/author_controls.py', ('--mutant', 'M5')):
        (1, '1a7ca14805737057103daa5c0045ee36459ddb40837b029fce6102d187b25115', 'f511c4c70a9c52e6f84d2a931907dd71927eb20e5aaf9972153b08b9c03334fe', 'G1a_inner_bound'),
    ('A3_5/author_controls.py', ('--mutant', 'M6')):
        (1, '1a7ca14805737057103daa5c0045ee36459ddb40837b029fce6102d187b25115', 'ccf2fe89fcfad2d6886fc309b99c3ff4017ed077ce144542222daabaaca4e29d', 'G2_exponents'),
    ('A3_5/author_controls.py', ('--mutant', 'M7')):
        (1, '1a7ca14805737057103daa5c0045ee36459ddb40837b029fce6102d187b25115', '36bd6fdab1e967a26ade00260cd111fdc9acaeb6ab6581eb66fbb01b8cdef927', 'D1_prop_D3'),
    ('A3_5/author_controls.py', ('--mutant', 'M8')):
        (1, 'c54b30aef280a5ee39d3979927d909cdb5d7a9598c458bdcfc8585f09d1a15cb', 'b5937f8dde1e7ff7e5df16e757977a71f845319df30d2ec3373db3ac75e2b753', 'F2_FW1'),
    ('A3_5/author_controls.py', ('--mutant', 'M9')):
        (1, '132abd915b426b3381bd0d45860ccbba3e73897b83b3fca26cdcac95ab4afafa', '42a8a5c652e734ed7ef37b73fb04b98f43c9a1d07b1980b565f3c60bffff5799', 'F2_FW2'),
    ('A3_5/author_controls.py', ('--mutant', 'M10')):
        (1, '9f82daa09adda5d24cf9c0adde4e22a35f2aedd710d7e82cb18aa7a1b3bc070e', 'c17e81d9ac6f1140c1e4a5464621ed1f38e89b318b33eb1cc4707f5b301d1f4b', 'F2_FW4'),
    ('A3_5/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '65b18625f68d8aa7b28667b23ea338d3b162126d20ea6477cc662f9246ba5cfe', 'usage: a35_exact.py [--mutant M1|...|M10]'),
    ('A3_5/author_controls.py', ('--mutant', 'M11')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '65b18625f68d8aa7b28667b23ea338d3b162126d20ea6477cc662f9246ba5cfe', 'usage: a35_exact.py [--mutant M1|...|M10]'),
    ('A3_6/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ac6b3ae6d76bd82dec6636b71bfcef44906c92a43b3a94f8a2800cb783b6a888', 'FAILED: X1_chart, X12_witness, X16_endpoint_chain'),
    ('A3_6/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '31dae24b868f836f9a9f4ddac102788d320a57594cde796c2af692a2acf7b26c', 'FAILED: X2_jacobian'),
    ('A3_6/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '137f71e7a1be90f405a9becb4d5b4ec0e67db661e93c781392096831a89c1470', 'FAILED: X5_elder_floor'),
    ('A3_6/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '12cbede6726c438a06b28c9db6b4fbee2099c74ae6d6d7bece81770c3b6fd717', 'FAILED: X7_radius'),
    ('A3_6/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '754f0674ace72d8f126243f08ec5c4069efe11ea751ee585269ec9add9198dfe', 'FAILED: X9_hardgap'),
    ('A3_6/author_controls.py', ('--mutant', 'M6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'd090a99859fbe57008b1a9fdc4952fc410da58163a6151ec2ab27840ddf48301', 'FAILED: X8_levelband'),
    ('A3_6/author_controls.py', ('--mutant', 'M7')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'b9d4a83f3b0f80aaa6f4cd9c1a3d6fae07dd7cfbc96f36a16ec83e97f4cc158f', 'FAILED: X11_ledgers'),
    ('A3_6/author_controls.py', ('--mutant', 'M8')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '44b7327fd1d6686f1577e04be5e4df2f6b54e7b6ab7eab5fa93b4324a70cde28', 'FAILED: X13_chord'),
    ('A3_6/author_controls.py', ('--mutant', 'M9')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'db57033261a452390cc359f24e523fe3b61834241b5cb0aad4132a3a4eb571c5', 'FAILED: X6_endpoint_floor'),
    ('A3_6/author_controls.py', ('--mutant', 'M10')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '7d637e942a5e2ca81f824a5a0adfb7c16983d563a5b405b0030cf8d059a7e058', 'FAILED: X14_coverage'),
    ('A3_6/author_controls.py', ('--mutant', 'M11')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '42b5323bf1b7a86bde8aff93beb03692b6ab8bb3ac499dd9a08b8dca6f3268ba', 'FAILED: X15_G3minus'),
    ('A3_6/author_controls.py', ('--mutant', 'M12')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '8865b9662578908c6efbd521ebc7cf81a95f437ae4c3787908f9ead73a15345c', 'FAILED: X17_inclusions'),
    ('A3_6/author_controls.py', ('--mutant', 'M13')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '678e7e25a484af0176e0cdf3481bc96d72710fcb92680662e4740f79a6952dca', 'FAILED: X13_chord'),
    ('A3_6/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '230b5ecba1d2582ee0d266ad94e94441c000ff845246535c4c88289d8c454610', 'usage: a36_exact.py [--mutant M1..M13]'),
    ('A3_6/author_controls.py', ('--mutant', 'M14')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '230b5ecba1d2582ee0d266ad94e94441c000ff845246535c4c88289d8c454610', 'usage: a36_exact.py [--mutant M1..M13]'),
    ('A3_6/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '230b5ecba1d2582ee0d266ad94e94441c000ff845246535c4c88289d8c454610', 'usage: a36_exact.py [--mutant M1..M13]'),
    ('A3_7/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'f1a2e4df0e9f6fcd9e0b5c0cc5e22e4fc75e6349c25cd3c2a3ad95297385a30b', 'FAILED: Y1_LB3prime'),
    ('A3_7/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'd7b443309b8b02c9ac37bef3e8971bcde1b4273b2760c5a7924156334066e4b3', 'FAILED: Y2_MB3'),
    ('A3_7/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'e8ac6a8e2e09aab66b1b991f4b829bd48659d8f2583290c8be22c2e7eb908169', 'FAILED: Y2_MB3'),
    ('A3_7/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'fa8620cec75b4e1220e05273f7099b6d277569942ade99e021e1bd9bbed77b6a', 'FAILED: Y3_LE3_margin'),
    ('A3_7/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '30679a441a94a9f0735e7223b452837926508c63421ad328a5444995684eb6a5', 'FAILED: Y3_LE3_margin'),
    ('A3_7/author_controls.py', ('--mutant', 'M6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6365ec18e6699d99164c5d855dd193b47d93f4a5321de7d7cd6fe53e9843e973', 'FAILED: Y4_LE3_taylor'),
    ('A3_7/author_controls.py', ('--mutant', 'M7')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '79d9bb9208131642fcfb2a313737c911dfe94c2a1671fb4a94b398dbe7423de9', 'FAILED: Y5_B3'),
    ('A3_7/author_controls.py', ('--mutant', 'M8')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '405b690812c0bfa5a29225a76418d7ae67aa4998a551c8db70a9979ceca0ba99', 'FAILED: Y6_corLE3'),
    ('A3_7/author_controls.py', ('--mutant', 'M9')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2c5a53d765f73d0fd3f2c7e1c5e10f720aaa927ded56ed4ba45d8d0d2d91d780', 'FAILED: Y7_ledgers'),
    ('A3_7/author_controls.py', ('--mutant', 'M10')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '4072f5dbc106e536950f7c0c7ec751ecc1a3b6d5a6002dd69d267c4d4062263a', 'FAILED: Y7_ledgers'),
    ('A3_7/author_controls.py', ('--mutant', 'M11')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'e15876074185e9a7089a6e1ab05e3d950a2d31d57e6d9774b9e5f2289e5f63a8', 'FAILED: Y8_A36_riders'),
    ('A3_7/author_controls.py', ('--mutant', 'M12')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'e4b4060075d92a81e29cb66b5de5a4001440b051ea2cecd8fdf8bcac50c1374a', 'FAILED: Y8_A36_riders'),
    ('A3_7/author_controls.py', ('--mutant', 'M13')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'a17fe1d763672006b91ba0896d0436263ca37353c9f35a949ad28ab560c7b21a', 'FAILED: Y8_A36_riders'),
    ('A3_7/author_controls.py', ('--mutant', 'M14')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'b9e3132356a548097f82336a297e5688bd0a65859c3db40c7db44b981630870b', 'FAILED: Y8_A36_riders'),
    ('A3_7/author_controls.py', ('--mutant', 'M15')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '711a5938a697c8fb693d00b89f3ccad8a4949df6c0a0e35f6c1a523a8c8db78b', 'FAILED: Y8_A36_riders'),
    ('A3_7/author_controls.py', ('--mutant', 'M16')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'b04a202f970b0d6ffb009a62b5fc8460cc8f608c15bb1191ed9115e866b1b0f6', 'FAILED: Y8_A36_riders'),
    ('A3_7/author_controls.py', ('--mutant', 'M17')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'e76827691d6b12b9d3ed8bcf0fd26218ffd816d820097d8d991f01b5c47f8676', 'FAILED: Y8_A36_riders'),
    ('A3_7/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '9d9813cf155e101b90f6dd6059f08bb586a8e5b70489940093f87631e81af5f8', 'usage: a37_exact.py [--mutant M1..M17]'),
    ('A3_7/author_controls.py', ('--mutant', 'M18')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '9d9813cf155e101b90f6dd6059f08bb586a8e5b70489940093f87631e81af5f8', 'usage: a37_exact.py [--mutant M1..M17]'),
    ('A3_7/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '9d9813cf155e101b90f6dd6059f08bb586a8e5b70489940093f87631e81af5f8', 'usage: a37_exact.py [--mutant M1..M17]'),
    ('A3_8/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '7ad5390e33f1329074d928186dd85957b93f4b8cb83635718b1eb267a81d1387', 'FAILED: Z1_QFE3_ledger'),
    ('A3_8/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2a6fddef0cbd9f28b6e67222454b1595670a45a767da521445a4947b0dc91c70', 'FAILED: Z1_QFE3_ledger'),
    ('A3_8/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'f2026cc8cfcd422d29a813a5f4882ccbdc655c16ea24d8f4f6727dd9edfbb9ad', 'FAILED: Z2_ER3_monomials'),
    ('A3_8/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'aa35b5662d8532ac554ac67431d59c78ffaa7da170ad5c2785d696270562fd36', 'FAILED: Z3_MB3_coverings'),
    ('A3_8/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'b80a278515df0e172200cc7c753131c30808b3b9527f02ef82d6b877f36d3ae5', 'FAILED: Z3_MB3_coverings'),
    ('A3_8/author_controls.py', ('--mutant', 'M6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '263110702402e75795453df6f35a534d43fca9530a738dc8e78ca641cbff821e', 'FAILED: Z4_H_integrals'),
    ('A3_8/author_controls.py', ('--mutant', 'M7')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '393c6bd23757da264807b8c37f77270ca4027c904b03138c87eca8a1f9c70fe8', 'FAILED: Z4_H_integrals'),
    ('A3_8/author_controls.py', ('--mutant', 'M8')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '9d530affd5ca846ed06743995388aeb515c0b70e7385212e5a16b621b7b41521', 'FAILED: Z5_PQS_facts'),
    ('A3_8/author_controls.py', ('--mutant', 'M9')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'bd0d1b31af615ef91d2afa03b842f46dc51f35cc97efcd48d2749adceb53d28d', 'FAILED: Z5_PQS_facts'),
    ('A3_8/author_controls.py', ('--mutant', 'M10')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '574efaeaef4c0725872a92dcbe94c378af2b7088c830ed033dbff9f7deef479e', 'FAILED: Z6_tails_algebra'),
    ('A3_8/author_controls.py', ('--mutant', 'M11')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'bcfa5f90ef1098d91f5714c63573cf5f6cb866d063124197a59827f5baa5dab2', 'FAILED: Z6_tails_algebra'),
    ('A3_8/author_controls.py', ('--mutant', 'M12')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'cc643cb47ccd9407d740b8ef4ddd3b72902c01ee4d356550b61ed2c796188cf4', 'FAILED: Z7_fixed_Lambda'),
    ('A3_8/author_controls.py', ('--mutant', 'M13')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'e734db56e4a165ea11c758100382a1c31b3e83eae5646c0fa9ac20aaf6b1ae6f', 'FAILED: Z6_tails_algebra'),
    ('A3_8/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'bb868414b248aff7a6f489b530c91448227ca6a7f9faac2b5ef0837c8642a4a6', 'usage: a38_exact.py [--mutant M1..M13]'),
    ('A3_8/author_controls.py', ('--mutant', 'M14')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'bb868414b248aff7a6f489b530c91448227ca6a7f9faac2b5ef0837c8642a4a6', 'usage: a38_exact.py [--mutant M1..M13]'),
    ('A3_8/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'bb868414b248aff7a6f489b530c91448227ca6a7f9faac2b5ef0837c8642a4a6', 'usage: a38_exact.py [--mutant M1..M13]'),
    ('A3_10/ledger_control.py', ('RATE_THIRD',)):
        (1, '2a568acce360350d2709db8dc00aaea13e0c42782a83d399b37a8ac2028f14ea', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'FAIL beta=1/10: relative error l^(beta/3)'),
    ('A3_10/ledger_control.py', ('LOG_HALF',)):
        (1, 'a46557a2f9ed64678d0a9d58c06f59249f30de07158a55686778121d7e2e0067', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'FAIL log bound at x=1, log k_+=1'),
    ('A3_10/ledger_control.py', ('CUM_HALF',)):
        (1, 'ef2521b703521bebb2f806242b441dc458dfe40b68d9f4c9756b4d651fc5e131', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'FAIL cumulative constant 1/(5/3) = 3/5'),
    ('A3_10/ledger_control.py', ('MOM_2000',)):
        (1, '567d0ead36c53a883fffa02bb2a0c0973cf37d15ba15eafa38960d77874cd570', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'FAIL the moment constant 2000 exceeds 24579/8'),
    ('A3_10/ledger_control.py', ('BOGUS',)):
        (2, 'a0758636c5e479dfd217fb60eadb689f69c39901577d819a78384952bb8a1762', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'unknown mutant label: BOGUS'),
    ('A3_11/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'a77e8384e66f898ba45d3a4810e5e5bc1d3b28ad784af5d5f135352f8bd171b6', 'FAILED: Z1_lemma11_constants'),
    ('A3_11/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '604d8f22fdb1a67c8231e77e776938aaf16292cd7a1b4380dffc927c80978109', 'FAILED: Z2_cubic_identities'),
    ('A3_11/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '5ecca1ca498c6c4094b41ea30e78b9f5ed5df65fbe3c179380f12df4db49ab33', 'FAILED: Z3_sublayer_integrals'),
    ('A3_11/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'e079f7298a2d567e16994282f94e74bddb21ff1966408caf14ffc91c93614edb', 'FAILED: Z4_margin_totals'),
    ('A3_11/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6b426aa8ab5e101a74e2a81387b5a31f50c7d7400c91a533423d4a7a23f93a94', 'FAILED: Z5_endpoint_shell'),
    ('A3_11/author_controls.py', ('--mutant', 'M6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '259b4d66f6781e516659d415cb653edb0702df9a69342ab0ac571234019c7b82', 'FAILED: Z6_shell_sums'),
    ('A3_11/author_controls.py', ('--mutant', 'M7')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '3d0d876a9813ef9cb20a9cd614b1ffddabc5a562ab5b9db5c4879673d74245d6', 'FAILED: Z7_exponent_tables'),
    ('A3_11/author_controls.py', ('--mutant', 'M8')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '022bd5032dcb504ce8a8fa9a14756161798113bfbe6a9edb5cec6f817b2e6f0d', 'FAILED: Z8_pd3_constants'),
    ('A3_11/author_controls.py', ('--mutant', 'M9')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '5f4083546fe7c72bc96b9d629bbe73aa8ffb4c125020b038179e7cf2424a00ed', 'FAILED: Z9_numeric_band'),
    ('A3_11/author_controls.py', ('--mutant', 'M10')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '604d8f22fdb1a67c8231e77e776938aaf16292cd7a1b4380dffc927c80978109', 'FAILED: Z2_cubic_identities'),
    ('A3_11/author_controls.py', ('--mutant', 'M11')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '022bd5032dcb504ce8a8fa9a14756161798113bfbe6a9edb5cec6f817b2e6f0d', 'FAILED: Z8_pd3_constants'),
    ('A3_11/author_controls.py', ('--mutant', 'M12')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '5ecca1ca498c6c4094b41ea30e78b9f5ed5df65fbe3c179380f12df4db49ab33', 'FAILED: Z3_sublayer_integrals'),
    ('A3_11/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'fa4348e128f06303b2347e387c87329662df0d75709c78795dd39a104fa940a0', 'usage: a311_exact.py [--mutant M1..M12]'),
    ('A3_11/author_controls.py', ('--mutant', 'M13')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'fa4348e128f06303b2347e387c87329662df0d75709c78795dd39a104fa940a0', 'usage: a311_exact.py [--mutant M1..M12]'),
    ('A3_11/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'fa4348e128f06303b2347e387c87329662df0d75709c78795dd39a104fa940a0', 'usage: a311_exact.py [--mutant M1..M12]'),
}

# Replacing A3.6's 5/4 by 1/4 with MUT=None omits the usual mutant-description line.
# This separately executed altered-source control must fail specifically at X9.
NEGATIVE_HARDGAP = (1, hashlib.sha256(b'').hexdigest(),
                    hashlib.sha256(b'FAILED: X9_hardgap\n').hexdigest(), 'X9_hardgap')


def check_rejection(result, expected):
    """Compare both full captured streams, not a permissive failure-message pattern."""
    code, out, err = result
    failures = []
    if type(code) is not int or code != expected[0]:
        failures.append('wrong exit code')
    if type(out) is not bytes or hashlib.sha256(out).hexdigest() != expected[1]:
        failures.append('stdout differs from intended diagnostic')
    if type(err) is not bytes or hashlib.sha256(err).hexdigest() != expected[2]:
        failures.append('stderr differs from intended diagnostic')
    return failures


def rejection_inventory_failures(manifest):
    listed = {}
    for obj in manifest['objects']:
        for replay in obj['replays']:
            for kind, code in (('mutants', 1), ('invalid', 2)):
                for args in replay[kind]:
                    key = replay['script'], tuple(args)
                    if key in listed:
                        return ['duplicate rejection invocation: ' + repr(key)]
                    listed[key] = code
    if set(listed) != set(REJECTION_CONTRACTS):
        return ['rejection invocation inventory differs from frozen contracts']
    if any(REJECTION_CONTRACTS[key][0] != code for key, code in listed.items()):
        return ['rejection invocation category differs from frozen contracts']
    return []


def report_control(script, args, result, reason):
    code, out, err = result
    print(json.dumps(dict(script=script, args=list(args), returncode=code,
                          stdout_sha256=hashlib.sha256(out).hexdigest(),
                          stderr_sha256=hashlib.sha256(err).hexdigest(),
                          expected_reason=reason), sort_keys=True))


def identity(data):
    return len(data), hashlib.sha256(data).hexdigest()


def interpreter_flags():
    flags = ['-B']
    if sys.flags.optimize:
        flags.append('-O')
    if sys.flags.no_site:
        flags.append('-S')
    return flags


def tree_failures(root, manifest):
    failures = []
    listed = {}
    for obj in manifest['objects']:
        for f in obj['stored']:
            listed[f['path']] = (f['bytes'], f['sha256'])
    present = set()
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            failures.append('symlink: ' + rel)
        elif path.is_file():
            present.add(rel)
    for rel in sorted(present ^ (set(listed) | OWN)):
        failures.append(('unlisted file: ' if rel in present else 'missing file: ') + rel)
    for rel, ident in sorted(listed.items()):
        if rel in present and identity((root / rel).read_bytes()) != ident:
            failures.append('identity mismatch: ' + rel)
    return failures


def extraction_failures(root, manifest):
    """Re-extract every script and stdout from its stored source comment and compare with the stored payloads."""
    failures = []
    for obj in manifest['objects']:
        extracted = [f for f in obj['stored'] if 'extracted_from' in f]
        for script in [f for f in extracted if f['path'].endswith('.py')]:
            stdout = [f for f in extracted if f['extracted_from'] == script['extracted_from']
                      and f['heading'] == script['heading'] and not f['path'].endswith('.py')]
            if len(stdout) != 1:
                failures.append('%s: no single stdout record for %s' % (obj['tag'], script['path']))
                continue
            stdout = stdout[0]
            fence = {'json': 'json', 'txt': 'text'}.get(stdout['path'].rsplit('.', 1)[-1])
            if fence is None:
                failures.append('%s: unsupported stdout suffix for %s' % (obj['tag'], stdout['path']))
                continue
            body = (root / script['extracted_from']).read_text(encoding='utf-8')
            if body.count(script['heading']) < 1:
                failures.append('%s: heading %r not found in %s' % (obj['tag'], script['heading'], script['extracted_from']))
                continue
            section = body[body.index(script['heading']):]
            m1 = re.search(r'```python\n(.*?)\n```\n', section, re.S)
            m2 = re.search(r'```%s\n(.*?)\n```\n' % fence, section[m1.end():], re.S) if m1 else None
            if not (m1 and m2):
                failures.append('%s: fences not found after %r' % (obj['tag'], script['heading']))
                continue
            if (m1.group(1) + '\n').encode('utf-8') != (root / script['path']).read_bytes():
                failures.append('%s: %s differs from the payload in %s' % (obj['tag'], script['path'], script['extracted_from']))
            if (m2.group(1) + '\n').encode('utf-8') != (root / stdout['path']).read_bytes():
                failures.append('%s: %s differs from the payload in %s' % (obj['tag'], stdout['path'], stdout['extracted_from']))
    return failures


PROCESS_TIMEOUT_SECONDS = 1800  # Unchanged production budget; tests shorten it for real timeout children.


def evidence_directory(script):
    """An explicit destination opts in; never put generated evidence in source directories."""
    raw = os.environ.get('QS_REPLAY_EVIDENCE_DIR')
    if raw is None:
        return None
    if not raw:
        raise ValueError('QS_REPLAY_EVIDENCE_DIR must not be empty')
    root = pathlib.Path(raw).expanduser().resolve()
    if root.is_relative_to(HERE.resolve().parents[1]) or root.is_relative_to(script.parent.resolve()):
        raise ValueError('QS replay evidence must be outside the checkout and child source directory')
    root.mkdir(parents=True, exist_ok=True)
    return pathlib.Path(tempfile.mkdtemp(prefix='invocation-', dir=root))


def save_process_evidence(folder, record, out, err):
    """Attempt every write independently. None is unavailable, not an observed empty stream."""
    record['streams'] = {}
    record['evidence_errors'] = []
    for name, data in (('stdout', out), ('stderr', err)):
        entry = dict(available=data is not None, bytes=len(data) if data is not None else None,
                     sha256=hashlib.sha256(data).hexdigest() if data is not None else None, saved=False)
        record['streams'][name] = entry
        try:
            (folder / (name + '.bin')).write_bytes(data if data is not None else b'')
            entry['saved'] = True
        except Exception as exc:
            record['evidence_errors'].append('%s.bin: %s: %s' % (name, type(exc).__name__, exc))
    try:
        data = (json.dumps(record, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')
        (folder / 'process.json').write_bytes(data)
    except Exception as exc:
        record['evidence_errors'].append('process.json: %s: %s' % (type(exc).__name__, exc))


def run(script, *args):
    command = [sys.executable, *interpreter_flags(), str(script), *args]
    folder = evidence_directory(script)  # Invalid/unwritable setup stops before starting a child.
    record = dict(schema=1, command=command, cwd=str(script.parent),
                  timeout_seconds=PROCESS_TIMEOUT_SECONDS, scientific_effect='NONE')
    try:
        proc = subprocess.run(command, capture_output=True, timeout=PROCESS_TIMEOUT_SECONDS,
                              cwd=str(script.parent))
    except (subprocess.TimeoutExpired, OSError) as exc:
        if folder is not None:
            record.update(status='timeout' if isinstance(exc, subprocess.TimeoutExpired) else 'spawn_error',
                          returncode=None, exception=dict(type=type(exc).__name__, message=str(exc)))
            exc.evidence_record = record
            try:
                save_process_evidence(folder, record, getattr(exc, 'stdout', None), getattr(exc, 'stderr', None))
                if record['evidence_errors']:
                    exc.add_note('QS replay evidence errors: ' + '; '.join(record['evidence_errors']))
            except Exception as secondary:
                exc.add_note('QS replay evidence recording failed: %s: %s' % (type(secondary).__name__, secondary))
        raise  # Never replace the primary timeout or launch error with a recording error.
    if folder is not None:
        record.update(status='completed', returncode=proc.returncode, exception=None)
        save_process_evidence(folder, record, proc.stdout, proc.stderr)
        if record['evidence_errors']:
            exc = RuntimeError('QS replay evidence errors: ' + '; '.join(record['evidence_errors']))
            exc.evidence_record = record
            raise exc  # Even exit 0 is not success when explicitly required evidence is missing.
    return proc.returncode, proc.stdout, proc.stderr


def replay_failures(root, manifest):
    failures = rejection_inventory_failures(manifest)
    if failures:
        return failures  # Do not execute an incomplete/changed control inventory.
    for obj in manifest['objects']:
        for replay in obj['replays']:
            label = '%s %s' % (obj['tag'], replay['name'])
            script = root / replay['script']
            code, out, err = run(script, *replay['args'])
            baseline_failures = []
            if code != 0:
                baseline_failures.append('%s: exit code %s' % (label, code))
            if out != (root / replay['stdout']).read_bytes():
                baseline_failures.append('%s: stdout differs from the published bytes' % label)
            if err:
                baseline_failures.append('%s: unexpected baseline stderr' % label)
            if baseline_failures:
                failures.extend(baseline_failures)
                continue
            report_control(replay['script'], replay['args'], (code, out, err), 'exact published baseline')
            for kind in ('mutants', 'invalid'):
                for args in replay[kind]:
                    expected = REJECTION_CONTRACTS[replay['script'], tuple(args)]
                    result = run(script, *args)
                    mismatches = check_rejection(result, expected)
                    failures.extend('%s %r: %s' % (label, args, why) for why in mismatches)
                    if not mismatches:
                        report_control(replay['script'], args, result, expected[3])
    return failures


def negative_control_failures(root, manifest):
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'packet'
        shutil.copytree(root, copy, symlinks=True)
        target = copy / 'A3_6' / 'PROOF.md'
        data = bytearray(target.read_bytes())
        data[100] ^= 0x01
        target.write_bytes(bytes(data))
        if 'identity mismatch: A3_6/PROOF.md' not in tree_failures(copy, manifest):
            failures.append('negative control: a one-byte change to A3_6/PROOF.md was not detected')
        script = copy / 'A3_6' / 'author_controls.py'
        text = script.read_text(encoding='utf-8')
        old = 'coef = F(1, 4) if MUT == "M5" else F(5, 4)'
        if text.count(old) != 1:
            failures.append('negative control: the hard-gap coefficient line was not found exactly once')
        else:
            script.write_text(text.replace(old, 'coef = F(1, 4) if MUT == "M5" else F(1, 4)'), encoding='utf-8')
            result = run(script)
            mismatches = check_rejection(result, NEGATIVE_HARDGAP)
            failures.extend('negative control: changed hard-gap constant: ' + why for why in mismatches)
            if not mismatches:
                report_control('A3_6/author_controls.py', [], result, 'changed 5/4 to 1/4: X9_hardgap')
    return failures


def main():
    manifest = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    failures = tree_failures(HERE, manifest)
    if not failures:
        failures = extraction_failures(HERE, manifest)
    if not failures:
        failures = replay_failures(HERE, manifest)
    if not failures:
        failures = negative_control_failures(HERE, manifest)
    n_scripts = sum(len(o['replays']) for o in manifest['objects'])
    n_mut = sum(len(r['mutants']) for o in manifest['objects'] for r in o['replays'])
    n_inv = sum(len(r['invalid']) for o in manifest['objects'] for r in o['replays'])
    n_files = sum(len(o['stored']) for o in manifest['objects'])
    mode = ' '.join(interpreter_flags())
    if failures:
        for f in failures:
            print('FAIL ' + f)
        print('QS d = 3 chain (A3-A3.11) incorporation replay (%s): %d failure(s)' % (mode, len(failures)))
        return 1
    print('QS d = 3 chain (A3-A3.11) incorporation replay (%s): %d stored identities, %d extractions, %d checker stdouts, '
          '%d mutants, %d invalid invocations and 2 negative controls PASS' % (mode, n_files, 2 * n_scripts, n_scripts, n_mut, n_inv))
    return 0


if __name__ == '__main__':
    sys.exit(main())
