from typing import Dict

from mock_server.settings import CONF_DIR, DATA_DIR
from mock_server.util import (
    generate_data,
    generate_from_request_data,
    read_json,
    validate_request_data,
    write_json,
)


def make_response_from_request_data(
    request_data,
    resource,
    strategy: str = None,
    method: str = "GET",
    identifier=None,
):
    # Read config
    config = read_json(CONF_DIR.joinpath(f"{resource}.config.json"))

    # Handlers
    handlers = {
        "POST": handle_update,
        "GET": handle_get,
    }

    # Get handler
    handler = handlers.get(method, handle_update)

    return handler(resource, request_data, strategy, config, identifier=identifier)


def handle_update(resource, request_data, strategy, config, *args, **kwargs):
    data, identifier = update_resource(resource, request_data, strategy, config)

    # Update dependent resources
    dependents = config.get("dependents", None)

    if dependents is not None:
        for resource in dependents:
            update_resource(resource, data, parent_identifier=identifier)

    return data


def handle_get(resource, request_data, strategy, config, identifier, *args, **kwargs):
    return read_json(DATA_DIR.joinpath(resource, f"{identifier}.json"))


def update_resource(
    resource,
    request_data,
    strategy: str = None,
    config: Dict = None,
    parent_identifier=None,
):
    if not config:
        # Read config
        config = read_json(CONF_DIR.joinpath(f"{resource}.config.json"))

    # Additional resources on which to get info, if any
    depends_on = config.get("depends_on", "request_data")

    if depends_on != "request_data":
        request_data = read_json(
            DATA_DIR.joinpath(
                depends_on,
                f"{parent_identifier}.json",
            ),
        )

    # Load base response data
    response_data = load_base_response(resource, strategy=strategy)

    updated_data, identifier = generate_from_request_data(
        request_data=request_data,
        response_data=response_data,
        config=config,
    )

    print(f"{resource} identifier: {identifier}")
    output_dir = DATA_DIR.joinpath(resource)

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    output_filename = output_dir.joinpath(f"{identifier}.json")
    write_json(updated_data, output_filename)

    return updated_data, identifier


def make_response_from_static_data(resource, method):
    data = read_json(DATA_DIR.joinpath(f"{resource}.json"))
    if method == "POST":
        validate_request_data(resource, data)
    return data


def make_response_from_generator(resource, strategy):
    return generate_data(load_base_response(resource, strategy))


def load_base_response(resource, strategy: str = None):
    filename = (
        f"{resource}.struct.json"
        if strategy == "generate"
        else f"{resource}.response.json"
    )
    filepath = CONF_DIR.joinpath(filename)
    return read_json(filepath)
