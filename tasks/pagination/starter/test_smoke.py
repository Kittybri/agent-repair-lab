import unittest
from app import GROUPS, paginate


class Smoke(unittest.TestCase):
    def test_returns_three_complete_parts(self):
        data = {name: name for group in GROUPS for name in group}
        self.assertEqual(len(paginate(data)), 3)
