"""
This module contains a base renderer for mazegen.
"""

try:
    from mazegen.lib import maze
except ImportError:
    print("ERROR: Can't import from mazegen.lib! Please install mazegen!")

    raise

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

    def create_renderer(self, args: dict = None) -> BaseRenderer:
        """
        Create a renderer with applied additional args
        """

        print(args)
        return BaseRenderer()
