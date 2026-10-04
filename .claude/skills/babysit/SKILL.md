---
name: babysit
description: Posture for watching a Math- pull request through CI and review events. Short form; the repository conventions are in the steward skill (`.claude/skills/steward/SKILL.md`), which takes precedence.
---

# Babysit: watching a Math- pull request

Read [`../steward/SKILL.md`](../steward/SKILL.md) first. It holds this repository's conventions: frozen heads, AMEND timing, gates, stacked bases and integration. This file adds only the watching posture.

- **Never punt.** Every event on a PR you own ends in one of three ways:
  - a validated push;
  - one comment that names the exact blocker and what is needed;
  - a recorded reason that nothing is yours to do, because the PR waits on a reviewer or an integrator.
- **Address every unresolved thread.** Answer each one where it was raised, and resolve the threads you fixed.
- **A failing test is never assumed to be an infra flake.** Reproduce it and root-cause it first (steward §4).
- **A green, mergeable head may wait on people. A red or conflicted head never waits unattended:** fix it, or, while a nonauthor read is open, post its diagnosis (steward §4).
- **Keep the head frozen while a nonauthor read is open**, even when a fix seems obvious or CI is red. Apply it after the verdict, or earlier only if the reader releases the pickup or agrees to re-point (steward §3–§4).
- **Update the PR body's disposition on every material change** (steward §2), and keep the lane's ledger in main#229 current.
- **Stop following a PR** when it is merged or closed, or when Dylan says stop.
