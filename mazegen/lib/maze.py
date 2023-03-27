"""
This module contains the Maze class, which represents a maze.
"""

import json

class Maze:
    """
    This class represents a maze.
    """
    # Defines the width and the height of the maze, including the border
    width = 0
    height = 0

    ### Example
    # rows = {
    #   0: {
    #       1: true # true for empty
    #   }
    # }
    rows = {}

    # X and Y coordinates of the start tile. Used for rendering and solving
    start_x = 0
    start_y = 0

    # Coordinates of the end tile.
    end_x = 0
    end_y = 0

    def __init__(self, rows: dict, width: int, height: int, start_x: int, start_y: int, end_x: int, end_y: int):
        self.rows = rows

        self.width = width
        self.height = height

        self.start_x = start_x
        self.start_y = start_y

        self.end_x = end_x
        self.end_y = end_y

class MazeFactoryError(Exception):
    """
    Raised when MazeFactory can't create a new Maze object

    Attributes
        * message - The message. Will include sub_exc in it.
        * sub_exc - The exception that could be raised instead of this one (TypeError when JSON value has an inappropriate type)
    """

    def __init__(self, message: str = "", sub_exc: Exception = Exception) -> None:
        self.sub_exc = sub_exc

        if sub_exc is not Exception:
            self.message = f"({sub_exc.__qualname__}) {message}"
        else:
            self.message = message

        super().__init__(self.message)

class MazeFactory:
    """
    Contains methods that are used to construct Maze objects.
    """
    def init_from_json_str(self, json_string, ignore_manifest_version = False):  # FIXME: Limit the amount of data to be parsed! (#13)
        """
        Initialize a new Maze object by parsing a JSON string.
        """
        rows = {}

        # width = 0
        # height = 0

        # startX = 0
        # startY = 0
        # endX = 0
        # endY = 0

        # Parse
        try:
            parsed = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise MazeFactoryError(f"Couldn't parse maze JSON file: unknown error ({e})", json.JSONDecodeError) from e

        # Check if dict
        if not isinstance(parsed, dict):
            raise MazeFactoryError(f"Couldn't parse maze JSON file: {type(parsed)} is not a valid type (expected dict)", TypeError)

        ### Validate manifest
        # Validate "manifest" key
        if not "manifest" in parsed:
            raise MazeFactoryError("Couldn't parse maze JSON file: no \"manifest\" key in file", KeyError)

        if not isinstance(parsed["manifest"], dict):
            raise MazeFactoryError(f"Couldn't parse maze JSON file: {type(parsed['manifest'])} is not a valid type (expected dict)", TypeError)

        # Validate "version" key
        if not "version" in parsed["manifest"]:
            raise MazeFactoryError("Couldn't parse maze JSON file: no \"version\" in manifest", KeyError)

        if not isinstance(parsed["manifest"]["version"], int):
            raise MazeFactoryError(f"Couldn't parse maze JSON file: {type(parsed['manifest']['version'])} is not a valid type (expected int)", TypeError)

        if parsed["manifest"]["version"] <= 1 or ignore_manifest_version:
            # Specific check for versions 0+, since manifest can be changed in later versions.
            if "mazeWidth" and "mazeHeight" and "startX" and "startY" and "endX" and "endY" not in parsed["manifest"]:
                raise MazeFactoryError("Couldn't parse maze JSON file: not enough keys in manifest exist (for versions >=1)", KeyError)

            # Check types
            if not (isinstance(parsed["manifest"]["mazeWidth"], int) and isinstance(parsed["manifest"]["mazeHeight"], int) and isinstance(parsed["manifest"]["startX"], int) and isinstance(parsed["manifest"]["startY"], int) and isinstance(parsed["manifest"]["endX"], int) and isinstance(parsed["manifest"]["endY"], int)):
                raise MazeFactoryError("Couldn't parse maze JSON file: some keys in manifest have the wrong type", TypeError)

            ### Manifest valid!
            ### Validate rows
            if len(parsed["rows"]) != parsed["manifest"]["mazeHeight"]:
                raise MazeFactoryError(f"Couldn't parse maze JSON file: the amount of rows is not equal to maze height (rows: {parsed['rows'].len()}, height: {parsed['mazeHeight']})", ValueError)

            ### Rows valid!
            for row_id in range(parsed["manifest"]["mazeHeight"]):
                if str(row_id) not in parsed["rows"]:
                    raise MazeFactoryError(f"Couldn't parse maze JSON file: row {row_id} doesn't exist", KeyError)

                if len(parsed["rows"][str(row_id)]) != parsed["manifest"]["mazeWidth"]:
                    raise MazeFactoryError(f"Couldn't parse maze JSON file: the amount of columns is not equal to maze width (columns: {parsed['rows'][str(row_id)].len()}, width: {parsed['mazeWidth']})", ValueError)

                current_row = {} # This variable will be appended to rows

                for column in range(parsed["manifest"]["mazeWidth"]):
                    if not isinstance(parsed["rows"][str(row_id)][str(column)], bool):
                        raise MazeFactoryError(f"Couldn't parse maze JSON file: {parsed['rows'][str(row_id)][str(column)]} is not a valid type (expected bool)", TypeError)

                    current_row[column] = parsed["rows"][str(row_id)][str(column)]

                rows[row_id] = current_row

            maze_obj = Maze(rows, parsed["manifest"]["mazeWidth"], parsed["manifest"]["mazeHeight"], parsed["manifest"]["startX"], parsed["manifest"]["startY"], parsed["manifest"]["endX"], parsed["manifest"]["endY"])
            return maze_obj

        raise MazeFactoryError(f"Couldn't parse maze JSON file: version {parsed['manifest']['version']} not supported", ValueError)
