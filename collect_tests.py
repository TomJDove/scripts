#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pytest",
# ]
# ///
"""
Script to collect all pytest tests in a directory and print them to stdout.

I use this so that I can fzf search through all the tests and pick one to run with the following command:
    `uv run pytest $(collect_tests.py | fzf)`
"""

import argparse
import subprocess
import sys
from pathlib import Path


def collect_tests(directory: Path) -> list[str]:
    """
    Collect all pytest tests in the given directory.
    """
    # Use pytest's --collect-only to discover tests
    # -q for quiet output
    try:
        result = subprocess.run(
            ["uv", "run", "pytest", "--collect-only", "-q", directory],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error collecting tests with pytest:\n\n{e.stderr}", file=sys.stderr)
        sys.exit(1)

    tests = []
    for line in result.stdout.splitlines():
        # Filter out summary lines and empty lines
        line = line.strip()
        if line and "::" in line and not line.startswith("="):
            tests.append(line)

    return tests


def main():
    parser = argparse.ArgumentParser(
        description="Collect all pytest tests in a directory"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to search for tests (default: current directory)",
    )

    args = parser.parse_args()

    tests = collect_tests(Path(args.directory))

    print("\n".join(tests))


if __name__ == "__main__":
    main()
