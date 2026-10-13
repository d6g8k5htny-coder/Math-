"""Protocol tests of the lifetime note C3-R replay wrapper: synthetic packets (fixtures are not mathematical evidence) and
the source checks of the stored packet."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'frontiers/lifetime_c3r_rate_20261013'
WRAPPER = PACKET / 'replay.py'


def load():
    spec = importlib.util.spec_from_file_location('c3r_replay_subject', WRAPPER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ident(data):
    return len(data), hashlib.sha256(data).hexdigest()


class SyntheticPacket:
    """a minimal packet tree: C3R/ bodies, a controls comment with the four-row pin table, controls/ files, SOURCES.json."""
    def __init__(self, tmp):
        self.root = Path(tmp) / 'packet'
        (self.root / 'C3R').mkdir(parents=True)
        (self.root / 'controls' / 'results').mkdir(parents=True)
        self.files = {}
        self.put('C3R/PROOF_v1_0_AS_READ.md', b'# synthetic note v1.0\n')
        self.put('C3R/PROOF.md', b'# synthetic note v1.1\n')
        rows = []
        for name in ('c3r_exact.py', 'c3r_mutants.py', 'c3r_stdout.txt', 'c3r_mutants_stdout.txt'):
            data = ('synthetic %s\n' % name).encode() * 300
            self.put(('controls/results/' if name.endswith('.txt') else 'controls/') + name, data)
            n, sha = ident(data)
            rows.append('| `%s` | %s | `%s` | `%s` |' % (name, '{:,}'.format(n), sha, '0' * 40))
        self.put('C3R/AUTHOR_CONTROLS_COMMENT.md', ('controls\n\n| File | Bytes | SHA-256 | Git blob |\n|---|---:|---|---|\n' + '\n'.join(rows) + '\n').encode())
        n, sha = self.files['C3R/PROOF_v1_0_AS_READ.md']
        self.put('C3R/REVIEW_SLICE_A.md', ('PASS; read v1.0, %s B, SHA-256 %s\n' % ('{:,}'.format(n), sha)).encode())
        self.names = {'C3R/REVIEW_SLICE_A.md': ['C3R/PROOF_v1_0_AS_READ.md']}
        for name in ('README.md', 'replay.py'):
            (self.root / name).write_bytes(b'own\n')
        self.write_manifest()

    def put(self, rel, data):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        self.files[rel] = ident(data)

    def write_manifest(self):
        stored = []
        for rel, (n, sha) in sorted(self.files.items()):
            e = dict(path=rel, bytes=n, sha256=sha)
            if rel in self.names:
                e['names_identities'] = self.names[rel]
            stored.append(e)
        self.manifest = dict(schema=2, stored=stored, replays=[])
        (self.root / 'SOURCES.json').write_text(json.dumps(self.manifest), encoding='utf-8')


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.p = SyntheticPacket(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_clean_synthetic_packet_passes_source_checks(self):
        self.assertEqual(self.m.tree_failures(self.p.root, self.p.manifest), [])
        self.assertEqual(self.m.controls_table_failures(self.p.root), [])
        self.assertEqual(self.m.named_identities_failures(self.p.root, self.p.manifest), [])

    def test_unlisted_and_missing_files(self):
        (self.p.root / 'C3R' / 'EXTRA.md').write_bytes(b'x')
        (self.p.root / 'C3R' / 'PROOF.md').unlink()
        f = self.m.tree_failures(self.p.root, self.p.manifest)
        self.assertIn('unlisted file: C3R/EXTRA.md', f)
        self.assertIn('missing file: C3R/PROOF.md', f)

    def test_one_byte_change_is_an_identity_mismatch(self):
        p = self.p.root / 'C3R' / 'PROOF.md'
        data = bytearray(p.read_bytes()); data[3] ^= 1; p.write_bytes(bytes(data))
        self.assertIn('identity mismatch: C3R/PROOF.md', self.m.tree_failures(self.p.root, self.p.manifest))

    @unittest.skipIf(os.name == 'nt', 'symlinks')
    def test_symlink_rejected(self):
        os.symlink(self.p.root / 'C3R' / 'PROOF.md', self.p.root / 'C3R' / 'LINK.md')
        self.assertIn('symlink: C3R/LINK.md', self.m.tree_failures(self.p.root, self.p.manifest))

    def test_pinned_control_changed_is_rejected(self):
        self.p.put('controls/c3r_exact.py', b'changed\n')
        self.assertIn('pinned identity mismatch: c3r_exact.py', self.m.controls_table_failures(self.p.root))

    def test_pin_table_row_count(self):
        p = self.p.root / 'C3R' / 'AUTHOR_CONTROLS_COMMENT.md'
        lines = p.read_text(encoding='utf-8').splitlines()
        p.write_text('\n'.join(lines[:-1]) + '\n', encoding='utf-8')
        f = self.m.controls_table_failures(self.p.root)
        self.assertTrue(any('expected 4 pinned files, found 3' in x for x in f), f)

    def test_named_identity_missing_hash(self):
        self.p.put('C3R/REVIEW_SLICE_A.md', b'PASS; no hash here\n')
        self.p.write_manifest()
        f = self.m.named_identities_failures(self.p.root, self.p.manifest)
        self.assertTrue(any('does not name the SHA-256 of C3R/PROOF_v1_0_AS_READ.md' in x for x in f), f)

    def test_named_identity_unstored_path(self):
        self.p.names['C3R/REVIEW_SLICE_A.md'] = ['C3R/NOPE.md']
        self.p.write_manifest()
        f = self.m.named_identities_failures(self.p.root, self.p.manifest)
        self.assertTrue(any('unstored path C3R/NOPE.md' in x for x in f), f)

    def test_interpreter_flags_follow_the_driver(self):
        flags = self.m.interpreter_flags()
        self.assertEqual(flags[0], '-B')
        self.assertEqual('-O' in flags, bool(sys.flags.optimize))
        self.assertEqual('-S' in flags, bool(sys.flags.no_site))

    def test_evidence_directory_must_be_outside_the_checkout(self):
        old = os.environ.get('QS_REPLAY_EVIDENCE_DIR')
        try:
            os.environ['QS_REPLAY_EVIDENCE_DIR'] = str(PACKET / 'evidence')
            with self.assertRaises(ValueError):
                self.m.evidence_directory(PACKET / 'controls' / 'c3r_exact.py')
            os.environ['QS_REPLAY_EVIDENCE_DIR'] = ''
            with self.assertRaises(ValueError):
                self.m.evidence_directory(PACKET / 'controls' / 'c3r_exact.py')
        finally:
            if old is None:
                os.environ.pop('QS_REPLAY_EVIDENCE_DIR', None)
            else:
                os.environ['QS_REPLAY_EVIDENCE_DIR'] = old


class StoredPacketTests(unittest.TestCase):
    """the stored packet passes the three source checks (the replays run in the workflow's replay step)."""
    def test_stored_packet_source_checks(self):
        m = load()
        manifest = json.loads((PACKET / 'SOURCES.json').read_text(encoding='utf-8'))
        self.assertEqual(m.tree_failures(PACKET, manifest), [])
        self.assertEqual(m.controls_table_failures(PACKET), [])
        self.assertEqual(m.named_identities_failures(PACKET, manifest), [])

    def test_manifest_scope(self):
        manifest = json.loads((PACKET / 'SOURCES.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['scientific_effect'], 'NONE')
        paths = {f['path'] for f in manifest['stored']}
        for p in ('C3R/PROOF.md', 'C3R/PROOF_v1_0_AS_READ.md', 'C3R/AUTHOR_CONTROLS_COMMENT.md', 'controls/c3r_exact.py', 'controls/c3r_mutants.py'):
            self.assertIn(p, paths)
        self.assertEqual([r['name'] for r in manifest['replays']], ['controls', 'mutants'])


if __name__ == '__main__':
    unittest.main()
