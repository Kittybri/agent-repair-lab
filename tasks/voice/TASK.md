# Repair a voice confidence gate

Silence, encrypted frames, and unreliable transcriptions must not reach the conversational model as trusted user speech. The starter checks only that a transcript exists.

Edit only `app.py`, preserving `accept_audio`. Return a boolean. Inputs are decoded 16-bit stereo PCM bytes, a transcript string, a list of speech-to-text segment dictionaries, and an explicit `encrypted` flag.

Reject encrypted data, empty PCM, byte lengths not divisible by four, and all-zero PCM. Reject blank transcripts and case-insensitive occurrences of `subtitles by`, `closed captioning`, or `amara.org`.

Require at least one segment. Every segment must contain finite numeric `no_speech_prob`, `avg_logprob`, and `compression_ratio`. Probability must be within [0, 1], log probability at most zero, and compression nonnegative. Missing or invalid metadata fails closed.

A speech segment has `no_speech_prob < 0.75`. Require at least `max(1, ceil(0.4 * segment_count))` speech segments. Every speech segment must have `avg_logprob > -0.65` and `compression_ratio < 2.5`. High-no-speech segments may be trailing silence and do not alone reject otherwise adequate speech.

This fixture does not implement DAVE decryption, Opus decoding, speaker recognition, real speech detection, or speech-to-text. Thresholds are specified task policy, not a claim of acoustic calibration.

Run `python -m unittest -v test_smoke.py`. Four groups worth 25 points each: clear speech/trailing silence; PCM/encryption; caption/empty text; metadata/confidence.
