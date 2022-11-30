import json

import xmltodict

from pathlib import Path

from flask import Flask, request
from flask_restful import Api

from json2xml import json2xml

from mock_server.util import (
    generate_data,
    read_json,
    generate_from_request_data,
    validate_request_data,
    write_json,
)
from mock_server.settings import DATA_DIR, DATA_STRATEGY, DEFAULT_DATA_FORMAT

app = Flask(__name__)
api = Api(app)


@api.representation("application/xml")
@app.route("/<path:subpath>", methods=["POST", "GET"])
def callback(subpath):
    print(f"{request.method} {request.url}")

    request_data = None
    data_format = request.args.get("format", DEFAULT_DATA_FORMAT).lower()

    if request.data and data_format == "xml":
        request_data = xmltodict.parse(request.data.decode())
    elif request.data and data_format == "json":
        request_data = json.loads(request.data)

    resource = get_resource(subpath)
    response = make_response(
        request_data,
        resource,
        strategy=DATA_STRATEGY,
        method=request.method,
        data_format=data_format,
    )
    return response


def get_resource(subpath):
    parts = subpath.split("/")
    return parts[0]


def make_response(
    request_data,
    resource,
    strategy: str = DATA_STRATEGY,
    method="POST",
    data_format: str = DEFAULT_DATA_FORMAT,
):
    print(f"Resource: {resource}")
    print("----request------")
    print(request_data)

    filename = (
        f"{resource}.struct.json"
        if strategy == "generate"
        else f"{resource}.response.json"
    )
    filepath = DATA_DIR.joinpath(filename)

    response_data = read_json(filepath)

    if strategy == "generate":
        data = generate_data(response_data)
    elif strategy == "from_request":
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

        data = generate_from_request_data(
            request_data=request_data,
            response_data=response_data,
            request_tree=request_tree,
            response_overrides=response_overrides,
        )

        print("-----response-------")
        print(data)

        output_filename = f"{resource}.json"
        print(f"-----saving {output_filename}-----")
        write_json(data, DATA_DIR.joinpath(output_filename))
    elif strategy == "static":
        data = read_json(DATA_DIR.joinpath(f"{resource}.json"))
        if method == "POST":
            validate_request_data(resource, data)
    else:
        data = response_data

    if data_format == "json":
        return data

    return json2xml.Json2xml(data).to_xml()


def start_app(host, port, debug):
    print(
        f"""
        DEFAULT_DATA_FORMAT: {DEFAULT_DATA_FORMAT}
        DATA_DIR: {DATA_DIR}
        DATA_STRATEGY: {DATA_STRATEGY}
        """
    )
    app.run(host=host, port=port, debug=debug)
