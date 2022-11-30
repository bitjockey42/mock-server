import json

import xmltodict

from pathlib import Path

from flask import Flask, request
from flask_restful import Api

from json2xml import json2xml

from mock_server.response import (
    get_base_data,
    make_response_from_generator,
    make_response_from_request_data,
)
from mock_server.util import (
    read_json,
    validate_request_data,
)
from mock_server.settings import DATA_DIR, DATA_STRATEGY, DEFAULT_DATA_FORMAT

app = Flask(__name__)
api = Api(app)


@api.representation("application/xml")
@app.route("/<path:subpath>", methods=["POST", "GET"])
def callback(subpath):
    resource = get_resource(subpath)

    print(f"RESOURCE: ({resource}) {request.method} {request.url}")

    request_data = None
    data_format = request.args.get("format", DEFAULT_DATA_FORMAT).lower()

    if request.data and data_format == "xml":
        request_data = xmltodict.parse(request.data.decode())
    elif request.data and data_format == "json":
        request_data = json.loads(request.data)

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
    if strategy == "generate":
        data = make_response_from_generator(resource=resource, strategy=strategy)
    elif strategy == "from_request":
        data = make_response_from_request_data(request_data, resource, strategy)
    elif strategy == "static":
        data = read_json(DATA_DIR.joinpath(f"{resource}.json"))
        if method == "POST":
            validate_request_data(resource, data)
    else:
        data = get_base_data(resource, strategy)

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
