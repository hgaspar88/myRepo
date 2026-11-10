import unittest
from text_utils.slugify import slugify

class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")
        self.assertEqual(slugify("  HELLO   WORLD  "), "hello-world")

    def test_unicode(self):
        self.assertEqual(slugify("Café Münster"), "cafe-muenster")
        self.assertEqual(slugify("éññα日本語"), "éññα日本語")

    def test_hyphens(self):
        self.assertEqual(slugify("Hello---World"), "hello-world")
        self.assertEqual(slugify("--hello--"), "hello")
        self.assertEqual(slugify("-hello-"), "hello")

    def test_empty(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("   "), "")
        self.assertEqual(slugify("!@#$%^&*()"), "")

if __name__ == '__main__':
    unittest.main()
