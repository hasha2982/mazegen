"""
Maze generator and solver written in Python
Use mazegen -h for help.
"""

import argparse

parser = argparse.ArgumentParser(
    prog="mazegen",
    description="Maze generator and solver written in Python"
)
parser.add_argument(
    "-m", "--mode",
    help="choose a mode (render/generate/solve)"
)
parser.add_argument(
    "-f", "--file",
    help=".json maze file to solve/render"
)

# Render args
parser.add_argument(
    "-r", "--renderer",
    help="rendering method"
)

parser.parse_args()
