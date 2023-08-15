def query_command(subparsers):
    query_parser = subparsers.add_parser("query", help="Query GPT for QA pairs.")
    query_parser.add_argument(
        "-c", "--config", help="OpenAI Config File", required=True
    )
    query_parser.add_argument(
        "-i", "--input", help="Input File of Information", required=True
    )
    query_parser.add_argument(
        "-s", "--split", action="store_true", help="Split every information"
    )
    query_parser.add_argument("-p", "--prompts", help="Prompts File", required=True)
    query_parser.add_argument(
        "--prompts_format",
        help="Format of prompts file",
        default="auto",
        choices=["auto", "json", "yaml", "yml"],
    )
    query_parser.set_defaults(func=query)


def query(args):
    print("Querying...")
