# C293 final exact-artifact nonauthor review

Date: 2026-10-18 UTC. Reviewer: OpenAI Codex delegated agent
`/root/c292_geometry_review`, for Dylan Roy.

**Verdict: ACCEPT_SCOPED_FORMAL.** The exact deterministic theorem
`TorusMorseFinite.quotientCriticalSet_finite` is accepted within the local source,
frozen build, complete declared-module axiom census, standard named-module kernel
replay, and negative-control scope documented below. No main-proof amendment is
required. This verdict is not acceptance of the remaining C292 geometry, a
Gaussian almost-sure theorem, hosted execution of these new modules, publication,
private custody, or scientific promotion. The final master artifact verifier is
a separate engineering gate; its pre-run review finding is recorded below.

## Reviewer exposure and work performed

I am a nonauthor of `MorseFiniteCritical.lean`, the controls, audit module, final
runner/preparer, and final master. I previously reviewed C292's conventional
proof, conducted a read-only feasibility audit for the present finite-critical
dependency, and suggested prospective controls. I saw the intended claim and
possible dependency routes before implementation. I read the complete main
source only after its freeze announcement, then the complete frozen controls and
audit sources after separate authorization. This is substantive nonauthor review
with disclosed source/design exposure, not blind or provider-distinct review.
The author and reviewer are both OpenAI agents: organizational-independence
credit **0**, human-review credit **0**.

This review incorporates the unchanged main-source reasoning in
`reviews/MAIN_SOURCE_REVIEW.md`, 16919 bytes, SHA-256
`105e6b528746110b5582dd4626f7055f1cc2869106c51974409c55c68dfb49c4`.
I reviewed the relevant complete literal definitions and quotient constructions
in the exact upstream inputs; the main source, controls and audit in full; the
full final runner/preparer/sequence/negative runner; the eight terminal receipts
and their stream identities; the complete raw axiom output; and the actual
negative-control diagnostic. I independently read and compared local source,
inventory, receipt, stream, and object bytes using read-only commands. I did not
rerun Lean, leanchecker, the final sequence, negative control, preparation, or the
master. I made no source-proof edits and no remote posts.

Paths below are relative to
`$C293_ROOT`.

## Bound source and execution identities

The final inventory is `FINAL_SOURCE_INVENTORY.json`, 2421 bytes, SHA-256
`f1a429935146b4e406e9ba8cc9ff8b84f7d40c22cc4fea74920dfc013c4911de`.
I recomputed this identity and checked that both `project/` and `final-project/`
contain the following exact source bytes. No change to the main proof occurred
between source review and final execution.

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `Lifetime.lean` | 51383 | `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6` |
| `TorusTopology.lean` | 12257 | `ddb145b3f791c181d4f2a51e54e711937297bd6476ba55bcd5252b7ddb57cfe1` |
| `MorseFiniteCritical.lean` | 9445 | `95a660134eda49eecfe6181884bd23b4e4ca210e228d2463de29e5f821df047b` |
| `MorseFiniteControls.lean` | 2843 | `e6171c949ec60a3aea21a8cc028180e16c82e4946a232107d9e82bf8018cdac1` |
| `MorseFiniteAxiomAudit.lean` | 3025 | `326a1cab271bf46a1c7db750ee1565e08dc4856c62e0abce3f5c9f90d923ce9d` |

`SOURCE_INPUTS.json` remains SHA-256
`6554ae0e27dd7a3bf9e280939710dff8948b6aef636c3920526668ccde299e0e`.
It binds Lifetime to Math- cut `db43694c9f9dbff2987e2e3c0a1260b5c48310ec`,
path `frontiers/source_lifetime_realization_20261017/inputs/Lifetime.lean`,
blob `f2508f7f2e3fd42f22f5aa52bc5ead5ff9e73b9a`; TorusTopology to cut
`c8ec07034608741585111603f1b506393c340908`, path
`companions/torus_filtration_20261011/TorusTopology.lean`, blob
`ed678ea322fe5315b3aaff44e4e2f06b018399d8`. This review did not freshly fetch
those upstream objects. Their local byte identity and earlier source custody are
separate from the mathematical proof analysis.

