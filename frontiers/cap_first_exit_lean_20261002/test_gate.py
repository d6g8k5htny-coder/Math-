"""Unit tests for gate.py (standard library only; no Lean needed)."""
import contextlib
import hashlib
import io
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate  # noqa: E402

ALLOWED = ['propext', 'Classical.choice', 'Quot.sound']
COMMIT = '5045d0056413266e57c625dcd7c365b10e377c52'
RELEASE = 'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit ' + COMMIT + ', Release)'
PIN = 'leanprover/lean4:v4.34.1'
VERSION_PROBE = ['lake', 'env', 'lean', '--version']


def packet_copy(case):
    """A throwaway repository holding a copy of this packet and its two pinned sources on main."""
    tmp = pathlib.Path(tempfile.mkdtemp())
    case.addCleanup(shutil.rmtree, tmp)
    repo = tmp / 'repo'
    packet = repo / 'frontiers' / HERE.name
    packet.mkdir(parents=True)
    for p in HERE.iterdir():
        if p.is_file():
            shutil.copy2(p, packet / p.name)
    m = json.loads((HERE / 'MANIFEST.json').read_text())
    for pin in m['pins_on_main']:
        dst = repo / pin['path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(gate.REPO / pin['path'], dst)
    return repo, packet


class SourceGate(unittest.TestCase):
    def test_tree_passes(self):
        m = gate.source_check()
        self.assertEqual(len(m["targets"]), 152)
        self.assertEqual(m['scientific_effect'], 'NONE')

    def copy(self):
        return packet_copy(self)

    def assertGateFails(self, repo, packet, fragment):
        with self.assertRaises(ValueError) as ctx:
            gate.source_check(packet, repo)
        self.assertIn(fragment, str(ctx.exception))

    def test_copy_passes(self):
        repo, packet = self.copy()
        gate.source_check(packet, repo)

    def test_modified_lean_rejected(self):
        repo, packet = self.copy()
        p = packet / 'CapFirstExit.lean'
        p.write_text(p.read_text().replace('h ≤ s := by', 'h < s := by', 1))
        self.assertGateFails(repo, packet, 'source identity mismatch')

    def test_extra_file_rejected(self):
        repo, packet = self.copy()
        (packet / 'Extra.lean').write_text('import Mathlib\n')
        self.assertGateFails(repo, packet, 'packet tree differs')

    def test_pin_drift_rejected(self):
        repo, packet = self.copy()
        m = json.loads((HERE / 'MANIFEST.json').read_text())
        p = repo / m['pins_on_main'][0]['path']
        p.write_bytes(p.read_bytes() + b'\n')
        self.assertGateFails(repo, packet, 'pinned source drifted')


class Tokens(unittest.TestCase):
    def test_comments_ignored(self):
        self.assertEqual(gate.forbidden_tokens('/- sorry -/\n-- axiom\ntheorem t : True := trivial\n'), [])

    def test_nested_comment(self):
        self.assertEqual(gate.forbidden_tokens('/- a /- sorry -/ b -/\ntheorem t : True := trivial\n'), [])

    def test_code_detected(self):
        self.assertEqual(gate.forbidden_tokens('theorem t : False := by sorry\n'), ['sorry'])
        self.assertEqual(gate.forbidden_tokens('set_option maxHeartbeats 0\n'), ['set_option'])
        self.assertEqual(gate.forbidden_tokens('axiom p : False\n'), ['axiom'])
        self.assertEqual(gate.forbidden_tokens('/- x -/ example : 1 = 1 := by native_decide\n'), ['native_decide'])

    def test_unterminated_comment(self):
        with self.assertRaises(ValueError):
            gate.forbidden_tokens('/- open\n')


class Declarations(unittest.TestCase):
    def test_namespaces(self):
        text = ('namespace A\ntheorem x : True := trivial\nnamespace B\nnoncomputable def y : Nat := 0\n'
                'end B\nstructure Z : Prop where\n  p : True\nend A\n')
        self.assertEqual(gate.declarations(text), ['A.x', 'A.B.y', 'A.Z'])

    def test_sections_do_not_prefix(self):
        text = ('namespace A\nsection S\ntheorem x : True := trivial\nend S\n'
                'theorem y : True := trivial\nend A\n')
        self.assertEqual(gate.declarations(text), ['A.x', 'A.y'])

    def test_anonymous_section_rejected(self):
        with self.assertRaises(ValueError):
            gate.declarations('section\ntheorem x : True := trivial\nend\n')

    def test_unbalanced(self):
        with self.assertRaises(ValueError):
            gate.declarations('namespace A\nend B\n')
        with self.assertRaises(ValueError):
            gate.declarations('namespace A\ntheorem x : True := trivial\n')


class Pins(unittest.TestCase):
    def test_version_exact(self):
        ok = RELEASE + '\n'
        self.assertTrue(gate.check_lean_version(ok, 'leanprover/lean4:v4.34.1').startswith('Lean (version 4.34.1,'))
        for bad in ('Lean (version 4.34.2, x86_64, Release)', 'Lean (version 4.34.10, x86_64, Release)',
                    'Lean (version 4.34.1-rc1, x86_64, Release)', ''):
            with self.assertRaises(ValueError):
                gate.check_lean_version(bad, 'leanprover/lean4:v4.34.1')
        with self.assertRaises(ValueError):
            gate.pinned_lean_version('leanprover/lean4:nightly')

    def assertVersionRejected(self, text, pin=PIN):
        with self.assertRaises(ValueError, msg=repr(text)):
            gate.check_lean_version(text, pin)

    def test_release_line_accepted_exactly(self):
        self.assertEqual(gate.check_lean_version(RELEASE + '\n', PIN), RELEASE)
        self.assertEqual(gate.check_lean_version('  ' + RELEASE + '  \r\n', PIN), RELEASE)
        arm = RELEASE.replace('x86_64-unknown-linux-gnu', 'aarch64-unknown-linux-gnu')
        self.assertEqual(gate.check_lean_version(arm, PIN), arm)

    def test_same_semver_other_commit_rejected(self):
        for commit in ('0123456789abcdef0123456789abcdef01234567', COMMIT[:-1] + '3', COMMIT.upper(), COMMIT[:12],
                       COMMIT + '0', 'abc'):
            self.assertVersionRejected(RELEASE.replace(COMMIT, commit))
        self.assertVersionRejected(RELEASE.replace(', commit ' + COMMIT, ''))

    def test_non_release_build_rejected(self):
        for build in (', Debug)', ', RelWithDebInfo)', ', release)', ', Release, dirty)', ')', ', )'):
            self.assertVersionRejected(RELEASE.replace(', Release)', build))
        self.assertVersionRejected(RELEASE[:-1])
        self.assertVersionRejected('Lean (version 4.34.1, commit ' + COMMIT + ', Release)')

    def test_text_around_the_version_line(self):
        for text in (RELEASE + ' extra', RELEASE + '\nextra', RELEASE + '\n\nwarning: toolchain override',
                     'warning: override\n' + RELEASE, RELEASE + '\n' + RELEASE, 'x ' + RELEASE,
                     RELEASE + '\ninfo: trailing', '\n \n'):
            self.assertVersionRejected(text)

    def test_info_lines_before_the_version_line_accepted(self):
        text = 'info: downloading component lean\ninfo: installing toolchain\n\n' + RELEASE + '\n'
        self.assertEqual(gate.check_lean_version(text, PIN), RELEASE)

    def test_version_comes_from_the_toolchain_pin(self):
        self.assertVersionRejected(RELEASE, 'leanprover/lean4:v4.34.2')
        self.assertVersionRejected(RELEASE.replace('4.34.1', '4.34.2'), 'leanprover/lean4:v4.34.2')
        self.assertVersionRejected(RELEASE.replace('4.34.1', '4.34.2'))

    def test_worktree_clean(self):
        gate.check_worktree_clean('mathlib', '')
        for status in (' M Mathlib/Order/Basic.lean\n', 'M  Mathlib/Order/Basic.lean\n', '?? extra.lean\n'):
            with self.assertRaises(ValueError):
                gate.check_worktree_clean('mathlib', status)


class Axioms(unittest.TestCase):
    def test_allowed(self):
        text = ("'A.x' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
                "'A.y' does not depend on any axioms\n")
        self.assertEqual(gate.audit_axioms(text, ['A.x', 'A.y'], ALLOWED),
                         {'A.x': ['Classical.choice', 'Quot.sound', 'propext'], 'A.y': []})

    def test_forbidden(self):
        for bad in ('sorryAx', 'Lean.ofReduceBool', 'hiddenPremise'):
            with self.assertRaises(ValueError) as ctx:
                gate.audit_axioms("'A.x' depends on axioms: [propext, " + bad + "]\n", ['A.x'], ALLOWED)
            self.assertIn('forbidden transitive axiom', str(ctx.exception))

    def test_missing_and_duplicate(self):
        with self.assertRaises(ValueError):
            gate.audit_axioms("'A.x' does not depend on any axioms\n", ['A.x', 'A.y'], ALLOWED)
        with self.assertRaises(ValueError):
            gate.audit_axioms("'A.x' does not depend on any axioms\n" * 2, ['A.x'], ALLOWED)
        with self.assertRaises(ValueError):
            gate.audit_axioms("'A.z' does not depend on any axioms\n", ['A.x'], ALLOWED)


class FakeLake:
    """Stands in for `lake`/`lean`/`git` at the subprocess boundary; no real Lean is ever invoked.

    `versions` are the successive outputs of `lake env lean --version`; `during` runs once, at the
    first negative control, i.e. after the build and the axiom audit and before the final observation."""

    def __init__(self, m, versions, during=None):
        self.m, self.versions, self.during = m, list(versions), during
        self.heads = dict(m['dependency_revisions'])
        self.status = {name: '' for name in self.heads}
        self.commands = []

    def run(self, command, cwd=None, **kwargs):
        self.commands.append(list(command))
        if command == VERSION_PROBE:
            stdout = self.versions.pop(0) if len(self.versions) > 1 else self.versions[0]
        elif command == ['lake', 'build']:
            stdout = 'Build completed successfully.\n'
        elif command[:3] == ['lake', 'env', 'leanchecker']:
            stdout = ''
        elif command[:3] == ['lake', 'env', 'lean'] and command[3].endswith('Axioms.lean'):
            stdout = ''.join("'" + n + "' depends on axioms: [" + ', '.join(self.m['expected_axioms'][n]) + ']\n'
                             for n in self.m['targets'])
        elif command[:3] == ['lake', 'env', 'lean'] and pathlib.Path(command[3]).name.startswith('Control_'):
            if self.during is not None:
                during, self.during = self.during, None
                during(self)
            bad = {'Control_sorry.lean': 'sorryAx', 'Control_custom_axiom.lean': 'hiddenPremise',
                   'Control_native_decide.lean': 'Lean.ofReduceBool'}[pathlib.Path(command[3]).name]
            stdout = "'injected' depends on axioms: [propext, " + bad + ']\n'
        else:
            raise AssertionError('unexpected command: ' + repr(command))
        return types.SimpleNamespace(stdout=stdout, stderr='', returncode=0)

    def check_output(self, command, text=True, **kwargs):
        name = pathlib.Path(command[2]).name
        if command[3:] == ['rev-parse', 'HEAD']:
            return self.heads[name] + '\n'
        if command[3:5] == ['status', '--porcelain']:
            return self.status[name]
        raise AssertionError('unexpected command: ' + repr(command))


class Execute(unittest.TestCase):
    """`execute` end to end against a copy of the packet, with Lean, lake and git faked."""

    def setUp(self):
        self.repo, self.packet = packet_copy(self)
        self.m = gate.source_check(self.packet, self.repo)

    def execute(self, versions=(RELEASE,), during=None):
        fake = FakeLake(self.m, versions, during)
        with mock.patch.object(gate, 'ROOT', self.packet), mock.patch.object(gate, 'REPO', self.repo), \
                mock.patch.object(subprocess, 'run', fake.run), mock.patch.object(subprocess, 'check_output', fake.check_output):
            receipt = gate.execute(self.m)
        return fake, receipt

    def assertExecuteFails(self, fragment, versions=(RELEASE,), during=None):
        with self.assertRaises(ValueError) as ctx:
            self.execute(versions, during)
        self.assertIn(fragment, str(ctx.exception))
        self.assertFalse((self.packet / '.lake' / 'evidence' / 'receipt.json').exists())

    def test_clean_run_observes_both_ends(self):
        fake, receipt = self.execute()
        self.assertEqual(fake.commands[0], VERSION_PROBE)
        self.assertEqual(fake.commands[-1], VERSION_PROBE)
        self.assertEqual(fake.commands.count(VERSION_PROBE), 2)
        self.assertEqual([c[3] for c in fake.commands if c[:3] == ['lake', 'env', 'lean'] and c != VERSION_PROBE][-1],
                         str(self.packet / '.lake' / 'evidence' / 'Control_native_decide.lean'))
        evidence = self.packet / '.lake' / 'evidence'
        self.assertEqual((evidence / 'version.log').read_text(), RELEASE)
        self.assertEqual((evidence / 'version_final.log').read_text(), RELEASE)
        self.assertEqual(json.loads((evidence / 'receipt.json').read_text()), receipt)

    def test_receipt_records_both_observations(self):
        _, receipt = self.execute()
        old_keys = {'scientific_effect', 'module', 'lean_version', 'toolchain', 'dependency_revisions', 'source_sha256',
                    'build', 'leanchecker', 'dependency_worktrees', 'axioms', 'negative_controls', 'alignment_review'}
        self.assertEqual(set(receipt), old_keys | {'observations'})
        self.assertEqual(receipt['lean_version'], RELEASE)
        self.assertEqual(receipt['dependency_revisions'], self.m['dependency_revisions'])
        self.assertEqual(receipt['source_sha256'], {e['path']: e['sha256'] for e in self.m['files']})
        self.assertEqual(receipt['negative_controls'], dict.fromkeys(('sorry', 'custom_axiom', 'native_decide'), 'REJECTED'))
        self.assertEqual((receipt['scientific_effect'], receipt['alignment_review']), ('NONE', 'NOT_CLAIMED'))
        obs = receipt['observations']
        self.assertEqual(set(obs), {'preflight', 'final'})
        digest = gate.source_identity(self.m, self.packet, self.repo)
        for side in ('preflight', 'final'):
            self.assertEqual(obs[side], {'lean_version': RELEASE, 'dependency_revisions': self.m['dependency_revisions'],
                                         'dependency_worktrees': 'CLEAN', 'source_identity_sha256': digest})

    def test_info_lines_before_version_accepted_in_execute(self):
        _, receipt = self.execute(versions=('info: downloading component lean\n' + RELEASE + '\n',))
        self.assertEqual(receipt['observations']['preflight']['lean_version'], RELEASE)

    def test_preflight_wrong_commit_rejected_before_any_build(self):
        wrong = RELEASE.replace(COMMIT, '0123456789abcdef0123456789abcdef01234567')
        fake = FakeLake(self.m, [wrong])
        with mock.patch.object(gate, 'ROOT', self.packet), mock.patch.object(gate, 'REPO', self.repo), \
                mock.patch.object(subprocess, 'run', fake.run), mock.patch.object(subprocess, 'check_output', fake.check_output):
            with self.assertRaises(ValueError) as ctx:
                gate.execute(self.m)
        self.assertIn('running Lean is not the pinned release', str(ctx.exception))
        self.assertEqual(fake.commands, [VERSION_PROBE])

    def test_preflight_debug_build_rejected(self):
        self.assertExecuteFails('running Lean is not the pinned release', versions=(RELEASE.replace('Release)', 'Debug)'),))

    def test_final_version_differs_from_preflight(self):
        other = RELEASE.replace('x86_64-unknown-linux-gnu', 'aarch64-unknown-linux-gnu')
        self.assertEqual(gate.check_lean_version(other, PIN), other)  # each alone is the pinned release
        self.assertExecuteFails('Lean runtime changed during execution', versions=(RELEASE, other))

    def test_final_version_not_the_release(self):
        for final, fragment in ((RELEASE.replace(COMMIT, 'f' * 40), 'running Lean is not the pinned release'),
                                (RELEASE.replace('Release)', 'Debug)'), 'running Lean is not the pinned release'),
                                (RELEASE + '\nextra', 'unexpected output around the Lean version')):
            self.assertExecuteFails(fragment, versions=(RELEASE, final))

    def test_main_execute_entry(self):
        for versions, passed in (((RELEASE,), True), ((RELEASE, RELEASE.replace(COMMIT, 'f' * 40)), False)):
            fake = FakeLake(self.m, versions)
            stdout = io.StringIO()
            with mock.patch.object(gate, 'ROOT', self.packet), mock.patch.object(gate, 'REPO', self.repo), \
                    mock.patch.object(subprocess, 'run', fake.run), mock.patch.object(subprocess, 'check_output', fake.check_output), \
                    mock.patch.object(sys, 'argv', ['gate.py', '--execute']), contextlib.redirect_stdout(stdout):
                if passed:
                    gate.main()
                else:
                    with self.assertRaises(ValueError):
                        gate.main()
            if passed:
                self.assertTrue(json.loads(stdout.getvalue())['passed'])
            else:
                self.assertEqual(stdout.getvalue(), '')
            self.assertEqual(fake.commands.count(VERSION_PROBE), 2)

    def test_lean_source_changed_during_execution(self):
        def edit(fake):
            p = self.packet / 'CapFirstExit.lean'
            p.write_text(p.read_text().replace('h ≤ s := by', 'h < s := by', 1))
        self.assertExecuteFails('source identity mismatch: CapFirstExit.lean', during=edit)

    def test_source_and_manifest_rewritten_together_during_execution(self):
        def rewrite(fake):
            p = self.packet / 'CapFirstExit.lean'
            p.write_text(p.read_text().replace('h ≤ s := by', 'h < s := by', 1))
            data = p.read_bytes()
            manifest = json.loads((self.packet / 'MANIFEST.json').read_text())
            for e in manifest['files']:
                if e['path'] == 'CapFirstExit.lean':
                    e['bytes'], e['sha256'] = len(data), hashlib.sha256(data).hexdigest()
            (self.packet / 'MANIFEST.json').write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + '\n')
            gate.source_check(self.packet, self.repo)  # the rewritten packet is self-consistent
        self.assertExecuteFails('MANIFEST.json differs from the manifest bound before execution', during=rewrite)

    def test_manifest_bytes_changed_during_execution(self):
        def touch(fake):
            p = self.packet / 'MANIFEST.json'
            p.write_bytes(p.read_bytes() + b'\n')
            self.assertEqual(gate.source_check(self.packet, self.repo), self.m)  # same parsed manifest
        self.assertExecuteFails('bound source changed during execution', during=touch)

    def test_main_pin_changed_during_execution(self):
        def drift(fake):
            p = self.repo / self.m['pins_on_main'][0]['path']
            p.write_bytes(p.read_bytes() + b'\n')
        self.assertExecuteFails('pinned source drifted', during=drift)

    def test_dependency_head_drift_during_execution(self):
        def move(fake):
            fake.heads['mathlib'] = '0' * 40
        self.assertExecuteFails('checked-out dependency revisions differ from MANIFEST.json', during=move)

    def test_dependency_worktree_dirtied_during_execution(self):
        def dirty(fake):
            fake.status['batteries'] = ' M Batteries/Data/List/Basic.lean\n'
        self.assertExecuteFails('dependency worktree is not clean: batteries', during=dirty)


if __name__ == '__main__':
    unittest.main()
