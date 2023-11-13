import syphus.dataset.mmbench as mmbench
import syphus.dataset.m3it as m3it


def convert_command(subparsers):
    convert_parser = subparsers.add_parser("convert", help="Initialize the project.")
    convert_parser.add_argument(
        "--type", help="Dataset type", choices=["mmbench", "m3it"]
    )
    convert_parser.add_argument("--input", help="input file", default=None)
    convert_parser.add_argument("--output", help="output folder")
    convert_parser.add_argument(
        "--image-format", help="output image format", default="parquet"
    )
    convert_parser.add_argument("--subset", help="subset of the dataset", default=None)
    convert_parser.add_argument("--cache", help="cache folder", default="./cache")
    convert_parser.set_defaults(func=convert)


def convert(args):
    if args.type == "mmbench":
        mmbench.convert(args.input, args.output, args.image_format)
    elif args.type == "m3it":
        m3it.convert(args.subset, args.output, args.cache, args.image_format)
