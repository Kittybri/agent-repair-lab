import math


def remember(bank, *, user_id, text, message_id, author_id, confidence):
    if user_id != author_id or not message_id:
        raise ValueError("Memory requires matching speaker and message evidence")
    confidence = float(confidence)
    if not math.isfinite(confidence) or not 0 <= confidence <= 1:
        raise ValueError("Confidence must be a finite value between zero and one")
    key = (user_id, text)
    old = bank.get(key)
    if old and old["confidence"] > confidence:
        return
    bank[key] = {"user_id": user_id, "text": text, "message_id": message_id,
                 "author_id": author_id, "confidence": confidence}


def recall(bank, user_id):
    return [dict(row) for (owner, _), row in bank.items() if owner == user_id]
