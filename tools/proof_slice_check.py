#!/usr/bin/env python3
"""Bounded proof-slice v5 custody/conformance checks; no scientific verdicts.

The in-memory APIs require independently acquired raw source/capture buffers.
The CLI supplies them only from explicit Git commits in the mapped Math clone.
"""
import argparse
import copy
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

_spec = importlib.util.spec_from_file_location('_proof_slice_retrofit', Path(__file__).with_name('retrofit_record_check.py'))
_retrofit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_retrofit)
load_strict = _retrofit.load_strict

REPOSITORY = 'd6g8k5htny-coder/Math-'
SOURCE_COMMIT = '9fd261135b41daf1e377f9ef2db193fee6ec36be'
INVENTORY_SCHEMA = 'proof-unit-inventory/v0-provisional-5'
SLICE_SCHEMA = 'proof-slice/v0-provisional-5'
KINDS = ('premise', 'context', 'reading_correction', 'scope_guard', 'check')
REASONS = ('INPUT_UNAVAILABLE', 'IDENTITY_MISMATCH', 'CONTRACT_SHAPE',
           'UNSUPPORTED_INFERENCE', 'EXPECTED_INVENTORY_MISMATCH', 'SOURCE_JOIN_MISMATCH')
FILE_KEYS = ('repository', 'commit', 'path', 'git_blob', 'sha256', 'bytes')
CORE_KEYS = ('consumer_statement_id', 'consumer_statement_source', 'consumer_semantics',
             'consumer_unit_id', 'consumer_source', 'suppliers', 'claimed_interface',
             'parameter_mapping', 'context', 'source_reading')


class ContractError(ValueError):
    def __init__(self, reason, failed_input, message):
        super().__init__(message)
        self.reason, self.failed_input = reason, failed_input


def fail(reason, where, message):
    raise ContractError(reason, where, message)


def require(condition, where, message, reason='CONTRACT_SHAPE'):
    if not condition:
        fail(reason, where, message)


def file_key(identity):
    return tuple(identity[k] for k in FILE_KEYS)


