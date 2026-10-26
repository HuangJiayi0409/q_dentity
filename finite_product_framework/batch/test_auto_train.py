"""Batch orchestration tests; synthetic statuses never count as Train proofs."""
from dataclasses import asdict
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from batch import auto_train as batch
from workflow.engine import Budget
from workflow.contracts import save


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.work=Path(self.temp.name)
        self.manifest=dict(identities=['synthetic-'+str(i) for i in range(7)],total=7,workers=3,
            budget=asdict(Budget()),frozen_files={},min_available_memory_gib=32,min_free_disk_gib=40)
        self.calls=[];self.active=0;self.peak=0;self.lock=threading.Lock()
    def tearDown(self):self.temp.cleanup()
    def task(self,identity,directory,budget):
        with self.lock:
            self.calls.append(identity);self.active+=1;self.peak=max(self.peak,self.active)
        time.sleep(.025)
        with self.lock:self.active-=1
        record=dict(identity=identity,status='proved' if identity.endswith('0') else 'unproved',
            classification='selected',proved=identity.endswith('0'),successful_methods=[],methods=[],
            problem_seconds=.025,pipeline_seconds=.02,method_seconds_sum=.01,preprocessing_cache_hit=True)
        save(Path(directory)/'result.json',record)
        return record
    def run_batch(self,resource=None):
        with (patch.object(batch,'task',side_effect=self.task),patch.object(batch,'audit') as audit,
              patch.object(batch,'verify'),patch.object(batch,'resources',return_value=resource or dict(available_memory_gib=100,free_disk_gib=100))):
            result=batch.run(self.work,self.manifest)
        return result,audit
    def test_global_concurrency_and_final_denominator(self):
        result,audit=self.run_batch()
        self.assertEqual(result['status'],'completed');self.assertEqual(len(self.calls),7)
        self.assertLessEqual(self.peak,3);self.assertGreater(self.peak,1)
        self.assertEqual(result['success_rate'],1/7);self.assertEqual(result['proved'],1)
        self.assertEqual(result['total'],7);self.assertEqual(result['completed'],7)
        self.assertAlmostEqual(result['problem_seconds_sum'],7*.025)
        self.assertEqual(audit.call_count,1)
        self.assertTrue((self.work/'REPORT.txt').exists())
        self.assertEqual(len((self.work/'per_identity.csv').read_text().splitlines()),8)
    def test_resume_does_not_rerun_completed_identities(self):
        self.run_batch();self.calls.clear()
        result,_=self.run_batch()
        self.assertEqual(self.calls,[]);self.assertEqual(result['completed'],7)
        self.assertEqual(len(batch.load(self.work/'timing.json')['sessions']),2)
    def test_resource_guard_stops_new_dispatch_without_final_rate(self):
        result,audit=self.run_batch(dict(available_memory_gib=31,free_disk_gib=100))
        self.assertEqual(result['status'],'resource_paused');self.assertEqual(self.calls,[])
        self.assertIsNone(result['success_rate']);audit.assert_not_called()
    def test_partial_resume_fills_only_missing_rows(self):
        self.task('synthetic-0',self.work/'tasks/synthetic-0',{})
        self.calls.clear();result,_=self.run_batch()
        self.assertEqual(len(self.calls),6);self.assertNotIn('synthetic-0',self.calls)
        self.assertEqual(result['success_rate'],1/7)
    def test_failure_before_pipeline_is_recorded_and_not_counted_as_proof(self):
        with patch.object(batch,'prove',side_effect=ValueError('synthetic failure')):
            record=batch.task('synthetic',self.work/'failure',asdict(Budget()))
        self.assertEqual(record['status'],'runner_error');self.assertFalse(record['proved'])
        self.assertTrue((self.work/'failure/result.json').exists())
    def test_task_requests_single_inner_worker_and_all_unknown_policy(self):
        report=dict(status='unproved',work_directory=str(self.work),elapsed_seconds=.1)
        save(self.work/'report.json',report)
        with (patch.object(batch,'prove',return_value=report) as prove,
              patch.object(batch,'inspect_report',return_value=('selected',[],[]))):
            record=batch.task('synthetic',self.work/'one',asdict(Budget()))
        self.assertEqual(prove.call_args.kwargs['unknown_workers'],1)
        self.assertEqual(prove.call_args.kwargs['unknown_policy'],'all')
        self.assertEqual(prove.call_args.kwargs['method'],'auto')
        self.assertFalse(record['proved'])
    def test_unaccepted_success_is_not_a_batch_success(self):
        report=dict(status='proved',work_directory=str(self.work),elapsed_seconds=.1)
        save(self.work/'report.json',report)
        with patch.object(batch,'prove',return_value=report),patch.object(batch,'inspect_report',side_effect=ValueError('bad proof')):
            record=batch.task('synthetic',self.work/'bad',asdict(Budget()))
        self.assertFalse(record['proved']);self.assertEqual(record['status'],'runner_error')
    def test_in_progress_rate_is_never_presented_as_final(self):
        result=batch.summarize(self.manifest,[],state='running',active=['synthetic-0'],
            first_started=time.time(),session_started=time.monotonic(),prior_active=0)
        self.assertIsNone(result['success_rate']);self.assertEqual(result['active_count'],1)


if __name__=='__main__':unittest.main()
