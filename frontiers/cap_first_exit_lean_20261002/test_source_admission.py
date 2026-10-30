"""Actual Cap source admission regression; no Lean execution in these tests."""
import hashlib
import json
import pathlib
import unittest

import gate
from test_gate import packet_copy


class SourceAdmission(unittest.TestCase):
    def mutate(self, injection):
        repo, packet = packet_copy(self)
        source = packet / 'CapFirstExit.lean'
        source.write_bytes(source.read_bytes() + injection.encode())
        manifest = json.loads((packet / 'MANIFEST.json').read_text())
        for row in manifest['files']:
            if row['path'] == 'CapFirstExit.lean':
                row['bytes'] = len(source.read_bytes())
                row['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
        (packet / 'MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False) + '\n')
        return repo, packet

    def test_digest_rebound_private_theorem_is_rejected(self):
        repo, packet = self.mutate('\nnamespace CapFirstExit\nprivate theorem cbzUnlisted : True := by trivial\nend CapFirstExit\n')
        with self.assertRaisesRegex(ValueError, 'forbidden tokens'):
            gate.source_check(packet, repo)

    def test_unlisted_definition_cannot_be_hidden_by_source_hash_rebinding(self):
        repo, packet = self.mutate('\nnamespace CapFirstExit\ndef unlistedDatum : Nat := 0\nend CapFirstExit\n')
        with self.assertRaisesRegex(ValueError, 'declared targets differ'):
            gate.source_check(packet, repo)

    def test_forged_visible_kind_map_is_rejected(self):
        repo, packet = packet_copy(self)
        m = json.loads((packet/'MANIFEST.json').read_text())
        m['compiled_visible_kinds']['CapFirstExit.CapHyp'] = 'theorem'
        (packet/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False)+'\n')
        with self.assertRaisesRegex(ValueError, 'visible declaration kinds'):
            gate.source_check(packet,repo)

    def test_absent_actual_census_cannot_self_qualify(self):
        m = gate.source_check()
        m['compiled_inventory'] = None
        with self.assertRaisesRegex(ValueError, 'UNQUALIFIED'):
            gate.compiled_contract(m, gate.compiled_implementation())

    def test_binding_observation_must_match_original_proof_identity(self):
        m=gate.source_check()
        m['compiled_inventory_observation']['proof_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'proof identity'):
            gate.compiled_contract(m,gate.compiled_implementation())

    def test_noncache_nested_source_is_not_silently_omitted(self):
        repo, packet = packet_copy(self)
        nested = packet/'extra'/'hidden.py'
        nested.parent.mkdir(); nested.write_text('extra = 1\n')
        with self.assertRaisesRegex(ValueError, 'packet tree differs'):
            gate.source_check(packet,repo)


if __name__ == '__main__':
    unittest.main()