def typed_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(typed_equal(left[k],right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(typed_equal(a,b) for a,b in zip(left,right))
    # The closed contract has no floating-point fields, including NaN/Infinity.
    return type(left) in (str,int,bool,type(None)) and left == right


def parse_input(raw, where):
    try:
        require(type(raw) is bytes, where, 'Original UTF-8 input bytes required')
        return load_strict(raw.decode('utf-8'))
    except (UnicodeError, ValueError, RecursionError) as exc:
        if isinstance(exc, ContractError):
            raise
        fail('CONTRACT_SHAPE', where, 'Strict UTF-8/JSON parsing failed: ' + str(exc))


def arr(kind, minimum=0):
    return ('array', kind, minimum)


def nullable(kind):
    return ('nullable', kind)


def enum(*values):
    return ('enum', values)


def literal(value):
    return ('literal', value)


SHAPES = {
    'File': dict(repository='repository', commit='sha1', path='path', git_blob='sha1', sha256='sha256', bytes='integer'),
    'SourceFile': dict(id='id', identity='File'),
    'Selection': dict(source_id='id', lines=nullable('lines'), locator='text', precision=enum('exact_lines', 'named_locator_unexpanded')),
    'XSelection': dict(file='File', lines=nullable('lines'), locator='text', precision=enum('exact_lines', 'named_locator_unexpanded')),
    'Performer': dict(provider=nullable('string'), agent=nullable('string'), session=nullable('string'), exposure='text'),
    'Comment': dict(kind=literal('github_comment_snapshot'), repository='repository', issue='positive', comment_id='decimal', url='text', updated_at='date', body_bytes='integer', body_sha256='sha256'),
    'Review': dict(kind=literal('github_review_snapshot'), repository='repository', pull_request='positive', review_id='decimal', native_commit='sha1', url='text', submitted_at='date', body_bytes='integer', body_sha256='sha256'),
    'GitRecord': dict(kind=literal('git_file'), file='File'),
    'Record': dict(id='id', identity='RecordIdentity', performer='Performer', role=enum('inventory','omission_read','author_response','applicability_review','design','withdrawal'), scope='text'),
    'RecordSelection': dict(record_id='id', locator='text'),
    'XRecordSelection': dict(record='RecordIdentity', locator='text'),
    'Text': dict(text='text', source_refs=arr('Selection'), record_refs=arr('RecordSelection'), unknown_refs=arr('id')),
    'XText': dict(text='text', source_refs=arr('XSelection'), record_refs=arr('XRecordSelection'), unknowns=arr('XUnknown')),
    'Unknown': dict(id='id', description='Text', affects_use_ids=arr('id'), provenance=arr('RecordSelection')),
    'XUnknown': dict(id='id', description='XText', affects_use_ids=arr('id'), provenance=arr('XRecordSelection')),
    'Semantics': dict(model='Text', observables=arr('Text'), normalization='Text', parameters='Text', limit_order='Text', conclusion='Text', exclusions=arr('Text')),
    'XSemantics': dict(model='XText', observables=arr('XText'), normalization='XText', parameters='XText', limit_order='XText', conclusion='XText', exclusions=arr('XText')),
    'Boundary': dict(id='id', source_id='id', consumed_lines=arr('lines'), excluded_lines=arr('lines'), reason='Text'),
    'XBoundary': dict(id='id', file='File', consumed_lines=arr('lines'), excluded_lines=arr('lines'), reason='XText'),
    'Root': dict(statement_id='id', source_statement='Selection', entry_unit_ids=arr('id',1), graph_node=nullable('string'), museum_card=nullable('string'), semantics='Semantics', reading_boundaries=arr('Boundary')),
    'Conclusion': dict(unit_id='id', source='XSelection'),
    'ExpectedUnit': dict(id='id', section='integer', lines='lines', locator='text'),
    'ExpectedUse': dict(id='id', consumer_unit_id='id', kind=enum(*KINDS)),
    'ExpectedGroup': dict(owner_unit_id='id', group_id='id', combination=literal('ALL'), conclusion='Conclusion', premise_use_ids=arr('id',1)),
    'Bundle': dict(id='id', combination=literal('ALL'), conclusion='Conclusion', group_ids=arr('id',2), basis='Text'),
    'Extraction': dict(rule=literal('maximal-contiguous-nonempty-nonheading-blocks'), heading_boundaries=literal([310,482]), payload_lines=literal([312,480]), line_convention=literal('one-based-inclusive-original-LF')),
    'Expected': dict(schema=literal(INVENTORY_SCHEMA), root_statement_id='id', root_boundary='Root', source='File', sources=arr('SourceFile',1), records=arr('Record'), unknowns=arr('Unknown'), extraction='Extraction', expected_units=arr('ExpectedUnit',1), expected_uses=arr('ExpectedUse'), provenance=arr('RecordSelection'), expected_groups=arr('ExpectedGroup'), consumer_span_rule=enum('whole_unit','same_file_contained_exact'), read_at='date', inventory_record='RecordSelection', omission_read_record='RecordSelection', expected_bundles=arr('Bundle')),
    'Group': dict(id='id', combination=literal('ALL'), conclusion='id', premise_use_ids=arr('id',1), basis=arr('RecordSelection')),
    'Use': dict(id='id', kind=enum(*KINDS), binding='Binding', provenance=arr('RecordSelection'), applicability_reviews=arr('ReviewBinding'), unknown_refs=arr('id')),
    'Binding': dict(consumer_statement_id='id', consumer_unit_id='id', consumer_source='Selection', supplier_ids=arr('id'), claimed_interface='Text', parameter_mapping='Text', context='Text', source_reading=arr('ReadingUse')),
    'ReadingUse': dict(boundary_id='id', supplier_ids=arr('id'), applies_to=arr('Selection'), explanation='Text'),
    'XReadingUse': dict(boundary='XBoundary', suppliers=arr('XSupplier'), applies_to=arr('XSelection'), explanation='XText'),
    'External': dict(title='string', authors=arr('string'), edition_or_version=nullable('string'), theorem_or_section=nullable('string'), url=nullable('string'), retained_record=nullable('RecordSelection')),
    'XExternal': dict(title='string', authors=arr('string'), edition_or_version=nullable('string'), theorem_or_section=nullable('string'), url=nullable('string'), retained_record=nullable('XRecordSelection')),
    'Supplier': dict(id='id', kind=enum('inventory_unit','source_section','import','external','unnamed'), unit_ids=arr('id'), source_refs=arr('Selection'), external_ref=nullable('External'), interface='Text', expansion=enum('in_slice','unexpanded'), unknown_refs=arr('id')),
    'XSupplier': dict(id='id', kind=enum('inventory_unit','source_section','import','external','unnamed'), unit_ids=arr('id'), source_refs=arr('XSelection'), external_ref=nullable('XExternal'), interface='XText', expansion=enum('in_slice','unexpanded'), unknowns=arr('XUnknown')),
    'Unit': dict(id='id', source='Selection', section='integer', description='Text', uses=arr('Use'), premise_groups=arr('Group'), related_unit_ids=arr('id')),
    'InventoryBinding': dict(expected_inventory='File', extraction_record='RecordSelection', correction_records=arr('RecordSelection')),
    'History': dict(id='id', kind=enum('inventory_statement','omission_observation','author_inventory_amendment','applicability_observation','supersession_note'), record='RecordSelection', affects_unit_ids=arr('id'), affects_use_ids=arr('id'), text='string'),
    'Core': dict(consumer_statement_id='id', consumer_statement_source='XSelection', consumer_semantics='XSemantics', consumer_unit_id='id', consumer_source='XSelection', suppliers=arr('XSupplier'), claimed_interface='XText', parameter_mapping='XText', context='XText', source_reading=arr('XReadingUse')),
    'Member': dict(use_id='id', use_kind=literal('premise'), core='Core'),
    'Inference': dict(group_id='id', combination=literal('ALL'), conclusion='Conclusion', premises=arr('Member',1)),
    'Contribution': dict(group_id='id', owner_unit_id='id', combination=literal('ALL'), conclusion='Conclusion', members=arr('Member',1)),
    'CompleteBundle': dict(bundle_id='id', combination=literal('ALL'), conclusion='Conclusion', basis='XText', groups=arr('Contribution',2)),
    'ReviewBinding': dict(record='RecordSelection', reviewed_use='Snapshot', scope='Text', disposition_as_recorded='string', limitations=arr('Text'), later_disposition_records=arr('RecordSelection')),
    'Slice': dict(schema=literal(SLICE_SCHEMA), artifact_kind=literal('source_companion'), id='id', read_at='date', author='Performer', scientific_effect=literal('NONE'), status_authority=literal(False), independence_credit=literal(0), root='Root', sources=arr('SourceFile',1), records=arr('Record'), inventory_binding='InventoryBinding', units=arr('Unit',1), suppliers=arr('Supplier'), unknowns=arr('Unknown'), history=arr('History'), bundles=arr('Bundle')),
}
SHAPES['Snapshot'] = {**SHAPES['Core'], 'use_id':'id', 'use_kind':enum(*KINDS),
                      'inference_context':nullable('Inference'), 'bundle_context':nullable('CompleteBundle')}


def shape(value, kind, where):
    if isinstance(kind, tuple):
        if kind[0] == 'nullable':
            if value is not None:
                shape(value, kind[1], where)
        elif kind[0] == 'array':
            require(type(value) is list and len(value) >= kind[2], where, 'Expected array with required cardinality')
            for i, item in enumerate(value):
                shape(item, kind[1], where + '/' + str(i))
            if kind[1] == 'id':
                require(len(value) == len(set(value)), where, 'Duplicate reference ID')
            if type(kind[1]) is str:
                unique_key = {'XSupplier':'id','XUnknown':'id','Member':'use_id','Contribution':'group_id'}.get(kind[1])
                if unique_key:
                    require(len(value) == len({v[unique_key] for v in value}), where, 'Duplicate expanded object ID')
        elif kind[0] == 'literal':
            require(typed_equal(value, kind[1]), where, 'Incorrect literal')
        elif kind[0] == 'enum':
            require(type(value) is str and value in kind[1], where, 'Unsupported typed value')
        return
    if kind == 'RecordIdentity':
        require(type(value) is dict, where, 'Record identity must be an object')
        require(type(value.get('kind')) is str, where, 'Record identity tag must be a string')
        selected = {'github_comment_snapshot':'Comment','github_review_snapshot':'Review','git_file':'GitRecord'}.get(value.get('kind'))
        require(selected is not None, where, 'Unknown record identity kind')
        shape(value, selected, where)
        return
    if kind in SHAPES:
        fields = SHAPES[kind]
        require(type(value) is dict and set(value) == set(fields), where, 'Closed ' + kind + ' shape required')
        for key, field_kind in fields.items():
            shape(value[key], field_kind, where + '/' + key)
        if kind in ('Selection', 'XSelection'):
            require((value['precision'] == 'exact_lines') == (value['lines'] is not None), where, 'Selection precision/lines disagree')
        elif kind in ('Text', 'XText'):
            require(value['source_refs'] or value['record_refs'] or value['unknown_refs' if kind == 'Text' else 'unknowns'], where, 'Sourced text requires a basis')
        elif kind in ('Unknown', 'XUnknown'):
            require(value['description']['source_refs'] or value['description']['record_refs'], where, 'Unknown description needs source/record basis')
        elif kind == 'Bundle':
            require(value['basis']['record_refs'], where, 'Bundle requires attributed record selection')
        elif kind == 'Conclusion':
            require(value['source']['precision'] == 'exact_lines', where, 'Conclusion requires exact source lines')
        elif kind in ('Comment','Review'):
            repo = re.escape(value['repository'])
            if kind == 'Comment':
                pattern = rf'https://github\.com/{repo}/(?:issues|pull)/{value["issue"]}#issuecomment-{value["comment_id"]}'
            else:
                pattern = rf'https://github\.com/{repo}/pull/{value["pull_request"]}#pullrequestreview-{value["review_id"]}'
            require(re.fullmatch(pattern, value['url']) is not None, where, 'Native URL contradicts identity')
        return
    if kind in ('text','id','string','repository','path','sha1','sha256','decimal','date'):
        require(type(value) is str, where, 'Expected string')
        try:
            value.encode('utf-8')
        except UnicodeError:
            fail('CONTRACT_SHAPE',where,'String contains an unpaired Unicode surrogate')
        if kind in ('text','id'):
            require(bool(value.strip()), where, 'Empty text/ID')
        elif kind == 'repository':
            require(re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', value) is not None, where, 'Invalid repository identity')
        elif kind == 'path':
            require(bool(value) and '\\' not in value and not value.startswith('/') and all(p not in ('','.','..') for p in value.split('/')) and '\x00' not in value, where, 'Unsafe repository-relative file path')
        elif kind in ('sha1','sha256'):
            require(re.fullmatch('[0-9a-f]{' + ('40' if kind == 'sha1' else '64') + '}', value) is not None, where, 'Full lowercase digest required')
        elif kind == 'decimal':
            require(re.fullmatch(r'[1-9][0-9]*', value) is not None, where, 'Positive native decimal ID required')
        elif kind == 'date':
            require(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', value) is not None, where, 'RFC3339 UTC timestamp required')
            try:
                datetime.datetime.fromisoformat(value)
            except ValueError:
                fail('CONTRACT_SHAPE', where, 'Invalid calendar timestamp')
    elif kind in ('integer','positive'):
        require(type(value) is int and value >= (1 if kind == 'positive' else 0), where, 'Integer required; booleans are not integers')
    elif kind == 'lines':
        require(type(value) is list and len(value) == 2, where, 'Inclusive line pair required')
        for n in value:
            shape(n, 'positive', where)
        require(value[0] <= value[1], where, 'Reversed source range')
    else:
        raise RuntimeError('Unknown internal shape ' + str(kind))


def walk(value):
    if type(value) is dict:
        yield value
        for child in value.values():
            yield from walk(child)
    elif type(value) is list:
        for child in value:
            yield from walk(child)


def unsupported(doc, expected, where):
    if type(doc) is not dict:
        return
    groups = []
    if expected and type(doc.get('expected_groups')) is list:
        groups = [(g.get('owner_unit_id'),g.get('group_id'),g) for g in doc['expected_groups'] if type(g) is dict]
    elif not expected and type(doc.get('units')) is list:
        for u in doc['units']:
            if type(u) is dict and type(u.get('premise_groups')) is list:
                groups.extend((u.get('id'),g.get('id'),g) for g in u['premise_groups'] if type(g) is dict)
    owners = {}
    for owner, gid, g in groups:
        if type(g.get('combination')) is str and g['combination'] in ('ANY','OR'):
            fail('UNSUPPORTED_INFERENCE', where, 'Only recorded ALL contributions are supported')
        if type(owner) is str and type(gid) is str:
            owners.setdefault(owner,set()).add(gid)
    require(all(len(ids) <= 1 for ids in owners.values()), where, 'A second current group under one owner is unsupported', 'UNSUPPORTED_INFERENCE')
    bs = doc.get('expected_bundles' if expected else 'bundles')
    if type(bs) is list:
        for b in bs:
            if type(b) is dict and type(b.get('combination')) is str and b['combination'] in ('ANY','OR'):
                fail('UNSUPPORTED_INFERENCE', where, 'Alternative bundle mode is unsupported')


def indexed(items, key, where):
    result = {}
    for item in items:
        require(item[key] not in result, where, 'Duplicate ' + key)
        result[item[key]] = item
    return result


def context(doc, expected, where):
    root = doc['root_boundary' if expected else 'root']
    units = indexed(doc['expected_units' if expected else 'units'], 'id', where)
    uses = indexed(doc['expected_uses'] if expected else [u for unit in units.values() for u in unit['uses']], 'id', where)
    groups = []
    if expected:
        groups = copy.deepcopy(doc['expected_groups'])
    else:
        for unit in units.values():
            for g in unit['premise_groups']:
                groups.append({**g, 'group_id':g['id'], 'owner_unit_id':unit['id']})
    return dict(doc=doc, expected=expected, where=where, root=root, units=units, uses=uses,
                groups=indexed(groups,'group_id',where), bundles=indexed(doc['expected_bundles' if expected else 'bundles'],'id',where),
                sources=indexed(doc['sources'],'id',where), records=indexed(doc['records'],'id',where),
                unknowns=indexed(doc['unknowns'],'id',where), boundaries=indexed(root['reading_boundaries'],'id',where),
                history={} if expected else indexed(doc['history'],'id',where),
                suppliers={} if expected else indexed(doc['suppliers'],'id',where))


def get(table, key, where):
    require(key in table, where, 'Unresolved reference: ' + key)
    return table[key]


def resolved_selection(selection, ctx):
    return {'file':get(ctx['sources'],selection['source_id'],ctx['where'])['identity'],
            **{k:v for k,v in selection.items() if k != 'source_id'}}


def expand(value, ctx, trail=()):
    if type(value) is list:
        return [expand(v,ctx,trail) for v in value]
    if type(value) is not dict:
        return value
    out = {}
    for key, v in value.items():
        if key == 'source_id':
            out['file'] = copy.deepcopy(get(ctx['sources'],v,ctx['where'])['identity'])
        elif key == 'record_id':
            out['record'] = copy.deepcopy(get(ctx['records'],v,ctx['where'])['identity'])
        elif key == 'supplier_ids':
            out['suppliers'] = [expand(get(ctx['suppliers'],i,ctx['where']),ctx,trail) for i in v]
        elif key == 'boundary_id':
            out['boundary'] = expand(get(ctx['boundaries'],v,ctx['where']),ctx,trail)
        elif key == 'unknown_refs':
            out['unknowns'] = []
            for uid in v:
                require(uid not in trail,ctx['where'],'Unknown-reference cycle')
                out['unknowns'].append(expand(get(ctx['unknowns'],uid,ctx['where']),ctx,(*trail,uid)))
        else:
            out[key] = expand(v,ctx,trail)
    return out


def expected_selection(unit, expected):
    return {'file':expected['source'],'lines':unit['lines'],'locator':unit['locator'],'precision':'exact_lines'}


def source_lines(raw, where):
    require(type(raw) is bytes,where,'Raw source bytes required','INPUT_UNAVAILABLE')
    try:
        raw.decode('utf-8')
    except UnicodeError:
        fail('CONTRACT_SHAPE',where,'Source is not UTF-8')
    require(b'\r' not in raw,where,'CR sources need a separately specified extraction version')
    parts = raw.split(b'\n')
    if parts[-1] == b'':
        parts.pop()
    return parts


def auth_file(identity, source_bytes, where):
    key = file_key(identity)
    require(key in source_bytes,where,'Required source buffer unavailable','INPUT_UNAVAILABLE')
    raw = source_bytes[key]
    require(type(raw) is bytes,where,'Source input must be original bytes','INPUT_UNAVAILABLE')
    actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(len(raw) == identity['bytes'] and hashlib.sha256(raw).hexdigest() == identity['sha256'] and actual == identity['git_blob'],where,'Source bytes contradict declared identity','IDENTITY_MISMATCH')
    source_lines(raw,where)
    return raw


def record_key(identity):
    if identity['kind'] == 'git_file':
        return 'git:' + json.dumps(identity['file'],sort_keys=True)
    return ':'.join([identity['kind'],identity['repository'],identity.get('comment_id',identity.get('review_id')),identity['body_sha256']])


def auth_record(identity, snapshots, source_bytes, where, rid=None):
    if identity['kind'] == 'git_file':
        auth_file(identity['file'],source_bytes,where)
        return
    snapshot = snapshots.get(record_key(identity), snapshots.get(rid))
    if snapshot is None:
        for candidate in snapshots.values():
            if type(candidate) is dict and str(candidate.get('id')) == identity.get('comment_id',identity.get('review_id')):
                snapshot = candidate
                break
    require(type(snapshot) is dict,where,'Retained native record is unavailable','INPUT_UNAVAILABLE')
    comment = identity['kind'] == 'github_comment_snapshot'
    native_id = identity['comment_id' if comment else 'review_id']
    date_key = 'updated_at' if comment else 'submitted_at'
    container_key = 'issue_url' if comment else 'pull_request_url'
    container = f'https://api.github.com/repos/{identity["repository"]}/' + ('issues/' + str(identity['issue']) if comment else 'pulls/' + str(identity['pull_request']))
    require(type(snapshot.get('id')) is int and str(snapshot['id']) == native_id and snapshot.get('html_url') == identity['url'] and snapshot.get(date_key) == identity[date_key] and snapshot.get(container_key) == container,where,'Retained native metadata mismatch','IDENTITY_MISMATCH')
    if not comment:
        require(snapshot.get('commit_id') == identity['native_commit'],where,'Native review commit mismatch','IDENTITY_MISMATCH')
    require(type(snapshot.get('body')) is str,where,'Native body is not retained text','IDENTITY_MISMATCH')
    try:
        body = snapshot['body'].encode('utf-8')
    except UnicodeError:
        fail('IDENTITY_MISMATCH',where,'Retained native body is not valid UTF-8 text')
    require(len(body) == identity['body_bytes'] and hashlib.sha256(body).hexdigest() == identity['body_sha256'],where,'Retained body digest mismatch','IDENTITY_MISMATCH')


def authenticate(ctx, source_bytes, snapshots):
    where = ctx['where']
    # The outer inventory artifact is authenticated by the caller and compared
    # separately. It is not an imported proof-source buffer.
    content = {k:v for k,v in ctx['doc'].items() if k != 'inventory_binding'}
    for value in walk(content):
        if set(value) == set(FILE_KEYS):
            auth_file(value,source_bytes,where)
        elif value.get('kind') in ('github_comment_snapshot','github_review_snapshot','git_file'):
            rid = next((r['id'] for r in ctx['records'].values() if typed_equal(r['identity'],value)),None)
            auth_record(value,snapshots,source_bytes,where,rid)
    for source in ctx['sources'].values():
        auth_file(source['identity'],source_bytes,where)
    for value in walk(ctx['doc']):
        if set(value) in (set(SHAPES['Selection']),set(SHAPES['XSelection'])):
            selection = resolved_selection(value,ctx) if 'source_id' in value else value
            if selection['lines'] is not None:
                raw = auth_file(selection['file'],source_bytes,where)
                require(selection['lines'][1] <= len(source_lines(raw,where)),where,'Source range exceeds authenticated original LF lines','SOURCE_JOIN_MISMATCH')


def joins(ctx, expected, source_bytes):
    where = ctx['where']
    expunits = {u['id']:u for u in expected['expected_units']}
    expuses = {u['id']:u for u in expected['expected_uses']}
    if ctx['expected']:
        require('P' in ctx['sources'] and typed_equal(ctx['sources']['P']['identity'],expected['source']),where,'Inventory P source contradicts source tuple','SOURCE_JOIN_MISMATCH')
        raw = source_bytes[file_key(expected['source'])]
        count = len(source_lines(raw,where))
        for u in ctx['units'].values():
            require(u['lines'][1] <= count and expected['extraction']['payload_lines'][0] <= u['lines'][0] <= u['lines'][1] <= expected['extraction']['payload_lines'][1],where,'Expected unit is outside fixed payload/source','SOURCE_JOIN_MISMATCH')
    else:
        for unit in ctx['units'].values():
            if unit['id'] in expunits:
                require(unit['section'] == expunits[unit['id']]['section'] and typed_equal(resolved_selection(unit['source'],ctx),expected_selection(expunits[unit['id']],expected)),where,'Unit contradicts independently fixed source/locator','SOURCE_JOIN_MISMATCH')
            for use in unit['uses']:
                binding = use['binding']
                require(binding['consumer_unit_id'] == unit['id'] and (use['id'] not in expuses or expuses[use['id']]['consumer_unit_id'] == unit['id']) and binding['consumer_statement_id'] == expected['root_statement_id'],where,'Use contradicts its actual expected owner/statement','SOURCE_JOIN_MISMATCH')
                selected = resolved_selection(binding['consumer_source'],ctx)
                owner = resolved_selection(unit['source'],ctx)
                require(selected['precision'] == 'exact_lines' and owner['precision'] == 'exact_lines' and typed_equal(selected['file'],owner['file']),where,'Consumer source is not its owner file','SOURCE_JOIN_MISMATCH')
                if expected['consumer_span_rule'] == 'whole_unit':
                    okay = typed_equal(selected,owner)
                else:
                    okay = owner['lines'][0] <= selected['lines'][0] <= selected['lines'][1] <= owner['lines'][1]
                require(okay,where,'Consumer selection is outside recorded owner/rule','SOURCE_JOIN_MISMATCH')
    for group in ctx['groups'].values():
        get(ctx['units'],group['owner_unit_id'],where)
        if ctx['expected']:
            conclusion = group['conclusion']
        else:
            unit = get(ctx['units'],group['conclusion'],where)
            conclusion = {'unit_id':unit['id'],'source':resolved_selection(unit['source'],ctx)}
            group['conclusion'] = conclusion
        unit = get(expunits,conclusion['unit_id'],where)
        require(typed_equal(conclusion['source'],expected_selection(unit,expected)),where,'Group conclusion contradicts expected source','SOURCE_JOIN_MISMATCH')
    for bundle in ctx['bundles'].values():
        unit = get(expunits,bundle['conclusion']['unit_id'],where)
        require(typed_equal(bundle['conclusion']['source'],expected_selection(unit,expected)),where,'Bundle conclusion contradicts expected source','SOURCE_JOIN_MISMATCH')


def composition_unsupported(ctx):
    groups = {}
    bundles = {}
    for g in ctx['groups'].values():
        groups.setdefault(g['conclusion']['unit_id'],[]).append(g['group_id'])
    for b in ctx['bundles'].values():
        bundles.setdefault(b['conclusion']['unit_id'],[]).append(b['id'])
    for cid, ids in groups.items():
        require(len(ids) <= 1 or len(bundles.get(cid,[])) >= 1,ctx['where'],'Shared conclusion needs an explicit recorded ALL bundle','UNSUPPORTED_INFERENCE')
    require(all(len(ids) <= 1 for ids in bundles.values()),ctx['where'],'Distinct bundles create a second route for one conclusion','UNSUPPORTED_INFERENCE')


def ranges_valid(boundary, identity, source_bytes, where):
    total = len(source_lines(source_bytes[file_key(identity)],where))
    for key in ('consumed_lines','excluded_lines'):
        prior = 0
        for pair in boundary[key]:
            require(pair[0] > prior and pair[1] <= total,where,'Reading ranges must be ordered, disjoint and in bounds')
            prior = pair[1]
    require(not any(a[0] <= b[1] and b[0] <= a[1] for a in boundary['consumed_lines'] for b in boundary['excluded_lines']),where,'Consumed reading overlaps an exclusion')


def selections_within_boundary(boundary, identity, selections, where):
    """Apply ranges to this exact file; local aliases never choose the rule."""
    for selection in selections:
        if typed_equal(selection['file'],identity) and selection['lines'] is not None:
            require(any(a <= selection['lines'][0] <= selection['lines'][1] <= z
                        for a,z in boundary['consumed_lines']),
                    where,'Reading selection is outside consumed ranges')


def supplier_intrinsics(supplier, where, expanded=False):
    """Constraints intrinsic to a supplier, without consulting another cut."""
    if supplier['kind'] == 'inventory_unit':
        require(supplier['unit_ids'],where,'Inventory supplier must resolve its included units')
        if expanded:
            require(any(s['precision'] == 'exact_lines' for s in supplier['source_refs']),
                    where,'Historical inventory supplier lacks its exact source selection')
    elif supplier['kind'] in ('source_section','import'):
        require(supplier['source_refs'],where,'Source/import supplier requires authenticated source')
        require(supplier['expansion'] != 'in_slice' or supplier['unit_ids'],where,'Expanded supplier requires included derivation')
    else:
        require(supplier['expansion'] == 'unexpanded',where,'External/unnamed mechanisms remain unexpanded')
        if supplier['kind'] == 'external' and (supplier['external_ref'] is None or
                any(supplier['external_ref'][k] is None for k in ('edition_or_version','theorem_or_section','url'))):
            require(supplier['unknowns' if expanded else 'unknown_refs'],where,'Unresolved external reference needs attributed unknown')


def within_file(ctx, expected, source_bytes):
    where = ctx['where']
    root = ctx['root']
    require(root['statement_id'] == (ctx['doc']['root_statement_id'] if ctx['expected'] else root['statement_id']),where,'Root statement ID inconsistent')
    for uid in root['entry_unit_ids']:
        get(ctx['units'],uid,where)
    for value in walk(ctx['doc']):
        # Expanded historical targets have no mutable table indirection.
        if 'record_id' in value:
            get(ctx['records'],value['record_id'],where)
        if 'source_id' in value:
            get(ctx['sources'],value['source_id'],where)
        for uid in value.get('unknown_refs',[]):
            get(ctx['unknowns'],uid,where)
    for unknown in ctx['unknowns'].values():
        for uid in unknown['affects_use_ids']:
            get(ctx['uses'],uid,where)
        expand(unknown,ctx,(unknown['id'],))
    for boundary in ctx['boundaries'].values():
        identity = get(ctx['sources'],boundary['source_id'],where)['identity']
        ranges_valid(boundary,identity,source_bytes,where)
    premise_sets = {}
    for uid,use in ctx['uses'].items():
        owner = use['consumer_unit_id'] if ctx['expected'] else use['binding']['consumer_unit_id']
        get(ctx['units'],owner,where)
        if use['kind'] == 'premise':
            premise_sets.setdefault(owner,set()).add(uid)
    owners = set()
    for g in ctx['groups'].values():
        require(g['owner_unit_id'] not in owners,where,'Multiple groups for one owner')
        owners.add(g['owner_unit_id'])
        require(set(g['premise_use_ids']) == premise_sets.get(g['owner_unit_id'],set()),where,'Group must equal its own complete recorded premise set')
    require(owners == set(premise_sets),where,'Missing group for recorded premises')
    membership = set()
    for b in ctx['bundles'].values():
        actual = {g['group_id'] for g in ctx['groups'].values() if g['conclusion']['unit_id'] == b['conclusion']['unit_id']}
        require(len(actual) >= 2 and set(b['group_ids']) == actual,where,'Bundle must equal all its own groups for the conclusion')
        require(not membership.intersection(actual),where,'Group belongs to multiple bundles')
        membership.update(actual)
    if ctx['expected']:
        for key,role in [('inventory_record','inventory'),('omission_read_record','omission_read')]:
            require(get(ctx['records'],ctx['doc'][key]['record_id'],where)['role'] == role,where,'Inventory evidence role mismatch')
        return
    for unit in ctx['units'].values():
        for uid in unit['related_unit_ids']:
            get(ctx['units'],uid,where)
    for h in ctx['doc']['history']:
        for uid in h['affects_unit_ids']:
            get(ctx['units'],uid,where)
        for uid in h['affects_use_ids']:
            get(ctx['uses'],uid,where)
    expunits = {u['id']:u for u in expected['expected_units']}
    for supplier in ctx['suppliers'].values():
        supplier_intrinsics(supplier,where)
        for uid in supplier['unit_ids']:
            get(ctx['units'],uid,where)
            get(expunits,uid,where)
        if supplier['kind'] == 'inventory_unit':
            selections = [resolved_selection(s,ctx) for s in supplier['source_refs']]
            for uid in supplier['unit_ids']:
                require(any(typed_equal(s,expected_selection(expunits[uid],expected)) for s in selections),where,'Inventory supplier lacks exact expected source','SOURCE_JOIN_MISMATCH')
    for use in ctx['uses'].values():
        for sid in use['binding']['supplier_ids']:
            get(ctx['suppliers'],sid,where)
        for reading in use['binding']['source_reading']:
            b = get(ctx['boundaries'],reading['boundary_id'],where)
            for sid in reading['supplier_ids']:
                require(sid in use['binding']['supplier_ids'],where,'Reading supplier is not part of the use')
            selections = list(reading['applies_to'])
            for sid in reading['supplier_ids']:
                selections.extend(get(ctx['suppliers'],sid,where)['source_refs'])
            identity=get(ctx['sources'],b['source_id'],where)['identity']
            selections_within_boundary(b,identity,[resolved_selection(s,ctx) for s in selections],where)
        for review in use['applicability_reviews']:
            record = get(ctx['records'],review['record']['record_id'],where)
            require(record['role'] == 'applicability_review' and review['reviewed_use']['use_id'] == use['id'],where,'Review role or holding-use identity mismatch')
            historical_consistency(review['reviewed_use'],where,source_bytes)


def canonical_target(target):
    out = copy.deepcopy(target)
    if out['inference_context'] is not None:
        out['inference_context']['premises'].sort(key=lambda m:m['use_id'].encode('utf-8'))
    if out['bundle_context'] is not None:
        out['bundle_context']['groups'].sort(key=lambda g:g['group_id'].encode('utf-8'))
        for g in out['bundle_context']['groups']:
            g['members'].sort(key=lambda m:m['use_id'].encode('utf-8'))
    return out


def historical_intrinsics(target, source_bytes, where):
    """Validate stored expansions against their own authenticated identities.

    No current source, boundary, supplier, unit or unknown table is available to
    this function. A well-formed differing historical target remains evidence.
    """
    def unknown_chain(unknown, trail=()):
        require(unknown['id'] not in trail,where,'Historical unknown-reference cycle')
        for nested in unknown['description']['unknowns']:
            unknown_chain(nested,(*trail,unknown['id']))

    for obj in walk(target):
        if set(obj) == set(SHAPES['XUnknown']):
            unknown_chain(obj)
        if set(obj) == set(SHAPES['XSupplier']):
            supplier_intrinsics(obj,where,expanded=True)
        if set(obj) not in (set(SHAPES['Core']),set(SHAPES['Snapshot'])):
            continue
        suppliers=indexed(obj['suppliers'],'id',where)
        for reading in obj['source_reading']:
            boundary=reading['boundary']
            ranges_valid(boundary,boundary['file'],source_bytes,where)
            selections=list(reading['applies_to'])
            for supplier in reading['suppliers']:
                require(supplier['id'] in suppliers and typed_equal(supplier,suppliers[supplier['id']]),
                        where,'Historical reading supplier contradicts its own stored use')
                selections.extend(supplier['source_refs'])
            selections_within_boundary(boundary,boundary['file'],selections,where)


def historical_consistency(target, where, source_bytes):
    historical_intrinsics(target,source_bytes,where)
    core = {k:target[k] for k in CORE_KEYS}
    inf, bundle = target['inference_context'], target['bundle_context']
    if target['use_kind'] != 'premise':
        require(inf is None and bundle is None,where,'Nonpremise historical target must have null contexts')
        return
    require(inf is not None,where,'Premise historical target lacks inference context')
    members = indexed(inf['premises'],'use_id',where)
    require(target['use_id'] in members and typed_equal(members[target['use_id']]['core'],core),where,'Historical owning premise/core mismatch')
    require(all(m['core']['consumer_unit_id'] == target['consumer_unit_id'] and
                m['core']['consumer_statement_id'] == target['consumer_statement_id'] for m in members.values()),
            where,'Historical inference member owner/statement mismatch')
    if bundle is not None:
        groups = indexed(bundle['groups'],'group_id',where)
        require(inf['group_id'] in groups and typed_equal(bundle['conclusion'],inf['conclusion']),where,'Historical complete bundle/own group disagree')
        own = groups[inf['group_id']]
        require(own['owner_unit_id'] == target['consumer_unit_id'],where,'Historical owner mismatch')
        owners, all_members = set(), set()
        for g in groups.values():
            indexed(g['members'],'use_id',where)
            require(typed_equal(g['conclusion'],bundle['conclusion']),where,'Historical bundle conclusion mismatch')
            require(g['owner_unit_id'] not in owners,where,'Historical bundle repeats an owner')
            owners.add(g['owner_unit_id'])
            for member in g['members']:
                require(member['use_id'] not in all_members,where,'Historical bundle repeats a use')
                all_members.add(member['use_id'])
                require(member['core']['consumer_unit_id'] == g['owner_unit_id'] and
                        member['core']['consumer_statement_id'] == target['consumer_statement_id'],
                        where,'Historical contribution member owner/statement mismatch')
        canonical = lambda members:sorted(members,key=lambda m:m['use_id'].encode('utf-8'))
        require(typed_equal(canonical(own['members']),canonical(inf['premises'])),where,'Historical owning group members disagree')


def core_for(use, ctx):
    binding = expand(use['binding'],ctx)
    return {**binding,'consumer_statement_source':expand(ctx['root']['source_statement'],ctx),
            'consumer_semantics':expand(ctx['root']['semantics'],ctx)}


def resolve_use_target(slice_data, use_id):
    """Resolve already validated current data; never used to fill a stored target."""
    ctx = context(slice_data,False,'companion')
    use = get(ctx['uses'],use_id,'companion')
    for g in ctx['groups'].values():
        u = get(ctx['units'],g['conclusion'],'companion')
        g['conclusion'] = {'unit_id':u['id'],'source':resolved_selection(u['source'],ctx)}
    result = {**core_for(use,ctx),'use_id':use_id,'use_kind':use['kind'],'inference_context':None,'bundle_context':None}
    if use['kind'] != 'premise':
        return result
    group = next(g for g in ctx['groups'].values() if use_id in g['premise_use_ids'])
    def members(g):
        return [{'use_id':uid,'use_kind':'premise','core':core_for(ctx['uses'][uid],ctx)} for uid in sorted(g['premise_use_ids'],key=lambda i:i.encode('utf-8'))]
    result['inference_context'] = {'group_id':group['group_id'],'combination':'ALL','conclusion':copy.deepcopy(group['conclusion']),'premises':members(group)}
    bundle = next((b for b in ctx['bundles'].values() if group['group_id'] in b['group_ids']),None)
    if bundle:
        result['bundle_context'] = {'bundle_id':bundle['id'],'combination':'ALL','conclusion':copy.deepcopy(bundle['conclusion']),
            'basis':expand(bundle['basis'],ctx),'groups':[{'group_id':gid,'owner_unit_id':ctx['groups'][gid]['owner_unit_id'],
            'combination':'ALL','conclusion':copy.deepcopy(ctx['groups'][gid]['conclusion']),'members':members(ctx['groups'][gid])}
            for gid in sorted(bundle['group_ids'],key=lambda i:i.encode('utf-8'))]}
    return result


def group_descriptor(g):
    return {k:(sorted(g[k],key=lambda i:i.encode('utf-8')) if k == 'premise_use_ids' else g[k]) for k in SHAPES['ExpectedGroup']}


def bundle_descriptor(b,ctx):
    out = expand(b,ctx)
    out['group_ids'].sort(key=lambda i:i.encode('utf-8'))
    return out


def compare_expected(exp, comp):
    where = 'companion'
    e, c = exp['doc'], comp['doc']
    require(list(exp['units']) == list(comp['units']),where,'Ordered unit membership differs from independent inventory','EXPECTED_INVENTORY_MISMATCH')
    uses = [{'id':u['id'],'consumer_unit_id':u['binding']['consumer_unit_id'],'kind':u['kind']} for u in comp['uses'].values()]
    sort = lambda rows:sorted(rows,key=lambda u:u['id'].encode('utf-8'))
    require(typed_equal(sort(e['expected_uses']),sort(uses)),where,'Use membership/kinds differ from independent inventory','EXPECTED_INVENTORY_MISMATCH')
    require(typed_equal(expand(exp['root'],exp),expand(comp['root'],comp)),where,'Resolved root differs from independent inventory','EXPECTED_INVENTORY_MISMATCH')
    er, cr = e['inventory_record'],c['inventory_binding']['extraction_record']
    record_join = lambda r,ctx:{'record':ctx['records'][r['record_id']],'locator':r['locator']}
    ej,cj = record_join(er,exp),record_join(cr,comp)
    ej['record'] = {k:v for k,v in ej['record'].items() if k != 'id'}
    cj['record'] = {k:v for k,v in cj['record'].items() if k != 'id'}
    require(typed_equal(ej,cj),where,'Extraction identity/role/performer/selector differs','EXPECTED_INVENTORY_MISMATCH')
    require(set(exp['groups']) == set(comp['groups']) and all(typed_equal(group_descriptor(g),group_descriptor(comp['groups'][gid])) for gid,g in exp['groups'].items()),where,'Group mapping differs from independent inventory','EXPECTED_INVENTORY_MISMATCH')
    require(set(exp['bundles']) == set(comp['bundles']) and all(typed_equal(bundle_descriptor(b,exp),bundle_descriptor(comp['bundles'][bid],comp)) for bid,b in exp['bundles'].items()),where,'Complete bundle descriptor differs from independent inventory','EXPECTED_INVENTORY_MISMATCH')


def cycles(ctx):
    edges = {uid:set() for uid in ctx['units']}
    for group in ctx['groups'].values():
        for uid in group['premise_use_ids']:
            use = ctx['uses'][uid]
            for sid in use['binding']['supplier_ids']:
                supplier = ctx['suppliers'][sid]
                if supplier['kind'] == 'inventory_unit':
                    edges[group['conclusion']['unit_id']].update(supplier['unit_ids'])
    visited,active = set(),set()
    def visit(uid):
        require(uid not in active,ctx['where'],'Mapped inferential cycle')
        if uid in visited:
            return
        active.add(uid)
        for next_id in edges[uid]:
            visit(next_id)
        active.remove(uid)
        visited.add(uid)
    for uid in edges:
        visit(uid)


def counts(expected):
    return {'units':len(expected['expected_units']),'uses':len(expected['expected_uses']),
            'by_kind':{k:sum(u['kind'] == k for u in expected['expected_uses']) for k in KINDS},
            'unknown_annotations':len(expected['unknowns'])}


def refusal(exc):
    return {'valid':False,'reason':exc.reason,'failed_input':exc.failed_input,'message':str(exc),'scientific_effect':'NONE'}


def preflight(expected, companion, expected_identity):
    """One shared shape/duplicate/pin order for memory and Git-object callers."""
    unsupported(expected,True,'inventory')
    if companion is not None:
        unsupported(companion,False,'companion')
    shape(expected,'Expected','inventory')
    exp=context(expected,True,'inventory')
    comp=None
    if companion is not None:
        shape(companion,'Slice','companion')
        comp=context(companion,False,'companion')
        shape(expected_identity,'File','expected_pin')
        require(typed_equal(companion['inventory_binding']['expected_inventory'],expected_identity),
                'expected_pin','Companion cannot replace the independently supplied inventory identity','IDENTITY_MISMATCH')
    return exp,comp


def _validate(expected, companion, expected_identity, source_bytes, snapshots):
    require(type(source_bytes) is dict and type(snapshots) is dict,'inputs','Required source/capture buffer maps unavailable','INPUT_UNAVAILABLE')
    if companion is not None:
        require(type(snapshots.get('expected')) is dict and type(snapshots.get('companion')) is dict,
                'inputs','Separate expected/companion capture maps required','INPUT_UNAVAILABLE')
    exp,comp=preflight(expected,companion,expected_identity)
    authenticate(exp,source_bytes,snapshots['expected'] if comp else snapshots)
    if comp:
        authenticate(comp,source_bytes,snapshots['companion'])
    joins(exp,expected,source_bytes)
    if comp:
        joins(comp,expected,source_bytes)
    composition_unsupported(exp)
    if comp:
        composition_unsupported(comp)
    within_file(exp,expected,source_bytes)
    if comp:
        within_file(comp,expected,source_bytes)
        compare_expected(exp,comp)
        cycles(comp)
    report = {'valid':True,'phase':'paired' if comp else 'inventory-only','counts':counts(expected),'scientific_effect':'NONE','status_authority':False,'independence_credit':0}
    if comp:
        matches = []
        for use in comp['uses'].values():
            target = resolve_use_target(companion,use['id'])
            for review in use['applicability_reviews']:
                matches.append({'use_id':use['id'],'record':expand(review['record'],comp),
                    'matches_current':typed_equal(canonical_target(review['reviewed_use']),target),
                    'meaning':'Technical target correspondence only; scope and scientific sufficiency are not assessed'})
        report['review_targets'] = matches
    return report


def validate_expected_inventory(data, source_bytes, record_snapshots):
    try:
        return _validate(data,None,None,source_bytes,record_snapshots)
    except ContractError as exc:
        return refusal(exc)
    except RecursionError:
        return refusal(ContractError('CONTRACT_SHAPE','inventory','Excessive recursive input'))


def validate_proof_slice(data, expected, expected_identity, source_bytes, record_snapshots):
    try:
        return _validate(expected,data,expected_identity,source_bytes,record_snapshots)
    except ContractError as exc:
        return refusal(exc)
    except RecursionError:
        return refusal(ContractError('CONTRACT_SHAPE','companion','Excessive recursive input'))


def _raw_run(repo, *args):
    # Match the consumed helper's routing/capability boundary, but retain bytes.
    env = {key:value for key,value in os.environ.items()
           if not key.startswith('GIT_') or key == 'GIT_CEILING_DIRECTORIES'}
    env['GIT_NO_LAZY_FETCH'] = '1'
    try:
        return subprocess.run(['git','--no-replace-objects','--no-lazy-fetch','-C',str(repo),*args],
                              capture_output=True,env=env)
    except OSError:
        fail('INPUT_UNAVAILABLE','git','Git backend could not be launched')


def _object_blob(repo, commit, path):
    shape(commit,'sha1','commit')
    shape(path,'path','path')
    try:
        blob = _retrofit._git_blob(repo,commit,path)
    except _retrofit._GitBackendError as exc:
        fail('INPUT_UNAVAILABLE','git',str(exc))
    require(blob is not None,'git','Required commit/path object is unavailable without fetching','INPUT_UNAVAILABLE')
    return blob


def verify_file_identity(identity, repo):
    """Authenticate one original blob in the explicitly mapped Math repository."""
    shape(identity,'File','file_identity')
    require(identity['repository'] == REPOSITORY,'file_identity','No clone mapping supplied for this repository','INPUT_UNAVAILABLE')
    blob = _object_blob(repo,identity['commit'],identity['path'])
    require(blob == identity['git_blob'],'file_identity','Commit/path does not name the declared blob','IDENTITY_MISMATCH')
    result = _raw_run(repo,'cat-file','blob',blob)
    require(result.returncode == 0,'file_identity','Raw blob unavailable without fetching','INPUT_UNAVAILABLE')
    raw = result.stdout
    actual_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(len(raw) == identity['bytes'] and hashlib.sha256(raw).hexdigest() == identity['sha256'] and actual_blob == blob,
            'file_identity','Original blob bytes fail their complete identity','IDENTITY_MISMATCH')
    return raw


def identity_at(repo, commit, path):
    blob = _object_blob(repo,commit,path)
    result = _raw_run(repo,'cat-file','blob',blob)
    require(result.returncode == 0,'git','Raw artifact object unavailable','INPUT_UNAVAILABLE')
    raw = result.stdout
    framed = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(framed == blob,'git','Raw artifact Git-framed digest mismatch','IDENTITY_MISMATCH')
    return dict(repository=REPOSITORY,commit=commit,path=path,git_blob=blob,
                sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),raw


def snapshot_path(artifact_path, identity):
    shape(artifact_path,'path','artifact_path')
    shape(identity,'RecordIdentity','record_identity')
    require(identity['kind'] != 'git_file','record_identity','Git-file records use their own FileIdentity')
    comment = identity['kind'] == 'github_comment_snapshot'
    native_id = identity['comment_id' if comment else 'review_id']
    name = ('comment-' if comment else 'review-') + native_id + '-' + identity['body_sha256'] + '.json'
    return str(PurePosixPath(artifact_path).parent / 'records' / name)


def acquire_sources(doc, artifact, repo, source_bytes):
    content = {k:v for k,v in doc.items() if k != 'inventory_binding'}
    captures = {}
    inputs = []
    for value in walk(content):
        if set(value) == set(FILE_KEYS):
            key = file_key(value)
            if key not in source_bytes:
                source_bytes[key] = verify_file_identity(value,repo)
        elif value.get('kind') in ('github_comment_snapshot','github_review_snapshot'):
            key = record_key(value)
            if key not in captures:
                path = snapshot_path(artifact['path'],value)
                identity,raw = identity_at(repo,artifact['commit'],path)
                captures[key] = parse_input(raw,path)
                inputs.append(identity)
    return captures,inputs


def tool_identity(path):
    raw = Path(path).read_bytes()
    return {'path':Path(path).name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}


class _Parser(argparse.ArgumentParser):
    def error(self,message):
        fail('CONTRACT_SHAPE','arguments',message)


def main(argv=None):
    try:
        parser = _Parser(description=__doc__)
        parser.add_argument('--repo',required=True)
        for name in ('inventory-commit','inventory-path','expected-commit','expected-path','companion-commit','companion-path'):
            parser.add_argument('--'+name)
        args = parser.parse_args(argv)
        inventory = args.inventory_commit is not None or args.inventory_path is not None
        if inventory:
            require(args.inventory_commit is not None and args.inventory_path is not None and
                    all(getattr(args,k) is None for k in ('expected_commit','expected_path','companion_commit','companion_path')),
                    'arguments','Use the complete inventory-only argument pair or complete paired arguments')
            ec,ep = args.inventory_commit,args.inventory_path
        else:
            require(all(getattr(args,k) is not None for k in ('expected_commit','expected_path','companion_commit','companion_path')),
                    'arguments','All independent expected and companion commit/path arguments are required')
            ec,ep = args.expected_commit,args.expected_path
        expected_identity,raw_expected = identity_at(args.repo,ec,ep)
        shallow = _raw_run(args.repo,'rev-parse','--is-shallow-repository')
        require(shallow.returncode == 0 and shallow.stdout == b'false\n','git','Non-shallow object checkout required','INPUT_UNAVAILABLE')
        expected = parse_input(raw_expected,'inventory')
        companion,companion_identity = None,None
        if not inventory:
            companion_identity,raw_companion = identity_at(args.repo,args.companion_commit,args.companion_path)
            companion = parse_input(raw_companion,'companion')
        # Referenced sources/captures are not acquired until both closed-shape
        # and duplicate phases have completed in the same order as the API.
        preflight(expected,companion,expected_identity)
        sources = {}
        es,er = acquire_sources(expected,expected_identity,args.repo,sources)
        if companion is None:
            report = validate_expected_inventory(expected,sources,es)
            inputs = {'inventory':expected_identity,'inventory_records':er}
        else:
            cs,cr = acquire_sources(companion,companion_identity,args.repo,sources)
            ancestor = _raw_run(args.repo,'merge-base','--is-ancestor',ec,args.companion_commit)
            require(ancestor.returncode in (0,1),'git','Ancestry objects unavailable','INPUT_UNAVAILABLE')
            require(ancestor.returncode == 0,'companion','A must be an ancestor of B','EXPECTED_INVENTORY_MISMATCH')
            later_inventory,_ = identity_at(args.repo,args.companion_commit,ep)
            require(later_inventory['git_blob'] == expected_identity['git_blob'],
                    'companion','Expected inventory file changed in B','EXPECTED_INVENTORY_MISMATCH')
            report = validate_proof_slice(companion,expected,expected_identity,sources,{'expected':es,'companion':cs})
            inputs = {'inventory':expected_identity,'companion':companion_identity,'inventory_records':er,'companion_records':cr}
        if report['valid']:
            report['inputs'] = inputs
            report['sources'] = [dict(zip(FILE_KEYS,key)) for key in sources]
            report['tools'] = {'checker':tool_identity(__file__),'retrofit':tool_identity(_retrofit.__file__),
                               'python':sys.version,'optimized':bool(sys.flags.optimize)}
    except ContractError as exc:
        report = refusal(exc)
    except RecursionError:
        report = refusal(ContractError('CONTRACT_SHAPE','input','Excessive recursive input'))
    print(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2))
    return 0 if report['valid'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
