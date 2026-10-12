"""Supplied-data controls only; never a live C183 experiment or collector."""
import ast
import copy
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/c183_experiment_inputs.py'
FIXTURE = json.loads((ROOT / 'tests/fixtures/c183_experiment_input_cases.json').read_text())
M = None
if SCRIPT.exists():
    SPEC = importlib.util.spec_from_file_location('c183_inputs', SCRIPT)
    M = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(M)


def supplied():
    return copy.deepcopy(FIXTURE['valid'])


def raw(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=True).encode('utf-8')


class C183InputControls(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(M, 'supplied-data helper is not implemented')
        for name in ('project', 'render', 'main'):
            self.assertTrue(callable(getattr(M, name, None)), 'required API absent')

    def check_fixed(self, report):
        self.assertEqual(report['historical_environment_equivalence'], 'NOT_ESTABLISHED')
        self.assertEqual(report['collector_qualification'], 'NOT_RUN')
        self.assertEqual(report['live_payload_suppression'], 'NOT_RUN')
        self.assertEqual(report['experiment_execution'], 'NOT_RUN')
        self.assertEqual(report['planned_experiment_cases'], 40)
        self.assertEqual(report['cause'], 'UNKNOWN')
        self.assertIs(report['promotion_permission'], False)
        self.assertEqual(report['pr397_disposition'], 'HOLD / NOT_READY / NO_MERGE')
        self.assertEqual(report['scientific_effect'], 'NONE')
        self.assertEqual(report['actual_environment_match'], 'NOT_ESTABLISHED')
        self.assertEqual(report['writer_inference'], 'NOT_EVALUATED')
        self.assertEqual(report['historical_missing_provenance'], [
            'effective_configuration', 'effective_environment', 'binary_library_identities',
            'mount_identity', 'writer_start_identity', 'residual_entries'])

    def report(self, value):
        result = M.project(raw(value))
        self.check_fixed(result)
        return result

    def invalid(self, value):
        result = self.report(value)
        self.assertEqual(result['status'], 'INVALID_INPUT')
        self.assertIsNone(result['projection'])
        self.assertTrue(result['errors'])
        return result

    def test_complete_synthetic_pair_is_only_structurally_valid(self):
        result = self.report(supplied())
        self.assertEqual(result['status'], 'VALID_SUPPLIED_INPUT')
        self.assertEqual(result['comparison']['status'], 'MATCHED_SUPPLIED_FIELDS')
        self.assertEqual(result['comparison']['differences'], [])
        self.assertEqual(result['projection'], supplied())
        self.assertEqual(result['event_model_status'], 'SUPPLIED_MODEL_ONLY')

    def test_reported_origin_is_not_machine_authentication(self):
        value = supplied()
        for record in value['records'].values():
            record['origin'] = 'SUPPLIED'
        result = self.report(value)
        self.assertEqual(result['status'], 'VALID_SUPPLIED_INPUT')
        self.assertEqual(result['actual_environment_match'], 'NOT_ESTABLISHED')

    def test_missing_whole_input_and_records_are_incomplete(self):
        for value in ({}, {'schema_version': 1}, {'schema_version': 1, 'records': {}, 'events': []}):
            with self.subTest(keys=sorted(value)):
                self.assertEqual(self.report(value)['status'], 'INCOMPLETE_INPUT')

    def test_missing_each_mandatory_scalar_and_group_is_incomplete(self):
        for key in supplied()['records']['U']:
            value = supplied()
            del value['records']['U'][key]
            with self.subTest(field=key):
                self.assertEqual(self.report(value)['status'], 'INCOMPLETE_INPUT')

    def test_missing_each_environment_configuration_binary_mount_value_is_incomplete(self):
        for group in ('environment', 'configuration', 'binaries', 'mount'):
            for key in supplied()['records']['U'][group]:
                value = supplied()
                del value['records']['U'][group][key]
                with self.subTest(group=group, field=key):
                    self.assertEqual(self.report(value)['status'], 'INCOMPLETE_INPUT')

    def test_unknown_mandatory_value_is_preserved_as_unknown(self):
        value = supplied()
        value['records']['U']['binaries']['git_sha256'] = {'state': 'UNKNOWN'}
        result = self.report(value)
        self.assertEqual(result['status'], 'INCOMPLETE_INPUT')
        self.assertEqual(result['projection']['records']['U']['binaries']['git_sha256'], {'state': 'UNKNOWN'})
        self.assertEqual(result['comparison']['status'], 'INCOMPLETE_SUPPLIED_COMPARISON')

    def test_unknown_with_value_and_reported_without_value_are_invalid(self):
        for tagged in ({'state': 'UNKNOWN', 'value': True}, {'state': 'REPORTED'}, {'state': 'COMPLETE'}):
            value = supplied()
            value['records']['U']['configuration']['maintenance_auto'] = tagged
            self.invalid(value)

    def test_complete_assertion_and_historical_equivalence_cannot_be_supplied(self):
        for key in ('complete', 'historical_environment_equivalence', 'promotion_permission', 'cause'):
            value = supplied()
            value[key] = True
            self.invalid(value)

    def test_matching_image_or_version_labels_cannot_substitute_identities(self):
        value = supplied()
        value['records']['U']['binaries'] = {'git_version': '2.55.0', 'image': 'ubuntu-24.04'}
        self.invalid(value)
        value = supplied()
        value['records']['I']['binaries']['git_sha256']['value'] = '9' * 64
        self.assertEqual(self.report(value)['comparison']['differences'], ['binaries.git_sha256'])

    def test_supplied_configuration_and_mount_differences_are_named_only(self):
        value = supplied()
        value['records']['I']['configuration']['gc_auto']['value'] = -1
        value['records']['I']['mount']['identity_sha256']['value'] = '9' * 64
        result = self.report(value)
        self.assertEqual(result['comparison']['status'], 'DIFFERENT_SUPPLIED_FIELDS')
        self.assertEqual(result['comparison']['differences'], ['configuration.gc_auto', 'mount.identity_sha256'])

    def test_mode_variant_and_source_changes_are_detected(self):
        for key, changed in (('mode', 'optimized'), ('variant', 'accept_numeric_required')):
            value = supplied()
            value['records']['I'][key] = changed
            if key == 'variant':
                value['records']['I']['sources']['numeric_mutant'] = {'state': 'REPORTED', 'value': '9' * 64}
            self.assertIn(key, self.report(value)['comparison']['differences'])
        value = supplied()
        value['records']['I']['sources']['pristine']['value'] = '9' * 64
        self.assertIn('sources.pristine', self.report(value)['comparison']['differences'])

    def test_wrong_command_shape_and_observer_assignment_are_invalid(self):
        for key, changed in (('command_shape', 'python arbitrary.py'), ('observer', 'OUTSIDE_SOURCE')):
            value = supplied()
            value['records']['U'][key] = changed
            self.invalid(value)

    def test_observer_identity_is_separate_and_required_only_for_instrumented_cell(self):
        value = supplied()
        value['records']['I']['sources']['observer'] = {'state': 'UNKNOWN'}
        self.assertEqual(self.report(value)['status'], 'INCOMPLETE_INPUT')
        value = supplied()
        value['records']['U']['sources']['observer'] = {'state': 'REPORTED', 'value': '9' * 64}
        self.invalid(value)

    def test_baseline_cannot_claim_mutant_and_numeric_variant_needs_identity(self):
        value = supplied()
        value['records']['U']['sources']['numeric_mutant'] = {'state': 'REPORTED', 'value': '9' * 64}
        self.invalid(value)
        value = supplied()
        value['records']['U']['variant'] = 'accept_numeric_required'
        self.assertEqual(self.report(value)['status'], 'INCOMPLETE_INPUT')

    def test_numeric_variant_positive_control(self):
        value = supplied()
        for rec in value['records'].values():
            rec['variant'] = 'accept_numeric_required'
            rec['sources']['numeric_mutant'] = {'state': 'REPORTED', 'value': '9' * 64}
        self.assertEqual(self.report(value)['status'], 'VALID_SUPPLIED_INPUT')

    def test_duplicate_json_keys_fail_closed_without_echo(self):
        for payload in (b'{"schema_version":1,"schema_version":1}',
                        b'{"records":{"U":{"origin":"SYNTHETIC","origin":"SUPPLIED"}}}'):
            report = M.project(payload)
            self.check_fixed(report)
            self.assertEqual(report['status'], 'INVALID_INPUT')
            self.assertEqual(report['errors'], [{'code': 'DUPLICATE_KEY', 'category': 'json'}])

    def test_nonfinite_and_float_numbers_are_refused(self):
        for token in ('NaN', 'Infinity', '-Infinity', '1e999', '1.0', '1e0'):
            payload = ('{"schema_version":' + token + '}').encode()
            report = M.project(payload)
            self.assertEqual(report['status'], 'INVALID_INPUT')
        self.invalid({'schema_version': True})

    def test_boolean_integer_confusion_and_integer_bounds(self):
        for key, invalid in (('gc_auto', True), ('gc_auto', -2), ('gc_auto', 1000001),
                             ('maintenance_auto', 1), ('maintenance_auto', 'true')):
            value = supplied()
            value['records']['U']['configuration'][key]['value'] = invalid
            self.invalid(value)
        for timestamp in (True, -1, 253402300800):
            value = supplied()
            value['records']['U']['observed_at_unix_s']['value'] = timestamp
            self.invalid(value)

    def test_wrong_containers_and_scalar_types(self):
        for value in ([], None, True, 1, 'text'):
            self.invalid(value)
        for key, wrong in (('records', []), ('events', {}), ('schema_version', '1')):
            value = supplied()
            value[key] = wrong
            self.invalid(value)

    def test_invalid_digests_fail_without_values(self):
        for digest in ('', 'a' * 63, 'a' * 65, 'G' * 64, 'A' * 64, 7, None):
            value = supplied()
            value['records']['U']['binaries']['git_sha256']['value'] = digest
            self.invalid(value)

    def test_raw_argv_paths_environment_and_unknown_keys_are_refused(self):
        for key in ('argv', 'cwd', 'env', 'raw_stream', 'write_payload', 'access_url'):
            value = supplied()
            value['records']['U'][key] = FIXTURE['canary']
            self.invalid(value)
        value = supplied()
        value['records']['U']['environment']['PATH'] = FIXTURE['canary']
        self.invalid(value)

    def test_allowlisted_keys_cannot_smuggle_arbitrary_text(self):
        for group, key in (('environment', 'locale'), ('configuration', 'hooks_policy'),
                           ('mount', 'filesystem'), ('binaries', 'git_sha256')):
            value = supplied()
            value['records']['U'][group][key]['value'] = FIXTURE['canary']
            self.invalid(value)

    def test_canary_absent_from_all_public_output_and_exception_paths(self):
        for location in ('top', 'nested', 'event', 'enum', 'duplicate', 'malformed'):
            value = supplied()
            if location == 'top':
                value[FIXTURE['canary']] = {'payload': FIXTURE['canary']}
            elif location == 'nested':
                value['records']['U']['configuration']['payload'] = FIXTURE['canary']
            elif location == 'event':
                value['events'][0]['write_payload'] = FIXTURE['canary']
            elif location == 'enum':
                value['events'][0]['result'] = FIXTURE['canary']
            payload = raw(value)
            if location == 'duplicate':
                payload = ('{"' + FIXTURE['canary'] + '":0,"' + FIXTURE['canary'] + '":1}').encode()
            if location == 'malformed':
                payload = ('{"x":"' + FIXTURE['canary']).encode()
            out, err = io.BytesIO(), io.StringIO()
            with patch('sys.stderr', err):
                result = M.main(io.BytesIO(payload), out)
            self.assertEqual(result, 2, location)
            self.assertNotIn(FIXTURE['canary'].encode(), out.getvalue(), location)
            self.assertEqual(err.getvalue(), '')
            self.assertEqual(json.loads(out.getvalue())['status'], 'INVALID_INPUT')

    def test_unicode_surrogates_and_invalid_utf8_fail_without_exception(self):
        for payload in (b'{"x":"\\ud800"}', b'{"x":"\xff"}'):
            self.assertEqual(M.project(payload)['status'], 'INVALID_INPUT')

    def test_accepted_scalar_string_byte_limit_is_enforced(self):
        for value_string in ('x' * 257, '\u00e9' * 129):
            value = supplied()
            value['records']['U']['origin'] = value_string
            self.invalid(value)

    def test_input_byte_cap_and_reader_request_are_bounded(self):
        payload = b' ' * (1024 * 1024 + 1)
        self.assertEqual(M.project(payload)['errors'], [{'code': 'INPUT_LIMIT', 'category': 'json'}])
        class BoundedReader:
            def read(self, size):
                self.size = size
                return payload
        reader, out = BoundedReader(), io.BytesIO()
        self.assertEqual(M.main(reader, out), 2)
        self.assertEqual(reader.size, 1024 * 1024 + 1)

    def test_depth_preflight_prevents_excessive_json_recursion(self):
        for payload in (b'[' * 9 + b'0' + b']' * 9,
                        b'[' * 10000 + b'0' + b']' * 10000):
            self.assertEqual(M.project(payload)['errors'], [{'code': 'DEPTH_LIMIT', 'category': 'json'}])
        # Braces and escaped quotes inside strings are data, not nesting.
        self.assertEqual(M.project(b'{"x":"[[[[[[[[[\\\\"}')['status'], 'INVALID_INPUT')

    def test_event_count_boundary_and_overflow(self):
        value = supplied()
        value['events'] *= 2048
        for index, event in enumerate(value['events']):
            value['events'][index] = dict(event, sequence=index)
        self.assertEqual(self.report(value)['status'], 'VALID_SUPPLIED_INPUT')
        value['events'].append(dict(value['events'][0], sequence=2048))
        self.invalid(value)

    def test_unknown_event_kind_operation_and_extra_field_are_invalid(self):
        for key, changed in (('kind', 'TRACE2_RAW'), ('operation', 'EXEC_RAW'), ('payload', 'text')):
            value = supplied()
            value['events'][0][key] = changed
            self.invalid(value)

    def test_event_required_fields_and_wrong_types_are_invalid(self):
        for key in supplied()['events'][0]:
            value = supplied()
            del value['events'][0][key]
            self.invalid(value)
        for key, changed in (('sequence', True), ('sequence', -1), ('errno', 4096),
                             ('result', 'NO_WRITER'), ('subject', '/tmp/private')):
            value = supplied()
            value['events'][0][key] = changed
            self.invalid(value)

    def test_empty_event_sample_never_means_no_writer(self):
        value = supplied()
        value['events'] = []
        result = self.report(value)
        self.assertEqual(result['status'], 'VALID_SUPPLIED_INPUT')
        self.assertEqual(result['event_model_status'], 'EMPTY_SUPPLIED_MODEL')
        self.assertEqual(result['writer_inference'], 'NOT_EVALUATED')

    def test_absent_events_are_incomplete_not_empty_success(self):
        value = supplied()
        del value['events']
        self.assertEqual(self.report(value)['status'], 'INCOMPLETE_INPUT')

    def test_event_operation_family_and_result_errno_consistency(self):
        value = supplied()
        value['events'][0].update(kind='PROCESS', operation='RMDIR')
        self.invalid(value)
        value = supplied()
        value['events'][0].update(result='OK', errno=39)
        self.invalid(value)

    def test_duplicate_or_unordered_event_sequences_are_invalid(self):
        for sequences in ((0, 0), (2, 1)):
            value = supplied()
            value['events'] = [dict(value['events'][0], sequence=x) for x in sequences]
            self.invalid(value)

    def test_valid_event_families_survive_projection(self):
        value = supplied()
        value['events'] = [
            {'kind': 'PROCESS', 'operation': 'START', 'sequence': 0, 'result': 'OK', 'subject': 'DESCENDANT', 'errno': 0},
            {'kind': 'CONFIG', 'operation': 'SELECT', 'sequence': 1, 'result': 'UNKNOWN', 'subject': 'FIXTURE', 'errno': 0}]
        self.assertEqual(self.report(value)['projection']['events'], value['events'])

    def test_output_overflow_refuses_without_truncation(self):
        value = supplied()
        value['events'] = [dict(value['events'][0], sequence=x) for x in range(100)]
        with patch.object(M, 'MAX_OUTPUT', 4096):
            output = M.render(raw(value))
        report = json.loads(output)
        self.check_fixed(report)
        self.assertEqual(report['status'], 'INVALID_INPUT')
        self.assertEqual(report['errors'], [{'code': 'OUTPUT_LIMIT', 'category': 'output'}])
        self.assertLessEqual(len(output), 4096)

    def test_render_is_deterministic_and_main_exit_codes_distinguish_states(self):
        for value, code in ((supplied(), 0), ({}, 1), ([], 2)):
            payload = raw(value)
            first = M.render(payload)
            self.assertEqual(first, M.render(payload))
            self.assertTrue(first.endswith(b'\n'))
            out = io.BytesIO()
            self.assertEqual(M.main(io.BytesIO(payload), out), code)
            self.assertEqual(out.getvalue(), first)

    def test_input_bytes_and_fixture_are_not_mutated(self):
        value = supplied()
        before = copy.deepcopy(value)
        payload = raw(value)
        M.project(payload)
        self.assertEqual(value, before)
        self.assertEqual(payload, raw(before))

    def test_purity_no_files_environment_network_or_process_access(self):
        import builtins
        import os
        import socket
        import subprocess
        payload = raw(supplied())
        def forbidden(*args, **kwargs):
            raise AssertionError('unexpected external operation')
        with patch.object(builtins, 'open', forbidden), patch.object(os, 'getenv', forbidden), \
             patch.object(socket, 'socket', forbidden), patch.object(subprocess, 'run', forbidden), \
             patch.object(Path, 'read_bytes', forbidden), patch.object(Path, 'write_bytes', forbidden):
            self.assertEqual(M.project(payload)['status'], 'VALID_SUPPLIED_INPUT')
            self.assertEqual(M.main(io.BytesIO(payload), io.BytesIO()), 0)

    def test_static_purity_boundary_and_no_assert_dependent_validation(self):
        tree = ast.parse(SCRIPT.read_text())
        imported = {node.names[0].name.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.Import)}
        self.assertLessEqual(imported, {'json', 're', 'sys'})
        self.assertFalse(any(isinstance(node, ast.ImportFrom) for node in ast.walk(tree)))
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
        banned = {'eval', 'exec', 'compile', '__import__', 'open', 'getattr', 'setattr'}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, banned)

    def test_historical_source_binding_and_missing_provenance_are_immutable(self):
        report = self.report(supplied())
        self.assertEqual(report['historical_reference']['repository'], 'd6g8k5htny-coder/Math-')
        self.assertEqual(report['historical_reference']['head'], '8177f47bbb66b7cc0dca430941832740a5480dee')
        self.assertEqual(report['historical_reference']['tested_merge'], '81c31f5d61c509256f8d13a4635ca0c85fb8d989')
        self.assertEqual(report['historical_reference']['wrapper_blob'], 'fcf6480529d6b521628e2635e7c1e271ecfa39a4')
        self.assertEqual(report['historical_reference']['run'], 37742226653)
        self.assertEqual(report['historical_reference']['job'], 113195346919)
        self.assertEqual(report['historical_reference']['artifact'], 11534366248)

    def test_bad_input_type_and_io_failure_use_fixed_diagnostics(self):
        for value in (None, 'not bytes', {}, bytearray(b'{}')):
            self.assertEqual(M.project(value)['status'], 'INVALID_INPUT')
        class BrokenReader:
            def read(self, size):
                raise OSError(FIXTURE['canary'])
        out = io.BytesIO()
        self.assertEqual(M.main(BrokenReader(), out), 2)
        self.assertNotIn(FIXTURE['canary'].encode(), out.getvalue())
        self.assertEqual(json.loads(out.getvalue())['errors'], [{'code': 'INPUT_IO', 'category': 'input'}])

    def test_chunked_input_is_acquired_through_explicit_eof(self):
        payload = raw(supplied())
        class Reader:
            def __init__(self):
                self.offset = 0
            def read(self, size):
                part = payload[self.offset:self.offset + min(size, 7)]
                self.offset += len(part)
                return part
        reader, out = Reader(), io.BytesIO()
        self.assertEqual(M.main(reader, out), 0)
        self.assertEqual(reader.offset, len(payload))
        self.assertEqual(out.getvalue(), M.render(payload))

    def test_valid_prefix_does_not_hide_trailing_bytes(self):
        prefix = raw(supplied())
        suffix = (' ' + FIXTURE['canary']).encode()
        class Reader:
            def __init__(self):
                self.chunks = [prefix, suffix, b'']
            def read(self, size):
                return self.chunks.pop(0)
        out = io.BytesIO()
        self.assertEqual(M.main(Reader(), out), 2)
        self.assertEqual(json.loads(out.getvalue())['status'], 'INVALID_INPUT')
        self.assertNotIn(FIXTURE['canary'].encode(), out.getvalue())

    def test_input_limit_counts_all_chunks_before_parsing(self):
        class Reader:
            def __init__(self):
                self.total = 0
            def read(self, size):
                length = min(size, 65536)
                self.total += length
                return b' ' * length
        reader, out = Reader(), io.BytesIO()
        self.assertEqual(M.main(reader, out), 2)
        self.assertEqual(reader.total, 1024 * 1024 + 1)
        self.assertEqual(json.loads(out.getvalue())['errors'],
                         [{'code': 'INPUT_LIMIT', 'category': 'json'}])

    def test_nonbytes_and_nonblocking_read_results_are_refused_without_retry(self):
        for returned in (None, 'text', bytearray(b'{}'), True):
            class Reader:
                calls = 0
                def read(self, size):
                    self.calls += 1
                    return returned
            reader, out = Reader(), io.BytesIO()
            self.assertEqual(M.main(reader, out), 2)
            self.assertEqual(reader.calls, 1)
            self.assertEqual(json.loads(out.getvalue())['errors'],
                             [{'code': 'INPUT_STREAM', 'category': 'input'}])

    def test_partial_writes_complete_exactly_without_truncation(self):
        class Writer:
            def __init__(self):
                self.output = bytearray()
                self.calls = 0
            def write(self, data):
                self.calls += 1
                amount = min(7, len(data))
                self.output.extend(data[:amount])
                return amount
        writer = Writer()
        payload = raw(supplied())
        self.assertEqual(M.main(io.BytesIO(payload), writer), 0)
        self.assertGreater(writer.calls, 1)
        self.assertEqual(bytes(writer.output), M.render(payload))

    def test_nonprogress_and_invalid_write_results_fail_without_retry(self):
        for returned in (None, 0, False, True, -1, 1000000000, '1'):
            class Writer:
                calls = 0
                def write(self, data):
                    self.calls += 1
                    return returned
            writer = Writer()
            self.assertEqual(M.main(io.BytesIO(raw(supplied())), writer), 2)
            self.assertEqual(writer.calls, 1)

    def test_write_error_after_partial_progress_does_not_claim_delivery_or_leak(self):
        class Writer:
            calls = 0
            def write(self, data):
                self.calls += 1
                if self.calls == 1:
                    return 1
                raise OSError(FIXTURE['canary'])
        writer, err = Writer(), io.StringIO()
        with patch('sys.stderr', err):
            self.assertEqual(M.main(io.BytesIO(raw(supplied())), writer), 2)
        self.assertEqual(writer.calls, 2)
        self.assertEqual(err.getvalue(), '')

    def test_read_error_after_partial_input_discards_prefix_and_suppresses_text(self):
        class Reader:
            calls = 0
            def read(self, size):
                self.calls += 1
                if self.calls == 1:
                    return raw(supplied())
                raise OSError(FIXTURE['canary'])
        reader, out, err = Reader(), io.BytesIO(), io.StringIO()
        with patch('sys.stderr', err):
            self.assertEqual(M.main(reader, out), 2)
        self.assertEqual(reader.calls, 2)
        self.assertNotIn(FIXTURE['canary'].encode(), out.getvalue())
        self.assertEqual(err.getvalue(), '')
        self.assertEqual(json.loads(out.getvalue())['errors'],
                         [{'code': 'INPUT_IO', 'category': 'input'}])


if __name__ == '__main__':
    unittest.main()