| Execution artifact | SHA-256 |
| --- | --- |
| `run_final_phase.py` | `e9b7bd0caa19889e2ba0974c788e13a573645fd3c0839890eee41bbf15831b23` |
| `prepare_final_inputs.py` | `72bbe39334fa2a7b09d621f81f6211e9a4019804b949f4ea2576e1c4f2927451` |
| `run_final_sequence.py` | `8cb8a75b384c0c84f1a000f217616a3d99710b34bf2e04237b65f220ff9302ce` |
| `FINAL_SEQUENCE_RESULT.json` | `80c3241fb619c9b250826c233bd927d6767d341977c9563a58984e20d299d9b3` |
| `FINAL_DEPENDENCY_ARTIFACTS.json` | `4e35e91a0b6f334eb6ad41e586b9704189e7063722d9c2e5f6a87f0839af0d21` |
| pinned Lean executable | `1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554` |
| pinned standard leanchecker executable | `cfde41cb11dde58c84e9c60c551fd104bb2fc1104ad44dca932a923120272a35` |

The runtime is the existing Lean 4.34.1 darwin_aarch64 runtime under
`$LEAN_RUNTIME`.
The Mathlib source/API pin is `d13f23b723b8a846827a245b89c10fc7d3f11612`.

## Exact mathematical statement and reconstruction

The endpoint quantifies over `d : ℕ`, `L : ℝ`, `hL : 0 < L`, and
`g : EuclideanSpace ℝ (Fin d) → ℝ`. The hypotheses are the literal Lifetime
predicates `IsSmooth d g`, `IsLPeriodic d L g`, and `IsMorseDistinct d L g`.
The conclusion is finiteness of

```lean
torus_proj d L hL '' {x : E d | IsCriticalPoint d g x}
```

on TorusTopology's actual period-lattice quotient. The core theorem needs only
the nondegeneracy clause of Morse-distinct: every critical point has some literal
Hessian inertia. Distinct heights are correctly unused. Natural dimension zero
is allowed, so the intended positive-dimensional C292 application is included.
No finite event list, local inverse, isolatedness, closedness, desired path,
death/elder relation, pairing, or count conclusion is assumed.

I checked each step of the source rather than inferring correctness from hashes
or successful execution:

1. `literal_hessian_eq_fderiv` identifies the literal iterated second Fréchet
   derivative with D(Dg)(x), in the proper argument order.
   `literal_hessian_symmetric` derives symmetry from C2 smoothness. The inertia
   definition itself does not assert symmetry.
2. For B=D(Dg)(x), a vector z in its kernel is decomposed as v+w in the
   complementary negative and positive subspaces. Evaluating Bz=0 on v and w,
   and using symmetry of cross terms, gives B(v,v)=B(w,w). Strict negative and
   positive signs force v=w=0, including the zero-component cases. This proves
   injectivity without any false orthogonality assumption. The unused dimension
   equalities in inertia do not undermine this argument.
3. The actual codomain of D(Dg)(x) is the continuous dual. The real Riesz
   equivalence converts B to an injective endomorphism of finite-dimensional E;
   `LinearEquiv.ofInjectiveEndo` and finite-dimensional continuity produce the
   actual continuous linear equivalence E ≃L continuous-dual(E). Equality with
   B is proved, not supplied as a certificate.
4. C2 regularity makes Dg C1. The inverse function theorem provides an open
   neighborhood on which Dg is injective, so its zero x is an isolated literal
   critical point. This uses no Morse normal form.
5. Literal lattice periodicity of g implies periodicity of Dg through the
   translation derivative identity. The lattice-vector formulas match exactly.
   The derivative therefore descends to the actual quotient as a continuous
   function to the fixed continuous dual.
6. The full image of literal critical points is proved equivalent to the zero
   set of the descended derivative. Surjectivity establishes the reverse
   inclusion. This makes the image closed without an invalid “continuous images
   of closed sets are closed” inference.
7. If U isolates a critical representative x, the open image π(U) isolates π(x)
   in the quotient critical set. For a critical class represented by y in U,
   the zero-set equivalence makes y itself critical, hence y=x. This uses
   saturation of criticality and does not require π to be injective on U.
8. The closed critical set is compact in the compact actual torus and is
   discrete by the preceding step. `IsCompact.finite` gives the conclusion.
   Thus the full finite-quotient result is derived, not just bilinear arithmetic
   or isolatedness on Euclidean space.

This is the closed/discrete derivative-descent route. It validly replaces the
prospective compact-parallelepiped route. There is no missing half-open-domain
boundary argument. The main theorem does not claim the periodically repeated
Euclidean critical set is finite.

## Frozen execution and object chain

`evidence/FINAL_BUILD_INITIALIZATION.json` records a newly created empty
`final-build/`; its SHA-256 is
`685830dc40fce94cabe10e4296a4a0eecced5afb782105c2828bd748dda59dff`.
The sequence contains exactly five ordered builds and three ordered new-module
kernel replays. Every terminal receipt records exit 0, no timeout, a reaped
process, exact frozen source maps before/after, unchanged imported objects,
the same inventory and runner hashes, and the correct executable identity.
I checked the receipt object maps form a chain starting empty and that all
current final object bytes match that chain.

