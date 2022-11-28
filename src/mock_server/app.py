import os

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
from mock_server.settings import DATA_DIR, DATA_STRATEGY

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@api.representation("application/xml")
@app.route("/<path:subpath>", methods=["POST", "GET"])
def callback(subpath):
    request_args = request.args
    request_data = None

    if request.data:
        if request_args.get("format", "XML").upper() == "JSON":
            request_data = json2xml.Json2xml(request.data).to_xml()
        else: 
            request_data = xmltodict.parse(request.data.decode())

    resource = get_resource(subpath)
    response = make_response(
        request_data, resource, strategy=DATA_STRATEGY, method=request.method
    )
    return response


def get_resource(subpath):
    parts = subpath.split("/")
    return parts[0]


def make_response(request_data, resource, strategy: str = DATA_STRATEGY, method = "POST"):
    print(f"STRATEGY: {strategy}")

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

    return json2xml.Json2xml(data).to_xml()


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
