"""Real malformed-input controls; never import either recovered payload."""
import argparse
import dataclasses
import gzip
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

import inert_decoder as decoder

WRAPPER = b""
HERE = Path(__file__).resolve().parent


def identity(name, raw):
    return decoder.Identity(name, len(raw), hashlib.sha256(raw).hexdigest())


def fixture(raw=b"nonexecutable fixture\n"):
    compressed = gzip.compress(raw, mtime=0)
    spec = decoder.PayloadSpec("SOURCE", identity("fixture.py", raw),
                               identity("fixture.gz", compressed))
    return raw, compressed, spec


class DecoderControls(unittest.TestCase):
    def test_complete_single_member_decodes_exactly(self):
        raw, compressed, spec = fixture()
        self.assertEqual(decoder.decode_member(compressed, spec), raw)

    def test_truncation_rejects_even_when_compressed_identity_matches(self):
        _, compressed, spec = fixture()
        broken = compressed[:-1]
        spec = dataclasses.replace(spec, gzip=identity("fixture.gz", broken))
        with self.assertRaisesRegex(ValueError, "incomplete gzip"):
            decoder.decode_member(broken, spec)

    def test_trailing_byte_rejects_even_when_compressed_identity_matches(self):
        _, compressed, spec = fixture()
        broken = compressed + b"x"
        spec = dataclasses.replace(spec, gzip=identity("fixture.gz", broken))
        with self.assertRaisesRegex(ValueError, "trailing gzip"):
            decoder.decode_member(broken, spec)

    def test_concatenated_member_rejects(self):
        _, compressed, spec = fixture()
        broken = compressed + gzip.compress(b"second member", mtime=0)
        spec = dataclasses.replace(spec, gzip=identity("fixture.gz", broken))
        with self.assertRaisesRegex(ValueError, "trailing gzip"):
            decoder.decode_member(broken, spec)

    def test_invalid_crc_rejects(self):
        _, compressed, spec = fixture()
        broken = compressed[:-8] + bytes([compressed[-8] ^ 1]) + compressed[-7:]
        spec = dataclasses.replace(spec, gzip=identity("fixture.gz", broken))
        with self.assertRaisesRegex(ValueError, "invalid gzip"):
            decoder.decode_member(broken, spec)

    def test_payload_size_mismatch_rejects(self):
        raw, compressed, spec = fixture()
        spec = dataclasses.replace(spec, source=dataclasses.replace(spec.source, bytes=len(raw)+1))
        with self.assertRaisesRegex(ValueError, "payload size"):
            decoder.decode_member(compressed, spec)

    def test_payload_hash_mismatch_rejects(self):
        _, compressed, spec = fixture()
        spec = dataclasses.replace(spec, source=dataclasses.replace(spec.source, sha256="0"*64))
        with self.assertRaisesRegex(ValueError, "payload sha256"):
            decoder.decode_member(compressed, spec)

    def test_unsafe_filename_rejects(self):
        _, compressed, spec = fixture()
        spec = dataclasses.replace(spec, source=dataclasses.replace(spec.source, name="../fixture.py"))
        with self.assertRaisesRegex(ValueError, "unsafe filename"):
            decoder.decode_member(compressed, spec)

    def test_exact_public_wrapper_reconstructs_original_basename_pair(self):
        decoded = decoder.decode_wrapper(WRAPPER)
        self.assertEqual(set(decoded), {"GP-DATA-114-v1.0_uniform_q_degree4_interval.py",
                                       "GP-DATA-114-v1.0_receipt.json"})
        self.assertEqual(len(decoded["GP-DATA-114-v1.0_uniform_q_degree4_interval.py"]), 9787)
        self.assertEqual(len(decoded["GP-DATA-114-v1.0_receipt.json"]), 5047)

    def test_altered_wrapper_identity_rejects(self):
        with self.assertRaisesRegex(ValueError, "wrapper sha256"):
            decoder.decode_wrapper(WRAPPER.replace(b"ACTIVE WRAPPER", b"XCTIVE WRAPPER", 1))

    def test_duplicate_marker_rejects_after_rebinding_wrapper_fixture(self):
        broken = WRAPPER.replace(b"BEGIN_SOURCE_GZIP_BASE64", b"BEGIN_SOURCE_GZIP_BASE64\r\nBEGIN_SOURCE_GZIP_BASE64", 1)
        with self.assertRaisesRegex(ValueError, "marker count"):
            decoder.decode_wrapper(broken, identity("wrapper.txt", broken))

    def test_declared_compressed_size_rejects_after_rebinding_wrapper_fixture(self):
        broken = WRAPPER.replace(b"gzip bytes: 3416", b"gzip bytes: 3417", 1)
        with self.assertRaisesRegex(ValueError, "declared gzip bytes"):
            decoder.decode_wrapper(broken, identity("wrapper.txt", broken))

    def test_invalid_base64_rejects_after_rebinding_wrapper_fixture(self):
        broken = WRAPPER.replace(b"BEGIN_SOURCE_GZIP_BASE64\r\nH", b"BEGIN_SOURCE_GZIP_BASE64\r\n!", 1)
        with self.assertRaisesRegex(ValueError, "invalid base64"):
            decoder.decode_wrapper(broken, identity("wrapper.txt", broken))

    def test_changed_existing_payload_rejects(self):
        decoded = decoder.decode_wrapper(WRAPPER)
        with tempfile.TemporaryDirectory(prefix="controls_", dir=HERE) as directory:
            for name, raw in decoded.items():
                Path(directory, name).write_bytes(raw)
            Path(directory, "GP-DATA-114-v1.0_receipt.json").write_bytes(b"altered")
            with self.assertRaisesRegex(ValueError, "existing payload"):
                decoder.verify_existing(Path(directory), decoded)

    def test_existing_payload_symlink_rejects(self):
        decoded = decoder.decode_wrapper(WRAPPER)
        self.assertIn("GP-DATA-114-v1.0_receipt.json", decoded)
        with tempfile.TemporaryDirectory(prefix="controls_", dir=HERE) as directory:
            for name, raw in decoded.items():
                Path(directory, name).write_bytes(raw)
            leaf = Path(directory, "GP-DATA-114-v1.0_receipt.json")
            leaf.unlink()
            leaf.symlink_to("GP-DATA-114-v1.0_uniform_q_degree4_interval.py")
            with self.assertRaisesRegex(ValueError, "symlink"):
                decoder.verify_existing(Path(directory), decoded)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wrapper-input", required=True, help="Exact UTF-8 wrapper file, or '-' for stdin bytes")
    args = parser.parse_args()
    WRAPPER = sys.stdin.buffer.read() if args.wrapper_input == "-" else Path(args.wrapper_input).read_bytes()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DecoderControls))
    print(json.dumps({"tests_run": result.testsRun, "failures": len(result.failures),
                      "errors": len(result.errors), "passed": result.wasSuccessful()}, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
