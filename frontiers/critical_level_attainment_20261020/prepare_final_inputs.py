"""C294 seven-source freeze and metadata-delta reuse; run only on root's frozen inputs."""
import fcntl, hashlib, json, shutil, sys, uuid
from run_final_phase import ROOT, PROJECT, BUILD, C291, MODULES, NEW, BASE_SHA, require, now, sha, stamp, write, runtime, dependencies


def main():
    require(sys.argv[1:] == ['--freeze'], 'usage: prepare_final_inputs.py --freeze (root-authorized freeze only)')
    with (ROOT / 'lean-slot.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        require(not PROJECT.exists() and not BUILD.exists(), 'final directories already exist')
        require(not (ROOT / 'FINAL_SOURCE_INVENTORY.json').exists(), 'final inventory exists')
        attempts = ROOT / 'final-prepare-attempts'; attempts.mkdir(exist_ok=True)
        require(not attempts.is_symlink(), 'unsafe preparation record directory')
        legacy = ROOT / 'FINAL_PREPARE_START.json'
        prior = {'path': str(legacy), 'sha256': sha(legacy)} if legacy.is_file() else None
        start_record = attempts / (now().replace(':', '').replace('+', '_') + '-' + uuid.uuid4().hex + '.json')
        write(start_record, {'started_utc': now(), 'prior_legacy_start': prior,
              'status': 'STARTED; missing final inventory means interrupted preparation; no overwrite/retry cleanup'})
        sources, imports = [], {}
        for m in MODULES:
            p = ROOT / 'project' / (m + '.lean'); before = stamp(p); digest = sha(p)
            require(stamp(p) == before, 'source changed during hash')
            sources.append({'name': p.name, 'sha256': digest, 'bytes': before[0]})
            imports[m] = [n for line in p.read_text().splitlines() if line.startswith('import ')
                          for n in line[7:].split() if n in MODULES]
        order, pending = [], list(MODULES)
        while pending:
            available = [m for m in pending if set(imports[m]) <= set(order)]
            require(available, 'local import cycle')
            for m in available:
                order.append(m); pending.remove(m)
        original = C291 / 'FINAL_DEPENDENCY_ARTIFACTS.json'
        original_raw = original.read_bytes()
        require(hashlib.sha256(original_raw).hexdigest() == BASE_SHA, 'C291 dependency inventory bytes changed')
        baseline = json.loads(original_raw); roots, _ = runtime()
        require(roots == baseline['roots'], 'dependency roots differ from C291')
        checked, delta = dependencies(baseline)
        checked.update(c291_inventory_sha256=BASE_SHA, checked_utc=now(), reuse_delta=delta)
        dep_path = ROOT / 'FINAL_DEPENDENCY_ARTIFACTS.json'; write(dep_path, checked)
        PROJECT.mkdir(); BUILD.mkdir()
        for item in sources:
            src = ROOT / 'project' / item['name']
            require(sha(src) == item['sha256'], 'source changed during freeze')
            shutil.copyfile(src, PROJECT / item['name'])
            require(sha(PROJECT / item['name']) == item['sha256'], 'source copy mismatch')
        inv = {'frozen_utc': now(), 'prepare_start_record': str(start_record),
               'prepare_start_sha256': sha(start_record), 'prior_legacy_start': prior, 'sources': sources, 'build_order': order, 'local_imports': imports,
               'new_modules': NEW, 'runner_sha256': sha(ROOT / 'run_final_phase.py'),
               'preparer_sha256': sha(ROOT / 'prepare_final_inputs.py'),
               'dependency_artifact_inventory_sha256': sha(dep_path), 'c291_inventory_sha256': BASE_SHA,
               'scientific_effect': 'NONE', 'execution_provenance': 'LOCAL; no hosted qualification'}
        write(ROOT / 'evidence/FINAL_BUILD_INITIALIZATION.json', {'utc': now(), 'initial_objects': [],
              'build_was_created_empty': not any(BUILD.iterdir()), 'dependency_reuse': delta,
              'prepare_start_record': str(start_record), 'prepare_start_sha256': sha(start_record)})
        write(ROOT / 'FINAL_SOURCE_INVENTORY.json', inv)
        print(json.dumps({'stage': 'FROZEN', 'modules': order, 'dependency_reuse': delta}), flush=True)


if __name__ == '__main__':
    main()
