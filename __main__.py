"""
Maze generator and solver written in Python
Use mazegen -h for help.
"""

import argparse
import sys

import colorama as co

# This works, ignore the error
from lib.logging import formatter as custom_formatter # pylint: disable=import-error,no-name-in-module
# FIXME: Edit .vscode to extend the import path

co.init()

LATEST_MANIFEST = 0 # Latest supported manifest version. Use -V to ignore

parser = argparse.ArgumentParser(
    prog="mazegen",
    description="Maze generator and solver written in Python"
)

# Logging
parser.add_argument(
    "-V", "--verbose",
    default="WARNING",
    type=str,
    help="set verbosity level. defaults to WARNING. [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]"
)

# All
parser.add_argument(
    "-m", "--mode",
    type=str,
    help="choose a mode (render/generate/solve)"
)

# Render/solve
parser.add_argument(
    "-f", "--file",
    help=".json maze file to solve/render (only render/solve)"
)
parser.add_argument(
    "--ignore-version",
    help="ignore the maze json file version. might cause errors (only render/solve)",
    action='store_true'
)

# Render args
parser.add_argument(
    "-r", "--renderer",
    help="rendering method"
)

args = parser.parse_args()

l = custom_formatter.get_formatted_logger()

match args.verbose.upper(): # the type of flag is str, so we're sure it has .upper()
    case "NOTSET" | "N":
        l.setLevel(0)
    case "DEBUG" | "D":
        l.setLevel(10)
    case "INFO" | "I":
        l.setLevel(20)
    case "WARNING" | "W":
        l.setLevel(30)
    case "ERROR" | "E":
        l.setLevel(40)
    case "CRITICAL" | "C":
        l.setLevel(50)
    case _:
        l.warning("Unknown logging level '%s'. Defaulting to 'WARNING'", args.verbose.upper())

# l.debug("Debug")
# l.info("Info")
# l.warn("Warning")
# l.warning("Warning")
# l.error("Error")
# l.critical("Critical")

if __name__ == "__main__":
    if args.mode is None:
        l.critical("Missing mode argument. Try -h or --help")
        sys.exit(1)
    
    match args.mode.lower():
        case "render" | "r":
            l.debug("render")
        case _:
            l.critical("Unknown mode: %s. Supported modes: render. Try -h or --help", args.mode)
    