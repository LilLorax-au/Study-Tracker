import unittest
from Study_Tracker_Modules.User import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User(1, "Isaac","isaac.brown154@outlook.com",User.password_hasher("TestPassword"))

    def test_user_getters_setters_id_in_range(self):
        self.user.user_id = 1
        self.assertEqual(self.user.user_id, 1)

    def test_user_getters_setters_id_out_lower_range(self):
        with self.assertRaises(ValueError):
            self.user.user_id = -1

    def test_user_getters_setters_name(self):
        self.user.name = "DAVID"
        self.assertEqual(self.user.name, "david")

    def test_user_getters_setters_email(self):
        self.user.email = "AnewEmail@email.com"
        self.assertEqual(self.user.email, "anewemail@email.com")

    def test_user_password_change_to_new(self):
        self.assertTrue(self.user.change_password("NewPassword","TestPassword"))

    def test_user_password_change_to_same(self):
        self.assertFalse(self.user.change_password("TestPassword","TestPassword"))

    def test_user_password_change_fail(self):
        self.assertFalse(self.user.change_password("NewPassword","Password"))

if __name__ == '__main__':
    unittest.main()
