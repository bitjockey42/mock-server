from bottle import route, run


@route("/hello")
def hello():
    return "Hello World!"


def start_server(host, port, debug):
    run(host=host, port=port, debug=debug)
