# Repair attachment retrieval

## Incident and scope

A fresh study PDF could be downloaded from its original Discord URL, but the cached endpoint returned HTTP 415. The starter incorrectly forces the cached path and has no resource bounds. This is a dependency-free reproduction; the production exception type was `discord.HTTPException`.

## Your task

Edit only `app.py`. Keep the `DownloadHTTPError` type and `download` signature. `attachment.size` is the declared integer size; `await attachment.read()` reads the original URL; `await attachment.read(use_cached=True)` reads its cache.

Required behavior:

1. Reject a declared size greater than `limit` with `ValueError` before making a read.
2. Read the original URL first. Only `DownloadHTTPError` permits one cached retry. Other errors propagate.
3. Apply `asyncio.wait_for` or equivalent to each read using the supplied `timeout`. Timeouts propagate and do not trigger a cached retry.
4. Reject a returned byte string larger than `limit`. Equality is allowed. Otherwise return the exact bytes.
5. Propagate failure if both URLs fail. Do not loop, swallow errors, or return placeholder material.

Run `python -m unittest -v test_smoke.py` in this workspace. Full acceptance checks additionally exercise overflow, both URL timeouts, and error classification. No network or third-party packages are necessary.

## Rubric

Four groups, 25 points each: URL selection and fallback; declared and actual size; timeouts; error propagation. Acceptance is 100/100. Grading is behavioral and does not require the reference implementation's exact code.
