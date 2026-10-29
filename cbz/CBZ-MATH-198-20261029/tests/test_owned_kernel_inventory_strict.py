"""Filesystem anomalies must fail before a source/cache inventory can certify coverage."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import owned_kernel_audit as audit


class StrictOwnedInventoryTests(unittest.TestCase):
    def test_special_cache_file_cannot_be_silently_omitted_before_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); cache=root/'cache'; cache.mkdir()
            (cache/'A.olean').write_bytes(b'bound')
            os.mkfifo(cache/'unlisted-pipe')
            staged=root/'staged'; staged.mkdir()
            with self.assertRaisesRegex(ValueError, 'special|unsupported|inventory'):
                audit.stage_cache(cache, staged, {'A.olean':hashlib.sha256(b'bound').hexdigest()})
            self.assertFalse((staged/'A.olean').exists())

    def test_added_special_source_file_cannot_disappear_from_recheck(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'source'; (source/'formal').mkdir(parents=True)
            (source/'formal/A.lean').write_text('theorem t : True := True.intro\n')
            (source/'audit_targets.json').write_text('{"names":["A.t"]}\n')
            snapshot=audit.freeze_sources(source,root/'snapshot')
            os.mkfifo(source/'formal/unlisted-pipe')
            with self.assertRaisesRegex(ValueError, 'special|unsupported|inventory|source'):
                audit.check_source_snapshot(source,snapshot)

    def test_formal_root_symlink_is_not_a_covered_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'source'; source.mkdir()
            outside=root/'outside'; outside.mkdir()
            (outside/'A.lean').write_text('theorem t : True := True.intro\n')
            (source/'formal').symlink_to(outside,target_is_directory=True)
            (source/'audit_targets.json').write_text('{"names":["A.t"]}\n')
            with self.assertRaisesRegex(ValueError, 'symlink|unsupported|inventory'):
                audit.freeze_sources(source,root/'snapshot')

    def test_unreadable_walk_is_not_an_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); cache=root/'cache'; cache.mkdir()
            (cache/'A.olean').write_bytes(b'bound')
            hidden=cache/'Hidden'; hidden.mkdir(); (hidden/'unseen.olean').write_bytes(b'unbound')
            real_scandir=os.scandir
            def unreadable(path):
                if Path(path)==hidden:
                    raise PermissionError(13, 'controlled filesystem read denial', str(hidden))
                return real_scandir(path)
            staged=root/'staged'; staged.mkdir()
            with patch('os.scandir', side_effect=unreadable):
                with self.assertRaisesRegex(ValueError, 'unreadable|inventory|filesystem'):
                    audit.stage_cache(cache, staged, {'A.olean':hashlib.sha256(b'bound').hexdigest()})
            self.assertFalse((staged/'A.olean').exists())

if __name__ == '__main__': unittest.main()
