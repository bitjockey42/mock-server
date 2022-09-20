import unittest

import util


class TestTraversalMethod(unittest.TestCase):
    def test_traverse_simple(self):
        self.assertEqual(util.traverse({}), {})


if __name__ == "__main__":
    unittest.main()
