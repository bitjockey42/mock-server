import unittest

import util


class TestTraversalMethod(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(util.traverse({}), {})
    
    def test_simple(self):
        data = {
            "author": "E.M. Forster",
            "age": 48,
        }
        expected = {"author": str, "age": int}
        self.assertEqual(util.traverse(data), expected)

    def test_nested(self):
        data = {
            "author": "E.M. Forster",
            "age": 48,
            "metadata": {
                "code": "abc1234",
                "data": {
                    "number": "twelve"
                }
            }
        }
        expected = {
            "author": str,
            "age": int,
            "metadata": {
                "code": str,
                "data": {
                    "number": str
                }
            }
        }
        self.assertEqual(util.traverse(data), expected)


if __name__ == "__main__":
    unittest.main()
