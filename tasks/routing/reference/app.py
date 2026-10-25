import hashlib

BOTS = ("scaramouche", "wanderer")


def owner(message_id, *, addressed=None, reply_to=None, blocked=False, solo=None):
    if blocked:
        return None
    if solo:
        return solo
    if addressed in BOTS:
        return addressed
    if reply_to in BOTS:
        return reply_to
    return BOTS[hashlib.sha256(str(message_id).encode()).digest()[0] % 2]
