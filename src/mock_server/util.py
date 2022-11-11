import json
import re
from typing import Dict

from mock_server.provider import fake


def generate_structure_from_file(
    input_filename: str,
    output_filename: str = None,
):
    data = read_json(input_filename)
    return generate_structure(data, output_filename)


def generate_structure(data: Dict, output_filename: str = None):
    traversed = traverse(data)

    if output_filename:
        write_json(traversed, output_filename)

    return traversed


def traverse(data: Dict, callback=None):
    """Traverse data and process"""
    if callback is None:
        callback = lambda key, value: determine_type(key, value)

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
    key = to_snake_case(key)

    return {
        "type": type_name,
        "generator": get_generator(key),
    }


def get_generator(key, type_name=None):
    # Date/Time
    if any([
        "date" in key,
        "period" in key,
    ]):
        if type_name == "int":
            return "iso8601"
        return "date_time"

    try:
        generator = getattr(fake, key)
        generator_name = generator.__name__
    except AttributeError:
        generator_name = None
    
    return generator_name


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(data, filename):
    with open(filename, "w+") as f:
        json.dump(data, f, indent=4)


def to_snake_case(name):
    # https://stackoverflow.com/a/1176023
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()
