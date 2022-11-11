from bottle import request, route, run

from mock_server import settings


callback_path = f"{settings.BASE_API_PATH}/<resource>/<endpoint>"
# "/".join(["resource", "endpoint"])


@route("/hello")
def hello():
    return "Hello World!"


@route(callback_path, method="POST")
def callback(resource, endpoint):  # this could also be dynamically generated
    request_data = request.json
    response = request_data
    response["query_strings"] = request.query_string
    response["query"] = dict(request.query)
    # response.headers['Content-Type'] = 'xml/application'
    return response


def start_server(host, port, debug):
    print("callback_path", callback_path)
    run(host=host, port=port, debug=debug)
