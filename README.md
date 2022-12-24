# mock-server

## Configuration

`{resource}.{config_type}.json`



`{resource}.config.json`

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
            "response_keys": ["text"]
        },
        {
            "request_keys": ["notebook"],
            "response_keys": ["notebook"]
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