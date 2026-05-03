import unittest
from datetime import datetime
from Study_Tracker_Modules.Session import Session

class TestSession(unittest.TestCase):

    def setUp(self):
        self.session = Session(1,"math",datetime.now(),1,"coding",1,1)

    def test_session_id_in_range(self):
        self.session.session_id = 3
        self.assertEqual(self.session.session_id, 3)

    def test_session_id_out_range(self):
        with self.assertRaises(ValueError):
            self.session.session_id = -1

    def test_session_subject_name_in_range(self):
        self.session.subject_name = 'Test'
        self.assertEqual(self.session.subject_name, 'Test')

    def test_session_subject_name_out_range(self):
        with self.assertRaises(ValueError):
            self.session.subject_name = ""

    def test_session_date_in_range(self):
        self.session.subject_date = datetime.strptime('2020-03-31', "%Y-%m-%d")
        self.assertEqual(self.session.subject_date, datetime(2020, 3, 31))

    def test_session_study_type_in_range(self):
        self.session.study_type = 'reading'
        self.assertEqual(self.session.study_type, 'reading')

    def test_session_study_type_out_range(self):
        with self.assertRaises(ValueError):
            self.session.study_type = "read"


if __name__ == '__main__':
    unittest.main()