| Phase | Run directory under `final-runs/` | Seconds | Terminal receipt SHA-256 |
| --- | --- | ---: | --- |
| build Lifetime | `20261018T025721Z-build-Lifetime-27665937` | 101.482 | `0c7f8c69c7eab4bcff5a507a37bc5ddfd191b6cac3567155b3594f7d0a69436f` |
| build TorusTopology | `20261018T025903Z-build-TorusTopology-7b11c9cf` | 100.614 | `21f63788ea07913666bb6ab2ab5c961174dd6787bd2af2f3fa14e8b3490bdf8b` |
| build MorseFiniteCritical | `20261018T030043Z-build-MorseFiniteCritical-84e29842` | 99.617 | `e42f724b4b6d976a00a4a2b37f874c504c4b2f127744e2456c2cc905812d78b2` |
| build MorseFiniteControls | `20261018T030223Z-build-MorseFiniteControls-b481974d` | 108.027 | `ed1bcedb2449d22777a4e5f4e88a0f1aa8e74fddf5a7821d599a4902c2227fcb` |
| build MorseFiniteAxiomAudit | `20261018T030411Z-build-MorseFiniteAxiomAudit-53575871` | 173.752 | `7d9ed09f2663e857207fa18a4c82342efa8c3f72458102d1c39b0396aad86dc4` |
| kernel MorseFiniteCritical | `20261018T030705Z-kernel-MorseFiniteCritical-d446fa38` | 86.456 | `b8892c46f304a0a9e38297c9c482e6a3c0840aeae4ee4993b96aee75f1b9723c` |
| kernel MorseFiniteControls | `20261018T030832Z-kernel-MorseFiniteControls-22a2daa0` | 88.140 | `177eb12fefb8d0a623a67f32e15cfa5267d862fc616a2d908cbebada0b13cda4` |
| kernel MorseFiniteAxiomAudit | `20261018T031000Z-kernel-MorseFiniteAxiomAudit-ba7cdd21` | 89.365 | `7399c066c1e7dc544a23ded914c8f8c867d67bb93c1878bacba3fd944990769e` |

All three new builds used `-DwarningAsError=true`. The four non-audit builds
have empty stdout and stderr; the audit stderr is empty and stdout is the actual
census. Each kernel stdout says `replaying` the correct named module, stderr is
empty, and the command is the pinned `leanchecker -v Module`. Stream bytes match
their receipt hashes. I did not treat the sequence summary's PASS string alone
as sufficient evidence.

| Final object | SHA-256 |
| --- | --- |
| `Lifetime.olean` | `b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4` |
| `TorusTopology.olean` | `ccb13e9469d55da8b5202706a1f013fa7a2755b2184542b8a0534f722d993125` |
| `MorseFiniteCritical.olean` | `34ff2a9ed529609dd48a22204b8eacc66eeb943805e2d6e8dee4481cde8ef4e2` |
| `MorseFiniteControls.olean` | `5eebfbb98a8cb05ac420d260dd08461ac037b2e086620fe79ee330defd345efa` |
| `MorseFiniteAxiomAudit.olean` | `3c3f30110ec4a3c0a0c1ba6f1769634d0c04bfc4e444ab1bcfd46c5dffa4ff4b` |

Execution scope is **local fresh compilation of these five sources, followed by
standard replay of the three named new modules against imported dependencies**.
It is not `--fresh` replay of every imported Mathlib declaration, an external
verifier, or a provider-independent repeat. The recorded LEAN_PATH starts at
`final-build/`, then the pinned dependency cache; no development build enters it.

The authenticated dependency inventory contains 83897 unique artifacts totaling
8418477755 bytes. Preparation and all before/after phase checks report reuse of
all 83897 earlier byte hashes at unchanged size/mtime_ns/inode, with zero
metadata-delta rehashes. This is explicitly **not a fresh full-content hash of
the shared dependency cache**. The exact runtime/manifests and pathset checks
provide the documented cooperative execution boundary; they are not protection
against hostile same-UID mutation that restores metadata.

## Complete axiom census

I read the full audit source and complete raw successful audit stdout:
`final-runs/20261018T030411Z-build-MorseFiniteAxiomAudit-53575871/stdout.txt`,
19899 bytes, SHA-256
`9f41da11dc9c082106bba058a36649e6886c8f8334ad0b9917fb1b58fd434be8`.

