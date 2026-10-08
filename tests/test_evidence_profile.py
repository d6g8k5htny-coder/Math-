"""Behavior of tools/evidence_profile.py (standard library only; the live graph is read, never written)."""
import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRAPH = ROOT / 'frontiers' / 'downstream_gate_20260925' / 'GRAPH.json'
SPEC = importlib.util.spec_from_file_location('evidence_profile', ROOT / 'tools' / 'evidence_profile.py')
ep = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ep)
GATE = ep.load_gate()


def node(classification, **fields):
    return dict(classification=classification, controlling=False, **fields)


def synthetic():
    return {
        'schema_version': 1,
        'object': 'SYNTHETIC',
        'nodes': {
            'math.top': node('OPEN_ACTIVE'),
            'math.mid': node('PROVED_REVIEWED', author_provider='OpenAI',
                             review_basis=[{'provider': 'xAI'}, {'provider': 'Anthropic/Claude'}]),
            'math.leaf': node('AUTHOR_SIDE_CANDIDATE', author_provider='Anthropic',
                              review_provider='Anthropic Claude session'),
            'math.shared': node('PROVED_REVIEWED', author_provider='OpenAI', review_providers=['nonauthor']),
            'math.boundary': node('REFUTED'),
        },
        'edges': [
            {'from': 'math.top', 'to': 'math.mid', 'required': True, 'relation': 'uses'},
            {'from': 'math.top', 'to': 'math.shared', 'required': True, 'relation': 'uses'},
            {'from': 'math.top', 'to': 'math.boundary', 'required': False, 'relation': 'boundary_only'},
            {'from': 'math.mid', 'to': 'math.leaf', 'required': True, 'relation': 'imports'},
            {'from': 'math.mid', 'to': 'math.shared', 'required': True, 'relation': 'imports'},
        ],
    }


