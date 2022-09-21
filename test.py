import unittest

from datetime import datetime

import util


class FakeDataType:
    def __init__(self) -> None:
        pass


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

    def test_datetime(self):
        data = {
            "name": "Maurice Hall",
            "dob": datetime(1898, 10, 1)
        }
        expected = {
            "name": str,
            "dob": datetime
        }
        self.assertEqual(util.traverse(data), expected)

    def test_custom_datatype(self):
        data = {
            "name": "Maurice Hall",
            "dob": datetime(1898, 10, 1),
            "fakedata": FakeDataType()
        }
        expected = {
            "name": str,
            "dob": datetime,
            "fakedata": FakeDataType
        }
        self.assertEqual(util.traverse(data), expected)


if __name__ == "__main__":
    unittest.main()
