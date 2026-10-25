def remember(bank, *, user_id, text, message_id, author_id, confidence):
    bank[text] = {"text": text, "confidence": confidence}


def recall(bank, user_id):
    return list(bank.values())
