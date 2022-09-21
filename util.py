from typing import Dict


def traverse(data: Dict):
    """Traverse data and determine types"""
    traversed = {}

    for k, v in data.items():
        if isinstance(v, dict):
            traversed[k] = traverse(v)
        else:
            traversed[k] = type(v)

    return traversed
