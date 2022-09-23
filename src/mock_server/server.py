from bottle import route, run


@route("/hello")
def hello():
    return "Hello World!"


@route('/<resource>/<endpoint>')
def callback(resource, endpoint):
    # TODO: Dynamically generate
    return f"{resource} - {endpoint}"


def start_server(host, port, debug):
    run(host=host, port=port, debug=debug)
