import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from app import download


class Smoke(unittest.IsolatedAsyncioTestCase):
    async def test_uses_original_url(self):
        attachment = SimpleNamespace(size=3, read=AsyncMock(return_value=b"pdf"))
        self.assertEqual(await download(attachment), b"pdf")
        attachment.read.assert_awaited_once_with()
