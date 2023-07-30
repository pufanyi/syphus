#!/bin/bash

# Function to display script usage
display_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -h, --help              Display this help message."
    echo "  -d, --dir <directory>   Specify the source directory to test coverage (default: src)."
    echo "  -o, --output <output>   Specify the output directory for coverage reports (default: htmlcov)."
    echo "  --                      Use double dash (--) to separate options from arguments for pytest."
}

# Default values for options
src_dir="src"
output_dir="htmlcov"

# Parse command-line options
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -h|--help)
            display_usage
            exit 0
            ;;
        -d|--dir)
            src_dir="$2"
            shift
            ;;
        -o|--output)
            output_dir="$2"
            shift
            ;;
        --)
            shift
            break # Remaining arguments will be passed to pytest
            ;;
        *)
            echo "Error: Unrecognized option $1"
            display_usage
            exit 1
            ;;
    esac
    shift
done

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest not found. Please install pytest before running this script."
    exit 1
fi

# Check if the source directory exists
if [ ! -d "$src_dir" ]; then
    echo "Error: Source directory '$src_dir' not found."
    exit 1
fi

# Run pytest with coverage
pytest --cov="$src_dir" --cov-report=term-missing --cov-report=html "$@" tests/
exit_code=$?

# Check if pytest ran successfully
if [ $exit_code -ne 0 ]; then
    echo "Error: pytest encountered some failures."
    exit $exit_code
fi

# Display the path to the coverage report
echo "Coverage report generated at: $output_dir/index.html"
