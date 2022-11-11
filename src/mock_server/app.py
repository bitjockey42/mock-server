from flask import Flask, request
from pathlib import Path

from mock_server.util import read_json

ROOT_DIR = Path(__file__).parent.parent.parent

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<path:subpath>", methods=["POST"])
def callback(subpath):
    response = read_json(ROOT_DIR.joinpath("tmp", "test.json"))
    return response


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
