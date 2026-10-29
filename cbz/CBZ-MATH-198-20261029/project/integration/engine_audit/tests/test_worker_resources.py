"""Resource accounting uses the real transport with the small fake subprocess."""
from pathlib import Path
import sys
import tempfile
import unittest
from ul_engine.worker import LeanWorker

FAKE = Path(__file__).with_name('fake_worker.py')

class WorkerResourceTests(unittest.TestCase):
    def test_session_resources_include_foreign_handles_and_actual_requests(self):
        with tempfile.TemporaryDirectory() as temp:
            with LeanWorker([sys.executable, '-B', str(FAKE), 'normal'],
                            receipt_dir=Path(temp)/'run', max_requests=9) as worker:
                self.assertEqual(worker.remaining_requests, 9)
                self.assertEqual(worker.active_state_count, 0)
                state = worker.request('open', task='x')['state']
                self.assertEqual(worker.remaining_requests, 8)
                self.assertEqual(worker.active_state_count, 1)
                worker.request('drop', state=state)
                self.assertEqual(worker.remaining_requests, 7)
                self.assertEqual(worker.active_state_count, 0)

    def test_larger_client_limit_cannot_hide_pinned_native_limit(self):
        with tempfile.TemporaryDirectory() as temp:
            with LeanWorker([sys.executable, '-B', str(FAKE), 'normal'],
                            receipt_dir=Path(temp)/'run', max_requests=1000) as worker:
                self.assertEqual(worker.remaining_requests, 256)
                worker.request('verify', task='x', certificate={})
                self.assertEqual(worker.remaining_requests, 255)

    def test_acknowledged_delayed_exit_has_time_for_bounded_teardown(self):
        import json
        with tempfile.TemporaryDirectory() as temp:
            receipt = Path(temp)/'run'
            with LeanWorker([sys.executable, '-B', str(FAKE), 'delayedexit'],
                            receipt_dir=receipt) as worker:
                pass
            value=json.loads((receipt/'receipt.json').read_text())
            self.assertEqual(worker.process.returncode, 0)
            self.assertTrue(value['shutdown_acknowledged'])
            self.assertFalse(value['forced_termination'])
            self.assertEqual(value['shutdown_grace_seconds'], 2.0)

    def test_stubborn_acknowledged_process_is_killed_after_configured_grace(self):
        import json,time
        with tempfile.TemporaryDirectory() as temp:
            receipt = Path(temp)/'run'
            started=time.monotonic()
            with LeanWorker([sys.executable, '-B', str(FAKE), 'stubbornexit'],
                            receipt_dir=receipt,shutdown_grace=0.1) as worker:
                pass
            value=json.loads((receipt/'receipt.json').read_text())
            self.assertLess(time.monotonic()-started, 1.0)
            self.assertLess(worker.process.returncode, 0)
            self.assertTrue(value['shutdown_acknowledged'])
            self.assertTrue(value['forced_termination'])

    def test_shutdown_grace_rejects_nonfinite_or_unbounded_values(self):
        for value in (True,0,-1,6,float('inf'),float('nan')):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp:
                with self.assertRaises(ValueError):
                    LeanWorker([sys.executable, '-B', str(FAKE), 'normal'],
                               receipt_dir=Path(temp)/'run',shutdown_grace=value)

if __name__ == '__main__': unittest.main()
