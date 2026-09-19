import unittest

from main import extract_title

class TestMainFunctions(unittest.TestCase):

    def test_extract_title1(self):
        input = "### test 1"
        with self.assertRaises(Exception):
            extract_title(input)

    def test_extract_title2(self):
            input = " ## test 2"
            with self.assertRaises(Exception):
                extract_title(input)

    def test_extract_title3(self):
            input = "# test 3        "
            extract_title(input)
            expected = "test 3"
            self.assertEqual(result, expected)

    def test_extract_title4(self):
            input = "test 4"
    
            with self.assertRaises(Exception):
                extract_title(input)

    def test_extract_title3(self):
        input = """### test 1
normaler text
## test 2
#     test 3        
noch mehr text"""

        result = extract_title(input)
        expected = "test 3"
        self.assertEqual(result, expected)