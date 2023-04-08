"""Stream Renderer for mazegen

Used for rendering mazes to stream (files, stdout, etc.)

Supported renderer arguments
    NOTE: When passing JSON renderer arguments as command line arguments, make
    sure you escape characters. (like quotes)
    * wall_char: string - character(s) that will be used for wall tiles.
      defaults to '█' (U+2588 Full block)
    * empty_char: string - character(s) that will be used for empty tiles.
      defaults to ' ' (space)
    * start_char: string - character(s) that will be used for starting tiles.
      defaults to 'S'
    * end_char: string - character(s) that will be used for finish tiles.
      defaults to 'E'
    * solution_char: string - character(s) that will be used for the solution path.
      defaults to '.'
    * unknown_char: string - character(s) that will be used for error (unknown) tiles.
      defaults to '?'

License
    MIT License
    
    Copyright (c) 2023 hasha2982
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import sys

try:
    from mazegen.lib.rendering.base import BaseRenderer
    from mazegen.lib.rendering.base import RendererFactory as BaseRendererFactory

    from mazegen.lib.maze import Maze
    from mazegen.lib.logging import formatter
except ImportError:
    print("ERROR: Can't import from mazegen.lib! Please install mazegen!")

    raise

l = formatter.get_formatted_logger("StreamRenderer") # This may not be forward compatible

# TODO: #28 Better docstrings
class StreamRenderer(BaseRenderer):
    """Renderer for streams (stdout, etc.)"""

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
        """Inits the StreamRenderer

        Arguments
            * wall_char: str - the character that will be used for wall tiles. defaults to '█' (U+2588 Full block)
            * empty_char: str - the character that will be used for empty tiles. defaults to ' ' (space)
            * start_char: str - the character that will be used for starting tiles. defaults to 'S'
            * end_char: str - the character that will be used for finish tiles. defaults to 'E'
            * solution_char: str - the character that will be used for the solution path. defaults to '.'
            * unknown_char: str - the character that will be used for error (unknown) tiles. defaults to '?'
        """
        self.wall_char = wall_char
        self.empty_char = empty_char

        self.start_char = start_char
        self.end_char = end_char

        self.solution_char = solution_char

        self.unknown_char = unknown_char

    def maze_to_list(self, maze: Maze) -> list:
        """Render each row of the Maze object as a string, return list with the rendered row strings.

        Arguments
            * maze: mazegen.lib.maze.Maze - the Maze object that will be rendered.
        
        Returns
            * str[] - list with the rows of maze, rendered as strings.
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

    def write_to_stream(self, stream, rows_list: list):
        """Iterate through rows_list and write each element to stream, then close the stream if it's not stdout or stderr
        
        Arguments
            * stream - the stream that will be used for rendering
            * rows_list: str[] - list of strings, each element will be written to stream
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
        """Render the maze object
        
        Arguments
            * maze_obj: mazegen.lib.maze.Maze - the Maze object to render
        
        Returns
            * True
        """
        rows_list = self.maze_to_list(maze_obj)

        self.write_to_stream(self.stream, rows_list)

        return True

class RendererFactory(BaseRendererFactory):
    """This class is used for creating StreamRenderer objects and applying renderer arguments to these objects"""
    def create_renderer(self, args: dict = None) -> StreamRenderer:
        """Create StreamRenderer object and apply any renderer args

        Arguments
            * args: dict - dictionary with the renderer args. not required

        Returns
            * StreamRenderer with any applied renderer args
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
