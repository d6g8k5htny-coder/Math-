"""Pure supplied-data C183 Q2/Q5 preparation, never environment acquisition."""
import json
import re
import sys

MAX_INPUT = 1024 * 1024
MAX_OUTPUT = 1024 * 1024
MAX_DEPTH = 8
MAX_STRING = 256
MAX_EVENTS = 2048

GROUPS = {
    'environment': {
        'locale': ('enum', ('C', 'C.UTF-8', 'OTHER')),
        'timezone': ('enum', ('UTC', 'OTHER')),
        'selection_sha256': ('digest',),
    },
    'configuration': {
        'gc_auto': ('int', -1, 1000000),
        'maintenance_auto': ('bool',),
        'gc_auto_detach': ('bool',),
        'maintenance_auto_detach': ('bool',),
        'hooks_policy': ('enum', ('DEFAULT', 'DISABLED', 'CUSTOM')),
        'template_policy': ('enum', ('DEFAULT', 'DISABLED', 'CUSTOM')),
        'effective_sha256': ('digest',),
    },
    'binaries': {
        'git_sha256': ('digest',),
        'python_sha256': ('digest',),
        'stdlib_sha256': ('digest',),
    },
    'mount': {
        'filesystem': ('enum', ('ext4', 'xfs', 'overlay', 'tmpfs', 'apfs', 'OTHER')),
        'identity_sha256': ('digest',),
        'read_only': ('bool',),
    },
}
RECORD_SCALARS = {
    'origin': ('enum', ('SYNTHETIC', 'SUPPLIED')),
    'command_shape': ('enum', ('C183_UNITTEST_DISCOVER_V1',)),
    'mode': ('enum', ('normal', 'optimized')),
    'variant': ('enum', ('baseline', 'accept_numeric_required')),
    'observer': ('enum', ('NONE', 'OUTSIDE_SOURCE')),
}
OPERATIONS = {
    'PROCESS': ('START', 'EXIT'),
    'FILESYSTEM': ('CREATE', 'WRITE', 'UNLINK', 'RMDIR'),
    'CONFIG': ('SELECT',),
}


class _Refusal(Exception):
    """Only fixed codes/categories may cross the public error boundary."""
    def __init__(self, code, category):
        super().__init__(code)
        self.code = code
        self.category = category


def _refuse(code, category):
    raise _Refusal(code, category)


def _base():
    # A new object each time: callers cannot mutate future historical defaults.
    return {
        'status': 'INVALID_INPUT',
        'errors': [],
        'missing': [],
        'projection': None,
        'comparison': {'status': 'NOT_EVALUATED', 'differences': []},
        'event_model_status': 'NOT_EVALUATED',
        'historical_reference': {
            'repository': 'd6g8k5htny-coder/Math-',
            'head': '8177f47bbb66b7cc0dca430941832740a5480dee',
            'tested_merge': '81c31f5d61c509256f8d13a4635ca0c85fb8d989',
            'wrapper_blob': 'fcf6480529d6b521628e2635e7c1e271ecfa39a4',
            'run': 37742226653,
            'job': 113195346919,
            'artifact': 11534366248,
        },
        'historical_missing_provenance': [
            'effective_configuration', 'effective_environment', 'binary_library_identities',
            'mount_identity', 'writer_start_identity', 'residual_entries',
        ],
        'historical_environment_equivalence': 'NOT_ESTABLISHED',
        'actual_environment_match': 'NOT_ESTABLISHED',
        'collector_qualification': 'NOT_RUN',
        'live_payload_suppression': 'NOT_RUN',
        'experiment_execution': 'NOT_RUN',
        'planned_experiment_cases': 40,
        'cause': 'UNKNOWN',
        'promotion_permission': False,
        'pr397_disposition': 'HOLD / NOT_READY / NO_MERGE',
        'scientific_effect': 'NONE',
        'writer_inference': 'NOT_EVALUATED',
    }


def _invalid(code, category):
    result = _base()
    result['errors'] = [{'code': code, 'category': category}]
    return result


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            _refuse('DUPLICATE_KEY', 'json')
        result[key] = value
    return result


def _no_float(value):
    _refuse('NUMBER_TYPE', 'json')


def _integer(value):
    # Bound digit conversion independently of Python's configurable digit cap.
    if len(value) > 20:
        _refuse('NUMBER_LIMIT', 'json')
    return int(value)


