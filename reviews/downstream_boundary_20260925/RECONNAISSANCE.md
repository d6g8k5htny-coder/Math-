# Bounded primary-source reconnaissance — 2026-09-25

Targets: finite-r Hermite pin consistency in Math PR9 and actual before/after deployment of main PR98.

Read the source-pinned project files named in README.md. The mathematical counterexample is derived directly from all six stated finite-r constraints; no external paper is treated as proving it. NIST DLMF Section3.3 was inspected for established interpolation/divided-difference background: https://dlmf.nist.gov/3.3 . Its discussion is background, not a novelty claim or a substitute for the explicit polynomial identities.

GitHub's official workflow-event reference was inspected: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows . Different event/checkout contexts have different commit semantics; a reviewed change gate must record the actual compared source identities rather than assume that checkout HEAD supplies both versions. The project CI currently uses an explicit tip-audit command; the architecture probe checks its executable behavior against distinct supplied inputs. This review neither changes permissions nor runs untrusted source in a privileged pull_request_target workflow.

The new workflow uses a read-only checkout at exact public source commits and no recurring scheduler. Only the scoped source files, temporary synthetic inputs and generated reports are used. No private sandbox or vault source is copied.

No historical priority, theorem closure, organizational independence or general proof-assistant certification is claimed. The literature and tool documentation do not determine the review outcome; exact source constraints and executed probes do.
