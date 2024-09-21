import argparse

from .lox import Lox


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        nargs="?",
        help="program read from script file", metavar="SCRIPT",
    )
    args = parser.parse_args()

    lox = Lox()
    if args.file:
        lox.run_file(args.file)
    else:
        lox.run_prompt()
