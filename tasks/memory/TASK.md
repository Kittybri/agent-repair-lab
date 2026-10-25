# Repair memory attribution

A shared memory bank currently stores facts under their text alone. Identical facts overwrite one another across people, and confidence can become detached from its supporting message.

Edit only `app.py`, preserving `remember` and `recall`. The bank is an initially empty dictionary; records are plain dictionaries. `remember` mutates the bank and `recall(bank, user_id)` returns a list of that user's records.

Store `user_id`, `text`, `message_id`, `author_id`, and `confidence`. Require `user_id == author_id` and a nonzero message ID. Confidence must be finite and within [0, 1]. Invalid evidence raises `ValueError` without a partial write.

Identical text from different users is separate evidence. Repeated text for the same user is one record. A weaker repetition must preserve both the previous confidence and its previous source. An equal or stronger repetition replaces both together. Returned records must be copies so caller mutation does not corrupt the bank.

This task tests identity isolation and evidence bookkeeping. It does not establish the truth of a user's statement, implement semantic contradiction resolution, or add production database migrations.

Run `python -m unittest -v test_smoke.py`. Four groups, 25 points each: user isolation; required evidence; confidence/source pairing; invalid confidence and mutable recall.
