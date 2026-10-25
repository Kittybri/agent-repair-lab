"""A deterministic, synthetic walkthrough of the five reference contracts."""

import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent


def reference(task):
    spec = importlib.util.spec_from_file_location(task, ROOT / "tasks" / task / "reference" / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def main():
    print("Synthetic offline demonstration; no AI generation or live Discord calls.\n")
    attachment = reference("attachment")
    async def read(**kwargs):
        if kwargs.get("use_cached"):
            raise attachment.DownloadHTTPError("Cached endpoint unavailable")
        return b"synthetic study material"
    data = await attachment.download(SimpleNamespace(size=24, read=read))
    print("Attachment: original endpoint returned", len(data), "bytes.")
    routing = reference("routing")
    print("Routing: a direct call to Wanderer belongs to", routing.owner(10, addressed="wanderer"))
    voice = reference("voice")
    print("Voice: silence plus a nonempty transcript is accepted:", voice.accept_audio(bytes(3840), "I can hear you", []))
    memory = reference("memory")
    bank = {}
    memory.remember(bank, user_id=1, author_id=1, message_id=10, text="Likes green", confidence=0.9)
    print("Memory: a different user recalls", len(memory.recall(bank, 2)), "private facts.")
    pagination = reference("pagination")
    sections = {name: name + ": synthetic complete interpretation." for group in pagination.GROUPS for name in group}
    print("Delivery: ten sections become", len(pagination.paginate(sections)), "complete ordered messages.")


if __name__ == "__main__":
    asyncio.run(main())
