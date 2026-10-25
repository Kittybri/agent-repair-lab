import asyncio


class DownloadHTTPError(Exception):
    pass


async def download(attachment, limit=20 * 1024 * 1024, timeout=1):
    return await attachment.read(use_cached=True)
