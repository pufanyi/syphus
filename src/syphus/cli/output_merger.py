import os

import syphus.data_generator.response as response


def merge_command(subparsers):
    merge_parser = subparsers.add_parser(
        "merge", help="Merge input files into an output file"
    )
    merge_parser.add_argument("-i", "--input", help="Input file", required=True)
    merge_parser.add_argument("-o", "--output", help="Output file", required=True)
    merge_parser.add_argument(
        "-m",
        "--input-format",
        help="Mandatory input format",
        default="auto",
        choices=["json", "yaml", "yml", "auto"],
    )
    merge_parser.add_argument(
        "-f", "--output-format", help="Output format", default="json"
    )
    merge_parser.add_argument(
        "--input-response",
        help="Input response file name",
        default="responses",
    )
    merge_parser.add_argument(
        "--input-error-message",
        help="Input error message file name",
        default="error_messages",
    )
    merge_parser.add_argument(
        "--input-full-response",
        help="Input full response file name",
        default="gpt_full_responses",
    )
    merge_parser.add_argument(
        "--output-response",
        help="Output response file name",
        default="responses",
    )
    merge_parser.add_argument(
        "--output-error-message",
        help="Output error message file name",
        default="error_messages",
    )
    merge_parser.add_argument(
        "--output-full-response",
        help="Output full response file name",
        default="gpt_full_responses",
    )
    merge_parser.add_argument(
        "-p",
        "--no-process-bar",
        dest="process_bar",
        action="store_false",
        help="Disable process bar",
    )

    merge_parser.set_defaults(func=merge)


def merge(args):
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Cannot find path {args.input}")
    if os.path.exists(args.output):
        overwrite = input(f"Path {args.output} exists. Overwrite? (y/n) ")
        if overwrite.lower() != "n":
            return
    response.merge(
        args.input,
        args.output,
        input_format=args.input_format,
        output_format=args.output_format,
        input_response_file_name=args.input_response,
        input_error_message_file_name=args.input_error_message,
        input_full_response_file_name=args.input_full_response,
        output_response_file_name=args.output_response,
        output_error_message_file_name=args.output_error_message,
        output_full_response_file_name=args.output_full_response,
        process_bar=args.process_bar,
    )
