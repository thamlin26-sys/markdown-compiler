import argparse
import os
import sys
from markdown_compiler import compile_lines


def main():
    parser = argparse.ArgumentParser(description="Compile Markdown to HTML.")
    parser.add_argument("--input_file", required=True, help="Path to input markdown file")
    parser.add_argument("--output_file", help="Path to output html file")
    parser.add_argument(
        "--add_css",
        action="store_true",
        help="Include default CSS styling in the output"
    )
    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    compiled_lines = compile_lines(lines, add_css=args.add_css)

    output_path = args.output_file
    if not output_path:
        base, _ = os.path.splitext(args.input_file)
        output_path = f"{base}.html"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(compiled_lines)


if __name__ == "__main__":
    main()
