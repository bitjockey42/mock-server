from datetime import datetime

from mock_server import util


class FakeDataType:
    def __init__(self) -> None:
        pass


def callback(value):
    return type(value)


def test_traverse_empty():
    assert util.traverse({}, callback) == {}


def test_traverse_simple():
    data = {
        "author": "E.M. Forster",
        "age": 48,
    }
    expected = {"author": str, "age": int}
    assert util.traverse(data, callback) == expected


def test_traverse_nested():
    data = {
        "author": "E.M. Forster",
        "age": 48,
        "metadata": {"code": "abc1234", "data": {"number": "twelve"}},
    }
    expected = {
        "author": str,
        "age": int,
        "metadata": {"code": str, "data": {"number": str}},
    }
    assert util.traverse(data, callback) == expected


def test_traverse_datetime():
    data = {"name": "Maurice Hall", "dob": datetime(1898, 10, 1)}
    expected = {"name": str, "dob": datetime}
    assert util.traverse(data, callback) == expected


def test_traverse_custom_datatype():
    data = {
        "name": "Maurice Hall",
        "dob": datetime(1898, 10, 1),
        "fakedata": FakeDataType(),
    }
    expected = {"name": str, "dob": datetime, "fakedata": FakeDataType}
    assert util.traverse(data, callback) == expected