def run(argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = ep.main(argv)
    return code, out.getvalue()


class SyntheticGraph(unittest.TestCase):
    def setUp(self):
        self.graph = synthetic()
        GATE.validate_graph_fail_closed(self.graph)

    def test_unsatisfied_required_is_transitive_and_ignores_context_edges(self):
        p = ep.profile(GATE, self.graph, 'math.top')
        self.assertEqual(p['unsatisfied_required'],
                         [{'node': 'math.leaf', 'classification': 'AUTHOR_SIDE_CANDIDATE'}])
        self.assertEqual(ep.profile(GATE, self.graph, 'math.shared')['unsatisfied_required'], [])

    def test_provider_distinct_reads_only_recorded_families(self):
        self.assertEqual(ep.provider_distinct(self.graph['nodes']['math.mid']), 'yes')
        self.assertEqual(ep.provider_distinct(self.graph['nodes']['math.leaf']), 'no')
        self.assertEqual(ep.provider_distinct(self.graph['nodes']['math.shared']), 'not recorded')
        self.assertEqual(ep.provider_distinct(self.graph['nodes']['math.top']), 'not recorded')
        self.assertIsNone(ep.family('OpenAI reviewed by xAI'))
        self.assertEqual(ep.family('xAI/Grok via Cursor'), 'xAI')

    def test_unresolved_reviewer_never_yields_no(self):
        # 6018400003 item 1: an unresolved or ambiguous reviewer must not be dropped before deciding 'no'.
        for reviewers in (['OpenAI', 'unattributed'], ['OpenAI', 'OpenAI / xAI'], ['OpenAI', 'nonauthor']):
            with self.subTest(reviewers=reviewers):
                self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='OpenAI',
                                                           review_providers=reviewers)), 'not recorded')
        self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='OpenAI',
                                                   review_providers=['unattributed', 'xAI'])), 'yes')
        self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='OpenAI',
                                                   review_providers=['OpenAI / GPT-6', 'Codex'])), 'no')
        self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='OpenAI',
                                                   review_providers=[])), 'not recorded')
        # EP381-UNKNOWN-01 (6018473703): the same rule across fields, singular review_provider plus review_basis.
        self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='OpenAI', review_provider='OpenAI',
                                                   review_basis=[{'provider': 'unidentified'}])), 'not recorded')
        self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='OpenAI', review_provider='OpenAI',
                                                   review_basis=[{'provider': 'xAI'}])), 'yes')
        self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='OpenAI',
                                                   review_providers=['OpenAI or xAI'])), 'not recorded')

    def test_negated_or_undisclosed_provider_is_unresolved(self):
        # EP381-02 (6018548621): non-identities must not be read as a provider.
        for text in ('not OpenAI; provider not disclosed', 'no Anthropic involvement', 'other than xAI',
                     'unidentified', 'provider not disclosed'):
            with self.subTest(text=text):
                self.assertIsNone(ep.family(text))
        self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='Anthropic',
                                                   review_providers=['not OpenAI; provider not disclosed'])),
                         'not recorded')
        self.assertEqual(ep.provider_distinct(node('PROVED_REVIEWED', author_provider='OpenAI',
                                                   review_providers=['claudette'])), 'not recorded')
        p = ep.profile(GATE, {'schema_version': 1, 'nodes': {'math.x': node(
            'PROVED_REVIEWED', author_provider='OpenAI', review_providers=['OpenAI', 'not disclosed'])},
            'edges': []}, 'math.x')
        self.assertEqual(p['provider_distinct'], 'not recorded')
        self.assertEqual(p['unresolved_reviewer_providers'], ['not disclosed'])

    def test_default_selection_covers_context_only_cycles(self):
        # 6018548621 nonblocking: a component without an edge-free root is still listed.
        graph = synthetic()
        graph['nodes']['math.a'] = node('OPEN_ACTIVE')
        graph['nodes']['math.b'] = node('PROVED_REVIEWED')
        graph['edges'] += [{'from': 'math.a', 'to': 'math.b', 'required': False, 'relation': 'context'},
                           {'from': 'math.b', 'to': 'math.a', 'required': False, 'relation': 'context'}]
        GATE.validate_graph_fail_closed(graph)
        self.assertEqual(ep.roots(graph), ['math.top', 'math.a'])

    def test_positive_identity_grammar(self):
        # EP381-02 residual (6018757501): only the documented positive form names a family.
        for text, expected in (('OpenAI / GPT-6 Astra Pro', 'OpenAI'), ('Grok 4.7', 'xAI'),
                               ('xAI/Grok via Cursor (D1-A-E, section 9 v1.1, partial slices)', 'xAI'),
                               ('Claude Code session', 'Anthropic'), ('Google DeepMind Gemini', 'Google')):
            with self.subTest(text=text):
                self.assertEqual(ep.family(text), expected)
        for text in ('possibly OpenAI', 'OpenAI or unspecified', 'review requested from OpenAI',
                     'OpenAI reviewed by xAI', 'OpenAI (a) (b)', 'OpenAI, probably', 'Claude/Grok'):
            with self.subTest(text=text):
                self.assertIsNone(ep.family(text))

    def test_family_matches_whole_tokens_only(self):
        # 6018400003 item 2: substring hits such as 'notopenai' or 'claudette' name no family.
        for text in ('notopenai', 'claudette', 'xairline', 'grokking-free', 'googleplex', ''):
            with self.subTest(text=text):
                self.assertIsNone(ep.family(text))
        for text, expected in (('OpenAI / GPT-6 Astra Pro', 'OpenAI'), ('Anthropic/Claude (A1-A7)', 'Anthropic'),
                               ('Claude Code session', 'Anthropic'), ('ChatGPT', 'OpenAI'), ('Gemini', 'Google')):
            with self.subTest(text=text):
                self.assertEqual(ep.family(text), expected)

    def test_tree_marks_context_edges_and_expands_shared_nodes_once(self):
        lines = ep.tree_lines(GATE, self.graph, 'math.top')
        text = '\n'.join(lines)
        self.assertIn('context (boundary_only) math.boundary  REFUTED', text)
        self.assertEqual(sum('math.shared' in line for line in lines[1:-1]), 2)
        self.assertEqual(sum('(expanded above)' in line for line in lines), 1)
        self.assertEqual(lines[-1], 'Unsatisfied required dependencies (1): math.leaf (AUTHOR_SIDE_CANDIDATE)')

    def test_roots_are_math_nodes_without_incoming_edges(self):
        self.assertEqual(ep.roots(self.graph), ['math.top'])

    def test_cli_on_file_json_and_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'graph.json'
            path.write_text(json.dumps(self.graph))
            code, text = run(['--graph', str(path)])
            self.assertEqual(code, 0)
            self.assertTrue(text.startswith('math.top  OPEN_ACTIVE'))
            self.assertIn('no status authority; scientific effect NONE', text)
            code, text = run(['--graph', str(path), '--node', 'math.mid', '--json'])
            data = json.loads(text)
            self.assertEqual([p['node'] for p in data['profiles']], ['math.mid'])
            self.assertIs(data['status_authority'], False)
            self.assertIs(data['lemma_closed'], False)
            self.assertEqual(data['scientific_effect'], 'NONE')
            self.assertIn('blind_reconstruction', data['axes_outside_graph'])

    def test_invalid_graphs_and_unknown_nodes_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'graph.json'
            bad = synthetic()
            bad['edges'].append({'from': 'math.leaf', 'to': 'math.top', 'required': True, 'relation': 'cycle'})
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, 'required dependency cycle'):
                run(['--graph', str(path)])
            bad = synthetic()
            bad['nodes']['math.top']['classification'] = 'CLOSED'
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, 'unknown node classification'):
                run(['--graph', str(path)])
            path.write_text(json.dumps(synthetic()))
            with self.assertRaisesRegex(KeyError, 'unknown node'):
                run(['--graph', str(path), '--node', 'math.absent'])


