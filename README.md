# Syphus: Automatic Instruction-Response Generation Pipeline

## Installation

```bash
pip install --upgrade syphus
```

## CLI Usage

You can easily use the Syphus CLI for operations.

First, choose an empty folder for initialization:

```bash
syphus init <folder>
```

The structure of the folder will be:

```
<folder>/
    config/
        gpt_info.yaml
        prompt.yaml
    resources/
        media_infos.json
```

### Configuration

You can edit gpt_info.yaml and prompt.yaml to customize the generation.

### Edit Media Data

Then, change the `resources/media_infos.json` to include the media data you want to generate.

You can use two different styles of `resources/media_infos.json`:

```json
{
    "id_1": {
        "data_1": "data_1_1",
        "data_2": {
            "data_2_1": "data_2_1_1",
            "data_2_2": "data_2_2_1",
        }
    },
    "id_2": [
        "data_2_1",
        "data_2_2",
    ],
    "id_3": "data_3",
    ...
}
```

or

```json
[
    {
        "id": "id_1",
        "data_1": "data_1",
        "data_2": {
            "data_2_1": "data_2_1",
            "data_2_2": "data_2_2",
        }
    },
    {
        "id": "id_2",
        "data_1": "data_1",
        "data_2": "data_2",
    },
    ...
]
```

Optionally, you can change the `resources/media_infos.json` to `resources/media_infos.jsonl`, but the format should like the second one of `resources/media_infos.json`:

```jsonl
{"id": "id_1", "data_1": "data_1", "data_2": "data_2"}
{"id": "id_2", "data_1": "data_1", "data_2": "data_2"}
```

### Generate

After editing the `resources/media_infos.json`, you can generate the instruction-response pairs:

```bash
syphus query <folder>
```

or

```bash
cd <folder>
syphus query
```

You can use `syphus query --help` to see more options.
