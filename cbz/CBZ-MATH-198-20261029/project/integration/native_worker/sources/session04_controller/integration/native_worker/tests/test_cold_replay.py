"""Offline cold-path and formal output/source binding controls, no Lean launch."""
import copy,hashlib,json
from pathlib import Path
import tempfile,unittest
import sys
import native
import runtime_support as runtime
sys.path.insert(0,str(runtime.ROOT/'integration/engine_audit'))
import catalog

class ColdReplayTests(unittest.TestCase):
    def test_external_outputs_are_allowed_for_unsealed_and_sealed_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'payload';root.mkdir()
            build=Path(temp)/'cold-build';evidence=Path(temp)/'cold-evidence'
            self.assertFalse(native.validate_destinations(root,build,evidence))
            (root/'checksum_manifest.json').write_text('{}')
            self.assertTrue(native.validate_destinations(root,build,evidence))
            with self.assertRaises(ValueError):native.validate_destinations(root,root/'build',evidence)
            with self.assertRaises(ValueError):native.validate_destinations(root,build,root/'evidence')
            self.assertEqual(sorted(p.name for p in root.iterdir()),['checksum_manifest.json'])

    def test_fresh_formal_evidence_binds_actual_outputs_and_sources_without_fallback(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);cache=root/'cache';cache.mkdir();path=root/'formal-results.json'
            sources=catalog.verify_catalog()['provenance']['copied_formal_sources_sha256']
            outputs={}
            for source in sources:
                relative=source[7:-5]+'.olean';file=cache/relative;file.parent.mkdir(parents=True,exist_ok=True)
                file.write_bytes(('fixture bytes for '+source).encode());outputs[relative]=runtime.rt._hash(file)
            value={'status':'PASS','cache_was_fresh':True,'old_project_cache_on_lean_path':False,
                   'runtime':{'lean_executable_sha256':runtime.rt.LEAN_SHA,'mathlib_commit':runtime.rt.MATHLIB_COMMIT,'trust':'fixture'},
                   'sources':{**sources,'formal/Integration/EndpointTasks.lean':runtime.rt._hash(runtime.ROOT/'formal/Integration/EndpointTasks.lean')},
                   'outputs':outputs}
            path.write_text(json.dumps(value));self.assertEqual(len(runtime.dependency_bindings(cache,path)),17)
            for key in ('outputs','sources'):
                bad=copy.deepcopy(value);first=next(iter(bad[key]));bad[key][first]='0'*64;path.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):runtime.dependency_bindings(cache,path)
            path.write_text(json.dumps(value));(cache/'Specifications/P15.olean').unlink()
            with self.assertRaisesRegex(ValueError,'missing compiled formal dependency'):
                runtime.dependency_bindings(cache,path)

if __name__=='__main__':unittest.main()
