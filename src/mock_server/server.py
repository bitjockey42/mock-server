from bottle import request, route, run


@route("/hello")
def hello():
    return "Hello World!"


@route('/<resource>/<endpoint>', method='POST')
def callback(resource, endpoint):
    # TODO: Dynamically generate
    request_data = request.json
    response = request_data
    response["query_strings"] = request.query_string
    response["query"] = dict(request.query)
    return response


def start_server(host, port, debug):
    run(host=host, port=port, debug=debug)
