import unittest
from src.common.utilities import valid_user_input


class TestValidUserInput(unittest.TestCase):

    def test_valid_user_input(self):
        self.assertTrue(valid_user_input('1'))
        self.assertTrue(valid_user_input('200'))
        self.assertTrue(valid_user_input('200.324'))
        self.assertTrue(valid_user_input('0.1234'))
        self.assertTrue(valid_user_input('99999999'))
        self.assertTrue(valid_user_input('0.00000000000001'))
        self.assertFalse(valid_user_input('-912'))
        self.assertFalse(valid_user_input('0'))
        self.assertFalse(valid_user_input('-0.1'))
        self.assertFalse(valid_user_input('00'))
        self.assertFalse(valid_user_input('000'))
        self.assertFalse(valid_user_input('00.124'))
        self.assertFalse(valid_user_input('-324.123'))
        self.assertFalse(valid_user_input('-1'))
        self.assertFalse(valid_user_input(''))
