# Core custody evidence checkpoint

This file is a source-bound observation index; [OBSERVATIONS.json](OBSERVATIONS.json) records the exact tested merge commits, real failure counts, prior component passes, artifact identities and limitations. Raw GitHub logs/artifacts remain at their native run IDs. Test-only #540 exposed six environment failures in both modes and a real 13-of-13 exit-2 false-kill on the old grader. Its D2 tree refusals are expected identity checks. The environment-only repair passed six simulated-helper tests in each mode; the strict combined grader has not yet run. The earlier #537 kernel run and downloaded-artifact seal passed at its tested merge and do not certify the newer source.

Endpoint source checks assume no transient change restored between observations. The mutation nonce distinguishes accidental record confusion, not hostile child-code forgery. No final CBZ or unconditional model assertion is made.

[2026-10-29 21:29:45 UTC] [phase3] [layerA] Record actual test-first failures and source-specific component results without transferring them to the combined candidate. Reversible: yes. Evidence: OBSERVATIONS.json and native job logs.
