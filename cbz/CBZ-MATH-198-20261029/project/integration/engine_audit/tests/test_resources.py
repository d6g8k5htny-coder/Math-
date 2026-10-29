"""Protocol-faithful capacity regressions; these do not prove or time Lean work."""
import unittest
from ul_engine.search import CheckpointSearch


class BoundedWorker:
    session = 'bounded-protocol'
    def __init__(self, *, length=127, capacity=64, request_limit=256, branching=False):
        self.ready = {'tasks': ['chain'], 'actions': ['advance', 'branch'], 'max_states': capacity}
        self.length, self.capacity = length, capacity
        self.request_limit, self.branching = request_limit, branching
        self.requests, self.live, self.calls = 0, set(), []
        self.next_state, self.peak_live = 1, 0
        self.transport_failed = False
    @property
    def active_state_count(self): return len(self.live)
    @property
    def remaining_requests(self): return self.request_limit - self.requests
    def request(self, op, **payload):
        if self.requests >= self.request_limit:
            self.transport_failed = True
            raise RuntimeError('worker fixed request limit exceeded')
        self.requests += 1
        self.calls.append((op, payload))
        if op == 'open':
            if len(self.live) >= self.capacity: return {'ok': False, 'status': 'rejected'}
            self.live.add(0)
            self.peak_live = max(self.peak_live, len(self.live))
            return {'ok': True, 'status': 'opened', 'state': 0, 'goals': ['P']}
        if op == 'drop':
            self.live.remove(payload['state'])
            return {'ok': True, 'status': 'dropped'}
        if op == 'verify': return {'ok': True, 'status': 'accepted'}
        if op == 'attempt':
            state = payload['state']
            if state not in self.live: raise ValueError('stale parent')
            # Real fixed worker refuses all actions once capacity is full,
            # including any action that could otherwise close the proof.
            if len(self.live) >= self.capacity: return {'ok': False, 'status': 'rejected'}
            if not self.branching and state == self.length:
                return {'ok': True, 'status': 'closed', 'goals': [],
                        'certificate': {'schema': 'synthetic', 'length': self.length}}
            child = self.next_state
            self.next_state += 1
            self.live.add(child)
            self.peak_live = max(self.peak_live, len(self.live))
            return {'ok': True, 'status': 'progress', 'state': child, 'goals': ['P']}
        raise ValueError(op)


