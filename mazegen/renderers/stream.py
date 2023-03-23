"""
This module contains a Stream Renderer for mazegen
"""

import sys
#import json

try:
    from mazegen.lib.renderer_api.base import BaseRenderer
    from mazegen.lib.renderer_api.base import RendererFactory as BaseRendererFactory

    from mazegen.lib.maze import Maze
    from mazegen.lib.logging import formatter
except ImportError:
    print("ERROR: Can't import from mazegen.lib! Please install mazegen!")

    raise

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

    # Default output stream
    stream = sys.stdout

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
                if maze.rows[row_id][cell_id] is True:
                    row_str += self.empty_char
                elif maze.rows[row_id][cell_id] is False:
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

        # Try to close stream
        if (stream.name is not sys.stdout.name) and (stream.name is not sys.stderr.name):
            l.debug("%s is not stdout or stderr, closing...", stream)
            stream.close()

    def render(self, maze_obj):
        """
        Render the Maze object
        """
        rows_list = self.maze_to_list(maze_obj)

        self.write_to_stream(self.stream, rows_list)
        # TODO: Implement writing to different streams with additional args (#14)

        return True

class RendererFactory(BaseRendererFactory):
    """
    Parse args and create StreamRenderer
    """
    def create_renderer(self, args: dict = None) -> StreamRenderer:
        """
        Apply args to renderer and return it
        """
        #parsed_args = json.loads(args)

        # Create renderer
        obj = StreamRenderer()

        if args is None: # Don't parse the args if args is None
            return obj

        # Apply args
        # Characters
        if "wall_char" in args:
            obj.wall_char = str(args["wall_char"])

        if "empty_char" in args:
            obj.empty_char = str(args["empty_char"])

        if "start_char" in args:
            obj.start_char = str(args["start_char"])

        if "end_char" in args:
            obj.end_char = str(args["end_char"])

        if "solution_char" in args:
            obj.solution_char = str(args["solution_char"])

        if "unknown_char" in args:
            obj.unknown_char = str(args["unknown_char"])

        # Stream
        if "stream" in args:
            match args["stream"]:
                case "stdout" | "sys.stdout":
                    obj.stream = sys.stdout
                case "stderr" | "sys.stderr":
                    obj.stream = sys.stderr
                case _:
                    obj.stream = open(args, "a", encoding="utf-8") # Append is the most safe way

        return obj
