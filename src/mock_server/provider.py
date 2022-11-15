import importlib

from faker import Faker


def get_provider(key):
    try:
        module = importlib.import_module(f"faker.providers.{key}")
        provider = module.Provider
    except (ImportError, AttributeError):
        raise ValueError(f"No provider for {key}")

    return provider


fake = Faker()
