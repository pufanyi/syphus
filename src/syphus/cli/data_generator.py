def query_command(subparsers):
    query_parser = subparsers.add_parser("query", help="Query GPT for QA pairs.")
    query_parser.add_argument("-s", "--source", help="Source file")
    query_parser.add_argument("-m", "--mode", help="Mode")
    query_parser.set_defaults(func=query)


def query(args):
    print("Querying...")
