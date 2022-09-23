from bottle import request, route, run


@route("/hello")
def hello():
    return "Hello World!"


@route('/<resource>/<endpoint>', method='POST')
def callback(resource, endpoint):
    # TODO: Dynamically generate
    request_data = request.json
    return request_data


def start_server(host, port, debug):
    run(host=host, port=port, debug=debug)
