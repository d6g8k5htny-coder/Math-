# Sharp Axial Escape Implementation Plan

> For agentic workers: use superpowers:executing-plans for this bounded task.

**Goal:** Establish a sharp deterministic escape theorem and quantify the
moment premise sufficient for its lifetime application.

**Architecture:** Add one proof packet without changing its predecessor.
Keep the full real-variable proof separate from finite algebra verification.

**Tech Stack:** Mathematical prose; Python standard-library Fraction arithmetic.

**Spec:** ../specs/2026-10-26-sharp-axial-escape-design.md

## Global constraints

Keep original source and status bytes unchanged. Scientific review must be by
a different model family. Local author checks do not supply that review.
No external comments, remote branch changes, workflow changes or publication.

## Review focus

Check strict versus weak threshold, Hermite extrapolation beyond the pins,
the fourth derivative's scaling in physical coordinates, normalized versus
unnormalized weighted moments, and the boundary exponent `s=4q+3`.

## Task 1: Mathematical candidate and exact controls

- [x] Read the original lifetime proof, relevant existing sharpness example,
  current source instructions and coordination records.
- [x] Derive the Hermite lower envelope, endpoint margin, equality obstruction
  and above-threshold obstruction on paper before implementing checks.
- [x] Write `frontiers/sharp_axial_escape_20261026/PROOF.md`, `README.md`,
  `SOURCES.json`, and `check_exact.py`.
- [x] Verify polynomial coefficients, pins, physical derivatives, the endpoint
  optimization identity, and exact abstract moment-obstruction examples.
- [x] Run checks with `python -B -S` and `python -B -S -O`; require identical
  deterministic JSON reports. Run `git diff --check` and verify the source
  manifest against unchanged Git blobs.
- [x] Record exact results and retained obligations in `VERIFICATION.md`.

Expected: new finite checks pass in both modes; no historical sources change.
The original publication-verifier suite needs Python 3.11, unavailable here;
its direct exact lifetime/loss checkers can run under Python 3.12.
