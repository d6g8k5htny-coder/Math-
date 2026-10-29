"""Unlisted symlink directories must not hide source/cache module files."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import owned_kernel_audit as audit

class OwnedInventoryPathTests(unittest.TestCase):
    def test_symlink_directory_cannot_hide_an_unbound_cache_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); cache=root/'cache'; cache.mkdir()
            (cache/'A.olean').write_bytes(b'bound cache')
            outside=root/'outside'; outside.mkdir()
            (outside/'Legacy.olean').write_bytes(b'unbound module')
            (cache/'Hidden').symlink_to(outside,target_is_directory=True)
            expected={'A.olean':hashlib.sha256(b'bound cache').hexdigest()}
            output=root/'staged'; output.mkdir()
            with self.assertRaisesRegex(ValueError,'symlink|unsupported|inventory'):
                audit.stage_cache(cache,output,expected)
            self.assertFalse((output/'A.olean').exists(),'malformed inventory should reject before copying')

    def test_source_snapshot_recheck_rejects_added_symlink_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'source'; (source/'formal').mkdir(parents=True)
            (source/'formal/A.lean').write_text('theorem t : True := True.intro\n')
            (source/'audit_targets.json').write_text('{"names":["A.t"]}\n')
            snapshot=audit.freeze_sources(source,root/'snapshot')
            outside=root/'outside'; outside.mkdir(); (outside/'Hidden.lean').write_text('axiom broken : False\n')
            (source/'formal/Hidden').symlink_to(outside,target_is_directory=True)
            with self.assertRaisesRegex(ValueError,'symlink|unsupported|source'):
                audit.check_source_snapshot(source,snapshot)

if __name__=='__main__': unittest.main()
