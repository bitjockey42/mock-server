import json

from pathlib import Path

from flask import Flask, request
from flask_restful import Api

from json2xml import json2xml
from json2xml.utils import readfromstring

from mock_server.util import generate_data, read_json
from mock_server.settings import DATA_DIR

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@api.representation("application/xml")
@app.route("/<path:subpath>", methods=["POST", "GET"])
def callback(subpath):
    # Get the data structure
    resource = get_resource(subpath)
    response = make_response(resource)
    return response


def get_resource(subpath):
    parts = subpath.split("/")
    return parts[0]


def make_response(resource, should_generate: bool = False):
    filename = f"{resource}.struct.json" if should_generate else f"{resource}.json"
    filepath = DATA_DIR.joinpath(filename)

    if should_generate:
        data = generate_data(read_json(filepath))
    else:
        data = read_json(filepath)

    return json2xml.Json2xml(data).to_xml()


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
