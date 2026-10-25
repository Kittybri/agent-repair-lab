import unittest
import candidate

PCM = bytes([1, 0, 1, 0]) * 960
GOOD = {"no_speech_prob": 0.01, "avg_logprob": -0.1, "compression_ratio": 1.2}


class Checks(unittest.TestCase):
    def test_clear_speech_and_trailing_silence(self):
        self.assertTrue(candidate.accept_audio(PCM, "My friend's name is Rowan.", [GOOD]))
        self.assertTrue(candidate.accept_audio(PCM, "Tell me a story.", [GOOD, dict(GOOD, no_speech_prob=0.98)]))

    def test_bad_pcm_and_encrypted_frames(self):
        for data in (b"", bytes(3840), b"abc"):
            self.assertFalse(candidate.accept_audio(data, "I can hear you", [GOOD]))
        self.assertFalse(candidate.accept_audio(PCM, "Hello", [GOOD], encrypted=True))

    def test_caption_and_empty_transcripts(self):
        for text in ("", "   ", "SUBTITLES BY someone", "Closed captioning provided by a channel", "amara.org"):
            self.assertFalse(candidate.accept_audio(PCM, text, [GOOD]))

    def test_metadata_is_required_and_validated(self):
        for rows in ([], [{}], [dict(GOOD, avg_logprob=-1.0)], [dict(GOOD, compression_ratio=3)], [dict(GOOD, no_speech_prob=0.99)], [dict(GOOD, avg_logprob=float("nan"))], [dict(GOOD, no_speech_prob=-1)]):
            self.assertFalse(candidate.accept_audio(PCM, "Hello there", rows))
