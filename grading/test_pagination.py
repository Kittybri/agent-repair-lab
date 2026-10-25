import unittest
import candidate

GROUPS = (("present", "challenge", "foundation", "recent past"),
          ("possibility", "near future", "your stance"),
          ("environment", "hopes and fears", "likely outcome"))


def sections():
    return {name: f"{name}: a complete interpretation." for group in GROUPS for name in group}


class Checks(unittest.TestCase):
    def test_three_ordered_messages_ignore_dict_insertion_order(self):
        data = sections()
        result = candidate.paginate(dict(reversed(list(data.items()))))
        self.assertEqual(result, ["\n".join(data[name] for name in group) for group in GROUPS])

    def test_text_preserved_and_boundary_is_allowed(self):
        data = sections()
        data["possibility"] = "Possibility: \u03b1\u03b2\u03b3 and a complete final sentence."
        expected = ["\n".join(data[name] for name in group) for group in GROUPS]
        self.assertEqual(candidate.paginate(data, limit=max(map(len, expected))), expected)

    def test_overflow_raises_instead_of_truncating(self):
        data = sections()
        data["likely outcome"] = "x" * 2001
        with self.assertRaises(ValueError):
            candidate.paginate(data)
        with self.assertRaises(ValueError):
            candidate.paginate(sections(), limit=0)

    def test_missing_empty_and_unexpected_sections_fail(self):
        for name in [n for group in GROUPS for n in group]:
            data = sections()
            data.pop(name)
            with self.assertRaises(ValueError):
                candidate.paginate(data)
        for data in (dict(sections(), present=" "), dict(sections(), bonus="extra")):
            with self.assertRaises(ValueError):
                candidate.paginate(data)
