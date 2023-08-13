import argparse


def init_command(subparsers):
    init_parser = subparsers.add_parser("init", help="Initialize something")
    # Define options specific to the "init" subcommand here
    init_parser.set_defaults(func=init_logic)


def run_command(subparsers):
    run_parser = subparsers.add_parser("run", help="Run something")
    run_parser.add_argument("-s", "--source", help="Source file")
    run_parser.add_argument("-m", "--mode", help="Mode")
    # Define options specific to the "run" subcommand here
    run_parser.set_defaults(func=run_logic)


def init_logic(args):
    # Logic for the "init" subcommand
    print("Initializing...")


def run_logic(args):
    # Logic for the "run" subcommand
    print("Running...")


def main():
    parser = argparse.ArgumentParser(description="Syphus CLI")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    init_command(subparsers)
    run_command(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
