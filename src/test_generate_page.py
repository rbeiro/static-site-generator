import unittest

from utils.generate_page import generate_page


class TestGeneratePage(unittest.TestCase):
    def test_generate_page(self):
        generate_page("content/index.md", "template.html", "public/index.html")
        pass

if __name__ == "__init__":
    unittest.main()
