"""
This module contains a Stream Renderer for mazegen
"""

import sys
import json

from .base import BaseRenderer
from .base import RendererFactory as BaseRendererFactory

from ..lib.maze import Maze
from ..lib.logging import formatter

l = formatter.get_formatted_logger("StreamRenderer")

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

    def maze_to_list(self, maze: Maze) -> list:
        """
        Go through all rows and cells of maze, render as strings representing rows, return list with strings
        """

        # List with rendered rows as strings.
        # This will be returned later.
        rows_list = []

        for row_id in range(maze.height):
            row_str = ""

            for cell_id in range(maze.width):
                # empty_char if no wall
                # wall_char if wall
                # unknown_char if error
                if maze["rows"][row_id][cell_id] is True:
                    row_str += self.empty_char
                elif maze["rows"][row_id][cell_id] is False:
                    row_str += self.wall_char
                else:
                    l.warning("Unknown cell in position (%i, %i). Replacing with '%s'", cell_id, row_id, self.unknown_char)
                    row_str += self.unknown_char
                l.info("Render cell (%i, %i)", cell_id, row_id)

            rows_list.append(row_str)

        return rows_list

    def write_to_stream(self, stream, rows_list):
        """
        Write the rows list to stream.
        """
        writable = False

        try:
            writable = stream.writable()
        except AttributeError as e:
            l.critical("AttributeError while trying to call stream.writable. Maybe stream is not a file object?", exc_info=e)
            raise
        except Exception as e: # pylint: disable=broad-exception-caught
            l.critical("Unknown error while trying to call stream.writable", exc_info=e)
            raise

        if not writable:
            l.critical("Stream is not writable.")
            raise IOError

        for row in rows_list:
            stream.write(row + "\n")
            l.debug("Written %s", row)

    def render(self, maze_obj):
        rows_list = self.maze_to_list(maze_obj)

        self.write_to_stream(sys.stdout, rows_list)
        # TODO: Implement writing to different streams with additional args

class RendererFactory(BaseRendererFactory):
    """
    Parse args and create StreamRenderer
    """
    def create_renderer(self, args: str = "") -> StreamRenderer:
        parsed_args = json.loads(args) # TODO: add try catch?

        obj = StreamRenderer()

        if "wall_char" in parsed_args:
            obj.wall_char = str(parsed_args["wall_char"])

        if "empty_char" in parsed_args:
            obj.empty_char = str(parsed_args["empty_char"])

        if "start_char" in parsed_args:
            obj.start_char = str(parsed_args["start_char"])

        if "end_char" in parsed_args:
            obj.end_char = str(parsed_args["end_char"])

        if "solution_char" in parsed_args:
            obj.solution_char = str(parsed_args["solution_char"])

        if "unknown_char" in parsed_args:
            obj.unknown_char = str(parsed_args["unknown_char"])

        return obj
