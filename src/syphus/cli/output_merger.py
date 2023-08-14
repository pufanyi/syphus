def merge_command(subparsers):
    merge_parser = subparsers.add_parser("merge", help="Format")
    merge_parser.add_argument("-i", "--input", help="Input file")
    merge_parser.add_argument("-o", "--output", help="Output file")
    merge_parser.add_argument("-m", "--mode", help="Output Format")
    merge_parser.set_defaults(func=merge)


def merge(args):
    print("Formatting...")
