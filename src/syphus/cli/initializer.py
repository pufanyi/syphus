import os
import shutil
import pkg_resources


def init_command(subparsers):
    init_parser = subparsers.add_parser("init", help="Initialize the project.")
    init_parser.add_argument("folder", help="Folder to initialize the project in")
    init_parser.set_defaults(func=init)


def init(args):
    if os.path.exists(args.folder):
        if os.listdir(args.folder):
            raise FileExistsError("Folder is not empty")
        else:
            os.rmdir(args.folder)

    resource_path = pkg_resources.resource_filename("syphus", "resources")
    template_path = os.path.join(resource_path, "template")

    shutil.copytree(template_path, args.folder)
