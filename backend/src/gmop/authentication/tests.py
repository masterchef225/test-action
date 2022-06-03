from django.test import TestCase
from .jwt import create_token


class TestCase1(TestCase):
    def test_missing_argument_for_token_creating(self):
        print('!!!')
        self.assertRaises(ValueError, create_token, username=None)
