import unittest

from process import Process
from fcfs import FCFS
from rr import RR
from spn import SPN
from srtn import SRTN
from hrrn import HRRN


class SchedulerStabilityTests(unittest.TestCase):
    def _build_processes(self):
        return [
            Process("P1", 0, 3, 0),
            Process("P2", 0, 5, 1),
            Process("P3", 2, 2, 2),
            Process("P4", 10, 1, 3),
        ]

    def _assert_finished(self, scheduler):
        scheduler.run()
        self.assertEqual(len(scheduler.history) > 0, True)
        for proc in scheduler.processes:
            self.assertEqual(proc.remain_bt, 0)
            self.assertGreaterEqual(proc.tt, proc.bt)
            self.assertGreaterEqual(proc.wt, 0)

    def test_fcfs_stable(self):
        self._assert_finished(FCFS(self._build_processes(), 2))

    def test_rr_stable(self):
        self._assert_finished(RR(self._build_processes(), 2, 2))

    def test_spn_stable(self):
        self._assert_finished(SPN(self._build_processes(), 2))

    def test_srtn_stable(self):
        self._assert_finished(SRTN(self._build_processes(), 2))

    def test_hrrn_stable(self):
        self._assert_finished(HRRN(self._build_processes(), 2))

    def test_srtn_no_idle_cpu_crash_on_preemption(self):
        # 과거 코드에서 idle CPU가 섞인 상태에서 preemption 비교 시 None.remain_bt 오류가 발생할 수 있었다.
        processes = [
            Process("P1", 0, 8, 0),
            Process("P2", 1, 1, 1),
            Process("P3", 2, 1, 2),
        ]
        scheduler = SRTN(processes, 3)
        scheduler.run()
        self.assertTrue(all(p.remain_bt == 0 for p in processes))

    def test_invalid_scheduler_inputs(self):
        with self.assertRaises(ValueError):
            FCFS([Process("P1", 0, 1, 0)], 0)
        with self.assertRaises(ValueError):
            RR([Process("P1", 0, 1, 0)], 1, 0)
        with self.assertRaises(ValueError):
            Process("P1", -1, 1, 0)
        with self.assertRaises(ValueError):
            Process("P1", 0, -1, 0)


if __name__ == "__main__":
    unittest.main()
