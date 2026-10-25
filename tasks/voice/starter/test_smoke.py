import unittest
from app import accept_audio


class Smoke(unittest.TestCase):
    def test_silence_is_rejected(self):
        self.assertFalse(accept_audio(bytes(3840), "Hello", []))
