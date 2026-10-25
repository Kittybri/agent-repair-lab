import unittest
from app import recall, remember


class Smoke(unittest.TestCase):
    def test_other_user_cannot_recall_fact(self):
        bank = {}
        remember(bank, user_id=1, text="Likes green", message_id=10, author_id=1, confidence=0.9)
        self.assertEqual(recall(bank, 2), [])
