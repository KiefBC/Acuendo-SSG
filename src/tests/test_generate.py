import os
import unittest

from src.generate import extract_title, generate_page
from src.main import delete_dir_files


class TestGenerate(unittest.TestCase):
    def test_heading_1(self):
        some = "# Hello"
        expected = "Hello"
        manipulated = extract_title(some)
        self.assertEqual(manipulated, expected)

    def test_heading_2(self):
        some = "### Hello"
        expected = "Hello"
        manipulated = extract_title(some)
        self.assertEqual(manipulated, expected)

    def test_wrong_heading(self):
        some = "* Hello"
        self.assertRaises(Exception, extract_title, some)

    def test_generate_page(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))

        md_path = os.path.abspath(os.path.join(test_dir, "../../content/index.md"))
        template_path = os.path.abspath(os.path.join(test_dir, "../../template.html"))
        dest_path = os.path.abspath(
            os.path.join(test_dir, "../../public/test_index.html")
        )
        generate_page(md_path, template_path, dest_path)
        self.assertTrue(os.path.exists(dest_path))
        os.remove(dest_path)  # Clean up the test file
        self.assertFalse(os.path.exists(dest_path))

    def test_generate_page_from_directory(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))

        # Use the content directory instead of a specific file
        content_dir = os.path.abspath(os.path.join(test_dir, "../../content"))
        template_path = os.path.abspath(os.path.join(test_dir, "../../template.html"))
        dest_path = os.path.abspath(
            os.path.join(test_dir, "../../public/test_dir_index.html")
        )
        generate_page(content_dir, template_path, dest_path)
        self.assertTrue(os.path.exists(dest_path))
        os.remove(dest_path)  # Clean up the test file
        self.assertFalse(os.path.exists(dest_path))
