import json
from typing import Dict

import xmltodict

from pathlib import Path

from flask import Flask, request
from flask_restful import Api

from json2xml import json2xml

from mock_server.response import (
    load_base_response,
    make_response_from_generator,
    make_response_from_request_data,
)
from mock_server.util import (
    read_json,
    validate_request_data,
)
from mock_server.settings import CONF_DIR, DATA_STRATEGY, DEFAULT_DATA_FORMAT, DATA_DIR

app = Flask(__name__)
api = Api(app)


@api.representation("application/xml")
@app.route("/<path:subpath>", methods=["POST", "GET", "PATCH"])
def callback(subpath):
    subpath_mapping = get_subpath_mapping(subpath)
    resource = subpath_mapping.get("resource")

    print(f"RESOURCE: {resource}")

    request_data = None
    data_format = request.args.get("format", DEFAULT_DATA_FORMAT).lower()

    if request.data and data_format == "xml":
        request_data = xmltodict.parse(request.data.decode())
    elif request.data and data_format == "json":
        request_data = json.loads(request.data)

    query_args = request.args
    print(f"QUERY ARGS: {query_args}")

    response = make_response(
        request_data,
        resource,
        strategy=DATA_STRATEGY,
        method=request.method,
        data_format=data_format,
        subpath_mapping=subpath_mapping,
        query_args=query_args
    )
    return response


def get_resource(subpath):
    return get_subpath_mapping(subpath).get("resource")


def get_subpath_mapping(subpath):
    parts = subpath.split("/")
    mapping = {}

    if not parts:
        return mapping

    routes_config = read_json(CONF_DIR.joinpath("routes.config.json"))
    subpath_keys = routes_config.get("subpath_keys")

    for i, part in enumerate(parts):
        mapping[subpath_keys[i]] = part

    return mapping


def make_response(
    request_data,
    resource,
    strategy: str = DATA_STRATEGY,
    method="POST",
    data_format: str = DEFAULT_DATA_FORMAT,
    subpath_mapping: Dict = None,
    query_args: Dict = None,
):
    if strategy == "generate":
        data = make_response_from_generator(resource=resource, strategy=strategy)
    elif strategy == "from_request":
        identifier = subpath_mapping.get("identifier")
        data = make_response_from_request_data(
            request_data,
            resource,
            strategy=strategy,
            method=method,
            identifier=identifier,
            query_args=query_args,
        )
        if method == "POST":
            validate_request_data(resource, data)
    else:
        data = load_base_response(resource, strategy)

    if data_format == "json":
        return data

    return json2xml.Json2xml(data).to_xml()


def start_app(host, port, debug):
    print(
        f"""
        DEFAULT_DATA_FORMAT: {DEFAULT_DATA_FORMAT}
        CONF_DIR: {CONF_DIR}
        DATA_DIR: {DATA_DIR}
        DATA_STRATEGY: {DATA_STRATEGY}
        """
    )
    app.run(host=host, port=port, debug=debug)
