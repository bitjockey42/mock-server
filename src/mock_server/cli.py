import click

from mock_server.app import start_app
from mock_server.server import start_server
from mock_server.util import generate_structure_from_file, generate_data_from_file


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


@cli.command()
@click.option("-H", "--host", default="localhost")
@click.option("-P", "--port", default=8080)
@click.option("-D", "--debug/--no-debug", default=False)
def app(host, port, debug):
    start_app(host, port, debug)


@cli.command()
@click.argument("input_filename", type=click.Path(exists=True))
@click.option("-o", "--output-filename", type=click.Path(exists=False))
def generate(input_filename, output_filename):
    generate_structure_from_file(input_filename, output_filename)


@cli.command()
@click.argument("input_filename", type=click.Path(exists=True))
@click.option("-o", "--output-filename")
def generate_data(input_filename, output_filename):
    generate_data_from_file(input_filename, output_filename)