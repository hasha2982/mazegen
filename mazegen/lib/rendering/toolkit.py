"""
This module contains various renderer-related tools.
"""

import importlib.util
from pathlib import Path

def import_renderer(path: str):
    """Try to import module from path, then check if the imported module
    could be used as a renderer.

    Arguments
        * path: str - path to the module
    
    Returns
        * Module, if the import was successful and all the checks passed
        * False, if the import was not successful or not all checks passed
        * Exception, if an exception has occurred
    """

    # Extract stem from path
    name = Path(path).stem

    # Import module
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e: # pylint: disable=broad-exception-caught
        return e # TODO: maybe don't return the exceptions?

    try:
        _factory = module.RendererFactory()
    except AttributeError:
        return False
    except Exception as e: # pylint: disable=broad-exception-caught
        return e

    return module
