from mock_server.settings import DATA_DIR
from mock_server.util import (
    generate_data,
    generate_from_request_data,
    read_json,
    validate_request_data,
    write_json,
)


def make_response_from_request_data(request_data, resource, strategy):
    base_data = get_base_data(resource, strategy=strategy)

    # Read config
    config = read_json(DATA_DIR.joinpath(f"{resource}.config.json"))

    # Additional resources on which to get info, if any
    depends_on = config.get("depends_on", "request_data")

    if depends_on != "request_data":
        request_data = read_json(DATA_DIR.joinpath(f"{depends_on}.json"))

    # Get request tree
    request_tree = config["request_tree"]

    # Get response overrides, if any
    response_overrides = config.get("response_overrides", None)

    # Generate data
    data = generate_from_request_data(
        request_data=request_data,
        response_data=base_data,
        request_tree=request_tree,
        response_overrides=response_overrides,
    )
    output_filename = f"{resource}.json"
    write_json(data, DATA_DIR.joinpath(output_filename))

    # Update dependent resources
    dependents = config.get("dependents", None)

    if dependents is not None:
        for resource in dependents:
            update_dependent_resource(resource, data)

    return data


def update_dependent_resource(resource, data):
    config = read_json(DATA_DIR.joinpath(f"{resource}.config.json"))
    response_data = read_json(DATA_DIR.joinpath(f"{resource}.json"))
    updated_data = generate_from_request_data(
        request_data=data,
        request_tree=config["request_tree"],
        response_data=response_data,
    )
    write_json(updated_data, DATA_DIR.joinpath(f"{resource}.json"))
    return updated_data


def make_response_from_static_data(resource, method):
    data = read_json(DATA_DIR.joinpath(f"{resource}.json"))
    if method == "POST":
        validate_request_data(resource, data)
    return data


def make_response_from_generator(resource, strategy):
    return generate_data(get_base_data(resource, strategy))


def get_base_data(resource, strategy):
    filename = (
        f"{resource}.struct.json"
        if strategy == "generate"
        else f"{resource}.response.json"
    )
    filepath = DATA_DIR.joinpath(filename)
    return read_json(filepath)
