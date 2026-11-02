# Import lane — partition-trajectory possibility, 2026-11-01

Scientific effect: **NONE**. This is a **candidate** import. Organizational-independence credit **0**. **OBL OPEN**. Acceptance stays open pending different-family review. A green replay leaves `lemma_closed`, prizes, and obligation state unchanged, and it records no scientific PASS. The preserved owner text in `README.md` and `docs/` remains the supplied candidate.

## What was placed

The owner package root is this directory. Every path listed in [MANIFEST.sha256](MANIFEST.sha256) is unchanged, and that manifest was not recomputed. `MANIFEST.sha256` lists those 22 owner paths. This note, `.gitignore`, and the repository workflow `.github/workflows/partition-trajectory-import.yml` are Math- lane files outside that list.

`__pycache__` directories that arrived inside the transport tarball are omitted. `MANIFEST.sha256` and the intake zip's source tree both omit them. The intake zip and its inner `Partition_Trajectory_Possibility.zip` stay outside this tree; both duplicate the same source files.

Root `README.md`, `PROOF_INDEX.md`, `STATUS` files, and `claims/` are unchanged. This repository does not keep a live register that every `imports/*` lane must join.

## Run

Python 3.11 or newer, standard library only. The working directory must be this lane. From the repository root:

```sh
cd imports/partition_trajectory_20261101
python3 -m partition_trajectory
python3 -m unittest discover -s tests -v
python3 -B -S examples/custom_analysis.py
```

The same two package commands with `python3 -B -S` and `python3 -B -O -S` are the repository's usual interpreter flags. `partition_trajectory` is not on the repository-root module path; `PYTHONPATH=imports/partition_trajectory_20261101` is the root-relative alternative for `python3 -m partition_trajectory`.

Expected finite checkpoints are in [docs/verification.md](docs/verification.md): parity 4; x-then-z 0 solutions with a stage-1 obstruction; flexibility 108 / 36 / 36 / 0; 12 tests. Those checks exercise this finite candidate.

## Transport identities

Hashes below are SHA-256 of the uploaded transport bytes. They are provenance for the copy, not a scientific record.

| Transport | SHA-256 |
|---|---|
| `partition_trajectory_package.tgz` | `0e24c823ab23bb2ad12bfb896da69b32766685bcadce8a7f6ac199fa6c4ebf15` |
| `partition-trajectory-intake.zip` | `d4b44f77ad0334d0b539de966853acd3d9589a3199a3b9a8b186a347465eeb7d` |
| inner `Partition_Trajectory_Possibility.zip` (23506 bytes, not stored) | `e3be31d77ba715a2985eac5287094569256c66b8b6f728d101bd59b97e5066c2` |

The 23 source files in the intake zip's `partition_trajectory_package/` tree match the tarball's source files byte for byte, including `MANIFEST.sha256`.