def _parse(raw):
    if type(raw) is not bytes:
        _refuse('INPUT_TYPE', 'input')
    if len(raw) > MAX_INPUT:
        _refuse('INPUT_LIMIT', 'json')
    text = raw.decode('utf-8')
    depth, quoted, escaped = 0, False, False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '[{':
            depth += 1
            if depth > MAX_DEPTH:
                _refuse('DEPTH_LIMIT', 'json')
        elif char in ']}':
            depth -= 1
            if depth < 0:
                _refuse('JSON_SYNTAX', 'json')
    data = json.loads(text, object_pairs_hook=_pairs, parse_constant=_no_float,
                      parse_float=_no_float, parse_int=_integer)
    # Traversal is bounded by the byte and predecode nesting caps. This also
    # checks unknown-key payloads without ever including them in diagnostics.
    pending = [data]
    while pending:
        value = pending.pop()
        if type(value) is str:
            if len(value.encode('utf-8')) > MAX_STRING:
                _refuse('STRING_LIMIT', 'json')
        elif type(value) is dict:
            pending.extend(value.keys())
            pending.extend(value.values())
        elif type(value) is list:
            pending.extend(value)
    return data


def _object(value, allowed, category):
    if type(value) is not dict:
        _refuse('OBJECT_TYPE', category)
    if set(value) - set(allowed):
        _refuse('UNKNOWN_FIELD', category)
    return value


def _scalar(value, schema, category):
    kind = schema[0]
    valid = False
    if kind == 'enum':
        valid = type(value) is str and value in schema[1]
    elif kind == 'bool':
        valid = type(value) is bool
    elif kind == 'int':
        valid = type(value) is int and schema[1] <= value <= schema[2]
    elif kind == 'digest':
        valid = type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None
    if not valid:
        _refuse('VALUE_SCHEMA', category)
    return value


def _tagged(value, schema, category, missing, mandatory=True):
    value = _object(value, ('state', 'value'), category)
    if value.get('state') == 'UNKNOWN' and set(value) == {'state'}:
        if mandatory:
            missing.add(category)
        return {'state': 'UNKNOWN'}
    if value.get('state') == 'REPORTED' and set(value) == {'state', 'value'}:
        return {'state': 'REPORTED', 'value': _scalar(value['value'], schema, category)}
    _refuse('TAG_SCHEMA', category)


def _record(value, cell, missing):
    keys = set(RECORD_SCALARS) | set(GROUPS) | {'sources', 'observed_at_unix_s'}
    value = _object(value, keys, 'record')
    result = {}
    for key in sorted(keys - set(value)):
        missing.add(cell + '.' + key)
    for key, schema in RECORD_SCALARS.items():
        if key in value:
            result[key] = _scalar(value[key], schema, 'record.' + key)
    expected_observer = 'NONE' if cell == 'U' else 'OUTSIDE_SOURCE'
    if 'observer' in result and result['observer'] != expected_observer:
        _refuse('OBSERVER_ASSIGNMENT', 'record.observer')
    if 'observed_at_unix_s' in value:
        result['observed_at_unix_s'] = _tagged(
            value['observed_at_unix_s'], ('int', 0, 253402300799),
            cell + '.observed_at_unix_s', missing)
    for group, fields in GROUPS.items():
        if group not in value:
            continue
        data = _object(value[group], fields, group)
        result[group] = {}
        for key, schema in fields.items():
            category = cell + '.' + group + '.' + key
            if key not in data:
                missing.add(category)
            else:
                result[group][key] = _tagged(data[key], schema, category, missing)
    if 'sources' in value:
        fields = ('pristine', 'numeric_mutant', 'observer')
        data = _object(value['sources'], fields, 'sources')
        result['sources'] = {}
        for key in fields:
            category = cell + '.sources.' + key
            if key not in data:
                missing.add(category)
                continue
            required = key == 'pristine' or (key == 'numeric_mutant' and
                        result.get('variant') == 'accept_numeric_required') or (
                        key == 'observer' and cell == 'I')
            tagged = _tagged(data[key], ('digest',), category, missing, required)
            forbidden_report = (key == 'observer' and cell == 'U') or (
                key == 'numeric_mutant' and result.get('variant') == 'baseline')
            if forbidden_report and tagged['state'] != 'UNKNOWN':
                _refuse('SOURCE_ROLE', 'sources')
            result['sources'][key] = tagged
    return result


