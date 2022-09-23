from typing import Dict


def traverse(data: Dict, callback):
    """Traverse data and process"""
    traversed = {}

    for k, v in data.items():
        if isinstance(v, dict):
            traversed[k] = traverse(v, callback)
        else:
            traversed[k] = callback(v)

    return traversed
