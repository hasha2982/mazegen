"""
This module contains a base renderer for mazegen.
"""

from ..lib import maze

class BaseRenderer:
    """
    This is a base renderer for mazegen.
    """
    def render(self, maze_obj: maze.Maze) -> bool:
        """
        This method renders the maze.
        """
        print(maze_obj)

        return True

class RendererFactory:
    """
    This class is used for creating Renderer classes. 
    """

    def __init__(self) -> None:
        pass

    def create_renderer(self, args: str = "") -> BaseRenderer:
        """
        Parse the additional args and return Renderer object
        """

        print(args)
        return BaseRenderer()
