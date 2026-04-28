import time
import unittest
from Study_Tracker_Modules.Stopwatch import Stopwatch


class StopwatchTest(unittest.TestCase):

    def setUp(self):
        self.stopwatch = Stopwatch()
        self.stopwatch.start_time()
        time.sleep(1)
        self.result = self.stopwatch.stop_time()

    def test_timer_in_range(self):
        self.assertTrue(1 < self.result < 2)

    def test_timer_out_of_range_upper(self):
        self.assertFalse(self.result > 2)

    def test_timer_out_of_range_lower(self):
        self.assertFalse(self.result < 1)

if __name__ == '__main__':
    unittest.main()
