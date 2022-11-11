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
@app.route("/<path:subpath>", methods=["POST"])
def callback(subpath):
    json_filename = ROOT_DIR.joinpath("tmp", "test.json")
    data = readfromjson(json_filename)
    response = json2xml.Json2xml(data).to_xml()
    return response


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
