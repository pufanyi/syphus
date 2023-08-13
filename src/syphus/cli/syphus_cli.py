import argparse

from syphus.cli.data_generator import query_command
from syphus.cli.initializer import init_command


def main():
    parser = argparse.ArgumentParser(description="Syphus CLI")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    init_command(subparsers)
    query_command(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
