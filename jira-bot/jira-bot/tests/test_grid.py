"""Grid helper tests. Need pandas, so run them with the web venv: python tests/test_grid.py"""
import unittest

import helpers  # noqa: F401

try:
    import pandas  # noqa: F401
except ImportError:  # pragma: no cover
    pandas = None

from jirabot.reviews import Annotation, Review


@unittest.skipIf(pandas is None, "pandas not installed (pip install -r requirements-web.txt)")
class GridTests(unittest.TestCase):
    def setUp(self):
        from jirabot.web import grid
        self.grid = grid
        self.review = Review(name="r", jql="q", columns=["summary", "key", "status", "priority"], hidden=["priority"])
        self.rows = [
            {"key": "ABC-1", "summary": "Login broken", "status": "To Do", "priority": "High"},
            {"key": "ABC-2", "summary": "Typo", "status": "Done", "priority": "Low"},
            {"key": "ABC-3", "summary": "Slow search", "status": "To Do", "priority": "Low"},
        ]
        self.anns = {"ABC-2": Annotation("Move out", "after release"), "ABC-3": Annotation("", "look at this")}

    def test_columns_key_first_and_hidden_removed(self):
        f = self.grid.build_frame(self.review, self.rows, self.anns, "x.atlassian.net")
        self.assertEqual(list(f.df.columns), ["Pick", "Mark", "Note", "key", "summary", "status"])
        self.assertEqual(f.df.loc[0, "key"], "https://x.atlassian.net/browse/ABC-1")
        self.assertEqual(f.keys, ["ABC-1", "ABC-2", "ABC-3"])
        self.assertIn("Move out", f.df.loc[1, "Mark"])
        self.assertTrue(f.df.loc[0, "Mark"] is None or f.df.loc[0, "Mark"] != f.df.loc[0, "Mark"])

    def test_no_site_keeps_plain_key(self):
        f = self.grid.build_frame(self.review, self.rows, {}, "")
        self.assertEqual(f.df.loc[0, "key"], "ABC-1")

    def test_search_covers_notes_and_marks_filter(self):
        f = self.grid.build_frame(self.review, self.rows, self.anns, "", search="look at")
        self.assertEqual(f.keys, ["ABC-3"])
        self.assertEqual(f.total, 3)
        f = self.grid.build_frame(self.review, self.rows, self.anns, "", mark_filter=["Move out"])
        self.assertEqual(f.keys, ["ABC-2"])
        f = self.grid.build_frame(self.review, self.rows, self.anns, "", mark_filter=[self.grid.UNMARKED])
        self.assertEqual(f.keys, ["ABC-1", "ABC-3"])

    def test_parse_edits_maps_positions_to_keys_after_filtering(self):
        f = self.grid.build_frame(self.review, self.rows, self.anns, "", mark_filter=["Move out", self.grid.UNMARKED])
        label = self.review.label_for("Not doing")
        changes, picked = self.grid.parse_edits(
            {"edited_rows": {"0": {"Mark": label, "Pick": True}, 1: {"Note": "  hi  "}, "9": {"Note": "x"}}}, f.keys, self.review
        )
        self.assertEqual(changes, {"ABC-1": {"mark": "Not doing"}, "ABC-2": {"note": "hi"}})
        self.assertEqual(picked, ["ABC-1"])

    def test_clearing_a_mark_and_junk_input(self):
        changes, _ = self.grid.parse_edits({"edited_rows": {"0": {"Mark": None, "Note": None}}}, ["ABC-1"], self.review)
        self.assertEqual(changes, {"ABC-1": {"mark": "", "note": ""}})
        self.assertEqual(self.grid.parse_edits(None, ["a"], self.review), ({}, []))
        self.assertEqual(self.grid.parse_edits({"edited_rows": {"x": {"Note": "a"}, "0": "bad"}}, ["a"], self.review), ({}, []))

    def test_styler_tints_marked_rows_only(self):
        f = self.grid.build_frame(self.review, self.rows, self.anns, "")
        html = self.grid.tint_styler(f.df, self.review).to_html()
        self.assertIn("background-color", html)
        self.assertEqual(html.count("rgba"), 1)  # one tint rule, for the single marked row
        none = self.grid.build_frame(self.review, self.rows, {}, "")
        self.assertNotIn("rgba", self.grid.tint_styler(none.df, self.review).to_html())


if __name__ == "__main__":
    unittest.main()
