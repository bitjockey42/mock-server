from typing import Dict


def traverse(data: Dict):
    """Traverse data and determine types"""
    traversed = {}

    for k, v in data.items():
        traversed[k] = type(v)

    return traversed
