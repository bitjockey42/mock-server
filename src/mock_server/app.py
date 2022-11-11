from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<path:subpath>", methods=["POST"])
def callback(subpath):
    request_data = request.json
    response = request_data
    response["query_strings"] = request.args
    return response


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