The audit enumerates declarations by their imported module origin, with export
filtering disabled, rather than only by a manually selected name prefix. It
checks each declaration exists in the checked environment, collects transitive
axioms, rejects every axiom outside the explicit allowed set, and checks a
required declaration list including both finiteness theorems and the key steps
and controls. Generated/private helpers are included; for example, equation
helpers carrying Lifetime/TorusFiltration namespaces are correctly counted in
the module that generated them.

| Audited source module | Unique declarations |
| --- | ---: |
| Lifetime | 103 |
| TorusTopology | 38 |
| MorseFiniteCritical | 20 |
| MorseFiniteControls | 8 |
| Total | 169 |

I independently parsed all complete bracketed axiom records, including wrapped
multiline lists: there are 169 records and 169 unique declaration names, with
the exact four module counts above and one final total 169. Every reported
transitive axiom is among `propext`, `Classical.choice`, and `Quot.sound`.
The explicit `#print axioms` results for both finiteness endpoints show those
three standard axioms. No `sorryAx` or extra domain axiom is reported. The
printed theorem type matches the literal endpoint reviewed above.

This is a complete module-origin census for the four stated source modules,
not a census of every Mathlib declaration or a claim that the imported
Lifetime specification's unproved scientific propositions have become theorems.
The audit module executes the census; it adds no new mathematical assumptions.

## Actual negative controls and their meaning

The frozen controls compiled warning-strictly and received their own standard
kernel replay. Their mathematical content is substantive:

- The explicitly bilinear nonsymmetric form
  B(v,w)=(v1−v2)(w1+w2) is negative on the second axis, positive on the first,
  and has nonzero left-radical vector (1,1). Axis decomposition/trivial
  intersection and unequal swapped cross terms are proved. Thus complementary
  signs alone do not imply nonsingularity for arbitrary bilinear forms. This
  exposes precisely why the main proof derives symmetry from smoothness.
- The norm on literal E 1 is nondifferentiable at zero while default `fderiv`
  equals zero there. It satisfies literal criticality at zero. This guards the
  distinction between literal criticality and differentiability. It is not
  asserted to be periodic or to refute the entire final theorem without
  smoothness.
- The half-open interval [0,1) is not compact, whereas [0,1] is. These controls
  are ancillary; the implemented quotient-descent proof uses neither as its
  compactness argument.

The separate actual interface rejection uses
`negative-project/WithoutMorse.lean`, 455 bytes, SHA-256
`4c9726b692dbb83237b82344e7b5aab621749da6da699c0187cf9893dca8d80f`,
with runner `run_negative.py`, SHA-256
`cb5a8db15b5b5881463fc5e6faea7f38c3de0a3f7e56b6fd9001f3326a815faa`.
It imports the actual final theorem and attempts its finite-set conclusion from
only smoothness and periodicity, omitting Morse-distinct. The terminal receipt
`negative-final/RECEIPT.json`, 2376 bytes, SHA-256
`482d1e7444fe1b25ee40caf3b610197d7b729cdb21ad649dee4db537b36d41fc`,
records exit 1, no timeout, elapsed 96.614084542 seconds, and unchanged tested
source, final imported source map, and final object map. The exact diagnostic is:

```text
error: Type mismatch
  quotientCriticalSet_finite d L hL g hs hp
has type
  IsMorseDistinct d L g → (quotientCriticalSet d L hL g).Finite
but is expected to have type
  (quotientCriticalSet d L hL g).Finite
```

Its stdout is 342 bytes, SHA-256
`2606cce55be96a1c241544374a6790e472c61b57ba369966f4a1e05649b4b10a`;
stderr is empty. I checked these bytes against the receipt and inspected the
actual source/diagnostic. This is the intended missing-premise rejection, not an
import, syntax, missing-object, or unknown-name failure. It verifies an interface
boundary; a failed theorem application alone is not a counterexample to every
possible theorem without that premise. Separately, a constant smooth periodic
function in positive dimension demonstrates mathematically why unrestricted
critical-set finiteness is false; that observation is not labeled an executed
Lean counterexample here.

## Failure history and corrected infrastructure

The earlier source review's “no current-source execution flaw found” statement
was bounded to its then-inspected runner bytes. Actual execution later exposed
two preparation defects, preserved rather than erased:

1. A runner wrongly required a compiled `lib/lean` directory for every manifest
   package. Cli has no such directory. The corrected runner still checks all
   package revisions, includes existing compiled roots/search paths, and then
   requires exact equality with the authenticated C291 roots. This does not
   silently drop a recorded dependency. Failure details are retained in
   `evidence/FINAL_PREPARE_FAILURE_20261018T023327Z.json` (SHA-256
   `b1b3a0d1bdb88b63e9548503c7c4c8c9dbc05da97f31413b9900d32c2b083900`).
