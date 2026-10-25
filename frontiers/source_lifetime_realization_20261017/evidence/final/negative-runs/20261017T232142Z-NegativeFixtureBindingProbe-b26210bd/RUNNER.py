"""Source-bound, two-part positive acceptance after observed proof-print elision."""
from pathlib import Path
from datetime import datetime, timezone
import fcntl
import json
import os
import re
import signal
import subprocess
import time
import uuid
from run_negative import ROOT, HERE, BIN, CACHE, require, sha, now, objects, production_sources


def main():
    generation = '0b581f8569781d82'
    project = HERE / 'generations' / generation
    probe = HERE / 'instrumentation' / ('proof-binding-' + generation)
    source = probe / 'NegativeFixtureBindingProbe.lean'
    manifest = json.loads((probe / 'MANIFEST.json').read_text())
    original_path = ROOT / manifest['original_compile_receipt']
    original = json.loads(original_path.read_text())
    require(original['returncode'] == 0 and not original['timed_out'] and not original['errors'],
            'original compiler must have succeeded')
    require(not original['control_pass'], 'preserve original harness failure')
    require(all(v for k, v in original['checks'].items() if not k.startswith('local_binding:')),
            'only proof-print instrumentation may have failed')
    require(sha(source) == manifest['source_sha256'], 'probe source mismatch')
    require(sha(project / 'MANIFEST.json') == original['manifest_sha256'], 'clone manifest mismatch')
    require(sha(project / 'NegativeFixtureBaseline.lean') == original['fixture_before']['NegativeFixtureBaseline'],
            'compiled baseline source changed')
    require(sha(BIN / 'lean') == original['executable_sha256'], 'runtime mismatch')
    require(sha(CACHE / 'lake-manifest.json') == 'd63753befccc21923783a5085148e3ff028d97134ea52f5a08bd87ecf1b0b043',
            'dependency manifest mismatch')
    dependencies = []
    for dep in json.loads((CACHE / 'lake-manifest.json').read_text())['packages']:
        root = CACHE / '.lake/packages' / dep['name']
        require((root / '.git/HEAD').read_text().strip() == dep['rev'], 'dependency pin mismatch')
        path = root / '.lake/build/lib/lean'
        if path.is_dir():
            dependencies.append(path)
    with (ROOT / 'lean-slot.lock').open('a+') as lock:
        print(json.dumps({'stage': 'WAITING_FOR_C291_SERIAL_SLOT', 'module': 'NegativeFixtureBindingProbe'}), flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        before_sources = production_sources()
        before_objects = objects(ROOT / 'build')
        original_objects = objects(project / 'build')
        require(original_objects == original['own_objects_after'], 'compiled original baseline objects changed')
        require(before_sources == original['production_sources_after'], 'production sources changed')
        require(before_objects == original['production_objects_after'], 'production objects changed')
        fixture_sha = sha(source)
        original_receipt_sha = sha(original_path)
        metadata = {str(p): (p.stat().st_size, p.stat().st_mtime_ns, p.stat().st_ino)
                    for d in dependencies for p in d.rglob('*') if p.is_file()}
        paths = [str(project / 'build'), str(ROOT / 'build')] + [str(p) for p in dependencies]
        env = os.environ.copy()
        env['LEAN_PATH'] = os.pathsep.join(paths)
        env['LEAN_NUM_THREADS'] = '2'
        command = [str(BIN / 'lean'), '-j2', '-M4096', '-DwarningAsError=true', '-o',
                   str(probe / 'build/NegativeFixtureBindingProbe.olean'), str(source)]
        run = ROOT / 'negative-runs' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') +
              '-NegativeFixtureBindingProbe-' + uuid.uuid4().hex[:8])
        run.mkdir()
        (run / 'RUNNER.py').write_bytes(Path(__file__).read_bytes())
        (run / 'IMPORTED_RUNNER.py').write_bytes((HERE / 'run_negative.py').read_bytes())
        receipt = {'generation': generation, 'module': 'NegativeFixtureBindingProbe', 'command': command,
            'started_utc': now(), 'original_compile_receipt': manifest['original_compile_receipt'],
            'original_compile_receipt_sha256': original_receipt_sha,
            'original_compile_returncode': original['returncode'], 'original_control_pass': original['control_pass'],
            'original_baseline_source_sha256': original['fixture_before']['NegativeFixtureBaseline'],
            'original_baseline_objects': original_objects, 'original_manifest_sha256': original['manifest_sha256'],
            'probe_source_sha256': fixture_sha, 'probe_manifest_sha256': sha(probe / 'MANIFEST.json'),
            'production_sources_before': before_sources, 'production_objects_before': before_objects,
            'runner_sha256': sha(Path(__file__)), 'imported_runner_sha256': sha(HERE / 'run_negative.py'),
            'executable_sha256': sha(BIN / 'lean'), 'lean_path': paths, 'timeout_seconds': 240,
            'scientific_effect': 'NONE',
            'scope': 'Two-part positive acceptance: unchanged exact clone compilation plus proof-reference observation; original harness failure preserved'}
        start = time.monotonic()
        with (run / 'stdout.txt').open('wb') as out, (run / 'stderr.txt').open('wb') as err:
            child = subprocess.Popen(command, cwd=probe, env=env, stdout=out, stderr=err, start_new_session=True)
            receipt['child_pid'] = child.pid
            (run / 'START.json').write_text(json.dumps(receipt, indent=2) + '\n')
            print(json.dumps({'stage': 'RUNNING', 'child_pid': child.pid, 'run': str(run)}), flush=True)
            timed_out = False
            try:
                code = child.wait(timeout=240)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    code = child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    code = child.wait()
        output = (run / 'stdout.txt').read_text()
        checks = {'compiler_success': code == 0, 'not_timed_out': not timed_out,
            'stderr_empty': (run / 'stderr.txt').read_bytes() == b'',
            'no_errors': not bool(re.search(r'\.lean:\d+:\d+: error', output)),
            'original_receipt_unchanged': sha(original_path) == original_receipt_sha,
            'original_objects_unchanged': objects(project / 'build') == original_objects,
            'probe_unchanged': sha(source) == fixture_sha,
            'production_sources_unchanged': production_sources() == before_sources,
            'production_objects_unchanged': objects(ROOT / 'build') == before_objects,
            'dependency_metadata_unchanged': all(Path(p).is_file() and
                (Path(p).stat().st_size, Path(p).stat().st_mtime_ns, Path(p).stat().st_ino) == stat
                for p, stat in metadata.items())}
        for reference in manifest['required_references']:
            checks['local_binding:' + reference] = reference in output
        passed = all(checks.values())
        receipt.update(returncode=code, timed_out=timed_out, ended_utc=now(), seconds=time.monotonic()-start,
            checks=checks, control_pass=passed, stdout_sha256=sha(run / 'stdout.txt'), stderr_sha256=sha(run / 'stderr.txt'),
            output_objects=objects(probe / 'build'))
        (run / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps({'stage': 'FINISHED', 'returncode': code, 'timed_out': timed_out,
            'control_pass': passed, 'seconds': receipt['seconds'], 'run': str(run),
            'failed_checks': [k for k, v in checks.items() if not v]}), flush=True)
        return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
