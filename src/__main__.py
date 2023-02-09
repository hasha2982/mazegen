"""
Maze generator and solver written in Python
Use mazegen -h for help.
"""

import argparse

LATEST_MANIFEST = 0 # Latest supported manifest version. Use -V to ignore

parser = argparse.ArgumentParser(
    prog="mazegen",
    description="Maze generator and solver written in Python"
)

# All
parser.add_argument(
    "-m", "--mode",
    help="choose a mode (render/generate/solve)"
)

# Render/solve
parser.add_argument(
    "-f", "--file",
    help=".json maze file to solve/render (only render/solve)"
)
parser.add_argument(
    "-V", "--ignore-version",
    help="ignore the maze json file version. might cause errors (only render/solve)",
    action='store_true'
)

# Render args
parser.add_argument(
    "-r", "--renderer",
    help="rendering method"
)

parser.parse_args()
