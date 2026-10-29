import unittest
from unittest.mock import patch

from ul_engine.search import CheckpointSearch


class BranchWorker:
    """Small explicit transition graph for scheduler behavior, not proof validity."""
    session = 'scheduler-test'
    ready = {'tasks': ['logic_conjunction'], 'actions': ['split', 'finish', 'fail']}

    def __init__(self, reject=False):
        self.reject = reject
        self.calls = []

    def request(self, op, **payload):
        self.calls.append((op, payload))
        if op == 'open':
            return {'ok': True, 'status': 'opened', 'state': 'root', 'goals': ['P ∧ Q']}
        if op == 'attempt':
            state, action = payload['state'], payload['action']
            if action == 'fail':
                return {'ok': True, 'status': 'tactic_error', 'reason': 'known failure'}
            if state == 'root' and action == 'split':
                return {'ok': True, 'status': 'progress', 'state': 'child', 'goals': ['P', 'Q']}
            if state == 'child' and action == 'finish':
                return {'ok': True, 'status': 'closed', 'certificate': {'schema': 'ul-closed-proof-certificate-v2'}}
            return {'ok': True, 'status': 'no_progress'}
        if op == 'verify':
            return {'ok': True, 'status': 'rejected' if self.reject else 'accepted'}
        if op == 'drop':
            return {'ok': True, 'status': 'dropped'}
        raise ValueError(op)


class CapacityWorker:
    """Synthetic native-storage limit; this does not measure proof memory use."""
    session = 'capacity-test'
    ready = {'tasks': ['logic_conjunction'], 'actions': ['advance', 'idle']}

    def __init__(self, length=80, capacity=64, drop_outcomes=()):
        self.length, self.capacity = length, capacity
        self.drop_outcomes = list(drop_outcomes)
        self.calls, self.live = [], set()
        self.peak_live = 0

    def retain(self, state):
        if len(self.live) >= self.capacity:
            return False
        self.live.add(state)
        self.peak_live = max(self.peak_live, len(self.live))
        return True

    def request(self, op, **payload):
        self.calls.append((op, payload))
        if op == 'open':
            self.retain(0)
            return {'ok': True, 'status': 'opened', 'state': 0, 'goals': ['P']}
        if op == 'attempt':
            state = payload['state']
            if state not in self.live:
                raise ValueError('unknown or stale state')
            if len(self.live) >= self.capacity:
                return {'ok': False, 'status': 'state_limit'}
            if payload['action'] == 'idle':
                return {'ok': True, 'status': 'no_progress'}
            child = state+1
            self.retain(child)
            if state == self.length:
                return {'ok': True, 'status': 'closed', 'state': child,
                        'goals': [], 'certificate': {'schema': 'synthetic', 'length': self.length}}
            return {'ok': True, 'status': 'progress', 'state': child, 'goals': ['P']}
        if op == 'verify':
            return {'ok': True, 'status': 'accepted'}
        if op == 'drop':
            state = payload['state']
            if state not in self.live:
                raise ValueError('unknown or stale state')
            if self.drop_outcomes:
                outcome = self.drop_outcomes.pop(0)
                if isinstance(outcome, Exception):
                    # The real transport stops the worker after a request error.
                    self.live.clear()
                    raise outcome
                return outcome
            self.live.remove(state)
            return {'ok': True, 'status': 'dropped'}
        raise ValueError(op)