class ProviderAttributionCLI(unittest.TestCase):
    """EP381-01/EP381-02 (review 5430026100) through the actual command line, in the current Python mode."""

    CASES = {
        'math.mixed-unknown': ('OpenAI', ['OpenAI', 'not disclosed'], 'not recorded'),
        'math.mixed-ambiguous': ('OpenAI', ['OpenAI', 'OpenAI or Anthropic'], 'not recorded'),
        'math.distinct-plus-unknown': ('OpenAI', ['not disclosed', 'xAI'], 'yes'),
        'math.negated': ('Anthropic', ['not OpenAI; provider not disclosed'], 'not recorded'),
        'math.embedded-name': ('OpenAI', ['claudette'], 'not recorded'),
        'math.anthropic-claude': ('OpenAI', ['Anthropic/Claude'], 'yes'),
        'math.chatgpt-codex': ('OpenAI', ['ChatGPT/Codex'], 'no'),
        'math.xai-grok-cursor': ('OpenAI', ['xAI/Grok via Cursor'], 'yes'),
        'math.all-same': ('xAI', ['xAI/Grok via Cursor', 'Grok 4.7'], 'no'),
        # Delta 6018757501: prose around a provider name is not a positive identity.
        'math.possibly': ('Anthropic', ['possibly OpenAI'], 'not recorded'),
        'math.or-unspecified': ('Anthropic', ['OpenAI or unspecified'], 'not recorded'),
        'math.invitation': ('Anthropic', ['review requested from OpenAI'], 'not recorded'),
        'math.astra-control': ('Anthropic', ['OpenAI / GPT-6 Astra Pro'], 'yes'),
    }

    def test_cli_json_reports_conservative_provider_attribution(self):
        graph = {'schema_version': 1, 'object': 'SYNTHETIC-CLI', 'edges': [],
                 'nodes': {nid: node('PROVED_REVIEWED', author_provider=a, review_providers=r)
                           for nid, (a, r, _) in self.CASES.items()}}
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'graph.json'
            path.write_text(json.dumps(graph))
            before = path.read_bytes()
            flags = ['-O'] if sys.flags.optimize else []
            run = subprocess.run([sys.executable, '-B', *flags, '-S', str(ROOT / 'tools' / 'evidence_profile.py'),
                                  '--graph', str(path), '--json'], capture_output=True, text=True, timeout=60)
            self.assertEqual((run.returncode, run.stderr), (0, ''))
            self.assertEqual(path.read_bytes(), before)
        profiles = {p['node']: p for p in json.loads(run.stdout)['profiles']}
        self.assertEqual(set(profiles), set(self.CASES))
        for nid, (_, reviewers, expected) in self.CASES.items():
            with self.subTest(node=nid):
                self.assertEqual(profiles[nid]['provider_distinct'], expected)
                self.assertEqual(profiles[nid]['reviewer_providers'], reviewers)
        self.assertEqual(profiles['math.mixed-unknown'].get('unresolved_reviewer_providers'), ['not disclosed'])
        self.assertEqual(profiles['math.negated'].get('unresolved_reviewer_providers'),
                         ['not OpenAI; provider not disclosed'])


