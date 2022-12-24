# mock-server

- [mock-server](#mock-server)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Developer Installation](#developer-installation)
  - [Configuration](#configuration)

## Introduction

`mock-server` is a utility to mock server responses.

## Installation

```shell
pip install git+https://github.com/bitjockey42/mock-server
```

## Developer Installation

`poetry` is used to manage dependencies for this project.

```shell
poetry install
```

## Configuration

- `{resource}.config.json`
- `{resource}.response.json`
- `{resource}.struct.json`

`{resource}.config.json`

The main configuration.

**Available Configuration**
- `identifier` (optional): 
- `request_tree`: This represents the mapping between the request data and the responses we return in the server.
- `response_overrides`: Anything in the response data that should be overriden with a different value.

```json
{
    "identifier": ["id"],
    "request_tree": [
        {
            "request_keys": ["title"],
            "response_keys": ["title"]
        },
        {
            "request_keys": ["text"],
            "response_keys": ["text"],
            "required": true
        },
        {
            "request_keys": ["notebook"],
            "response_keys": ["notebook"],
            "required": true
        }
    ],
    "response_overrides": [
        {
            "response_keys": ["id"],
            "generator": "random_number",
            "type": "int"
        },
        {
            "response_keys": ["timestamp"],
            "generator": "unix_time",
            "type": "int"
        }
    ]
}
```

`{resource}.response.json`

The base response used to structure the generated response.

```json
{
    "id": 1,
    "uuid": "ef11e85b-3e21-41d6-9fda-65d835901d29",
    "title": "Title 1",
    "text": "Hello there",
    "timestamp": 1669565225,
    "notebook": 1
}
```

`{resource}.struct.json`

The structure of the request.

```json
{
    "id": {
        "required": false,
        "type": "int",
        "generator": "numerify",
        "length": null
    },
    "uuid": {
        "required": false,
        "type": "str",
        "generator": "UUID",
        "length": 36
    },
    "title": {
        "required": false,
        "type": "str",
        "generator": "lexify",
        "length": 7
    },
    "text": {
        "required": true,
        "type": "str",
        "generator": "text",
        "length": 11
    },
    "timestamp": {
        "required": false,
        "type": "int",
        "generator": "numerify",
        "length": null
    },
    "notebook": {
        "required": true,
        "type": "int",
        "generator": "numerify",
        "length": null
    }
}
```