2. The next preparation compared Path-sorted baseline paths with string-sorted
   current paths. Actual unique sets were equal, with no added/removed artifact.
   The corrected code compares canonical string-sorted sets and explicitly
   rejects duplicate baseline paths while preserving every path/hash/stat
   association. `evidence/FINAL_PREPARE_PATHSET_FAILURE_20261018T0237Z.json`
   (SHA-256 `6a85cce34ed2d4a8c9a67c00e0d1edb06931656577bdb635fa251495817e9857`)
   preserves the actual failed START at 02:45:09 UTC and explains its provisional
   filename timestamp. Both failures preceded final source/build directories.

The failed START records remain; the successful freeze binds a new unique START.
The earlier development audit timed out at 240 seconds without completing.
The final runner gives only the audit build a 900-second bound, with other phases
at 420 seconds. The actual final audit completed in 173.752 seconds. The timeout
is preserved negative execution history, not an axiom violation or a successful
audit. Earlier control elaboration failures likewise remain development history,
not successful negative controls. I read the corrected scripts and failure
records; the terminal receipts above establish the successful final run on their
exact frozen identities.

## Master artifact verifier engineering review

I read the complete initial `final_master.py`, SHA-256
`92f420d05176b1d3bb1bd6a578a1de72cd7ec5c531c34e5ad9da234fe0150d33`,
and its contract. It binds completed local evidence and future publication,
hosted-job, archive, and custody readbacks. It does not run Lean or supply an
additional mathematical proof. No master invocation was run by this reviewer.

I found and reported a concrete pre-run defect: the initial parser iterated over
`audit.splitlines()` and required `AXIOMS [...]` on a single line. The actual raw
audit has many wrapped axiom lists. It would omit those records and reject a
valid complete census. This was reported promptly to the parent for correction
by the master author, without editing their file. It has no effect on the actual
Lean census, the proof, or the successful build/kernel evidence. Its engineering
resolution was then reviewed before the first master run.

The master author corrected the parser; I read the complete corrected source and
updated contract. The corrected `final_master.py` is 14011 bytes, SHA-256
`1d5d93787c92826c9e1950125962e93db4a634c3898242400c63005b62945ec1`;
`evidence/MASTER_CONTRACT.md` is 9281 bytes, SHA-256
`603f65119bf025aa7ca805989ca1850b83e4566638e973aab7a454376e1b6d4b`.
The replacement uses full-text `re.finditer` records with bracket-excluding,
4096-character-bounded axiom contents. It retains section counts, allowed-axiom
checks, uniqueness, required names, and the final total, and additionally requires
every raw declaration marker to be parsed and exactly 169 declarations. This
addresses the observed wrapping defect without accepting malformed omitted
records. The actual complete stdout independently parsed by this reviewer has
the counts and allowed axioms required by the corrected logic.

The updated contract reports the author's focused execution of the extracted
parser AST block against actual output and six malformed in-memory controls.
I read that report but did not rerun those tests or count them as extra theorem
evidence. I observed master START/output still absent during the review. The
identified engineering finding is resolved at these corrected source bytes;
there is no remaining source-review objection to the master being invoked after
all of its required delivery records exist. Actual master success remains a
future terminal evidence gate.

With that correction, source inspection found the master
appropriately treats receipt/object/hash consistency, standard axiom names,
actual rejection diagnostics, review binding, native/remote publication bytes,
hosted-job head identity, canonical archive verification, and private raw-byte
readback as artifact-evidence checks. Its eventual PASS must remain
`PASS_ARTIFACT_VERIFICATION_NOT_THEOREM_PROOF`. The receipt inputs and publication
records are trusted observations supplied to it; it performs no remote read
itself. This review does not claim those future records already exist or that
the master has passed.

## Final disposition

The mathematical source and completed local formal gates justify
**ACCEPT_SCOPED_FORMAL** for the stated finite projected critical-set theorem and
its named dependency/control declarations. No theorem hypothesis has been hidden
or replaced by the desired conclusion. The strongest derived result here is the
full finite quotient critical set under the literal deterministic hypotheses.

The remainder of C292 remains outside this formal result: Morse normal form,
closed-level local path connectedness, literal death attainment, closed traps,
fixed older endpoints and closed paths, ordinary-H0 interval consumption, all-bar
classification, saddle pairing, collision laws, and almost-sure Gaussian Morse
genericity. The C292 conventional proof remains frozen under its separate scope.

No hosted CI run or registration of these new formal modules, no new public
landing, no private custody, and no master terminal result is claimed by this
report. Same-provider nonauthor review remains independence credit 0. Scientific
effect: **NONE**.
