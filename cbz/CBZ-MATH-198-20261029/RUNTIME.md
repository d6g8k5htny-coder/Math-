# Pinned runtime reproduction

These are standalone runtime instructions for the scoped CBZ-MATH-198 contribution.
They contain no federation repository inventory or private connector payload.
Use a new absolute directory in place of `/ABS/NEW_RUNTIME_ROOT`. Existing paths
are never replaced. This document is a provisioning recipe; it does not claim a
successful fresh tagged-clone acceptance run.

## Provision a fresh Linux x86_64 runtime

Prerequisites are Python3.12+, Git, curl, tar with zstd support, flock, network access to GitHub and the official Mathlib cache, and at least16GiB RAM with15GiB free runtime disk space. The binary archive/shared libraries and official dependency cache remain external trust inputs; this is not a full compiler/Mathlib source rebuild. Run no other native campaign during provisioning. Destinations below must be new; these commands never replace an existing runtime. They are documented reproduction instructions, not a newly observed successful cold-start run.

```sh
set -e
CBZ_RUNTIME_ROOT=/ABS/NEW_RUNTIME_ROOT
mkdir -p "$CBZ_RUNTIME_ROOT"
test ! -e "$CBZ_RUNTIME_ROOT/lean-4.34.1-linux"
test ! -e "$CBZ_RUNTIME_ROOT/mathlib-d13f23b7"
test ! -e "$CBZ_RUNTIME_ROOT/lean-4.34.1-linux.tar.zst"
curl --fail --location --retry 3 \
  https://github.com/leanprover/lean4/releases/download/v4.34.1/lean-4.34.1-linux.tar.zst \
  --output "$CBZ_RUNTIME_ROOT/lean-4.34.1-linux.tar.zst"
printf '%s  %s\n' \
  47bf4bbd78f70c2e9670598ab7124d92b6efb7330ff33e5fbb4030f6fd72e4e4 \
  "$CBZ_RUNTIME_ROOT/lean-4.34.1-linux.tar.zst" | sha256sum --check
tar --zstd --extract --file "$CBZ_RUNTIME_ROOT/lean-4.34.1-linux.tar.zst" \
  --directory "$CBZ_RUNTIME_ROOT"
printf '%s  %s\n' \
  e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550 \
  "$CBZ_RUNTIME_ROOT/lean-4.34.1-linux/bin/lean" | sha256sum --check
printf '%s  %s\n' \
  ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe \
  "$CBZ_RUNTIME_ROOT/lean-4.34.1-linux/bin/leanchecker" | sha256sum --check
export PATH="$CBZ_RUNTIME_ROOT/lean-4.34.1-linux/bin:$PATH"
export LEAN_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
git init "$CBZ_RUNTIME_ROOT/mathlib-d13f23b7"
git -C "$CBZ_RUNTIME_ROOT/mathlib-d13f23b7" remote add origin \
  https://github.com/leanprover-community/mathlib4.git
git -C "$CBZ_RUNTIME_ROOT/mathlib-d13f23b7" fetch --depth 1 origin \
  d13f23b723b8a846827a245b89c10fc7d3f11612
git -C "$CBZ_RUNTIME_ROOT/mathlib-d13f23b7" checkout --detach \
  d13f23b723b8a846827a245b89c10fc7d3f11612
cd "$CBZ_RUNTIME_ROOT/mathlib-d13f23b7"
python -B - <<'PINS'
import json
from pathlib import Path
import subprocess
expected = {
    'plausible': '118aa17ee84656b8bd727fef7c458ee8c833385c',
    'LeanSearchClient': 'ddf04cf3949fa556442341e87d47f9f6e6074707',
    'importGraph': 'e928b72544873815af278d38681b31c0293588e3',
    'proofwidgets': '106ff4fafc74ef4ac99d81dbf3ab399118f497a5',
    'aesop': '355695d523e41d0554926416cba2a2b3544fbbc9',
    'Qq': '6a489d9af5d0c47e5b259e2e8bcdfc1811b5a259',
    'batteries': 'f2effa3d803fda822b1f97b806c47cf2adfbcbc2',
    'Cli': 'e92c9f15fdfacc8536f31cfb3b7ad26c3c8cd204',
}
packages = json.loads(Path('lake-manifest.json').read_text())['packages']
if len(packages) != 8 or {p['name']: p['rev'] for p in packages} != expected:
    raise SystemExit('Pinned dependency manifest mismatch')
if Path('lean-toolchain').read_text().strip() != 'leanprover/lean4:v4.34.1':
    raise SystemExit('Pinned Lean toolchain mismatch')
for package in packages:
    destination = Path('.lake/packages') / package['name']
    if destination.exists():
        raise SystemExit('Dependency destination already exists: ' + str(destination))
    destination.mkdir(parents=True)
    subprocess.run(['git', 'init', str(destination)], check=True)
    subprocess.run(['git', '-C', str(destination), 'remote', 'add', 'origin', package['url']], check=True)
    subprocess.run(['git', '-C', str(destination), 'fetch', '--depth', '1', 'origin', package['rev']], check=True)
    subprocess.run(['git', '-C', str(destination), 'checkout', '--detach', package['rev']], check=True)
    actual = subprocess.check_output(['git', '-C', str(destination), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != expected[package['name']]:
        raise SystemExit('Dependency HEAD mismatch: ' + package['name'])
PINS
lean --version
lake exe cache get Mathlib
```

After every command succeeds, pass the selected executable and Mathlib paths to
`tools/contribution_gate.py` as documented in README.md. The adapter honors
`UL_LEAN` and `UL_MATHLIB_ROOT` for direct native component commands; explicit
SHA/commit checks remain required. Do not run `lake update`.

The official compiler, shared libraries and precompiled dependency cache are
external trusted inputs. No independent compiler or complete Mathlib source
rebuild follows from downloading them. A prior local setup used same-byte
executables at a distinct hardlink path with an explicit shared library symlink;
that setup is not an independent runtime implementation or a cold-start pass.
