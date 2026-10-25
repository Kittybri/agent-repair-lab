# Repair turn ownership

Two bot processes receive the same event. They must independently agree on one reply owner. A fixed speaker makes one character monopolize the channel; Python's built-in hash can differ across processes.

Edit only `app.py`, preserving `owner`. Valid bot names are `scaramouche` and `wanderer`. Inputs provide resolved targets, so this task does not test natural-language name resolution.

Priority contract:

1. `blocked=True` returns `None`, even with a direct address, reply, or solo bot.
2. A valid `solo` bot owns an allowed event.
3. A valid `addressed` bot overrides the reply target.
4. Otherwise a valid `reply_to` bot owns the event.
5. An ambient event returns one valid bot, deterministically from `message_id`. Results must agree across fresh Python processes and vary across a reasonable collection of IDs. No randomness, mutable turn counter, clock, or process-randomized built-in hash.

Both processes call this same owner function and compare its return value with their identity. An unavailable partner and bot-to-bot autoplay are outside this fixture's scope.

Run `python -m unittest -v test_smoke.py`. Four acceptance groups worth 25 points each cover explicit targeting, reply/solo, blocks, and cross-process ambient ownership.