class LiveGraph(unittest.TestCase):
    def test_live_graph_renders_without_writing(self):
        before = hashlib.sha256(GRAPH.read_bytes()).hexdigest()
        code, text = run([])
        self.assertEqual(code, 0)
        graph = GATE.load_graph(GRAPH)
        for root in ep.roots(graph):
            self.assertIn('\n' + root + '  ' if not text.startswith(root) else root, text)
        code, text = run(['--json'])
        data = json.loads(text)
        self.assertEqual(len(data['profiles']), len(ep.roots(graph)))
        for p in data['profiles']:
            self.assertEqual(p['classification'], graph['nodes'][p['node']]['classification'])
        self.assertEqual(hashlib.sha256(GRAPH.read_bytes()).hexdigest(), before)


class ControllingEligibilityCLI(unittest.TestCase):
    """Opt-in graph eligibility is not scientific acceptance; use the real gate and real CLI."""

    def fixture(self):
        graph = {
            'schema_version': 1, 'object': 'ELIGIBILITY-FIXTURE',
            'nodes': {
                'math.candidate': node('AUTHOR_SIDE_CANDIDATE'),
                'math.good': node('PROVED_REVIEWED'),
                'math.done': node('PROVED_REVIEWED'),
                'math.missing': node('PROVED_REVIEWED'),
                'math.context': node('PROVED_REVIEWED'),
                'math.refuted': node('REFUTED'),
                'math.blocked': node('PROVED_REVIEWED'),
                'math.refuted-root': node('PROVED_REVIEWED'),
                'math.revalidate': node('REVALIDATION_REQUIRED'),
                'aux.absent': node('BLOCKED_ABSENT'),
                'hist.lemma_closed': node('FALSE'),
            },
            'edges': [
                {'from': 'math.good', 'to': 'math.done', 'required': True, 'relation': 'uses'},
                {'from': 'math.missing', 'to': 'math.candidate', 'required': True, 'relation': 'uses'},
                {'from': 'math.context', 'to': 'math.refuted', 'required': False, 'relation': 'context'},
                {'from': 'math.blocked', 'to': 'aux.absent', 'required': True, 'relation': 'uses'},
                {'from': 'math.refuted-root', 'to': 'math.refuted', 'required': True, 'relation': 'uses'},
            ],
        }
        GATE.validate_graph_fail_closed(graph)
        return graph

    def invoke(self, graph, *args):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'graph.json'
            path.write_text(json.dumps(graph), encoding='utf-8')
            before = path.read_bytes()
            flags = ['-O'] if sys.flags.optimize else []
            process = subprocess.run(
                [sys.executable, '-B', *flags, '-S', str(ROOT / 'tools' / 'evidence_profile.py'),
                 '--graph', str(path), *args], capture_output=True, timeout=60)
            self.assertEqual(path.read_bytes(), before)
            return process

    def test_opt_in_json_returns_exact_gate_decisions(self):
        graph = self.fixture()
        expected = {
            'math.candidate': False, 'math.good': True, 'math.done': True,
            'math.missing': False, 'math.context': True, 'math.refuted': False,
            'math.blocked': False, 'math.refuted-root': False,
            'math.revalidate': False, 'hist.lemma_closed': False,
        }
        args = ['--eligibility', '--json']
        for nid in expected:
            args += ['--node', nid]
        process = self.invoke(graph, *args)
        self.assertEqual((process.returncode, process.stderr), (0, b''))
        data = json.loads(process.stdout)
        self.assertIs(data['status_authority'], False)
        self.assertIs(data['lemma_closed'], False)
        self.assertEqual(data['scientific_effect'], 'NONE')
        self.assertIn('formal_evidence', data['axes_outside_graph'])
        profiles = {p['node']: p for p in data['profiles']}
        self.assertEqual(set(profiles), set(expected))
        for nid, allowed in expected.items():
            with self.subTest(node=nid):
                self.assertEqual(profiles[nid]['controlling_eligibility'], {
                    'target': 'CONTROLLING', 'decision': GATE.promotion_allowed(graph, nid)})
                self.assertIs(profiles[nid]['controlling_eligibility']['decision']['allowed'], allowed)
        self.assertEqual(profiles['math.candidate']['unsatisfied_required'], [])
        self.assertFalse(profiles['math.candidate']['controlling_eligibility']['decision']['allowed'])

    def test_opt_in_text_reports_reasons_and_acceptance_limit(self):
        graph = self.fixture()
        for nid in ('math.candidate', 'math.good', 'math.missing', 'math.blocked', 'math.revalidate'):
            with self.subTest(node=nid):
                process = self.invoke(graph, '--node', nid, '--eligibility')
                self.assertEqual((process.returncode, process.stderr), (0, b''))
                text = process.stdout.decode('utf-8')
                decision = GATE.promotion_allowed(graph, nid)
                self.assertIn('Selected-node CONTROLLING eligibility (recorded graph): '
                              + ('yes' if decision['allowed'] else 'no'), text)
                for reason in decision['reasons']:
                    self.assertIn('  - ' + reason, text)
                self.assertIn('integrity decision only; not theorem acceptance', text)
                self.assertIn('no status authority; scientific effect NONE', text)

    def test_no_flag_output_is_byte_identical_to_predecessor(self):
        graph = {'schema_version': 1, 'object': 'ELIGIBILITY-GOLDEN',
                 'nodes': {'math.candidate': node('AUTHOR_SIDE_CANDIDATE')}, 'edges': []}
        # SHA256 of complete predecessor stdout: no fixture paths or runtime-specific values.
        expected = {False: 'f04f9e77e7e65c2c1ecb9875ed7209946a3a3b675028eb4a92dfb9d51a82dc0f', True: 'e6d3a4d3287d2378ee06f9c6303035d7dc8ae4efa93f271a63c1feadf6bde187'}
        for as_json, digest in expected.items():
            with self.subTest(as_json=as_json):
                args = ['--node', 'math.candidate'] + (['--json'] if as_json else [])
                process = self.invoke(graph, *args)
                self.assertEqual((process.returncode, process.stderr), (0, b''))
                self.assertEqual(hashlib.sha256(process.stdout).hexdigest(), digest)
                self.assertNotIn(b'controlling_eligibility', process.stdout)
                self.assertNotIn(b'Selected-node CONTROLLING eligibility', process.stdout)

    def test_opt_in_unknown_node_refuses_before_any_output(self):
        process = self.invoke(self.fixture(), '--eligibility', '--json',
                              '--node', 'math.good', '--node', 'math.absent')
        self.assertEqual((process.returncode, process.stdout), (1, b''))
        self.assertIn(b'unknown node: math.absent', process.stderr)
        self.assertNotIn(b'unrecognized arguments', process.stderr)

    def test_opt_in_invalid_graph_still_fails_closed(self):
        graph = self.fixture()
        graph['edges'].append({'from': 'math.done', 'to': 'math.good', 'required': True, 'relation': 'uses'})
        process = self.invoke(graph, '--eligibility', '--json')
        self.assertEqual((process.returncode, process.stdout), (1, b''))
        self.assertIn(b'required dependency cycle', process.stderr)
        self.assertNotIn(b'unrecognized arguments', process.stderr)


