import unittest
from Study_Tracker_Modules.Subject import Subject

class TestSubject(unittest.TestCase):
    def setUp(self):
        self.subject = Subject(1,
                               "algo",
                               "A look into the deeper use of data structures",
                               12,
                               9)
    def test_subject_getters_setters_id_in_range(self):
        self.subject.id = 10
        self.assertEqual(self.subject.id, 10)

    def test_subject_getters_setters_id_out_lower_range(self):
        self.subject.id = -1
        with self.assertRaises(ValueError):
            self.subject.subject_id = -1

    def test_subject_getters_setters_name(self):
        self.subject.name = "math"
        self.assertEqual(self.subject.name, "math")

    def test_subject_getters_setters_name_empty_string(self):
        with self.assertRaises(ValueError):
            self.subject.name = ""

    def test_subject_getters_setters_description(self):
        self.subject.description = "a very long description"
        self.assertEqual(self.subject.description, "a very long description")

    def test_subject_getters_setters_description_empty_string(self):
        with self.assertRaises(ValueError):
            self.subject.description = ""

    def test_subject_getters_setters_weekly_recommended_hours_in_range(self):
        self.subject.goal = 10
        self.assertEqual(self.subject.goal, 10)

    def test_subject_getters_setters_weekly_recommended_hours_out_lower_range(self):
        with self.assertRaises(ValueError):
            self.subject.goal = -1

    def test_subject_getters_setters_weekly_recommended_hours_out_upper_range(self):
        with self.assertRaises(ValueError):
            self.subject.goal = 500

    def test_subject_getters_setters_difficulty_in_range(self):
        self.subject.difficulty = 6
        self.assertEqual(self.subject.difficulty, 6)

    def test_subject_getters_difficulty_in_out_lower_range(self):
        with self.assertRaises(ValueError):
            self.subject.difficulty = -1

    def test_subject_getters_difficulty_in_out_upper_range(self):
        with self.assertRaises(ValueError):
            self.subject.difficulty = 11

if __name__ == '__main__':
    unittest.main()
