"""Bounded deterministic checkpoint search; only closed verified proofs succeed."""
import heapq
import math
import time

DEFAULT_ACTIONS = ('intro_all', 'assumption', 'all_assumption', 'simp', 'omega',
                   'norm_num', 'ring', 'aesop')


def _identifiers(entries):
    return {entry if isinstance(entry, str) else entry['id'] for entry in entries}


class _DropNotConfirmed(RuntimeError):
    pass


class _ResourceExhausted(RuntimeError):
    pass


class CheckpointSearch:
    def __init__(self, worker):
        self.worker = worker

    def solve(self, task, *, actions=None, max_attempts=32, heartbeat_limit=20000,
              wall_budget=30.0):
        """Explore native states without equating states by pretty-goal text.

        The graph/journal is diagnostic, not an admitted RL training dataset.
        Native checkpoints are process-local. The returned action path can be
        replayed in a new worker; accepted structural proofs can be rechecked.
        """
        if type(max_attempts) is not int or not 1 <= max_attempts <= 128:
            raise ValueError('max_attempts must be an integer from 1 to 128')
        if type(heartbeat_limit) is not int or not 1 <= heartbeat_limit <= 1000000:
            raise ValueError('heartbeat_limit must be from 1 to 1000000')
        if type(wall_budget) not in (int, float) or not math.isfinite(wall_budget) or wall_budget <= 0:
            raise ValueError('wall_budget must be a finite positive number')
        if task not in _identifiers(self.worker.ready['tasks']):
            raise ValueError('unknown trusted task')
        allowed = _identifiers(self.worker.ready['actions'])
        actions = tuple(a for a in DEFAULT_ACTIONS if a in allowed) if actions is None else tuple(actions)
        if not actions or any(type(a) is not str or a not in allowed for a in actions):
            raise ValueError('actions must be nonempty and fixed worker action IDs')
        if len(set(actions)) != len(actions):
            raise ValueError('duplicate actions would repeat work')
        start = time.monotonic()
        deadline = start+wall_budget
        journal, nodes, owned = [], [], set()
        attempts = 0
        certificate, accepted_path = None, []
        final_status = 'exhausted'
        termination_reason = None

        def admit(*, opening=False):
            # Capacity belongs to the worker session, including checkpoints
            # that callers opened before this search. Never evict a queued
            # child to manufacture room or silently change search coverage.
            capacity = self.worker.ready.get('max_states')
            live = getattr(self.worker, 'active_state_count', len(owned))
            if type(capacity) is int and capacity > 0 and live >= capacity:
                raise _ResourceExhausted('state_capacity')
            remaining = getattr(self.worker, 'remaining_requests', None)
            # An action can allocate one child, return a candidate requiring
            # verify, and leave all live handles to drop. Reserve shutdown too.
            # A fresh open only needs its own request/root-drop/shutdown.
            needed = 3 if opening else len(owned)+4
            if type(remaining) is int and remaining < needed:
                raise _ResourceExhausted('request_capacity')

        def call(op, *, cleanup=False, **payload):
            before = time.monotonic()
            timeout = 0.1 if cleanup else deadline-before
            try:
                if timeout <= 0:
                    raise TimeoutError('search operation budget exhausted')
                response = self.worker.request(op, timeout=timeout, **payload)
            except Exception as exc:
                journal.append({'op': op, 'request': payload,
                                'response': {'ok': False, 'status': 'transport_error',
                                             'error': type(exc).__name__, 'reason': str(exc)},
                                'parent_observed_wall_seconds': time.monotonic()-before})
                raise
            journal.append({'op': op, 'request': payload, 'response': response,
                            'parent_observed_wall_seconds': time.monotonic()-before})
            return response

        def release(state, *, cleanup=False):
            response = call('drop', cleanup=cleanup, state=state)
            if response.get('ok') is not True or response.get('status') != 'dropped':
                raise _DropNotConfirmed('worker did not confirm checkpoint release')
            owned.remove(state)

        try:
            admit(opening=True)
            opened = call('open', task=task)
            if not opened.get('ok') or opened.get('status') != 'opened' or 'state' not in opened:
                raise RuntimeError('worker could not open trusted task')
            root = opened['state']
            owned.add(root)
            nodes.append({'state': root, 'parent': None, 'action': None, 'depth': 0})
            queue = [(0, len(opened.get('goals', [])), 0, root, [])]
            sequence = 0
            while queue and attempts < max_attempts:
                if time.monotonic() >= deadline:
                    final_status = 'wall_budget'
                    break
                depth, _, _, state, path = heapq.heappop(queue)
                for action in actions:
                    if attempts >= max_attempts or time.monotonic() >= deadline:
                        final_status = 'attempt_budget' if attempts >= max_attempts else 'wall_budget'
                        break
                    admit()
                    attempts += 1
                    response = call('attempt', state=state, action=action,
                                    heartbeat_limit=heartbeat_limit)
                    status = response.get('status')
                    if not response.get('ok'):
                        continue
                    if 'state' in response:
                        child = response['state']
                        if child != state:
                            owned.add(child)
                    if status == 'closed':
                        candidate = response.get('certificate')
                        if type(candidate) is not dict:
                            continue
                        checked = call('verify', task=task, certificate=candidate)
                        if checked.get('ok') is True and checked.get('status') == 'accepted':
                            certificate = candidate
                            accepted_path = path+[action]
                            final_status = 'accepted'
                            break
                    elif status == 'progress' and 'state' in response:
                        child = response['state']
                        if child != state:
                            sequence += 1
                            next_path = path+[action]
                            nodes.append({'state': child, 'parent': state, 'action': action, 'depth': depth+1})
                            # Splitting a conjunction raises the goal count while
                            # often making it easier. Depth comes first to avoid
                            # starvation behind cosmetically smaller states.
                            heapq.heappush(queue, (depth+1, len(response.get('goals', [])),
                                                   sequence, child, next_path))
                else:
                    # All actions used the unchanged parent before it is freed.
                    # A queued alias still owns the handle until its expansion.
                    if not any(entry[3] == state for entry in queue):
                        if time.monotonic() >= deadline:
                            final_status = 'wall_budget'
                            break
                        release(state)
                if certificate is not None:
                    break
            if certificate is None and attempts >= max_attempts:
                final_status = 'attempt_budget'
        except Exception as exc:
            resource = isinstance(exc, _ResourceExhausted)
            final_status = 'resource_exhausted' if resource else 'worker_failure'
            termination_reason = str(exc) if resource else None
            certificate, accepted_path = None, []
            journal.append({'op': 'search', 'response': {'ok': False,
                                                        'status': 'resource_exhausted' if resource else 'drop_not_confirmed' if isinstance(exc, _DropNotConfirmed) else 'transport_error',
                                                        'error': type(exc).__name__, 'reason': str(exc)}})
        finally:
            # Native states are resources, not cross-session identities. Dropping
            # them leaves the durable proof and action journal for fresh replay.
            for state in sorted(owned, key=lambda s: (str(type(s)), str(s))):
                try:
                    release(state, cleanup=True)
                except Exception as exc:
                    journal.append({'op': 'drop', 'request': {'state': state},
                                    'cleanup_error': type(exc).__name__+': '+str(exc)})
        return {'task': task, 'session': self.worker.session, 'status': final_status,
                'termination_reason': termination_reason or ('frontier_exhausted' if final_status == 'exhausted' else final_status),
                # A verified proof remains valid after a failed release. Keep
                # that proof fact separate from unconfirmed session cleanup.
                'cleanup_complete': not owned,
                'cleanup_status': 'incomplete' if owned else 'complete',
                'unreleased_states': sorted(owned, key=lambda s: (str(type(s)), str(s))),
                'resources_after_cleanup': {
                    'worker_active_state_count': getattr(self.worker, 'active_state_count', None),
                    'worker_remaining_requests': getattr(self.worker, 'remaining_requests', None),
                    'unreleased_states_meaning': 'Search-owned handles whose drop was not confirmed; a terminated worker may already have freed their storage.'},
                'solved': certificate is not None, 'certificate': certificate,
                'path': accepted_path, 'attempted_actions': attempts, 'nodes': nodes,
                'journal': journal, 'parent_observed_wall_seconds': time.monotonic()-start,
                'cost_boundary': 'Search budget bounds admission and individual requests, including expanded-parent release and final verify. Advertised state/request capacity is checked before admission, reserving verify, live-handle cleanup and shutdown requests. Cleanup is separately bounded at 0.1 seconds per retained handle and included in this solve elapsed. Request/native action times are nested; worker startup/whole CPU are separate receipts.',
                'training_eligible': False,
                'scope': 'Fixed deterministic local search; no learned routing or generalization evidence.'}
