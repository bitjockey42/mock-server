import json
from typing import Dict

from faker import Faker


def traverse(data: Dict, callback):
    """Traverse data and process"""
    traversed = {}

    for k, v in data.items():
        if isinstance(v, dict):
            traversed[k] = traverse(v, callback)
        else:
            traversed[k] = callback(key=k, value=v)

    return traversed


def determine_type(key, value):
    """Infer Faker provider type from key name"""
    type_name = type(value).__name__
    return {
        "type": type_name,
        "provider": get_provider(key, type_name),
    }


def get_provider(key, type_name):
    if any([
        "date" in key.lower(),
        "period" in key.lower(),
    ]):
        if type_name == "int":
            return "iso8601"
        return "date_time"

    if "email" in key.lower():
        return "email"

    return None


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(data, filename):
    with open(filename, "w+") as f:
        json.dump(data, f, indent=4)
