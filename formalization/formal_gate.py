"""Layer 1 formal-verification gate for Math- (fail-closed).

Validates ``formalization/FORMALIZATION_STATUS.json`` against the landing claim
manifest, the downstream dependency graph, the pinned Lean sources and the
pinned axiom audits. Optionally (``--with-lean``) replays ``lake build`` and the
axiom audit script with the installed toolchain.

Scientific effect: NONE. A kernel-checked Lean theorem verifies exactly its
written statement. This gate never promotes a landing disposition, never sets a
graph node controlling, and never flips ``lemma_closed``. Layer 0 (provenance,
scope, downstream hard gate) is consumed read-only and is unchanged.

Run from the repository root:

    python -B -S formalization/formal_gate.py
    python -B -S formalization/formal_gate.py --with-lean           # needs elan/lake on PATH
    python -B -S formalization/formal_gate.py --refresh-pins        # deliberate pin regeneration
    python -B -S -m unittest discover -s formal -p 'test_*.py' -v
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REGISTRY_PATH = HERE / 'FORMALIZATION_STATUS.json'
RESULTS_PATH = HERE / 'FORMAL_RESULTS.json'
HARD_GATE_PATH = ROOT / 'frontiers' / 'downstream_gate_20260925' / 'hard_gate.py'

STATUS_ORDER = ('none', 'specified', 'proved', 'kernel_checked')
LANE_VERDICTS = {
    'none': 'FORMAL_NONE',
    'specified': 'FORMAL_SPECIFIED',
    'proved': 'FORMAL_PROVED_UNREPLAYED',
    'kernel_checked': 'FORMAL_KERNEL_CHECKED_AUTHOR_SIDE',
}
ALIGNED_VERDICT = 'FORMAL_KERNEL_CHECKED_ALIGNED'
# Tokens the formal lane could offer Layer 0. Layer 0 must refuse every one of them
# as sole evidence; the composition check below asserts that it does.
FORMAL_TOKENS = ('LEAN_KERNEL_CHECK', 'LEAN_STATEMENT_SPECIFIED', 'FORMAL_ALIGNMENT_ACCEPT')
FORBIDDEN_SOURCE_PATTERNS = (
    (re.compile(r'\bsorry\b'), 'sorry'),
    (re.compile(r'\bnative_decide\b'), 'native_decide'),
    (re.compile(r'^\s*axiom\b', re.MULTILINE), 'axiom declaration'),
    (re.compile(r'\bLean\.ofReduceBool\b'), 'Lean.ofReduceBool'),
    (re.compile(r'\bimplemented_by\b'), 'implemented_by'),
    (re.compile(r'\bextern\b'), 'extern'),
)


class FormalGateError(ValueError):
    pass


# --------------------------------------------------------------------------- helpers

def strict_json(text: str) -> Any:
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise FormalGateError('duplicate JSON key: ' + key)
            out[key] = value
        return out

    def constant(value):
        raise FormalGateError('non-finite JSON constant: ' + value)

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def safe_relpath(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise FormalGateError('nonempty repository-relative path required')
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or '\\' in value or ':' in value:
        raise FormalGateError('unsafe repository-relative path: ' + value)
    return p.as_posix()


def read_regular(root: Path, rel: str) -> bytes:
    path = root / rel
    parts = PurePosixPath(rel).parts
    for i in range(1, len(parts) + 1):
        if (root / Path(*parts[:i])).is_symlink():
            raise FormalGateError('symlink in pinned path rejected: ' + rel)
    if not path.is_file():
        raise FormalGateError('pinned source missing: ' + rel)
    return path.read_bytes()


def identity(raw: bytes) -> dict[str, Any]:
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def module_relpath(package: dict[str, Any], module: str) -> str:
    if not isinstance(module, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*', module):
        raise FormalGateError('malformed Lean module name: ' + str(module))
    parts = module.split('.')
    if parts[0] != package['library']:
        raise FormalGateError(f'module {module} is outside library {package["library"]}')
    return safe_relpath(package['path'] + '/' + '/'.join(parts) + '.lean')


def load_hard_gate(root: Path):
    path = root / 'frontiers' / 'downstream_gate_20260925' / 'hard_gate.py'
    if not path.is_file():
        raise FormalGateError('Layer 0 hard gate module is missing: ' + str(path))
    spec = importlib.util.spec_from_file_location('math_layer0_hard_gate', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def parse_axiom_audit(text: str) -> dict[str, list[str]]:
    """Parse ``<decl> <axiom,axiom|->`` lines; tolerate a ``file:line:col: info:`` prefix."""
    table: dict[str, list[str]] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        line = re.sub(r'^.*?:\d+:\d+:\s*info:\s*', '', line)
        parts = line.split()
        if len(parts) != 2:
            raise FormalGateError('malformed axiom audit line: ' + raw_line)
        name, axioms = parts
        if name in table:
            raise FormalGateError('duplicate axiom audit entry: ' + name)
        table[name] = [] if axioms == '-' else axioms.split(',')
    if not table:
        raise FormalGateError('empty axiom audit')
    return table


# --------------------------------------------------------------------------- validation

def _require(condition: bool, message: str) -> None:
    if not condition:
        raise FormalGateError(message)


def _validate_vocabulary(reg: dict[str, Any]) -> None:
    _require(isinstance(reg, dict) and reg.get('schema_version') == 1, 'schema_version 1 required')
    _require(reg.get('repository') == 'd6g8k5htny-coder/Math-', 'unexpected repository identity')
    _require(reg.get('scientific_effect') == 'NONE', 'scientific_effect must be NONE')
    _require(reg.get('promotion_permission') is False, 'promotion_permission must be exactly false')
    _require(reg.get('lemma_closed') is False, 'lemma_closed must be exactly false')
    _require(list(reg.get('allowed_statuses', [])) == list(STATUS_ORDER), 'allowed_statuses vocabulary changed')
    _require(set(reg.get('allowed_alignment', [])) == {'NONE', 'REVIEW_REQUIRED', 'ACCEPT', 'AMEND_REQUIRED'},
             'allowed_alignment vocabulary changed')
    _require(set(reg.get('allowed_component_kinds', [])) == {'theorem', 'prop_specification', 'interface'},
             'allowed_component_kinds vocabulary changed')
    allowed = reg.get('allowed_axioms')
    forbidden = reg.get('forbidden_axioms')
    _require(isinstance(allowed, list) and set(allowed) == {'propext', 'Classical.choice', 'Quot.sound'},
             'allowed_axioms must be exactly the three standard Lean axioms')
    _require(isinstance(forbidden, list) and {'sorryAx', 'Lean.ofReduceBool'} <= set(forbidden),
             'forbidden_axioms must include sorryAx and Lean.ofReduceBool')
    _require(not (set(allowed) & set(forbidden)), 'an axiom cannot be both allowed and forbidden')
    tool = reg.get('toolchain')
    _require(isinstance(tool, dict) and isinstance(tool.get('lean'), str) and tool['lean'].startswith('leanprover/lean4:v'),
             'toolchain.lean must be a pinned leanprover/lean4 release')
    ml = tool.get('mathlib')
    _require(isinstance(ml, dict) and re.fullmatch(r'[0-9a-f]{40}', str(ml.get('commit'))), 'mathlib commit must be a full SHA')


def _validate_packages(reg: dict[str, Any], root: Path) -> None:
    packages = reg.get('packages')
    _require(isinstance(packages, dict) and packages, 'packages object required')
    for name, pkg in packages.items():
        _require(isinstance(pkg, dict), 'package record must be an object')
        pdir = safe_relpath(pkg.get('path'))
        _require((root / pdir).is_dir(), 'package directory missing: ' + pdir)
        _require(isinstance(pkg.get('library'), str) and pkg['library'], 'package library name required')
        _require(type(pkg.get('depends_on_mathlib')) is bool, 'depends_on_mathlib must be exact boolean')
        toolchain = read_regular(root, pdir + '/lean-toolchain').decode().strip()
        _require(toolchain == reg['toolchain']['lean'], f'package {name} toolchain {toolchain} differs from registry')
        lakefile = read_regular(root, pdir + '/lakefile.toml').decode()
        _require(f'name = "{pkg["library"]}"' in lakefile, f'package {name} lakefile does not declare its library name')
        has_mathlib = 'name = "mathlib"' in lakefile
        _require(has_mathlib == pkg['depends_on_mathlib'], f'package {name} Mathlib dependency flag disagrees with lakefile')
        if has_mathlib:
            manifest = strict_json(read_regular(root, pdir + '/lake-manifest.json').decode())
            revs = {p.get('name'): p.get('rev') for p in manifest.get('packages', []) if isinstance(p, dict)}
            _require(revs.get('mathlib') == reg['toolchain']['mathlib']['commit'],
                     f'package {name} lake-manifest Mathlib commit differs from registry pin')
            for p in manifest.get('packages', []):
                if p.get('type') == 'path':
                    _require(not str(p.get('dir', '')).startswith('/'), 'absolute path dependency leaked into manifest')
        audit_rel = safe_relpath(pkg.get('axioms_expected'))
        _require(audit_rel.startswith(pdir + '/'), 'axioms_expected must live inside its package')
        table = parse_axiom_audit(read_regular(root, audit_rel).decode())
        allowed = set(reg['allowed_axioms'])
        for decl, axioms in table.items():
            _require(decl.startswith(pkg['library'] + '.'), f'audit line outside library namespace: {decl}')
            bad = sorted(set(axioms) - allowed)
            _require(not bad, f'pinned axiom audit for {decl} uses non-allowed axioms {bad}')
        pkg['_audit'] = table


def _validate_sources(reg: dict[str, Any], root: Path) -> None:
    sources = reg.get('sources')
    _require(isinstance(sources, dict) and sources, 'sources pin table required')
    for rel, pin in sources.items():
        rel = safe_relpath(rel)
        raw = read_regular(root, rel)
        current = identity(raw)
        _require(isinstance(pin, dict) and pin.get('bytes') == current['bytes'] and pin.get('sha256') == current['sha256'],
                 f'pinned Lean source drift: {rel}')
        if rel.endswith('.lean') and '/scripts/' not in rel:
            text = raw.decode()
            for pattern, label in FORBIDDEN_SOURCE_PATTERNS:
                _require(not pattern.search(text), f'forbidden construct ({label}) in {rel}')
    # Every Lean file inside every package must be pinned (no unpinned sources).
    for name, pkg in reg['packages'].items():
        pdir = root / pkg['path']
        for path in sorted(pdir.rglob('*.lean')):
            if '.lake' in path.parts:
                continue
            rel = path.relative_to(root).as_posix()
            _require(rel in sources, f'unpinned Lean source in package {name}: {rel}')
        for extra in ('lakefile.toml', 'lean-toolchain', pkg['axioms_expected'].split('/')[-1]):
            rel = (pdir / extra).relative_to(root).as_posix()
            _require(rel in sources, f'unpinned package file: {rel}')
        if pkg['depends_on_mathlib']:
            rel = (pdir / 'lake-manifest.json').relative_to(root).as_posix()
            _require(rel in sources, f'unpinned lake-manifest: {rel}')


def _validate_companions(reg: dict[str, Any], root: Path, claims: dict[str, Any]) -> dict[str, Any]:
    """Read-only index of sibling Lean packets that own their own manifest and gate.

    The lane never edits a companion. It only asserts that the companion still
    exists, that its own source-identity gate passes, that its toolchain and
    Mathlib pins agree with this registry, and that its source modules avoid the
    same forbidden constructs. A companion's own manifest remains the authority
    for its targets and alignment state; nothing here re-awards either.
    """
    companions = reg.get('companion_packages', {})
    _require(isinstance(companions, dict), 'companion_packages must be an object')
    out: dict[str, Any] = {}
    for name, comp in companions.items():
        _require(isinstance(comp, dict), f'companion {name} must be an object')
        _require(comp.get('relationship') == 'read_only_index', f'companion {name} relationship must be read_only_index')
        pdir = safe_relpath(comp.get('path'))
        _require((root / pdir).is_dir(), f'companion directory missing: {pdir}')
        for key in ('manifest', 'gate'):
            rel = safe_relpath(comp.get(key))
            _require(rel.startswith(pdir + '/'), f'companion {name} {key} must live inside its directory')
        manifest_rel = safe_relpath(comp['manifest'])
        manifest = strict_json(read_regular(root, manifest_rel).decode())
        _require(manifest.get('schema_version') == 1, f'companion {name} manifest schema unsupported')
        _require(manifest.get('scientific_effect') == 'NONE', f'companion {name} manifest claims a scientific effect')
        status = manifest.get('formalization_status')
        _require(status in STATUS_ORDER, f'companion {name} formalization_status {status!r} outside lane vocabulary')
        alignment = manifest.get('alignment_status')
        _require(isinstance(alignment, str) and alignment and 'ACCEPT' not in alignment.upper(),
                 f'companion {name} manifest self-declares alignment acceptance')
        toolchain = read_regular(root, pdir + '/lean-toolchain').decode().strip()
        _require(toolchain == reg['toolchain']['lean'], f'companion {name} toolchain {toolchain} differs from registry')
        lakefile = read_regular(root, pdir + '/lakefile.toml').decode()
        _require(isinstance(comp.get('library'), str) and f'name = "{comp["library"]}"' in lakefile,
                 f'companion {name} lakefile does not declare library {comp.get("library")!r}')
        revs = manifest.get('dependency_revisions', {})
        _require(isinstance(revs, dict) and revs.get('mathlib') == reg['toolchain']['mathlib']['commit'],
                 f'companion {name} Mathlib commit differs from registry pin')
        claim_ids = comp.get('claim_ids')
        known = {c.get('claim_id') for c in claims.get('claims', []) if isinstance(c, dict)}
        _require(isinstance(claim_ids, list) and all(cid in known for cid in claim_ids),
                 f'companion {name} cites claim_ids outside the landing manifest')
        modules = manifest.get('source_modules', [])
        _require(isinstance(modules, list) and modules, f'companion {name} declares no source modules')
        for module in modules:
            rel = pdir + '/' + safe_relpath(module)
            text = read_regular(root, rel).decode()
            for pattern, label in FORBIDDEN_SOURCE_PATTERNS:
                _require(not pattern.search(text), f'forbidden construct ({label}) in companion source {rel}')
        gate_rel = safe_relpath(comp['gate'])
        proc = subprocess.run([sys.executable, '-B', '-S', str(root / gate_rel)], cwd=root, capture_output=True,
                              text=True, timeout=600)
        _require(proc.returncode == 0, f'companion {name} gate refused:\n{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}')
        prefix = comp.get('source_check_prefix')
        _require(isinstance(prefix, str) and prefix and proc.stdout.startswith(prefix),
                 f'companion {name} gate output does not begin with the declared source-check prefix')
        out[name] = {
            'library': comp['library'],
            'source_identity': 'PASS',
            'formalization_status': status,
            'alignment_status': alignment,
            'toolchain_agrees': True,
            'mathlib_commit_agrees': True,
            'authority': comp['manifest'],
        }
    return out


def _decl_declared(text: str, decl: str, kind: str) -> bool:
    short = decl.split('.')[-1]
    keyword = 'theorem' if kind == 'theorem' else 'def'
    pattern = re.compile(r'^\s*(?:noncomputable\s+)?(?:private\s+)?' + keyword + r'\s+' + re.escape(short) + r'\b', re.MULTILINE)
    return bool(pattern.search(text))


def _validate_ref(reg: dict[str, Any], root: Path, ref: dict[str, Any], *, label: str) -> None:
    kind = ref.get('kind')
    _require(kind in reg['allowed_component_kinds'], f'{label}: unknown kind {kind}')
    if kind == 'interface' and ref.get('decl') is None:
        _require(ref.get('package') is None and ref.get('module') is None, f'{label}: prose-only interface cannot name a module')
        _require(isinstance(ref.get('note'), str) and ref['note'].strip(), f'{label}: prose-only interface requires a note')
        _require(ref.get('status') == 'none', f'{label}: prose-only interface must have status none')
        return
    pkg = reg['packages'].get(ref.get('package'))
    _require(isinstance(pkg, dict), f'{label}: unknown package {ref.get("package")}')
    rel = module_relpath(pkg, ref.get('module'))
    _require(rel in reg['sources'], f'{label}: module {ref.get("module")} is not a pinned source')
    text = read_regular(root, rel).decode()
    decl = ref.get('decl')
    _require(isinstance(decl, str) and decl.startswith(pkg['library'] + '.'), f'{label}: decl must be fully qualified inside {pkg["library"]}')
    _require(_decl_declared(text, decl, kind), f'{label}: declaration {decl} not found as {kind} in {rel}')
    _require(isinstance(ref.get('informal_location'), str) and ref['informal_location'].strip(),
             f'{label}: informal_location required')
    status = ref.get('status')
    if kind == 'theorem':
        _require(status in ('proved', 'kernel_checked'), f'{label}: theorem status must be proved or kernel_checked')
        if status == 'kernel_checked':
            _require(decl in pkg['_audit'], f'{label}: kernel_checked theorem {decl} is absent from the pinned axiom audit')
    else:
        _require(status == 'specified', f'{label}: {kind} status must be specified')
        _require(decl not in pkg['_audit'], f'{label}: {decl} is audited as a theorem but registered as {kind}')


def _validate_alignment(reg: dict[str, Any], root: Path, entry: dict[str, Any]) -> None:
    review = entry.get('alignment_review')
    _require(isinstance(review, dict) and review.get('status') in reg['allowed_alignment'],
             f'{entry["claim_id"]}: alignment_review.status invalid')
    status = review['status']
    record = review.get('record')
    if entry['status'] == 'none':
        _require(status == 'NONE' and record is None, f'{entry["claim_id"]}: unformalized claim cannot carry an alignment review')
        return
    _require(status != 'NONE', f'{entry["claim_id"]}: formalized claim requires alignment status other than NONE')
    if status in ('ACCEPT', 'AMEND_REQUIRED'):
        _require(isinstance(record, dict), f'{entry["claim_id"]}: alignment {status} requires a record')
        rel = safe_relpath(record.get('path'))
        _require(rel.startswith('reviews/'), f'{entry["claim_id"]}: alignment record must live under reviews/')
        raw = read_regular(root, rel)
        pin = identity(raw)
        _require(record.get('sha256') == pin['sha256'] and record.get('bytes') == pin['bytes'],
                 f'{entry["claim_id"]}: alignment record pin drift')
        reviewer = record.get('reviewer')
        _require(isinstance(reviewer, dict) and isinstance(reviewer.get('provider'), str) and reviewer['provider'],
                 f'{entry["claim_id"]}: alignment reviewer provider required')
        author = entry.get('formal_author', {})
        _require(reviewer.get('agent') not in (None, '', author.get('agent')) or reviewer.get('session') not in (None, '', author.get('session')),
                 f'{entry["claim_id"]}: alignment reviewer must be a distinct agent/session from the formal author')
        _require(type(record.get('organizational_independence')) is bool,
                 f'{entry["claim_id"]}: organizational_independence must be an explicit boolean')
        _require(record.get('reviewed_informal_blob') == entry['informal']['blob'],
                 f'{entry["claim_id"]}: alignment record reviewed a different informal blob')
        for rel_lean, pinned in (record.get('reviewed_sources') or {}).items():
            _require(reg['sources'].get(safe_relpath(rel_lean)) == pinned,
                     f'{entry["claim_id"]}: alignment record reviewed a stale Lean source {rel_lean}')
        _require(record.get('reviewed_sources'), f'{entry["claim_id"]}: alignment record must list reviewed Lean sources')
    else:
        _require(record is None, f'{entry["claim_id"]}: {status} cannot carry a record')


def _validate_entries(reg: dict[str, Any], root: Path, claims: dict[str, Any], graph: dict[str, Any]) -> None:
    entries = reg.get('entries')
    _require(isinstance(entries, list) and entries, 'nonempty entries list required')
    ids = [e.get('claim_id') for e in entries if isinstance(e, dict)]
    _require(len(ids) == len(entries) and all(isinstance(i, str) and i for i in ids), 'every entry requires claim_id')
    _require(len(set(ids)) == len(ids), 'duplicate claim_id in registry')
    manifest_ids = {c['claim_id'] for c in claims['claims']}
    _require(set(ids) == manifest_ids,
             f'registry/manifest mismatch: missing={sorted(manifest_ids - set(ids))} unknown={sorted(set(ids) - manifest_ids)}')
    by_id = {c['claim_id']: c for c in claims['claims']}
    for entry in entries:
        cid = entry['claim_id']
        claim = by_id[cid]
        informal = entry.get('informal')
        _require(isinstance(informal, dict), f'{cid}: informal binding required')
        _require(informal.get('path') == claim['statement_path'], f'{cid}: informal path differs from landing manifest')
        _require(informal.get('blob') == claim['source']['blob'],
                 f'{cid}: informal blob differs from landing manifest (alignment is stale; re-review required)')
        node = entry.get('graph_node')
        if node is not None:
            _require(node in graph['nodes'], f'{cid}: graph_node {node} is not in the dependency graph')
        status = entry.get('status')
        _require(status in STATUS_ORDER, f'{cid}: unknown status {status}')
        _require(isinstance(entry.get('status_reason'), str) and entry['status_reason'].strip(), f'{cid}: status_reason required')
        components = entry.get('components')
        _require(isinstance(components, list), f'{cid}: components must be a list')
        statement = entry.get('statement')
        if status == 'none':
            _require(statement is None and not components, f'{cid}: status none forbids statement/components')
        else:
            _require(isinstance(statement, dict), f'{cid}: formalized claim requires a statement record')
            _require(isinstance(entry.get('formal_author'), dict) and entry['formal_author'].get('provider'),
                     f'{cid}: formal_author provenance required')
            stmt = dict(statement)
            if status == 'specified':
                _require(stmt.get('kind') == 'prop_specification', f'{cid}: specified requires a prop_specification statement')
                stmt['status'] = 'specified'
            else:
                _require(stmt.get('kind') == 'theorem', f'{cid}: {status} requires a theorem statement')
                stmt['status'] = status
            _validate_ref(reg, root, stmt, label=f'{cid} statement')
            comp_ids = [c.get('id') for c in components]
            _require(all(isinstance(i, str) and i for i in comp_ids) and len(set(comp_ids)) == len(comp_ids),
                     f'{cid}: component ids must be unique nonempty strings')
            for comp in components:
                _validate_ref(reg, root, comp, label=f'{cid} component {comp.get("id")}')
            if status == 'kernel_checked':
                _require(all(c.get('status') == 'kernel_checked' for c in components if c.get('kind') == 'theorem'),
                         f'{cid}: kernel_checked claim cannot rest on unreplayed theorem components')
        _validate_alignment(reg, root, entry)


def _compose_with_layer0(reg: dict[str, Any], root: Path, graph: dict[str, Any], hard_gate) -> dict[str, Any]:
    """Assert the formal lane changes nothing in Layer 0 and that Layer 0 refuses formal tokens alone."""
    hard_gate.validate_graph_fail_closed(graph)
    composed = {}
    for entry in reg['entries']:
        node = entry.get('graph_node')
        if node is None:
            continue
        before = hard_gate.promotion_allowed(graph, node)
        refusals = {}
        for token in FORMAL_TOKENS:
            decision = hard_gate.refuse_non_discharge_promotion(graph, node, [token])
            _require(decision['refused'] is True, f'Layer 0 accepted formal token {token} alone for {node}')
            refusals[token] = 'REFUSED'
        after = hard_gate.promotion_allowed(graph, node)
        _require(json.dumps(before, sort_keys=True) == json.dumps(after, sort_keys=True), 'Layer 0 decision changed during composition')
        _require(graph['nodes'][node].get('controlling') is False, f'formal lane observed a controlling node: {node}')
        composed[entry['claim_id']] = {
            'graph_node': node,
            'layer0_classification': graph['nodes'][node]['classification'],
            'layer0_promotion_allowed': before['allowed'],
            'formal_tokens_alone': refusals,
        }
    return composed


def lane_verdict(entry: dict[str, Any]) -> str:
    status = entry['status']
    if status == 'kernel_checked' and entry['alignment_review']['status'] == 'ACCEPT':
        return ALIGNED_VERDICT
    return LANE_VERDICTS[status]


def validate(root: Path | None = None, registry_path: Path | None = None) -> dict[str, Any]:
    root = (root or ROOT).resolve()
    registry_path = registry_path or (root / 'formalization' / 'FORMALIZATION_STATUS.json')
    reg = strict_json(registry_path.read_text())
    _validate_vocabulary(reg)
    claims = strict_json(read_regular(root, safe_relpath(reg.get('claims_manifest'))).decode())
    _require(claims.get('repository') == reg['repository'], 'claims manifest repository mismatch')
    hard_gate = load_hard_gate(root)
    graph = hard_gate.load_json_strict(read_regular(root, safe_relpath(reg.get('dependency_graph'))).decode())
    hard_gate.validate_graph_fail_closed(graph)
    _validate_packages(reg, root)
    _validate_sources(reg, root)
    _validate_entries(reg, root, claims, graph)
    companions = _validate_companions(reg, root, claims)
    composed = _compose_with_layer0(reg, root, graph, hard_gate)

    lanes = {}
    for entry in reg['entries']:
        counts = {s: 0 for s in STATUS_ORDER}
        for comp in entry['components']:
            counts[comp['status']] += 1
        lanes[entry['claim_id']] = {
            'status': entry['status'],
            'alignment': entry['alignment_review']['status'],
            'lane_verdict': lane_verdict(entry),
            'component_counts': counts,
            'statement_decl': (entry.get('statement') or {}).get('decl'),
        }
    audited = {name: len(pkg['_audit']) for name, pkg in reg['packages'].items()}
    return {
        'object': reg['object'],
        'schema_version': 1,
        'claims_covered': len(reg['entries']),
        'lanes': lanes,
        'layer0_composition': composed,
        'companion_packages': companions,
        'audited_theorems': audited,
        'pinned_sources': len(reg['sources']),
        'toolchain': reg['toolchain'],
        'lemma_closed': False,
        'promotion_permission': False,
        'scientific_effect': 'NONE',
        'meaning': 'formal-lane identity/consistency/composition check; kernel replay is the --with-lean step; never theorem acceptance',
    }


# --------------------------------------------------------------------------- Lean replay

def replay_lean(root: Path | None = None, packages: list[str] | None = None, timeout: int = 3600) -> dict[str, Any]:
    """Run ``lake build`` and the axiom audit for each package; compare with the pinned audit."""
    root = (root or ROOT).resolve()
    reg = strict_json((root / 'formalization' / 'FORMALIZATION_STATUS.json').read_text())
    lake = shutil.which('lake')
    _require(lake is not None, 'lake is not on PATH; install elan and the pinned toolchain before --with-lean')
    out: dict[str, Any] = {}
    for name, pkg in reg['packages'].items():
        if packages and name not in packages:
            continue
        pdir = root / safe_relpath(pkg['path'])
        env = dict(os.environ)
        build = subprocess.run([lake, 'build'], cwd=pdir, capture_output=True, text=True, timeout=timeout, env=env)
        _require(build.returncode == 0, f'lake build failed for {name}:\n{build.stdout[-4000:]}\n{build.stderr[-4000:]}')
        audit = subprocess.run([lake, 'env', 'lean', 'scripts/Axioms.lean'], cwd=pdir, capture_output=True, text=True, timeout=timeout, env=env)
        _require(audit.returncode == 0, f'axiom audit failed for {name}:\n{audit.stdout[-4000:]}\n{audit.stderr[-4000:]}')
        actual = parse_axiom_audit(audit.stdout)
        expected = parse_axiom_audit((root / safe_relpath(pkg['axioms_expected'])).read_text())
        _require(actual == expected, f'axiom audit for {name} differs from pinned AXIOMS.expected; regenerate deliberately')
        forbidden = set(reg['forbidden_axioms'])
        for decl, axioms in actual.items():
            _require(not (set(axioms) & forbidden), f'forbidden axiom in {decl}: {sorted(set(axioms) & forbidden)}')
        out[name] = {'lake_build': 'ok', 'audited_theorems': len(actual), 'axioms_match_pinned': True}
    _require(out, 'no package replayed')
    return out


def refresh_pins(root: Path | None = None) -> dict[str, Any]:
    """Deliberately regenerate the ``sources`` pin table. Statuses are never touched."""
    root = (root or ROOT).resolve()
    path = root / 'formalization' / 'FORMALIZATION_STATUS.json'
    reg = strict_json(path.read_text())
    sources: dict[str, Any] = {}
    for pkg in reg['packages'].values():
        pdir = root / safe_relpath(pkg['path'])
        files = [p for p in pdir.rglob('*.lean') if '.lake' not in p.parts]
        files += [pdir / 'lakefile.toml', pdir / 'lean-toolchain', root / safe_relpath(pkg['axioms_expected'])]
        if pkg['depends_on_mathlib']:
            files.append(pdir / 'lake-manifest.json')
        for f in files:
            rel = f.relative_to(root).as_posix()
            sources[rel] = identity(f.read_bytes())
    reg['sources'] = dict(sorted(sources.items()))
    path.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + '\n')
    return reg['sources']


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--with-lean', action='store_true', help='replay lake build and the axiom audit')
    parser.add_argument('--package', action='append', help='restrict --with-lean to named packages')
    parser.add_argument('--refresh-pins', action='store_true', help='deliberately regenerate the sources pin table')
    parser.add_argument('--output', type=Path, help='write the report to a NEW file')
    parser.add_argument('--no-results-check', action='store_true', help='skip the FORMAL_RESULTS.json byte comparison')
    args = parser.parse_args(argv)
    try:
        if args.refresh_pins:
            pins = refresh_pins(args.root)
            print(f'refreshed {len(pins)} pins in formalization/FORMALIZATION_STATUS.json; statuses untouched', file=sys.stderr)
        report = validate(args.root)
        text = json.dumps(report, indent=2, sort_keys=True) + '\n'
        if args.with_lean:
            report['lean_replay'] = replay_lean(args.root, args.package)
        payload = json.dumps(report, indent=2, sort_keys=True) + '\n'
        if args.output:
            out = args.output.resolve()
            if out.exists():
                raise FormalGateError('output must be new')
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(payload)
        print(payload, end='')
        if not args.no_results_check:
            results = (Path(args.root).resolve() / 'formalization' / 'FORMAL_RESULTS.json')
            if not results.is_file() or results.read_text() != text:
                raise FormalGateError('FORMAL_RESULTS.json byte mismatch; regenerate deliberately')
        return 0
    except (FormalGateError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError, TypeError) as exc:
        print('FORMAL_GATE_REFUSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
