"""Check local packet custody; this neither authenticates reviews nor proves mathematics."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import stat
import sys


ESSENTIAL = {'PROOF.md', 'SOURCES.json', 'VALIDATION.json', 'REVIEW_RECORD.json'}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: '+key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('nonfinite JSON constant: '+value)


def finite_float(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('nonfinite JSON number: '+value)
    return result


def read_regular(path):
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError('not a regular, nonsymlink file: '+str(path))
    return path.read_bytes()


def read_json(data, label):
    result = json.loads(data, object_pairs_hook=unique_object, parse_constant=reject_constant,
                        parse_float=finite_float)
    if not isinstance(result, dict):
        raise ValueError(label+' must be a JSON object')
    if type(result.get('schema')) is not int or result['schema'] != 1:
        raise ValueError(label+' must have integer schema 1')
    if result.get('scientific_effect') != 'NONE':
        raise ValueError(label+' scientific_effect must be NONE')
    return result


def safe_name(value):
    if (not isinstance(value, str) or not value or value in {'.', '..'}
            or any(c in value for c in '/\\:\0')):
        raise ValueError('unsafe or nonflat packet path: '+repr(value))
    return value


def check_identity(record, data, label):
    if not isinstance(record, dict):
        raise ValueError(label+' identity must be an object')
    size = record.get('bytes')
    if type(size) is not int or size < 0 or size != len(data):
        raise ValueError(label+' byte count mismatch or invalid type')
    actual = {'sha256': hashlib.sha256(data).hexdigest(),
              'git_blob': hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()}
    for key, length in [('sha256', 64), ('git_blob', 40)]:
        value = record.get(key)
        if not isinstance(value, str) or re.fullmatch('[0-9a-f]{'+str(length)+'}', value) is None:
            raise ValueError(label+' invalid '+key)
        if value != actual[key]:
            raise ValueError(label+' '+key+' mismatch')


def verify(packet_root):
    root = Path(packet_root)
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise ValueError('packet root must be a nonsymlink directory')
    manifest = read_json(read_regular(root / 'MANIFEST.json'), 'MANIFEST.json')
    if manifest.get('manifest_self_excluded') is not True:
        raise ValueError('MANIFEST.json must explicitly exclude itself')
    records = manifest.get('files')
    if not isinstance(records, list) or not records:
        raise ValueError('MANIFEST.json files must be a nonempty list')
    indexed = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError('manifest file entry must be an object')
        name = safe_name(record.get('path'))
        if name == 'MANIFEST.json' or name in indexed:
            raise ValueError('self or duplicate manifest path: '+name)
        indexed[name] = record
    if not ESSENTIAL <= indexed.keys():
        raise ValueError('manifest lacks essential packet files')
    observed = {p.name for p in root.iterdir()}
    expected = set(indexed) | {'MANIFEST.json'}
    if observed != expected:
        raise ValueError('packet membership mismatch; missing='+repr(sorted(expected-observed))
                         +'; undeclared='+repr(sorted(observed-expected)))
    payloads = {}
    for name, record in indexed.items():
        data = read_regular(root / name)
        check_identity(record, data, name)
        payloads[name] = data
    proof = payloads['PROOF.md']
    validation = read_json(payloads['VALIDATION.json'], 'VALIDATION.json')
    # VALIDATION is a retained author execution/history record, not finite_checks output.
    if validation.get('proof_sha256') != hashlib.sha256(proof).hexdigest():
        raise ValueError('VALIDATION.json proof_sha256 does not bind current PROOF.md')
    reviews = read_json(payloads['REVIEW_RECORD.json'], 'REVIEW_RECORD.json')
    proof_record = reviews.get('proof')
    if not isinstance(proof_record, dict) or proof_record.get('path') != 'PROOF.md':
        raise ValueError('REVIEW_RECORD.json must bind PROOF.md')
    check_identity(proof_record, proof, 'REVIEW_RECORD.json proof')
    return {'schema': 1, 'scientific_effect': 'NONE', 'packet_files_verified': len(indexed),
            'validation_proof_identity_verified': True, 'review_proof_identity_verified': True,
            'remote_review_authenticity_checked': False, 'mathematical_acceptance': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet-root', type=Path, default=Path(__file__).absolute().parent)
    args = parser.parse_args()
    try:
        result = verify(args.packet_root)
    except (ValueError, OSError) as error:
        print('packet identity failed: '+str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
