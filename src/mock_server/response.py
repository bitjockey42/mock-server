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
    query_args: Dict = None,
):
    # Read config
    config = read_json(CONF_DIR.joinpath(f"{resource}.config.json"))
    has_identifier = bool(identifier)

    # Handlers
    handlers = {
        "POST": handle_update,
        "GET": handle_get if has_identifier else handle_get_list,
    }

    # Get handler
    handler = handlers.get(method, handle_update)

    return handler(
        resource,
        request_data,
        strategy,
        config,
        identifier=identifier,
        query_args=query_args,
    )


def handle_update(resource, request_data, strategy, config, *args, **kwargs):
    data, identifier = update_resource(resource, request_data, strategy, config)

    # Update dependent resources
    dependents = config.get("dependents", None)

    if dependents is not None:
        for resource in dependents:
            update_resource(resource, data, parent_identifier=identifier)

    return data


def handle_get(resource, request_data, strategy, config, identifier, query_args, *args, **kwargs):
    response = read_json(DATA_DIR.joinpath(resource, f"{identifier}.json"))

    if query_args:
        _embed = query_args.get("_embed")
        has_many = config.get("has_many")

        if _embed:
            _embed_list = handle_get_list(has_many, request_data, strategy, config, identifier)
            response[has_many] = _embed_list

    return response


def handle_get_list(
    resource, request_data, strategy, config, identifier, *args, **kwargs
):
    data_dir = DATA_DIR.joinpath(resource)

    response = []

    for filename in data_dir.glob("*.json"):
        response.append(read_json(filename))

    return response


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
