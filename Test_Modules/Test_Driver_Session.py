import unittest
from datetime import datetime
from Study_Tracker_Modules.Session import Session

class TestSession(unittest.TestCase):
    def setUp(self):
        self.session = Session(1,datetime.now().date(), 60*60*1.5,)

if __name__ == '__main__':
    unittest.main()
