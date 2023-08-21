import os
import argparse
import syphus

from glob import glob

from syphus.data_generator.syphus import Syphus
from syphus.utils.file_format import create_output_folder


def query_command(subparsers):
    query_parser = subparsers.add_parser("query", help="Query GPT for QA pairs.")
    query_parser.add_argument(
        "file", help="The file to query GPT with.", nargs="?", default=None
    )
    query_parser.add_argument("-c", "--config", help="OpenAI Config File", default=None)
    query_parser.add_argument(
        "-i", "--input", help="Input File of Information", default=None
    )
    query_parser.add_argument(
        "-o", "--output", help="Output File of Responses", default=None
    )
    query_parser.add_argument("-p", "--prompts", help="Prompts File", default=None)
    query_parser.add_argument(
        "-s", "--split", action="store_true", help="Split every information"
    )
    query_parser.add_argument(
        "--output_format",
        help="Format of output file",
        default="json",
        choices=["json", "jsonl", "yaml", "yml"],
    )
    query_parser.add_argument(
        "--threads", "-t", help="Number of threads to use", default=4, type=int
    )
    query_parser.set_defaults(func=query)


def get_file(path: str, prefix: str = "media_infos"):
    files = glob(os.path.join(path, f"{prefix}*"))
    if not files:
        raise ValueError(f"No resource files found in {path}.")
    elif len(files) > 1:
        raise ValueError(
            f"Multiple files found in {path} with prefix {prefix}, they are: {files}."
        )
    else:
        return files[0]


def get_files_from_args(args: argparse.Namespace):
    if args.file is None:
        args.file = os.getcwd()
    resources_path = os.path.join(args.file, "resources")
    config_path = os.path.join(args.file, "config")
    if args.config is None:
        args.config = os.path.join(config_path, "gpt_info.yaml")
    if args.input is None:
        args.input = get_file(resources_path, "media_infos")
    if args.prompts is None:
        args.prompts = os.path.join(config_path, "prompts.yaml")
    if args.output is None:
        args.output = os.path.join(args.file, "responses")
    if args.output_format == "yml":
        args.output_format = "yaml"
    if args.split:
        assert args.output_format in [
            "json",
            "yaml",
        ], "Split only supports json and yaml."
    else:
        assert args.output_format in [
            "json",
            "jsonl",
        ], "Output format must be json, or jsonl."
    assert os.path.exists(args.config), f"Config file {args.config} does not exist."
    assert os.path.exists(args.input), f"Input file {args.input} does not exist."
    assert os.path.exists(args.prompts), f"Prompts file {args.prompts} does not exist."
    create_output_folder(args.output)


def query(args: argparse.Namespace):
    get_files_from_args(args)
    syphus_object = Syphus(gpt_info_path=args.config, prompts=args.prompts)
    infos = list(syphus.prompts.info.load(args.input))
    syphus_object.query_all_infos_and_save(
        infos,
        args.output,
        num_threads=args.threads,
        format=args.output_format,
        split=args.split,
    )
