def init_command(subparsers):
    init_parser = subparsers.add_parser("init", help="Initialize the project.")
    init_parser.add_argument("-s", "--source", help="Source file")
    init_parser.add_argument("-m", "--mode", help="Mode")
    init_parser.set_defaults(func=init)


def init(args):
    print(args.mode)
    print("Initializing...")