class GraphInputIdentity(unittest.TestCase):
    """The optional digest identifies the single consumed byte buffer, not a canonicalized graph."""

    MEANING = ('identity of graph input bytes only; not freshness, Git provenance, '
               'program identity or acceptance')

    def invoke(self, raw, *args):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'private-local-name.json'
            path.write_bytes(raw)
            flags = ['-O'] if sys.flags.optimize else []
            result = subprocess.run(
                [sys.executable, '-B', *flags, '-S', str(ROOT / 'tools' / 'evidence_profile.py'),
                 '--graph', str(path), *args], capture_output=True, timeout=60)
            self.assertEqual(path.read_bytes(), raw)
            self.assertNotIn(str(path).encode(), result.stdout)
            return result

    def expected_identity(self, raw):
        return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                'meaning': self.MEANING}

    def test_json_binds_exact_bytes_and_composes_with_eligibility(self):
        graph = synthetic()
        graph['object'] = 'INPUT-IDENTITY-\u03c0'
        texts = [json.dumps(graph, ensure_ascii=False),
                 json.dumps(graph, ensure_ascii=False, indent=2),
                 json.dumps(graph, ensure_ascii=False, indent=2).replace('\n', '\r\n') + '\r\n',
                 json.dumps(graph, ensure_ascii=True, sort_keys=True)]
        digests = set()
        for text in texts:
            raw = text.encode('utf-8')
            with self.subTest(raw_bytes=len(raw)):
                args = ('--json', '--eligibility', '--node', 'math.top', '--node', 'math.mid')
                plain = self.invoke(raw, *args)
                identified = self.invoke(raw, '--input-identity', *args)
                self.assertEqual((plain.returncode, plain.stderr), (0, b''))
                self.assertEqual((identified.returncode, identified.stderr), (0, b''))
                data = json.loads(identified.stdout)
                self.assertEqual(data.pop('input_identity'), self.expected_identity(raw))
                self.assertEqual(data, json.loads(plain.stdout))
                self.assertEqual([p['node'] for p in data['profiles']], ['math.top', 'math.mid'])
                for profile in data['profiles']:
                    self.assertEqual(profile['controlling_eligibility']['decision'],
                                     GATE.promotion_allowed(graph, profile['node']))
                digests.add(hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(digests), len(texts))

    def test_text_adds_one_identity_without_disclosing_paths(self):
        raw = json.dumps(synthetic()).encode('utf-8')
        for extra in ((), ('--eligibility',)):
            with self.subTest(extra=extra):
                plain = self.invoke(raw, *extra)
                identified = self.invoke(raw, '--input-identity', *extra)
                self.assertEqual((plain.returncode, plain.stderr), (0, b''))
                self.assertEqual((identified.returncode, identified.stderr), (0, b''))
                prefix = ('Graph input SHA-256: %s (%d bytes)\n%s\n\n' % (
                    hashlib.sha256(raw).hexdigest(), len(raw), self.MEANING)).encode('utf-8')
                self.assertEqual(identified.stdout, prefix + plain.stdout)

    def test_invalid_inputs_refuse_before_any_identity_or_report(self):
        valid = json.dumps(synthetic())
        bad_class = synthetic()
        bad_class['nodes']['math.top']['classification'] = 'CLOSED'
        cycle = synthetic()
        cycle['edges'].append({'from': 'math.leaf', 'to': 'math.top',
                               'required': True, 'relation': 'uses'})
        cases = [(b'{"schema_version":1,' + valid[1:].encode(), b'duplicate JSON key'),
                 (valid.replace('"SYNTHETIC"', 'NaN').encode(), b'non-finite JSON constant'),
                 (valid.replace('"SYNTHETIC"', 'Infinity').encode(), b'non-finite JSON constant'),
                 (json.dumps(bad_class).encode(), b'unknown node classification'),
                 (json.dumps(cycle).encode(), b'required dependency cycle'),
                 (b'{not-json', b'JSONDecodeError'),
                 (b'\xff', b'UnicodeDecodeError')]
        for raw, diagnostic in cases:
            for output in ((), ('--json',)):
                with self.subTest(diagnostic=diagnostic, output=output):
                    result = self.invoke(raw, '--input-identity', *output)
                    self.assertEqual((result.returncode, result.stdout), (1, b''))
                    self.assertIn(diagnostic, result.stderr)
                    self.assertNotIn(b'unrecognized arguments', result.stderr)

    def test_unknown_node_and_missing_path_emit_no_partial_identity(self):
        raw = json.dumps(synthetic()).encode()
        for output in ((), ('--json',)):
            result = self.invoke(raw, '--input-identity', '--node', 'math.mid',
                                 '--node', 'math.absent', *output)
            self.assertEqual((result.returncode, result.stdout), (1, b''))
            self.assertIn(b'unknown node: math.absent', result.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            missing = pathlib.Path(tmp) / 'absent.json'
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                try:
                    ep.main(['--graph', str(missing), '--input-identity', '--json'])
                except FileNotFoundError:
                    pass
                except SystemExit as exc:
                    self.fail('input identity CLI unavailable: %s' % exc)
                else:
                    self.fail('missing graph unexpectedly accepted')
            self.assertEqual(out.getvalue(), '')

    def test_identity_and_report_use_one_read_despite_backing_path_change(self):
        from unittest import mock
        first = synthetic()
        first['object'] = 'FIRST-CONSUMED'
        later = synthetic()
        later['object'] = 'LATER-PATH-CONTENT'
        raw = json.dumps(first).encode()
        replacement = json.dumps(later).encode()
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'graph.json'
            path.write_bytes(raw)
            original = pathlib.Path.read_bytes
            calls = []

            def capture_then_change(p):
                data = original(p)
                if p == path:
                    calls.append(p)
                    # The parser and hash must consume the returned bytes, not reread this path.
                    path.write_bytes(replacement)
                return data

            out, err = io.StringIO(), io.StringIO()
            with mock.patch.object(pathlib.Path, 'read_bytes', capture_then_change):
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    try:
                        code = ep.main(['--graph', str(path), '--input-identity', '--json'])
                    except SystemExit as exc:
                        self.fail('input identity CLI unavailable: %s; %s' % (exc, err.getvalue()))
            self.assertEqual(code, 0)
            self.assertEqual(err.getvalue(), '')
            self.assertEqual(calls, [path])
            data = json.loads(out.getvalue())
            self.assertEqual(data['object'], 'FIRST-CONSUMED')
            self.assertEqual(data['input_identity'], self.expected_identity(raw))
            self.assertEqual(path.read_bytes(), replacement)

    def test_no_flag_keeps_existing_loader_and_report_contract(self):
        from unittest import mock
        graph = synthetic()
        raw = json.dumps(graph).encode()
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'graph.json'
            path.write_bytes(raw)
            # No flag means no new binary acquisition path at all.
            with mock.patch.object(pathlib.Path, 'read_bytes', side_effect=AssertionError('new read without opt-in')):
                code, text = run(['--graph', str(path), '--json'])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(text), ep.report(GATE, graph, ep.roots(graph)))
            self.assertNotIn('input_identity', json.loads(text))
            self.assertEqual(path.read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
