import subprocess
import sys
import unittest
import candidate


class Checks(unittest.TestCase):
    def test_explicit_address_overrides_reply(self):
        for bot, other in (("scaramouche", "wanderer"), ("wanderer", "scaramouche")):
            self.assertEqual(candidate.owner(10, addressed=bot, reply_to=other), bot)

    def test_reply_and_solo_routing(self):
        for bot in ("scaramouche", "wanderer"):
            self.assertEqual(candidate.owner(91, reply_to=bot), bot)
            self.assertEqual(candidate.owner(92, solo=bot), bot)

    def test_channel_block_has_highest_priority(self):
        for bot in ("scaramouche", "wanderer"):
            self.assertIsNone(candidate.owner(77, addressed=bot, reply_to=bot, solo=bot, blocked=True))

    def test_ambient_is_stable_across_processes_and_not_constant(self):
        ids = [1, 2, 3, 100, 999, 123456789, 9007199254740993]
        expected = [candidate.owner(i) for i in ids]
        self.assertEqual(set(expected), {"scaramouche", "wanderer"})
        code = "import importlib.util,json; s=importlib.util.spec_from_file_location('x'," + repr(candidate.__file__) + "); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(json.dumps([m.owner(i) for i in " + repr(ids) + "]))"
        import json
        for _ in range(2):
            result = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, check=True, timeout=3)
            self.assertEqual(json.loads(result.stdout), expected)
