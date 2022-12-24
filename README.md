# mock-server

- [mock-server](#mock-server)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Developer Installation](#developer-installation)
  - [Setup and Configuration](#setup-and-configuration)
    - [Configurations](#configurations)
  - [Usage](#usage)

## Introduction

`mock-server` is a utility to mock server responses.

This is very much in alpha still and a lot of it needs refactoring

## Installation

```shell
pip install git+https://github.com/bitjockey42/mock-server
```

## Developer Installation

`poetry` is used to manage dependencies for this project.

```shell
poetry install
```

## Setup and Configuration

How this works is the mock-server reads from `CONF_DIR/{resource}.{config_type}.json` to generate responses and persists objects as JSON files under a `DATA_DIR` (which can also be overriden as an env var). The `resource` corresponds to the plural of ad resource. For example, `notes` instead of `note`.

Create a `CONF_DIR` and place these configuration files within that folder for each `resource` you want to mock:

- `{resource}.config.json`
- `{resource}.response.json`
- `{resource}.struct.json`

Then see [Configurate](#configurations) for more info on what to put in those files.

### Configurations

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

## Usage

```shell
mock-server app
```

Override the `DATA_DIR` and `CONF_DIR`:

```shell
DATA_DIR=../mydata CONF_DIR=../myconf mock-server app
```
