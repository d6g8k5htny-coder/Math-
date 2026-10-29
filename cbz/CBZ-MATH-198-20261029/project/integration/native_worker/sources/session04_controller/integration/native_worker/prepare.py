"""Generate exact source-exposed trusted task wrappers and copied native baseline."""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
AUDIT = ROOT/'integration/engine_audit'
sys.path.insert(0, str(AUDIT))
import catalog
BASELINE = Path('/workspace/scratch/universal-law-certified-frontier-v2/engine')


def generate(project=ROOT, native=HERE, baseline=BASELINE):
    entries = catalog.verify_catalog(project=project)['endpoints']
    lines = ['import Completion.FinalAudit', '',
             '/- Source-exposed reuse of the49 original P15 packet targets.',
             '   These wrappers supply no discovery or training credit. -/',
             'namespace ClosedProof.Endpoints', '']
    tasks = []
    for e in entries:
        short = e['target'].rsplit('.', 1)[1]
        generic = '{X : Type}' in e['statement']
        target = (f'∀ (X : Type) [Fintype X] [DecidableEq X] '
                  f'(F : UniversalLaw.Spec.P15.RealizedData X), {e["target"]} F') if generic else e['target']
        lines += [f'def {short} : Prop := {target}', '',
                  f'theorem reuse_{short} : {short} := by']
        lines += ['  intro X _ _ F', f'  exact {e["theorem"]} F'] if generic else [f'  exact {e["theorem"]}']
        lines.append('')
        tasks.append({'id':'p15.'+short, 'action':'reuse_'+short,
                      'task_constant':'ClosedProof.Endpoints.'+short,
                      'wrapper':'ClosedProof.Endpoints.reuse_'+short,
                      'original_target':e['target'], 'original_theorem':e['theorem'],
                      'generic':generic, 'training_eligible':False, 'source_exposed':True})
    lines += ['end ClosedProof.Endpoints', '']
    formal = Path(project)/'formal/Integration/EndpointTasks.lean'
    formal.write_text('\n'.join(lines))
    lean = Path(native)/'lean'
    lean.mkdir(exist_ok=False)
    pins = {}
    for name in ['TrustedTasks.lean','ClosedProofCore.lean','ExprCodec.lean','ExprDag.lean',
                 'ClosedProofWorker.lean','WorkerBootstrap.lean']:
        data = (baseline/'lean'/name).read_bytes()
        (lean/name).write_bytes(data)
        pins[name] = hashlib.sha256(data).hexdigest()
    (lean/'Integration').mkdir()
    (lean/'Integration/EndpointTasks.lean').write_bytes(formal.read_bytes())
    trusted = lean/'TrustedTasks.lean'
    trusted.write_text('import Integration.EndpointTasks\n'+trusted.read_text())
    worker = lean/'ClosedProofWorker.lean'
    source = worker.read_text()
    task_array = ', '.join(json.dumps(t['id']) for t in tasks)
    action_array = ', '.join(json.dumps(t['action']) for t in tasks)
    source = source.replace('def taskIds : Array String :=',
                            f'def endpointTaskIds : Array String := #[{task_array}]\n'
                            'def taskIds : Array String :=',1)
    source = source.replace('"p15_log_bound"]', '"p15_log_bound"] ++ endpointTaskIds',1)
    source = source.replace('"p15_log_known"]', f'"p15_log_known"] ++ #[{action_array}]',1)
    source = source.replace('  | _ => none', '\n'.join(
        f'  | "{t["id"]}" => some (mkConst ``{t["task_constant"]})' for t in tasks)+'\n  | _ => none',1)
    source = source.replace('    | _ => throwError "unknown action"', '\n'.join(
        f'    | "{t["action"]}" => `(tactic| exact {t["wrapper"]})' for t in tasks)+
        '\n    | _ => throwError "unknown action"',1)
    source = source.replace('("max_states", toJson (64 : Nat)),',
                            '("max_states", toJson (64 : Nat)), '
                            '("source_exposed_tasks", toJson endpointTaskIds), '
                            '("training_eligible", toJson false),',1)
    worker.write_text(source)
    mapping={'schema':'ul-native-endpoint-tasks-v1','tasks':tasks,
             'formal_source':'formal/Integration/EndpointTasks.lean',
             'formal_source_sha256':hashlib.sha256(formal.read_bytes()).hexdigest(),
             'baseline_lean_source_sha256':pins,
             'scope':'Fixed source-exposed wrapper reuse; no discovery or training eligibility.'}
    (Path(native)/'endpoint_tasks.json').write_text(json.dumps(mapping,indent=2)+'\n')
    return mapping


if __name__ == '__main__':
    value=generate()
    print(json.dumps({'tasks':len(value['tasks']), 'formal_source_sha256':value['formal_source_sha256']}))
