import unittest
import candidate


def add(bank, user=1, message=10, author=None, confidence=0.9):
    candidate.remember(bank, user_id=user, text="Favorite color is green", message_id=message,
                       author_id=user if author is None else author, confidence=confidence)


class Checks(unittest.TestCase):
    def test_user_isolation_and_identical_facts(self):
        bank = {}
        add(bank, user=1)
        add(bank, user=2, message=20)
        self.assertEqual(len(candidate.recall(bank, 1)), 1)
        self.assertEqual(candidate.recall(bank, 1)[0]["author_id"], 1)
        self.assertEqual(candidate.recall(bank, 2)[0]["message_id"], 20)
        self.assertEqual(candidate.recall(bank, 3), [])

    def test_evidence_required_without_partial_write(self):
        for kwargs in ({"author": 2}, {"message": 0}):
            bank = {}
            with self.assertRaises(ValueError):
                add(bank, **kwargs)
            self.assertEqual(bank, {})

    def test_strongest_evidence_and_confidence_stay_together(self):
        bank = {}
        add(bank, message=10, confidence=0.9)
        add(bank, message=20, confidence=0.4)
        item = candidate.recall(bank, 1)[0]
        self.assertEqual((item["message_id"], item["confidence"]), (10, 0.9))
        add(bank, message=30, confidence=0.99)
        self.assertEqual(candidate.recall(bank, 1)[0]["message_id"], 30)
        self.assertEqual(len(candidate.recall(bank, 1)), 1)

    def test_invalid_confidence_and_mutable_recall(self):
        for confidence in (-1, 1.1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                add({}, confidence=confidence)
        bank = {}
        add(bank)
        candidate.recall(bank, 1)[0]["text"] = "corrupted"
        self.assertEqual(candidate.recall(bank, 1)[0]["text"], "Favorite color is green")