class ResourceTests(unittest.TestCase):
    def test_request_limit_preserves_verification_and_cleanup_capacity(self):
        # Latest old scheduler consumes request256 on a closed candidate, then
        # fails its required verify at257 and cannot clean the live checkpoint.
        worker = BoundedWorker()
        result = CheckpointSearch(worker).solve('chain', actions=['advance'], max_attempts=128)
        self.assertEqual(result['status'], 'resource_exhausted')
        self.assertEqual(result['termination_reason'], 'request_capacity')
        self.assertFalse(result['solved'])
        self.assertFalse(worker.transport_failed)
        self.assertEqual(worker.live, set())
        self.assertGreaterEqual(worker.remaining_requests, 1)  # shutdown remains possible
        self.assertLess(result['attempted_actions'], 128)

    def test_full_frontier_is_reported_without_wasting_attempts_or_eviction(self):
        # Branching fills three live slots midway through parent expansion.
        # Parents/children are preserved until the explicit final cleanup.
        worker = BoundedWorker(capacity=3, branching=True)
        result = CheckpointSearch(worker).solve('chain', actions=['advance', 'branch'], max_attempts=20)
        self.assertEqual(result['status'], 'resource_exhausted')
        self.assertEqual(result['termination_reason'], 'state_capacity')
        self.assertEqual(result['attempted_actions'], 3)
        self.assertEqual(worker.peak_live, 3)
        self.assertFalse(any(op == 'attempt' and state not in {0, 1}
                             for op, p in worker.calls for state in [p.get('state')]))
        self.assertFalse(any(e['op'] == 'attempt' and e['response'].get('status') == 'rejected'
                             for e in result['journal']))
        self.assertEqual(worker.live, set())

    def test_reclamation_keeps_long_chain_solvable_with_sufficient_requests(self):
        worker = BoundedWorker(length=80)
        result = CheckpointSearch(worker).solve('chain', actions=['advance'], max_attempts=100)
        self.assertTrue(result['solved'])
        self.assertEqual(result['path'], ['advance']*81)
        self.assertEqual(worker.peak_live, 2)
        self.assertEqual(worker.live, set())
        self.assertEqual(sum(op == 'verify' for op, _ in worker.calls), 1)

    def test_true_attempt_budget_remains_distinct(self):
        worker = BoundedWorker(length=80)
        result = CheckpointSearch(worker).solve('chain', actions=['advance'], max_attempts=1)
        self.assertEqual(result['status'], 'attempt_budget')
        self.assertEqual(result['termination_reason'], 'attempt_budget')
        self.assertEqual(result['attempted_actions'], 1)
        self.assertEqual(worker.live, set())

    def test_compatibility_frontier_exhaustion_is_explicit(self):
        class DeadEnd(BoundedWorker):
            def request(self, op, **payload):
                if op == 'attempt':
                    self.requests += 1
                    return {'ok': True, 'status': 'no_progress'}
                return super().request(op, **payload)
        result = CheckpointSearch(DeadEnd()).solve('chain', actions=['advance'])
        self.assertEqual(result['status'], 'exhausted')
        self.assertEqual(result['termination_reason'], 'frontier_exhausted')

    def test_accepted_proof_reports_unconfirmed_final_cleanup(self):
        # Acceptance remains a proof fact, while release acknowledgement is a
        # separate session resource fact. Neither may hide the other's result.
        for outcome in ({'ok': False, 'status': 'rejected'}, TimeoutError('drop deadline')):
            with self.subTest(outcome=outcome):
                class FailedDrop(BoundedWorker):
                    def request(self, op, **payload):
                        if op == 'drop':
                            self.requests += 1
                            self.calls.append((op, payload))
                            if isinstance(outcome, Exception):
                                # Real LeanWorker invalidates/reaps transport on
                                # a timeout; no successful release ack is known.
                                self.live.clear()
                                raise outcome
                            return outcome
                        return super().request(op, **payload)
                worker = FailedDrop(length=0)
                result = CheckpointSearch(worker).solve('chain', actions=['advance'])
                self.assertTrue(result['solved'])
                self.assertEqual(result['status'], 'accepted')
                self.assertEqual(result['certificate'], {'schema': 'synthetic', 'length': 0})
                self.assertFalse(result['cleanup_complete'])
                self.assertEqual(result['cleanup_status'], 'incomplete')
                self.assertEqual(result['unreleased_states'], [0])
                self.assertEqual(result['resources_after_cleanup']['worker_active_state_count'],
                                 0 if isinstance(outcome, Exception) else 1)
                self.assertEqual(sum(op == 'verify' for op, _ in worker.calls), 1)

    def test_successful_cleanup_reports_confirmed_release(self):
        result = CheckpointSearch(BoundedWorker(length=0)).solve('chain', actions=['advance'])
        self.assertTrue(result['cleanup_complete'])
        self.assertEqual(result['cleanup_status'], 'complete')
        self.assertEqual(result['unreleased_states'], [])
        self.assertEqual(result['resources_after_cleanup']['worker_active_state_count'], 0)

    def test_rejected_candidate_never_becomes_proof_success(self):
        class Rejected(BoundedWorker):
            def request(self, op, **payload):
                response = super().request(op, **payload)
                return {'ok': True, 'status': 'rejected'} if op == 'verify' else response
        worker = Rejected(length=0)
        result = CheckpointSearch(worker).solve('chain', actions=['advance'])
        self.assertFalse(result['solved'])
        self.assertIsNone(result['certificate'])
        self.assertEqual(worker.live, set())


if __name__ == '__main__': unittest.main()
