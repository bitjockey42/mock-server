from pathlib import Path

from flask import Flask, request
from flask_restful import Api

from json2xml import json2xml
from json2xml.utils import readfromjson

from mock_server.util import read_json

ROOT_DIR = Path(__file__).parent.parent.parent

app = Flask(__name__)
api = Api(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@api.representation("application/xml")
@app.route("/<path:subpath>", methods=["POST", "GET"])
def callback(subpath):
    resource = get_resource(subpath)
    json_filepath = ROOT_DIR.joinpath("tmp", f"{resource}.json")
    data = readfromjson(json_filepath)
    response = json2xml.Json2xml(data).to_xml()
    return response


def get_resource(subpath):
    parts = subpath.split("/")
    return parts[0]


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
