import argparse


def main():
    parser = argparse.ArgumentParser(description="Syphus CLI")
    parser.add_argument("-o", "--output", help="Output file path", required=True)
    args = parser.parse_args()

    result = "try"
    with open(args.output, "w") as f:
        f.write(result)


if __name__ == "__main__":
    main()
