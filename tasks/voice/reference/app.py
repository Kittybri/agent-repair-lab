import math


def accept_audio(pcm, transcript, segments, *, encrypted=False):
    if encrypted or not pcm or len(pcm) % 4 or not any(pcm):
        return False
    text = transcript.strip().lower()
    if not text or any(marker in text for marker in ("subtitles by", "closed captioning", "amara.org")):
        return False
    if not segments:
        return False
    speech = 0
    for row in segments:
        try:
            probability = float(row["no_speech_prob"])
            confidence = float(row["avg_logprob"])
            compression = float(row["compression_ratio"])
        except (KeyError, TypeError, ValueError):
            return False
        if not all(math.isfinite(x) for x in (probability, confidence, compression)):
            return False
        if not 0 <= probability <= 1 or confidence > 0 or compression < 0:
            return False
        if probability < 0.75:
            if confidence <= -0.65 or compression >= 2.5:
                return False
            speech += 1
    return speech >= max(1, math.ceil(0.4 * len(segments)))
