import json

import xmltodict

from pathlib import Path

from flask import Flask, request
from flask_restful import Api

from json2xml import json2xml
from json2xml.utils import readfromstring

from mock_server.util import (
    generate_data,
    read_json,
    generate_from_request_data,
    write_json,
)
from mock_server.settings import DATA_DIR

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@api.representation("application/xml")
@app.route("/<path:subpath>", methods=["POST", "GET"])
def callback(subpath):
    request_data = None

    if request.data:
        request_data = xmltodict.parse(request.data.decode())

    resource = get_resource(subpath)
    response = make_response(request_data, resource, strategy="from_request")
    return response


def get_resource(subpath):
    parts = subpath.split("/")
    return parts[0]


def make_response(request_data, resource, strategy: str = "from_request"):
    print(f"Resource: {resource}")
    print("----request------")
    print(request_data)

    filename = (
        f"{resource}.struct.json" if strategy == "generate" else f"{resource}.json"
    )
    filepath = DATA_DIR.joinpath(filename)

    response_data = read_json(filepath)

    if strategy == "generate":
        data = generate_data(response_data)
    elif strategy == "from_request":
        request_tree = read_json(DATA_DIR.joinpath(f"{resource}.request.tree.json"))
        data = generate_from_request_data(
            request_data=request_data,
            response_data=response_data,
            request_tree=request_tree,
        )
        print("-----response-------")
        print(data)

        print("-----saving-----")
        write_json(data, filename)
    else:
        data = response_data

    return json2xml.Json2xml(data).to_xml()


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
