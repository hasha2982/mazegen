"""
This module contains a CLI Renderer for mazegen
"""

from base import BaseRenderer
from lib.maze import Maze

class StreamRenderer(BaseRenderer):
    """
    Renderer for streams (stdout, etc.)
    """

    # Characters to represent wall cells and empty cells
    wall_char = "█"
    empty_char = " "

    # Characters to represent start cells and end cells
    start_char = "S"
    end_char = "E"

    # Character to represent solution path
    solution_char = "."

    # Character for unknown (error) cells
    unknown_char = "?"

    def __init__(self, wall_char = "█", empty_char = " ", start_char = "S", end_char = "E", solution_char = ".", unknown_char = "?"):
        self.wall_char = wall_char
        self.empty_char = empty_char

        self.start_char = start_char
        self.end_char = end_char

        self.solution_char = solution_char

        self.unknown_char = unknown_char

    def maze_to_list(self, maze: Maze):
        """
        Go through all rows and cells of maze, render as strings representing rows, return list with strings
        """

        rows_list = []

        