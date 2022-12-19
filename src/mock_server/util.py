import json
import re
from typing import Dict

from mock_server.provider import fake
from mock_server.settings import CONF_DIR


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


def generate_data_from_file(
    input_filename: str,
    output_filename: str = None,
):
    data = read_json(input_filename)
    return generate_data(data, output_filename)


def generate_data(data: Dict, output_filename: str = None):
    generated = traverse(data, callback=generate_value)

    if output_filename:
        write_json(generated, output_filename)

    return generated


def generate_value(key, value):
    if value.get("default"):
        return value["default"]

    if value.get("generator") is None:
        return None

    generator = getattr(fake, value["generator"])

    max_length = value.get("max_length")
    if max_length is not None:
        return generator(max_length)

    return generator()


def traverse(data: Dict, callback=None, *args, **kwargs):
    """Traverse data and process"""
    if callback is None:
        callback = lambda key, value: determine_type(key, value)

    traversed = {}

    for k, v in data.items():
        if isinstance(v, dict) and "generator" not in v:
            traversed[k] = traverse(v, callback, *args, **kwargs)
        else:
            traversed[k] = callback(key=k, value=v, *args, **kwargs)

    return traversed


def generate_from_request_data(
    request_data: Dict,
    response_data: Dict,
    config: Dict,
    should_override: bool = True,
):
    # Get request tree
    request_tree = config["request_tree"]

    # Traverse through request data
    request_data = process_request(request_data, request_tree)

    # Construct the response_data by making any necessary modifictions
    response_data = modify_response(
        response_data, config["request_tree"], check_value=True
    )

    # Get response overrides, if any
    response_overrides = config.get("response_overrides", None)
    if should_override and response_overrides:
        response_data = modify_response(
            response_data,
            response_overrides,
            check_value=False,
            callback_fn=generate_value,
        )

    identifier = get_identifier(response_data, config)

    return response_data, identifier


def process_request(request_data, request_tree):
    for node in request_tree:
        request_value = request_data

        for key in node["request_keys"]:
            request_value = request_value.get(key, None)
            if request_value is None and node.get("required", True):
                raise AttributeError(f"{key} not found in request")

        node["value"] = request_value

    return request_data


def modify_response(
    response_data, config_setting, check_value: bool = True, callback_fn=None
):
    # Traverse the base response data
    for node in config_setting:
        res = response_data

        if check_value and "value" not in node:
            continue

        for key in node["response_keys"]:
            if key in res and isinstance(res[key], Dict):
                res = res[key]

        res[key] = callback_fn(key, node) if callback_fn else node["value"]

    return response_data


def get_identifier(data, config):
    identifier = None

    res = data

    for key in config.get("identifier", []):
        if key not in res:
            break

        if isinstance(res[key], Dict):
            res = res[key]
        else:
            identifier = res[key]

    return identifier


def validate_request_data(resource: str, request_data: Dict):
    config_filename = CONF_DIR.joinpath(f"{resource}.config.json")
    config = read_json(config_filename)
    request_tree = config["request_tree"]

    for node in request_tree:
        request_value = request_data

        for key in node["request_keys"]:
            request_value = request_value.get(key, None)
            if request_value is None and node.get("required", True):
                raise AttributeError(f"{key} not found in request")


def determine_type(key, value):
    """Infer Faker provider type from key name"""
    type_name = type(value).__name__
    key = to_snake_case(key)
    length = get_length(value)

    return {
        "required": type_name != "NoneType",
        "type": type_name,
        "generator": get_generator(key, type_name),
        "length": length,
    }


def get_length(value):
    try:
        length = len(value)
    except TypeError:
        length = None

    return length


def get_generator(key, type_name=None):
    key_parts = key.split("_")

    if "id" in key_parts[-1].lower():
        return "numerify"

    # Date/Time
    if any(
        [
            "date" in key,
            "period" in key,
        ]
    ):
        if type_name == "int":
            return "unix_time"
        return "iso8601"

    # Address
    if "address1" in key:
        return "street_address"

    if "number" in key and key != "phone_number":
        return "random_number"

    generator_name = None

    try:
        generator = getattr(fake, key)
        generator_name = generator.__name__
    except AttributeError:
        if type_name == "str":
            generator_name = "lexify"
        elif type_name == "int":
            generator_name = "numerify"

    return generator_name


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(data, filename):
    with open(filename, "w+") as f:
        json.dump(data, f, indent=4)


def to_snake_case(name):
    # https://stackoverflow.com/a/1176023
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()
