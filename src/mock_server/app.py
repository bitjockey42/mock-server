import json
from pathlib import Path

from flask import Flask, request
from flask_restful import Api

from json2xml import json2xml
from json2xml.utils import readfromstring

from mock_server.util import generate_data, read_json

ROOT_DIR = Path(__file__).parent.parent.parent

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
    # Find structure file
    json_filepath = ROOT_DIR.joinpath("tmp", f"{resource}.struct.json")
    json_data = read_json(json_filepath)
    # Generate Data
    data = generate_data(json_data) 
    # Set response
    response = json2xml.Json2xml(data).to_xml()
    return response


def get_resource(subpath):
    parts = subpath.split("/")
    return parts[0]


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
