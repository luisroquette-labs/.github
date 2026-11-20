import unittest

from scripts.check_comments import comment_lines


class CommentLinesTest(unittest.TestCase):
    def test_comment(self):
        self.assertEqual(comment_lines("<svg>\n<!-- old -->\n</svg>"), [2])

    def test_url_and_svg_markup(self):
        self.assertEqual(comment_lines('<svg xmlns="http://www.w3.org/2000/svg"/>'), [])


if __name__ == "__main__":
    unittest.main()
