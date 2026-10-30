"""Source-bound exact finite MomentTail observations (Python 3.9+, stdlib).

Public API: evaluate_case, generate_cases, run_campaign. See CONTRACT.json
for schemas, examples, CLI exits and the explicit unsupported scope.
Observations are falsification evidence, never a universal proof or admission.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import re
import sys
import time

TARGET = 'ResearchFormalCoreR1.p02_lm009_moment40_tail'
REFERENCE_COMMIT = '19a55750451b8016b50d1d20be6a18c021807ecb'
REFERENCE_TREE = '0e28d1077fffb77e66ff635a112899ccb091b3ba'
SOURCE_HASHES = {
    'formal/ResearchFormalCoreR1/MomentTail.lean': '87fe3ee90afc52d8c2652881f1ae195d1b0b15a2ffc18c84d6166d1a4d0de2aa',
    'formal/tests/test_moment_tail.py': 'd50c46220ff6c4b95ee1cb42b037738740d314508019161ad6fb478ed3b0f7d5',
}
SOURCE_FILES = tuple(SOURCE_HASHES)
DEFAULT_ROOT = Path(__file__).resolve().parents[2]
_FIELDS = {'target', 'p', 'R', 'r', 'epsilon', 'M'}
_RATIONAL = re.compile(r'-?[0-9]+(?:/[1-9][0-9]*)?\Z', re.ASCII)


def _number(value):
    if type(value) is int or isinstance(value, F):
        return F(value)
    if isinstance(value, str) and _RATIONAL.fullmatch(value):
        return F(value)
    raise ValueError('numeric values must be integers, Fraction, or integer/rational strings')


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def _identity(value):
    return hashlib.sha256(_json(value).encode('ascii')).hexdigest()


def verify_sources(source_root=None):
    """Hash actual source bytes; a reference commit label alone is insufficient.

    This verifies the two scoped source files, not the entire Git tree, imports,
    Lean build, live deployment, or ancestry of an enclosing repository.
    """
    root = Path(source_root) if source_root is not None else DEFAULT_ROOT
    records = {}
    for path, expected in SOURCE_HASHES.items():
        try:
            data = (root / path).read_bytes()
            actual = hashlib.sha256(data).hexdigest()
            records[path] = {'expected_sha256': expected, 'actual_sha256': actual,
                             'bytes': len(data), 'matches': actual == expected}
        except OSError as exc:
            records[path] = {'expected_sha256': expected, 'actual_sha256': None,
                             'bytes': None, 'matches': False, 'error': type(exc).__name__}
    return {'status': 'VERIFIED' if all(r['matches'] for r in records.values()) else 'MISMATCH',
            'reference_commit': REFERENCE_COMMIT, 'reference_tree': REFERENCE_TREE,
            'scope': 'TWO_EXACT_SOURCE_FILES_ONLY', 'files': records}


def _evaluate(case, binding):
    if binding['status'] != 'VERIFIED':
        return {'status': 'SOURCE_MISMATCH', 'reason': 'required source bytes do not match',
                'source_binding': binding}
    if not isinstance(case, dict) or set(case) != _FIELDS:
        return {'status': 'INVALID', 'reason': 'case must contain exactly target,p,R,r,epsilon,M'}
    if not isinstance(case['target'], str):
        return {'status': 'INVALID', 'reason': 'target must be a string'}
    if case['target'] != TARGET:
        return {'status': 'UNSUPPORTED', 'reason': 'only the exact finite moment40_tail target is supported',
                'target': case['target']}
    try:
        if not isinstance(case['p'], (list, tuple)) or not isinstance(case['R'], (list, tuple)):
            raise ValueError('p and R must be nonempty equal-length lists or tuples')
        if not case['p'] or len(case['p']) != len(case['R']):
            raise ValueError('p and R must be nonempty and have equal length')
        p = [_number(x) for x in case['p']]
        values = [_number(x) for x in case['R']]
        r, epsilon, M = [_number(case[key]) for key in ('r', 'epsilon', 'M')]
        if any(w < 0 for w in p) or sum(p, F(0)) != 1:
            raise ValueError('probability masses must be nonnegative and sum exactly to one')
        if r <= 0 or epsilon <= 0 or M < 0:
            raise ValueError('r and epsilon must be positive; M must be nonnegative')
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        return {'status': 'INVALID', 'reason': str(exc)}
    normalized = dict(target=TARGET, p=[str(x) for x in p], R=[str(x) for x in values],
                      r=str(r), epsilon=str(epsilon), M=str(M))
    result = {'case': normalized, 'case_id': _identity(normalized), 'target': TARGET}
    moment = sum((weight * value ** 40 for weight, value in zip(p, values)), F(0))
    result['moment40'] = str(moment)
    if M < moment:
        return dict(result, status='FALSE_PREMISE', reason='supplied M is below the actual fortieth moment')
    event = [epsilon < r * value ** 5 for value in values]
    mass = sum((weight for weight, inside in zip(p, event) if inside), F(0))
    bound = (M / epsilon ** 8) * r ** 8
    result.update(status='OBSERVED_BOUND' if mass <= bound else 'COUNTEREXAMPLE',
                  event=event, event_mass=str(mass), bound=str(bound),
                  slack=str(bound - mass))
    return result


def evaluate_case(case, *, source_root=None):
    """Validate and observe one finite law; return a JSON-serializable result.

    Source mismatch, invalid domains, false premises and unsupported targets
    have distinct non-success statuses. No assert statement enforces a premise.
    """
    binding = verify_sources(source_root)
    result = _evaluate(case, binding)
    result['source_binding'] = binding
    return result


def _make_case(p, values, r, epsilon, slack=F(0)):
    moment = sum((w * x ** 40 for w, x in zip(p, values)), F(0))
    return dict(target=TARGET, p=[str(w) for w in p], R=[str(x) for x in values],
                r=str(r), epsilon=str(epsilon), M=str(moment + slack))


def generate_cases(*, seed=20261030, count=10019):
    """Yield exactly count distinct valid cases; deterministic integer sampling.

    A fixed adversarial prefix precedes boundary-biased seeded finite laws.
    Canonical rational identities deduplicate the actual observations.
    """
    if type(seed) is not int or type(count) is not int or count <= 0:
        raise ValueError('seed must be an integer and count a positive integer')
    pathological = [
        _make_case([F(1)], [F(1)], F(1,2), F(1,4)),
        _make_case([F(1)], [F(2)], F(1,16), F(1)),
        _make_case([F(1)], [F(2)], F(1), F(16)),
        _make_case([F(1,2),F(1,2)], [F(1),F(-1)], F(1), F(1)),
        _make_case([F(1)], [F(0)], F(1), F(1)),
        _make_case([F(0),F(1)], [F(10**20),F(0)], F(7), F(1)),
        _make_case([F(1)], [F(-10**20)], F(13), F(1)),
        _make_case([F(1)], [F(1)], F(17), F(1)),
        _make_case([F(1)], [F(1)], F(1), F(10**30-1,10**30)),
        _make_case([F(1)], [F(1)], F(1), F(10**30+1,10**30)),
        _make_case([F(1)], [F(1,10**20)], F(10**30), F(1,10**80)),
        _make_case([F(1)], [F(10**20)], F(1,10**30), F(10**60)),
        _make_case([F(1)], [F(1)], F(2), F(1), F(10**30)),
    ]
    rng, seen, emitted = random.Random(seed), set(), 0
    for item in pathological:
        if emitted == count:
            return
        seen.add(_identity(item)); emitted += 1
        yield item
    while emitted < count:
        n = rng.randint(1, 5)
        weights = [rng.randint(0, 20) for _ in range(n)]
        if not sum(weights):
            weights[0] = 1
        p = [F(w, sum(weights)) for w in weights]
        values = [F(rng.randint(-30, 30), rng.randint(1, 15)) for _ in range(n)]
        r = F(rng.randint(1, 50), rng.randint(1, 50))
        positive = [x for x in values if x > 0]
        mode = emitted % 5
        if positive and mode < 3:
            threshold = r * rng.choice(positive)**5
            offset = F(1, 10**rng.randint(2, 20))
            epsilon = threshold * (1 + (mode - 1) * offset)
        else:
            epsilon = F(rng.randint(1, 100), rng.randint(1, 100))
        slack = F(rng.randint(0, 20), rng.randint(1, 20)) if emitted % 3 == 0 else F(0)
        item = _make_case(p, values, r, epsilon, slack)
        identity = _identity(item)
        if identity not in seen:
            seen.add(identity); emitted += 1
            yield item


def run_campaign(*, cases=None, seed=20261030, count=10019, source_root=None):
    """Observe supplied list/tuple cases or a generated distinct population.

    Any refused case prevents BOUNDED_OBSERVATIONS. Repeated valid cases earn
    observation counts but only one distinct identity. Empty runs always refuse.
    """
    binding = verify_sources(source_root)
    counts = dict(attempted=0, valid=0, invalid=0, false_premise=0,
                  unsupported=0, source_mismatch=0, counterexamples=0, distinct_valid=0)
    report = dict(schema='finite-moment-tail-campaign/v1', target=TARGET,
                  status='REFUSED', source_binding=binding, counts=counts,
                  population='generated' if cases is None else 'supplied',
                  seed=seed if cases is None and type(seed) is int else None,
                  cases_digest=hashlib.sha256(b'').hexdigest(), witnesses=[],
                  full_federation_admitted=False, scientific_effect='NONE',
                  scope='FINITE_RATIONAL_OBSERVATIONS_ONLY')
    if binding['status'] != 'VERIFIED':
        report['reason'] = 'source binding failed before campaign execution'
        return report
    if cases is None:
        if type(seed) is not int or type(count) is not int or count <= 0:
            report['reason'] = 'seed must be an integer and count a positive integer'
            return report
        population = generate_cases(seed=seed, count=count)
    elif isinstance(cases, (list, tuple)):
        population = cases
    else:
        report['reason'] = 'supplied cases must be a list or tuple'
        return report
    seen, digest = set(), hashlib.sha256()
    status_keys = {'INVALID':'invalid', 'FALSE_PREMISE':'false_premise',
                   'UNSUPPORTED':'unsupported', 'SOURCE_MISMATCH':'source_mismatch'}
    for item in population:
        counts['attempted'] += 1
        result = _evaluate(item, binding)
        status = result['status']
        if status in ('OBSERVED_BOUND', 'COUNTEREXAMPLE'):
            counts['valid'] += 1
            seen.add(result['case_id'])
            digest.update((result['case_id'] + '\n').encode('ascii'))
            if status == 'COUNTEREXAMPLE':
                counts['counterexamples'] += 1
                report['witnesses'].append(dict(index=counts['attempted']-1, result=result))
        else:
            counts[status_keys[status]] += 1
            report['witnesses'].append(dict(index=counts['attempted']-1, result=result))
    counts['distinct_valid'] = len(seen)
    report['cases_digest'] = digest.hexdigest()
    rejected = sum(counts[k] for k in status_keys.values())
    if counts['counterexamples']:
        report['status'] = 'COUNTEREXAMPLE'
    elif counts['valid'] and not rejected:
        report['status'] = 'BOUNDED_OBSERVATIONS'
    else:
        report['reason'] = 'empty population or refused cases; no successful campaign classification'
    return report


def _strict_load(stream):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON object key: ' + key)
            result[key] = value
        return result
    def reject_constant(value):
        raise ValueError('nonfinite JSON number: ' + value)
    return json.load(stream, object_pairs_hook=pairs, parse_constant=reject_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=DEFAULT_ROOT,
                        help='root containing the exact two required formal source files')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('evaluate', help='read one strict JSON case from stdin')
    campaign = sub.add_parser('campaign', help='generate observations or read a JSON array')
    campaign.add_argument('--seed', type=int, default=20261030)
    campaign.add_argument('--count', type=int, default=10019)
    campaign.add_argument('--stdin-cases', action='store_true')
    args = parser.parse_args(argv)
    start = time.perf_counter()
    try:
        if args.command == 'evaluate':
            report = evaluate_case(_strict_load(sys.stdin), source_root=args.source_root)
        else:
            cases = _strict_load(sys.stdin) if args.stdin_cases else None
            # JSON null must not silently select the generated population.
            if args.stdin_cases and not isinstance(cases, list):
                raise ValueError('--stdin-cases requires a JSON array')
            report = run_campaign(cases=cases, seed=args.seed, count=args.count, source_root=args.source_root)
    except (ValueError, TypeError) as exc:
        report = dict(status='INVALID', reason=str(exc))
    report['execution'] = dict(argv=list(sys.argv if argv is None else argv),
                              python=sys.version, optimization=sys.flags.optimize,
                              elapsed_seconds=time.perf_counter()-start)
    print(json.dumps(report, sort_keys=True, indent=2))
    if report['status'] in ('OBSERVED_BOUND', 'BOUNDED_OBSERVATIONS'):
        return 0
    return 1 if report['status'] == 'COUNTEREXAMPLE' else 2


if __name__ == '__main__':
    sys.exit(main())
