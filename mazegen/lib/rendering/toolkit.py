"""
This module contains various renderer-related tools.
"""

import importlib.util
from pathlib import Path

try:
    from mazegen.lib import maze
except (ImportError, ModuleNotFoundError) as exc:
    raise ImportError("Can't import mazegen! Please install mazegen with pip or add it to PYTHONPATH!") from exc

def import_renderer(path: str):
    """Try to import module from path, then check if the imported module
    could be used as a renderer.

    Arguments
        * path: str - path to the module
    
    Returns
        * Module, if the import was successful and all the checks passed
        * False, if not all checks passed
    
    Raises
        * FileNotFoundError - if file from path does not exist
    """

    if not Path(path).is_file():
        raise FileNotFoundError(f"File {path} does not exist")
    
    # Extract stem from path
    name = Path(path).stem

    # Import module
    #try:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    #except Exception as e: # pylint: disable=broad-exception-caught
    #    return e

    try:
        _factory = module.RendererFactory()
    except AttributeError:
        return False
    #except Exception as e: # pylint: disable=broad-exception-caught
    #    return e

    return module

class RenderingError(Exception):
    """Raised when there's a rendering error."""

def render_maze_obj(renderer_module, maze_obj: maze.Maze, additional_args: dict = None):
    """Renders the Maze object using the renderer module, and applies additional args, if any.

    Arguments
        * renderer_module - the renderer module with RendererFactory
        * maze_obj: mazegen.lib.maze.Maze - the Maze object that will be rendered
        * additional_args: dict - the dictionary with additional args that will be passed to the renderer
    """

    try:
        factory = renderer_module.RendererFactory()
    except AttributeError as e:
        raise RenderingError("Can't render: Renderer module has no RendererFactory") from e
    except Exception as e:
        raise RenderingError("Can't render: couldn't construct RendererFactory") from e

    try:
        renderer = factory.create_renderer(additional_args)
    except Exception as e:
        raise RenderingError("Can't render: Couldn't create renderer with factory") from e

    try:
        renderer.render(maze_obj)
    except Exception as e:
        raise RenderingError("Couldn't render: unknown error") from e
