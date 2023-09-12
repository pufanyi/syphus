# Syphus: Automatic Instruction-Response Generation Pipeline

![](https://img.shields.io/badge/syphus-v0.0.6-darkcyan)
![](https://img.shields.io/github/stars/pufanyi/Syphus?style=social)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpufanyi%2FSyphus&count_bg=%23FFA500&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=visitors&edge_flat=false)](https://hits.seeyoufarm.com)
![](https://black.readthedocs.io/en/stable/_static/license.svg)
![](https://img.shields.io/badge/code%20style-black-000000.svg)

[Paper](https://arxiv.org/abs/2306.05425) | [Documents](https://pufanyi.github.io/syphus/) | [PyPI](https://pypi.org/project/syphus/) | [Source Code](https://github.com/pufanyi/Syphus)

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