class SearchTests(unittest.TestCase):
    def test_expanded_parent_release_allows_chain_beyond_worker_capacity(self):
        worker = CapacityWorker()
        result = CheckpointSearch(worker).solve('logic_conjunction',
            actions=['advance'], max_attempts=100)
        self.assertTrue(result['solved'], result['status'])
        self.assertEqual(result['path'], ['advance']*81)
        self.assertEqual(result['certificate'], {'schema': 'synthetic', 'length': 80})
        self.assertEqual(worker.peak_live, 2)
        drops = [p['state'] for op, p in worker.calls if op == 'drop']
        self.assertCountEqual(drops, range(82))
        self.assertEqual(worker.live, set())

    def test_parent_release_preserves_siblings_until_their_expansion(self):
        class SiblingWorker(CapacityWorker):
            ready = {'tasks': ['logic_conjunction'], 'actions': ['left', 'right', 'finish']}

            def request(self, op, **payload):
                if op != 'attempt':
                    return super().request(op, **payload)
                self.calls.append((op, payload))
                state, action = payload['state'], payload['action']
                if state not in self.live:
                    raise ValueError('unknown or stale state')
                if state == 0 and action in ('left', 'right'):
                    child = 1 if action == 'left' else 2
                    self.retain(child)
                    return {'ok': True, 'status': 'progress', 'state': child,
                            'goals': ['P']}
                if state == 2 and action == 'finish':
                    self.retain(3)
                    return {'ok': True, 'status': 'closed', 'state': 3,
                            'goals': [], 'certificate': {'schema': 'synthetic'}}
                return {'ok': True, 'status': 'no_progress'}

        worker = SiblingWorker(capacity=4)
        result = CheckpointSearch(worker).solve('logic_conjunction',
            actions=['left', 'right', 'finish'])
        self.assertTrue(result['solved'], result['status'])
        self.assertEqual(result['path'], ['right', 'finish'])
        self.assertEqual([(op, p.get('state'), p.get('action'))
                          for op, p in worker.calls if op in ('attempt', 'drop')][:8],
                         [('attempt', 0, 'left'), ('attempt', 0, 'right'),
                          ('attempt', 0, 'finish'), ('drop', 0, None),
                          ('attempt', 1, 'left'), ('attempt', 1, 'right'),
                          ('attempt', 1, 'finish'), ('drop', 1, None)])
        self.assertEqual(worker.live, set())

    def test_queued_alias_keeps_checkpoint_live_until_last_expansion(self):
        class AliasWorker(CapacityWorker):
            ready = {'tasks': ['logic_conjunction'], 'actions': ['left', 'right']}

            def request(self, op, **payload):
                if op != 'attempt':
                    return super().request(op, **payload)
                self.calls.append((op, payload))
                state = payload['state']
                if state not in self.live:
                    raise ValueError('unknown or stale state')
                if state == 0:
                    self.retain(1)
                    return {'ok': True, 'status': 'progress', 'state': 1, 'goals': ['P']}
                return {'ok': True, 'status': 'no_progress'}

        worker = AliasWorker()
        result = CheckpointSearch(worker).solve('logic_conjunction', actions=['left', 'right'])
        self.assertEqual(result['status'], 'exhausted')
        self.assertEqual([p['state'] for op, p in worker.calls if op == 'attempt'],
                         [0, 0, 1, 1, 1, 1])
        self.assertEqual([p['state'] for op, p in worker.calls if op == 'drop'], [0, 1])
        self.assertEqual(worker.live, set())

    def test_rejected_fresh_closed_checkpoint_is_still_cleaned(self):
        class RejectWorker(CapacityWorker):
            def request(self, op, **payload):
                response = super().request(op, **payload)
                if op == 'verify':
                    return {'ok': True, 'status': 'rejected'}
                return response

        worker = RejectWorker(length=0)
        result = CheckpointSearch(worker).solve('logic_conjunction', actions=['advance'])
        self.assertFalse(result['solved'])
        self.assertIsNone(result['certificate'])
        self.assertEqual([p['state'] for op, p in worker.calls if op == 'drop'], [0, 1])
        self.assertEqual(worker.live, set())

    def test_unconfirmed_parent_drop_fails_closed_and_retains_cleanup_ownership(self):
        for response in ({'ok': False, 'status': 'drop_rejected'},
                         {'ok': True, 'status': 'not_dropped'}):
            with self.subTest(response=response):
                worker = CapacityWorker(length=1, drop_outcomes=[response])
                result = CheckpointSearch(worker).solve('logic_conjunction', actions=['advance'])
                self.assertFalse(result['solved'])
                self.assertEqual(result['status'], 'worker_failure')
                self.assertEqual([p['state'] for op, p in worker.calls if op == 'attempt'], [0])
                self.assertEqual([p['state'] for op, p in worker.calls if op == 'drop'], [0, 0, 1])
                drops = [e for e in result['journal'] if e['op'] == 'drop']
                self.assertEqual(drops[0]['response'], response)
                self.assertTrue(any(e['response'].get('status') == 'drop_not_confirmed'
                                    for e in result['journal'] if e['op'] == 'search'))
                self.assertEqual(worker.live, set())

    def test_parent_drop_transport_failure_fails_closed_and_retries_cleanup(self):
        worker = CapacityWorker(length=1, drop_outcomes=[TimeoutError('drop deadline')])
        result = CheckpointSearch(worker).solve('logic_conjunction', actions=['advance'])
        self.assertFalse(result['solved'])
        self.assertEqual(result['status'], 'worker_failure')
        self.assertEqual([p['state'] for op, p in worker.calls if op == 'attempt'], [0])
        self.assertEqual([p['state'] for op, p in worker.calls if op == 'drop'], [0, 0, 1])
        drops = [e for e in result['journal'] if e['op'] == 'drop']
        self.assertEqual(drops[0]['response']['status'], 'transport_error')
        self.assertEqual(drops[0]['response']['error'], 'TimeoutError')
        self.assertEqual(sum('cleanup_error' in e for e in drops), 2)
        self.assertEqual(worker.live, set())

    def test_search_drop_uses_remaining_budget_and_can_exhaust_it(self):
        now = [0.0]

        class BudgetWorker(CapacityWorker):
            def request(self, op, **payload):
                response = super().request(op, **payload)
                now[0] += {'open': 0.125, 'attempt': 0.25, 'drop': 0.625}.get(op, 0)
                return response

        worker = BudgetWorker(length=1)
        with patch('ul_engine.search.time.monotonic', side_effect=lambda: now[0]):
            result = CheckpointSearch(worker).solve('logic_conjunction',
                actions=['advance'], wall_budget=1)
        self.assertEqual(result['status'], 'wall_budget')
        self.assertEqual([p['state'] for op, p in worker.calls if op == 'attempt'], [0])
        drops = [p for op, p in worker.calls if op == 'drop']
        self.assertEqual([(p['state'], p['timeout']) for p in drops], [(0, 0.625), (1, 0.1)])

    def test_partial_expansion_keeps_parent_for_separately_bounded_cleanup(self):
        for max_attempts in (1, 2):
            with self.subTest(max_attempts=max_attempts):
                worker = CapacityWorker(length=1)
                result = CheckpointSearch(worker).solve('logic_conjunction',
                    actions=['advance', 'idle'], max_attempts=max_attempts)
                self.assertEqual(result['status'], 'attempt_budget')
                drops = [p for op, p in worker.calls if op == 'drop']
                self.assertEqual([p['state'] for p in drops], [0, 1])
                self.assertEqual(drops[0]['timeout'] == 0.1, max_attempts == 1)

    def test_wall_budget_before_next_action_keeps_parent_for_cleanup(self):
        for actions in (['advance'], ['advance', 'idle']):
            with self.subTest(actions=actions):
                now = [0.0]

                class ExpiringWorker(CapacityWorker):
                    def request(self, op, **payload):
                        response = super().request(op, **payload)
                        if op == 'attempt':
                            now[0] = 1.0
                        return response

                worker = ExpiringWorker(length=1)
                with patch('ul_engine.search.time.monotonic', side_effect=lambda: now[0]):
                    result = CheckpointSearch(worker).solve('logic_conjunction',
                        actions=actions, wall_budget=1)
                self.assertEqual(result['status'], 'wall_budget')
                self.assertEqual([p['state'] for op, p in worker.calls if op == 'attempt'], [0])
                self.assertEqual([(p['state'], p['timeout']) for op, p in worker.calls if op == 'drop'],
                                 [(0, 0.1), (1, 0.1)])

    def test_closed_branch_requires_separate_acceptance(self):
        worker = BranchWorker()
        result = CheckpointSearch(worker).solve('logic_conjunction', actions=['split', 'finish', 'fail'])
        self.assertTrue(result['solved'])
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(sum(op == 'verify' for op, _ in worker.calls), 1)
        self.assertEqual(result['path'], ['split', 'finish'])

    def test_closed_looking_rejected_candidate_has_no_success(self):
        result = CheckpointSearch(BranchWorker(reject=True)).solve(
            'logic_conjunction', actions=['split', 'finish'], max_attempts=6)
        self.assertFalse(result['solved'])
        self.assertIsNone(result['certificate'])
        self.assertTrue(any(e['response'].get('status') == 'rejected'
                            for e in result['journal'] if e['op'] == 'verify'))

    def test_siblings_follow_failure_from_unchanged_parent(self):
        worker = BranchWorker()
        result = CheckpointSearch(worker).solve('logic_conjunction', actions=['fail', 'split', 'finish'])
        self.assertTrue(result['solved'])
        attempts = [p for op, p in worker.calls if op == 'attempt']
        self.assertEqual(attempts[0]['state'], attempts[1]['state'])
        self.assertEqual(attempts[0]['action'], 'fail')
        self.assertEqual(attempts[1]['action'], 'split')

    def test_limits_unknown_actions_and_task(self):
        worker = BranchWorker()
        with self.assertRaises(ValueError): CheckpointSearch(worker).solve('unknown')
        with self.assertRaises(ValueError): CheckpointSearch(worker).solve('logic_conjunction', actions=['arbitrary'])
        with self.assertRaises(ValueError): CheckpointSearch(worker).solve('logic_conjunction', max_attempts=0)
        result = CheckpointSearch(worker).solve('logic_conjunction', actions=['fail'], max_attempts=1)
        self.assertFalse(result['solved'])
        self.assertEqual(result['attempted_actions'], 1)
        self.assertFalse(result['training_eligible'])

    def test_cleanup_and_journal_keep_failed_paths(self):
        worker = BranchWorker()
        result = CheckpointSearch(worker).solve('logic_conjunction', actions=['fail', 'split', 'finish'])
        self.assertTrue(any(e['response'].get('status') == 'tactic_error' for e in result['journal']))
        self.assertEqual({p['state'] for op, p in worker.calls if op == 'drop'}, {'root', 'child'})

    def test_each_operation_receives_remaining_wall_budget(self):
        worker = BranchWorker()
        CheckpointSearch(worker).solve('logic_conjunction', actions=['split', 'finish'], wall_budget=0.5)
        requests = [p for op, p in worker.calls if op != 'drop']
        self.assertTrue(all(0 < p.get('timeout', 99) <= 0.5 for p in requests))

    def test_worker_failure_is_retained_and_never_success(self):
        class TimedWorker(BranchWorker):
            def request(self, op, **payload):
                if op == 'attempt': raise TimeoutError('known request deadline')
                return super().request(op, **payload)
        result = CheckpointSearch(TimedWorker()).solve('logic_conjunction', actions=['split'])
        self.assertFalse(result['solved'])
        self.assertEqual(result['status'], 'worker_failure')
        self.assertTrue(any(e.get('response', {}).get('status') == 'transport_error' for e in result['journal']))

    def test_goal_count_does_not_starve_a_productive_split(self):
        class SplittingWorker(BranchWorker):
            ready = {'tasks': ['logic_conjunction'], 'actions': ['intro', 'split', 'finish']}
            def __init__(self):
                super().__init__()
                self.number = 0
            def request(self, op, **payload):
                if op == 'attempt' and payload['action'] == 'intro':
                    self.number += 1
                    return {'ok': True, 'status': 'progress', 'state': 'noop'+str(self.number), 'goals': ['P ∧ Q']}
                if op == 'attempt' and payload['action'] == 'split' and payload['state'] != 'child':
                    return {'ok': True, 'status': 'progress', 'state': 'child', 'goals': ['P', 'Q']}
                return super().request(op, **payload)
        result = CheckpointSearch(SplittingWorker()).solve('logic_conjunction',
            actions=['intro', 'split', 'finish'], max_attempts=15)
        self.assertTrue(result['solved'])


if __name__ == '__main__':
    unittest.main()
