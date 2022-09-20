import unittest

import util


class TestTraversalMethod(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(util.traverse({}), {})
    
    def test_simple(self):
        data = {"name": "E.M. Forster"}
        expected = {"name": str}
        self.assertEqual(util.traverse(data), expected)


if __name__ == "__main__":
    unittest.main()
