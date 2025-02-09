import unittest
from diff_finder.diff_finder import DiffFinder, DiffReason

class TestDiffFinder(unittest.TestCase):
    
    def test__basic(self):
        diffs = DiffFinder.find_diffs({"a": 12}, {"a": "a"})
        self.assertEqual([
            DiffReason(description="a=12 != b='a'", path=".a")
        ], diffs)

    def test__nested(self):
        a = {
            "status": 200,
            "body": {
                "list": [
                    {"key": "a", "count": 20},
                    {"key": "b", "count": 20},
                    {"key": "c", "count": 20},
                ],
                "bool": True,
                "nested": {"a": {"b": {"c": "d"}}},
            }
        }
        b = {
            "status": 400,
            "body": {
                "list": [
                    {"key": "x", "count": 10},
                    {"key": "b", "count": 10},
                    {"key": "c", "count": "undefined"},
                ],
                "bool": False,
                "nested": {"a": {"b": {"c": "x"}}},
            }
        }

        expected_diffs = [
            DiffReason(description="a=200 != b=400", path=".status"),
            DiffReason(description="a='a' != b='x'", path=".body.list[0].key"),
            DiffReason(description="a=20 != b=10", path=".body.list[0].count"),
            DiffReason(description="a=20 != b=10", path=".body.list[1].count"),
            DiffReason(description="a=20 != b='undefined'", path=".body.list[2].count"),
            DiffReason(description="a='d' != b='x'", path=".body.nested.a.b.c"),
            DiffReason(description="a=True != b=False", path=".body.bool"),
        ]
        diffs = DiffFinder.find_diffs(a, b)
        
        self.assertCountEqual(expected_diffs, diffs)
