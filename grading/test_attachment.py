import asyncio
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock

import candidate


class Checks(unittest.IsolatedAsyncioTestCase):
    async def test_original_and_http_fallback(self):
        for failures in (False, True):
            read = AsyncMock(side_effect=[candidate.DownloadHTTPError(), b"pdf"] if failures else [b"pdf"])
            self.assertEqual(await candidate.download(SimpleNamespace(size=3, read=read)), b"pdf")
            self.assertEqual(read.await_args_list[0].kwargs, {})
            if failures:
                self.assertEqual(read.await_args_list[1].kwargs, {"use_cached": True})

    async def test_size_limits_before_and_after_download(self):
        read = AsyncMock(return_value=b"x" * 11)
        with self.assertRaises(ValueError):
            await candidate.download(SimpleNamespace(size=11, read=read), limit=10)
        read.assert_not_awaited()
        with self.assertRaises(ValueError):
            await candidate.download(SimpleNamespace(size=1, read=read), limit=10)
        self.assertEqual(await candidate.download(SimpleNamespace(size=10, read=AsyncMock(return_value=b"x" * 10)), limit=10), b"x" * 10)

    async def test_timeout_applies_to_both_urls(self):
        async def slow(**kwargs):
            await asyncio.sleep(0.15)
            return b"late"
        for fallback in (False, True):
            calls = []
            async def read(**kwargs):
                calls.append(kwargs)
                if fallback and not kwargs:
                    raise candidate.DownloadHTTPError()
                return await slow(**kwargs)
            with self.assertRaises(asyncio.TimeoutError):
                await candidate.download(SimpleNamespace(size=1, read=read), timeout=0.01)
            self.assertEqual(len(calls), 2 if fallback else 1)

    async def test_non_http_errors_and_double_failure_propagate(self):
        for error in (RuntimeError(), candidate.DownloadHTTPError()):
            read = AsyncMock(side_effect=error)
            with self.assertRaises(type(error)):
                await candidate.download(SimpleNamespace(size=1, read=read))
            self.assertEqual(read.await_count, 2 if isinstance(error, candidate.DownloadHTTPError) else 1)
