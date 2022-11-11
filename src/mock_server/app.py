from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<path:subpath>", methods=["POST"])
def callback(subpath):
    return f"{subpath}"


def start_app(host, port, debug):
    app.run(host=host, port=port, debug=debug)
