import click

from mock_server.server import start_server


@click.group()
def cli():
    """Mock server for testing"""
    pass


@cli.command()
@click.option("-H", "--host", default="localhost")
@click.option("-P", "--port", default=8080)
@click.option("-D", "--debug/--no-debug", default=False)
def start(host, port, debug):
    start_server(host, port, debug)