def _events(value):
    if type(value) is not list:
        _refuse('ARRAY_TYPE', 'events')
    if len(value) > MAX_EVENTS:
        _refuse('EVENT_LIMIT', 'events')
    result, previous = [], -1
    fields = {
        'kind': ('enum', tuple(OPERATIONS)),
        'sequence': ('int', 0, 1000000000),
        'result': ('enum', ('OK', 'ERROR', 'UNKNOWN')),
        'subject': ('enum', ('FIXTURE', 'DESCENDANT', 'OUTSIDE')),
        'errno': ('int', 0, 4095),
    }
    for item in value:
        item = _object(item, set(fields) | {'operation'}, 'events')
        if set(item) != set(fields) | {'operation'}:
            _refuse('EVENT_FIELD_MISSING', 'events')
        projected = {key: _scalar(item[key], schema, 'events.' + key)
                     for key, schema in fields.items()}
        projected['operation'] = _scalar(
            item['operation'], ('enum', OPERATIONS[projected['kind']]), 'events.operation')
        if projected['sequence'] <= previous:
            _refuse('EVENT_ORDER', 'events.sequence')
        previous = projected['sequence']
        if projected['result'] != 'ERROR' and projected['errno'] != 0:
            _refuse('EVENT_RESULT', 'events.errno')
        result.append(projected)
    return result


def _comparison(records, missing):
    # Compare only schema-selected values, never raw dumps or collector claims.
    selected = {}
    for cell in ('U', 'I'):
        record = records.get(cell, {})
        fields = {key: record[key] for key in ('command_shape', 'mode', 'variant')
                  if key in record}
        for group in (*GROUPS, 'sources'):
            for key, tagged in record.get(group, {}).items():
                if group == 'sources' and key == 'observer':
                    continue
                if tagged['state'] == 'REPORTED':
                    fields[group + '.' + key] = tagged['value']
        selected[cell] = fields
    differences = sorted(key for key in selected['U'].keys() & selected['I'].keys()
                         if selected['U'][key] != selected['I'][key])
    if any(field == 'records' or field in ('U', 'I') or
           field.startswith(('U.', 'I.')) for field in missing):
        status = 'INCOMPLETE_SUPPLIED_COMPARISON'
    else:
        status = 'DIFFERENT_SUPPLIED_FIELDS' if differences else 'MATCHED_SUPPLIED_FIELDS'
    return {'status': status, 'differences': differences}


def project(raw):
    """Return only bounded structural findings about explicitly supplied bytes."""
    try:
        data = _object(_parse(raw), ('schema_version', 'records', 'events'), 'input')
        missing = set()
        projection = {}
        for key in ('schema_version', 'records', 'events'):
            if key not in data:
                missing.add(key)
        if 'schema_version' in data:
            projection['schema_version'] = _scalar(data['schema_version'], ('int', 1, 1), 'schema')
        records = {}
        if 'records' in data:
            supplied_records = _object(data['records'], ('U', 'I'), 'records')
            for cell in ('U', 'I'):
                if cell not in supplied_records:
                    missing.add(cell)
                else:
                    records[cell] = _record(supplied_records[cell], cell, missing)
            projection['records'] = records
        if 'events' in data:
            projection['events'] = _events(data['events'])
        result = _base()
        result.update(status='INCOMPLETE_INPUT' if missing else 'VALID_SUPPLIED_INPUT',
                      missing=sorted(missing), projection=projection,
                      comparison=_comparison(records, missing))
        if 'events' not in projection:
            result['event_model_status'] = 'NOT_SUPPLIED'
        else:
            result['event_model_status'] = ('SUPPLIED_MODEL_ONLY' if projection['events']
                                            else 'EMPTY_SUPPLIED_MODEL')
        return result
    except _Refusal as error:
        return _invalid(error.code, error.category)
    except UnicodeError:
        return _invalid('INVALID_UNICODE', 'json')
    except (ValueError, RecursionError):
        # Never expose JSON's input excerpt or exception text.
        return _invalid('JSON_SYNTAX', 'json')


def _serialize(report):
    return (json.dumps(report, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                       allow_nan=False) + '\n').encode('ascii')


def render(raw):
    """Canonical JSON; overflow becomes an explicit refusal, never truncation."""
    output = _serialize(project(raw))
    if len(output) > MAX_OUTPUT:
        return _serialize(_invalid('OUTPUT_LIMIT', 'output'))
    return output


def main(binary_input, binary_output):
    """Read at most the fixed byte cap plus one from the supplied stream."""
    try:
        raw = binary_input.read(MAX_INPUT + 1)
    except (OSError, ValueError):
        output = _serialize(_invalid('INPUT_IO', 'input'))
    else:
        output = render(raw)
    try:
        binary_output.write(output)
    except (OSError, ValueError):
        return 2
    status = json.loads(output)['status']
    return {'VALID_SUPPLIED_INPUT': 0, 'INCOMPLETE_INPUT': 1, 'INVALID_INPUT': 2}[status]


if __name__ == '__main__':
    if len(sys.argv) != 1:
        sys.stdout.buffer.write(_serialize(_invalid('ARGUMENTS_REFUSED', 'input')))
        sys.exit(2)
    sys.exit(main(sys.stdin.buffer, sys.stdout.buffer))
