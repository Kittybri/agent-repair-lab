import asyncio


class DownloadHTTPError(Exception):
    pass


async def download(attachment, limit=20 * 1024 * 1024, timeout=1):
    if attachment.size > limit:
        raise ValueError("File exceeds size limit")
    try:
        data = await asyncio.wait_for(attachment.read(), timeout=timeout)
    except DownloadHTTPError:
        data = await asyncio.wait_for(attachment.read(use_cached=True), timeout=timeout)
    if len(data) > limit:
        raise ValueError("File exceeds size limit")
    return data
