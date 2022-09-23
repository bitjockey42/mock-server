import json
from typing import Dict


def traverse(data: Dict, callback):
    """Traverse data and process"""
    traversed = {}

    for k, v in data.items():
        if isinstance(v, dict):
            traversed[k] = traverse(v, callback)
        else:
            traversed[k] = callback(v)

    return traversed


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(data, filename):
    with open(filename, "w+") as f:
        json.dump(data, f, indent=4)
