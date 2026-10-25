import unittest
from app import owner


class Smoke(unittest.TestCase):
    def test_explicit_target(self):
        self.assertEqual(owner(11, addressed="wanderer"), "wanderer")
