import os
import pkg_resources


def init_command(subparsers):
    init_parser = subparsers.add_parser("init", help="Initialize the project.")
    init_parser.add_argument("folder", help="Folder to initialize the project in")
    # init_parser.add_argument("-s", "--source", help="Source file")
    # init_parser.add_argument("-m", "--mode", help="Mode")
    init_parser.set_defaults(func=init)


def init(args):
    if not os.path.exists(args.folder):
        os.makedirs(args.folder)
    elif os.listdir(args.folder):
        raise FileExistsError("Folder is not empty")

    resource_path = pkg_resources.resource_filename("syphus", "resources")
    assert os.path.exists(resource_path), f"Template folder does not exist: {resource_path}"
    # raise ValueError(resource_path)
