import syphus.dataset.mmbench as mmbench


def convert_command(subparsers):
    convert_parser = subparsers.add_parser("convert", help="Initialize the project.")
    convert_parser.add_argument("--type", help="Dataset type", choices=["mmbench"])
    convert_parser.add_argument("--input", help="input file")
    convert_parser.add_argument("--output", help="output folder")
    convert_parser.set_defaults(func=convert)


def convert(args):
    if args.type == "mmbench":
        mmbench.convert(args.input, args.output)
