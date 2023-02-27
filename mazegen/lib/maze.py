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
        parsed = json.loads(json_string)

        # Check if dict
        if not isinstance(parsed, dict):
            raise TypeError(f"Couldn't parse maze JSON file: {type(parsed)} is not a valid type (expected dict)")

        ### Validate manifest
        # Validate "manifest" key
        if not "manifest" in parsed:
            raise KeyError("Couldn't parse maze JSON file: no \"manifest\" key in file")

        if not isinstance(parsed["manifest"], dict):
            raise TypeError(f"Couldn't parse maze JSON file: {type(parsed['manifest'])} is not a valid type (expected dict)")

        # Validate "version" key
        if not "version" in parsed["manifest"]:
            raise KeyError("Couldn't parse maze JSON file: no \"version\" in manifest")

        if not isinstance(parsed["manifest"]["version"], int):
            raise TypeError(f"Couldn't parse maze JSON file: {type(parsed['manifest']['version'])} is not a valid type (expected int)")

        if parsed["manifest"]["version"] <= 1 or ignore_manifest_version:
            # Specific check for versions 0+, since manifest can be changed in later versions.
            if "mazeWidth" and "mazeHeight" and "startX" and "startY" and "endX" and "endY" not in parsed["manifest"]:
                raise KeyError("Couldn't parse maze JSON file: not enough keys in manifest exist (for versions >=1)")

            # Check types
            if not (isinstance(parsed["manifest"]["mazeWidth"], int) and isinstance(parsed["manifest"]["mazeHeight"], int) and isinstance(parsed["manifest"]["startX"], int) and isinstance(parsed["manifest"]["startY"], int) and isinstance(parsed["manifest"]["endX"], int) and isinstance(parsed["manifest"]["endY"], int)):
                raise TypeError("Couldn't parse maze JSON file: some keys in manifest have the wrong type")

            ### Manifest valid!
            ### Validate rows
            if len(parsed["rows"]) != parsed["manifest"]["mazeHeight"]:
                raise ValueError(f"Couldn't parse maze JSON file: the amount of rows is not equal to maze height (rows: {parsed['rows'].len()}, height: {parsed['mazeHeight']})")

            ### Rows valid!
            for row_id in range(parsed["manifest"]["mazeHeight"]):
                if str(row_id) not in parsed["rows"]:
                    raise KeyError(f"Couldn't parse maze JSON file: row {row_id} doesn't exist")

                if len(parsed["rows"][str(row_id)]) != parsed["manifest"]["mazeWidth"]:
                    raise ValueError(f"Couldn't parse maze JSON file: the amount of columns is not equal to maze width (columns: {parsed['rows'][str(row_id)].len()}, width: {parsed['mazeWidth']})")

                current_row = {} # This variable will be appended to rows

                for column in range(parsed["manifest"]["mazeWidth"]):
                    if not isinstance(parsed["rows"][str(row_id)][str(column)], bool):
                        raise TypeError(f"Couldn't parse maze JSON file: {parsed['rows'][str(row_id)][str(column)]} is not a valid type (expected bool)")

                    current_row[column] = parsed["rows"][str(row_id)][str(column)]

                rows[row_id] = current_row

            maze_obj = Maze(rows, parsed["manifest"]["mazeWidth"], parsed["manifest"]["mazeHeight"], parsed["manifest"]["startX"], parsed["manifest"]["startY"], parsed["manifest"]["endX"], parsed["manifest"]["endY"])
            return maze_obj

        raise ValueError(f"Couldn't parse maze JSON file: version {parsed['manifest']['version']} not supported")
