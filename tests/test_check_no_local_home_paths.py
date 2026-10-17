import json, pathlib, subprocess, sys, tempfile, unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check_no_local_home_paths as chk

S = '/'
MAC_HOME = S + 'Us' + 'ers' + S + 'synthetic' + 'user'
LIN_HOME = S + 'ho' + 'me' + S + 'synthetic' + 'user'
WIN_HOME = 'C:' + '\\' + 'Us' + 'ers' + '\\' + 'synthetic' + 'user'
RUN_HOME = S + 'ho' + 'me' + S + 'run' + 'ner' + S + 'work'
ROOT_SCRATCH = S + 'root' + S + 'scratch_dir'


def repo(files, allow=None):
    d = tempfile.TemporaryDirectory()
    r = pathlib.Path(d.name)
    subprocess.run(['git', 'init', '-q', str(r)], check=True)
    for k, v in files.items():
        (r / k).parent.mkdir(parents=True, exist_ok=True)
        (r / k).write_text(v, encoding='utf-8')
    if allow is not None:
        (r / 'docs/custody').mkdir(parents=True, exist_ok=True)
        (r / chk.MAP).write_text(json.dumps({'schema': 'local-path-map/v1', 'files': allow}))
    subprocess.run(['git', '-C', str(r), 'add', '-A'], check=True)
    return d, r


class NegativeControls(unittest.TestCase):
    def test_each_synthetic_home_fails(self):
        for home in (MAC_HOME, LIN_HOME, WIN_HOME, WIN_HOME.replace('\\', '/')):
            d, r = repo({'a.md': 'ran ' + home + '/venv/bin/python\n'})
            with d:
                self.assertEqual(len(chk.scan(r)), 1, home)

    def test_runner_and_root_scratch_pass(self):
        d, r = repo({'a.log': RUN_HOME + '\n' + ROOT_SCRATCH + '\n'})
        with d:
            self.assertEqual(chk.scan(r), [])

    def test_allowlisted_unchanged_passes_and_changed_fails(self):
        body = 'x ' + MAC_HOME + '/p\n'
        d, r = repo({'e.json': body})
        with d:
            b = chk.blob(body.encode())
            (r / 'docs/custody').mkdir(parents=True)
            (r / chk.MAP).write_text(json.dumps({'schema': 'local-path-map/v1', 'files': [{'path': 'e.json', 'git_blob': b}]}))
            subprocess.run(['git', '-C', str(r), 'add', '-A'], check=True)
            self.assertEqual(chk.scan(r), [])
            (r / 'e.json').write_text(body + 'y ' + LIN_HOME + '/q\n')
            self.assertEqual(len(chk.scan(r)), 2)

    def test_cli_exit_code(self):
        d, r = repo({'a.txt': MAC_HOME + '\n'})
        with d:
            p = subprocess.run([sys.executable, str(ROOT / 'tools/check_no_local_home_paths.py'), str(r)], capture_output=True)
            self.assertEqual(p.returncode, 1)

    def test_own_sources_have_no_literal_home_path(self):
        for f in ('tools/check_no_local_home_paths.py', 'tests/test_check_no_local_home_paths.py', '.github/workflows/no-local-home-paths.yml', chk.MAP):
            p = ROOT / f
            if p.exists():
                self.assertFalse(chk.PATTERN.search(p.read_text(encoding='utf-8')), f)


class PositiveControl(unittest.TestCase):
    def test_current_tree_passes(self):
        self.assertEqual(chk.scan(ROOT), [])


if __name__ == '__main__':
    unittest.main()
