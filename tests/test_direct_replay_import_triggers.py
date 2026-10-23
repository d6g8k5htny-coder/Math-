"""Two bare-helper import trigger contracts; stdlib-only, synthetic import probes.

This checks the deliberately restricted current YAML layout, not GitHub's
scheduler. No scientific checker is executed by the synthetic import probes.
"""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tests/test_direct_replay_import_triggers.py'
SPECS = (
    ('c6-cluster-coefficients-numerics.yml', 'c6_coefficient_numerics_replay',
     'frontiers/c6_cluster_coefficients_numerics_20260930/**',
     'tests/test_c6_coefficient_numerics_workflow.py'),
    ('remainder-rate.yml', 'remainder_rate_replay',
     'frontiers/remainder_rate_20260930/**', 'tests/test_remainder_rate_workflow.py'),
)


def positive_paths(text):
    """Only this flat positive list, with literal paths or terminal /**."""
    prefix = '  pull_request:\n    paths:\n'
    if text.count(prefix) != 1:
        raise ValueError('expected one pull-request path list')
    tail = text.split(prefix, 1)[1]
    if '  workflow_dispatch:\n' not in tail:
        raise ValueError('missing path-list boundary')
    block = tail.split('  workflow_dispatch:\n', 1)[0]
    paths = []
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match = re.fullmatch(r"      - '([A-Za-z0-9_./-]+(?:/\*\*)?)'", line)
        if not match:
            raise ValueError('unsupported path-list syntax')
        path = match.group(1)
        literal = path[:-3] if path.endswith('/**') else path
        if any(part in ('', '.', '..') for part in literal.split('/')):
            raise ValueError('noncanonical path')
        paths.append(path)
    if not paths or len(paths) != len(set(paths)):
        raise ValueError('empty or duplicate path list')
    return paths


def covered(paths, changed):
    return any(changed.startswith(p[:-2]) if p.endswith('/**') else changed == p
               for p in paths)


def source(name):
    return (ROOT / '.github/workflows' / name).read_text()


class DirectReplayImportTriggers(unittest.TestCase):
    def test_same_name_package_and_descendants_trigger(self):
        for name, module, _, _ in SPECS:
            paths = positive_paths(source(name))
            for relative in ('__init__.py', 'nested/data.py'):
                with self.subTest(workflow=name, relative=relative):
                    self.assertTrue(covered(paths, 'tools/' + module + '/' + relative))

    def test_regression_file_triggers_both_workflows(self):
        for name, *_ in SPECS:
            with self.subTest(workflow=name):
                self.assertTrue(covered(positive_paths(source(name)), SELF))

    def test_both_modes_are_wired_before_existing_contract_suite(self):
        for name, _, _, old_test in SPECS:
            text = source(name)
            for flags in ('-B -S', '-B -O -S'):
                command = '          python ' + flags + ' ' + SELF + '\n'
                with self.subTest(workflow=name, flags=flags):
                    self.assertEqual(text.count(command), 1)
                    self.assertLess(text.index(command), text.index(' -p ' + Path(old_test).name))

    def test_original_paths_and_unrelated_negatives(self):
        for name, module, packet, old_test in SPECS:
            paths = positive_paths(source(name))
            for expected in (packet, '.github/workflows/' + name, 'tools/' + module + '.py', old_test):
                with self.subTest(workflow=name, preserved=expected):
                    self.assertIn(expected, paths)
            for unrelated in ('tools.py', 'docs/README.md', 'other/tools/' + module + '/__init__.py'):
                with self.subTest(workflow=name, unrelated=unrelated):
                    self.assertFalse(covered(paths, unrelated))

    def test_list_reader_rejects_unsupported_syntax(self):
        template = "  pull_request:\n    paths:\n%s\n  workflow_dispatch:\n"
        for row in ("      - '!tools/**'", "      - 'tools/*.py'", "      - '../escape'",
                    "      - '/tools/file.py'", "      - 'tools/**' # suffix",
                    "      - 'tools/**'\n      - 'tools/**'", '      paths-ignore: []'):
            with self.subTest(row=row), self.assertRaises(ValueError):
                positive_paths(template % row)
        self.assertEqual(positive_paths(template % "      # note\n      - 'tools/**'"), ['tools/**'])

    def test_real_bare_import_selects_shadow_package_not_tools_package(self):
        for name, module, _, _ in SPECS:
            text = source(name)
            lines = text.splitlines()
            start = "          sys.path.insert(0, str(pathlib.Path('tools').resolve()))"
            self.assertEqual(lines.count(start), 1)
            index = lines.index(start)
            self.assertEqual(lines[index + 1], '          from ' + module + ' import replay')
            snippet = '\n'.join(line[10:] for line in lines[index:index + 2])
            for optimized in (False, True):
                for variant in ('module', 'shadow-package', 'namespace-directory', 'tools-init', 'root-tools'):
                    with self.subTest(workflow=name, optimized=optimized, variant=variant):
                        with tempfile.TemporaryDirectory() as directory:
                            root = Path(directory); tools = root / 'tools'; tools.mkdir()
                            module_body = "def replay():\n    return 'MODULE'\n"
                            (tools / (module + '.py')).write_text(module_body)
                            if variant in ('shadow-package', 'namespace-directory'):
                                (tools / module).mkdir()
                            if variant == 'shadow-package':
                                (tools / module / '__init__.py').write_text(
                                    "from pathlib import Path\nPath('package.marker').write_text('loaded')\n"
                                    "def replay():\n    return 'PACKAGE'\n")
                            if variant == 'tools-init':
                                (tools / '__init__.py').write_text("raise RuntimeError('tools initializer executed')\n")
                            if variant == 'root-tools':
                                (root / 'tools.py').write_text("raise RuntimeError('root tools executed')\n")
                            code = 'import pathlib, sys\n' + snippet + '\nprint(replay())\n'
                            argv = [sys.executable, '-B'] + (['-O'] if optimized else []) + ['-S', '-c', code]
                            result = subprocess.run(argv, cwd=root, capture_output=True, timeout=10)
                            self.assertEqual(result.returncode, 0, repr(result.stderr))
                            self.assertEqual(result.stderr, b'')
                            self.assertEqual(result.stdout, b'PACKAGE\n' if variant == 'shadow-package' else b'MODULE\n')
                            self.assertEqual((root / 'package.marker').exists(), variant == 'shadow-package')
                            self.assertEqual((tools / (module + '.py')).read_text(), module_body)


if __name__ == '__main__':
    unittest.main()
