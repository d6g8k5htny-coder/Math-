"""Protocol tests of the lifetime note DD replay wrapper on synthetic packets; fixtures are not mathematical evidence."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / 'frontiers/lifetime_dd_model_d_20261013/replay.py'


def load():
    spec = importlib.util.spec_from_file_location('dd_replay_subject', WRAPPER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ident(data):
    return len(data), hashlib.sha256(data).hexdigest()


class SyntheticPacket:
    """a minimal packet tree: DD/ bodies, a controls comment with a pinned-file table, certificate/ files, SOURCES.json."""
    def __init__(self, tmp):
        self.root = Path(tmp) / 'packet'
        (self.root / 'DD').mkdir(parents=True)
        (self.root / 'certificate' / 'nodes').mkdir(parents=True)
        (self.root / 'certificate' / 'results').mkdir(parents=True)
        self.files = {}
        self.put('DD/PROOF.md', b'# synthetic note\n\nnothing here\n')
        cert = {}
        names = ['ddcore.py', 'ddbounds.py', 'ddtaylor.py', 'ddint.py', 'ddvq.py', 'ddgauss.py', 'ddS.py', 'dd_exact.py',
                 'dd_controls.py', 'dd_mutants.py', 'cells_full.json'] + ['nodes/nodes_%d.json' % k for k in range(12)]
        for n in names:
            data = ('synthetic %s\n' % n).encode()
            self.put('certificate/' + n, data)
            cert[n] = ident(data)
        table = '\n'.join('| `dd/%s` | %d | `%s` |' % (n, b, s) for n, (b, s) in cert.items())
        self.put('DD/AUTHOR_CONTROLS_COMMENT.md', ('controls\n\n| File | Bytes | SHA-256 |\n|---|---|---|\n' + table + '\n').encode())
        add = {}
        for n in ['dd_gapcheck.py', 'results/gapcheck_stdout.txt', 'results/gapcheck_stdout_O.txt']:
            data = ('synthetic %s\n' % n).encode()
            self.put('certificate/' + n, data)
            add[n] = ident(data)
        table2 = '\n'.join('| `dd/%s` | %d | `%s` |' % (n, b, s) for n, (b, s) in add.items())
        self.put('DD/AUTHOR_CONTROLS_ADDENDUM_C10.md', ('addendum\n\n| File | Bytes | SHA-256 |\n|---|---|---|\n' + table2 + '\n').encode())
        note_b, note_s = ident(self.files['DD/PROOF.md'])
        ctrl_b, ctrl_s = ident(self.files['DD/AUTHOR_CONTROLS_COMMENT.md'])
        self.put('DD/REVIEW_SLICE_A.md', ('PASS; note %d B %s; controls %d B %s\n' % (note_b, note_s, ctrl_b, ctrl_s)).encode(),
                 names_identities=['DD/PROOF.md', 'DD/AUTHOR_CONTROLS_COMMENT.md'])
        self.put('certificate/results/controls_stdout.txt', b'controls: ALL PASS\n')
        self.put('README.md', b'readme\n', own=True)
        self.replays = [dict(name='controls', script='dd_controls.py', args=[], stdout='certificate/results/controls_stdout.txt')]
        self.write_sources()

    def put(self, rel, data, own=False, names_identities=None):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        if not own:
            self.files[rel] = data
            self.meta = getattr(self, 'meta', {})
            self.meta[rel] = names_identities

    def manifest(self):
        stored = []
        for rel, data in sorted(self.files.items()):
            b, s = ident(data)
            e = dict(path=rel, bytes=b, sha256=s)
            if self.meta.get(rel): e['names_identities'] = self.meta[rel]
            stored.append(e)
        return dict(stored=stored, replays=self.replays)

    def write_sources(self):
        (self.root / 'SOURCES.json').write_text(json.dumps(self.manifest(), indent=1) + '\n')
        (self.root / 'replay.py').write_bytes(WRAPPER.read_bytes())


class ReplayProtocolTests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.tmp = tempfile.mkdtemp(prefix='dd-replay-test-')
        self.pk = SyntheticPacket(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_tree_passes_on_intact_packet(self):
        self.assertEqual(self.m.tree_failures(self.pk.root, self.pk.manifest()), [])

    def test_tree_rejects_changed_bytes(self):
        p = self.pk.root / 'DD' / 'PROOF.md'
        p.write_bytes(p.read_bytes() + b'x')
        self.assertTrue(any(f.startswith('identity mismatch: DD/PROOF.md') for f in self.m.tree_failures(self.pk.root, self.pk.manifest())))

    def test_tree_rejects_extra_and_missing_files(self):
        (self.pk.root / 'certificate' / 'extra.txt').write_bytes(b'x')
        (self.pk.root / 'certificate' / 'ddS.py').unlink()
        f = self.m.tree_failures(self.pk.root, self.pk.manifest())
        self.assertIn('unlisted file: certificate/extra.txt', f)
        self.assertIn('missing file: certificate/ddS.py', f)

    def test_tree_rejects_symlink(self):
        os.symlink(self.pk.root / 'README.md', self.pk.root / 'DD' / 'link.md')
        self.assertTrue(any(f.startswith('symlink: DD/link.md') for f in self.m.tree_failures(self.pk.root, self.pk.manifest())))

    def test_controls_table_passes_and_detects_mismatch(self):
        self.assertEqual(self.m.controls_table_failures(self.pk.root), [])
        p = self.pk.root / 'certificate' / 'ddvq.py'
        p.write_bytes(p.read_bytes() + b'y')
        self.assertIn('pinned identity mismatch: ddvq.py', self.m.controls_table_failures(self.pk.root))

    def test_controls_table_requires_23_rows(self):
        p = self.pk.root / 'DD' / 'AUTHOR_CONTROLS_COMMENT.md'
        body = p.read_text().split('\n')
        p.write_text('\n'.join(l for l in body if '`dd/ddS.py`' not in l))
        self.assertTrue(any(f.startswith('controls comment: expected 23 pinned files') for f in self.m.controls_table_failures(self.pk.root)))

    def test_addendum_table_requires_3_rows_and_detects_mismatch(self):
        p = self.pk.root / 'certificate' / 'dd_gapcheck.py'
        p.write_bytes(p.read_bytes() + b'z')
        self.assertIn('pinned identity mismatch: dd_gapcheck.py', self.m.controls_table_failures(self.pk.root))
        a = self.pk.root / 'DD' / 'AUTHOR_CONTROLS_ADDENDUM_C10.md'
        a.write_text('\n'.join(l for l in a.read_text().split('\n') if 'gapcheck_stdout_O' not in l))
        self.assertTrue(any(f.startswith('controls addendum: expected 3 pinned files') for f in self.m.controls_table_failures(self.pk.root)))

    def test_named_identities(self):
        self.assertEqual(self.m.named_identities_failures(self.pk.root, self.pk.manifest()), [])
        p = self.pk.root / 'DD' / 'REVIEW_SLICE_A.md'
        p.write_bytes(b'PASS without the hashes\n')
        self.pk.files['DD/REVIEW_SLICE_A.md'] = p.read_bytes()
        f = self.m.named_identities_failures(self.pk.root, self.pk.manifest())
        self.assertTrue(any('does not name the SHA-256 of DD/PROOF.md' in x for x in f))
        self.assertTrue(any('does not name the byte count of DD/AUTHOR_CONTROLS_COMMENT.md' in x for x in f))

    def test_named_identities_rejects_unstored_reference(self):
        man = self.pk.manifest()
        for e in man['stored']:
            if e['path'] == 'DD/REVIEW_SLICE_A.md':
                e['names_identities'] = ['DD/PROOF.md', 'DD/NOT_STORED.md']
        f = self.m.named_identities_failures(self.pk.root, man)
        self.assertTrue(any('unstored path DD/NOT_STORED.md' in x for x in f))

    def test_replay_matches_stored_stdout(self):
        (self.pk.root / 'certificate' / 'dd_controls.py').write_text("import sys\nsys.stdout.write('controls: ALL PASS\\n')\n")
        self.assertEqual(self.m.replay_failures(self.pk.root, self.pk.manifest(), quick=False), [])

    def test_replay_rejects_different_stdout_exit_and_stderr(self):
        (self.pk.root / 'certificate' / 'dd_controls.py').write_text("import sys\nsys.stdout.write('controls: FAILED\\n')\nsys.stderr.write('noise\\n')\nsys.exit(1)\n")
        f = self.m.replay_failures(self.pk.root, self.pk.manifest(), quick=False)
        self.assertIn('controls: exit 1', f)
        self.assertIn('controls: stdout differs from the stored record', f)
        self.assertIn('controls: stderr not empty', f)

    def test_quick_skips_long_replays(self):
        self.pk.replays = [dict(name='long', script='dd_exact.py', args=[], stdout='certificate/results/controls_stdout.txt', long=True)]
        self.assertEqual(self.m.replay_failures(self.pk.root, self.pk.manifest(), quick=True), [])

    def test_interpreter_flags_reflect_current_mode(self):
        flags = self.m.interpreter_flags()
        self.assertEqual(flags[0], '-B')
        self.assertEqual('-O' in flags, bool(sys.flags.optimize))
        self.assertEqual('-S' in flags, bool(sys.flags.no_site))

    def test_production_sources_consistent(self):
        """the real SOURCES.json lists the 23 certificate files and the stored DD/ records, with no duplicates."""
        man = json.loads((WRAPPER.parent / 'SOURCES.json').read_text())
        paths = [f['path'] for f in man['stored']]
        self.assertEqual(len(paths), len(set(paths)))
        cert = [p for p in paths if p.startswith('certificate/') and not p.startswith('certificate/results/')]
        self.assertEqual(len(cert), 25)   # 11 files + 12 node files + the artifact record + dd_gapcheck.py (C10)
        self.assertTrue(any(p == 'DD/PROOF.md' for p in paths))
        self.assertEqual(len(man['replays']), 4)

    def test_production_tree_and_table(self):
        """the real packet passes the tree, controls-table and named-identity checks."""
        man = json.loads((WRAPPER.parent / 'SOURCES.json').read_text())
        self.assertEqual(self.m.tree_failures(WRAPPER.parent, man), [])
        self.assertEqual(self.m.controls_table_failures(WRAPPER.parent), [])
        self.assertEqual(self.m.named_identities_failures(WRAPPER.parent, man), [])


if __name__ == '__main__':
    unittest.main()
