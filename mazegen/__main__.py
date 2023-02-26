"""
Maze generator and solver written in Python
Use mazegen -h for help.
"""

import argparse
import os
import textwrap
import importlib.util
import pathlib

import colorama as co

from mazegen.lib.logging import formatter as custom_formatter

co.init() # Init colorama

LATEST_MANIFEST = 0 # Latest supported manifest version.

parser = argparse.ArgumentParser(
    prog="mazegen",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
    Maze generator and solver written in Python.
    Modes:
    list | l
        list all available generators, solvers and renderers
    
    render | r
        render .json maze file
    """)
)

# Logging
parser.add_argument(
    "-V", "--verbose",
    default="WARNING",
    type=str,
    help="set verbosity level. defaults to WARNING. [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]"
)

# All
# parser.add_argument(
#     "-m", "--mode",
#     type=str,
#     help="choose a mode (render/generate/solve)"
# )
parser.add_argument(
    "mode",
    help="choose a mode (render/generate/solve)"
)

# Render/solve
parser.add_argument(
    "-f", "--file",
    help=".json maze file to solve/render (only render/solve)"
)
parser.add_argument(
    "--ignore-version",
    help="ignore the maze json file version. might cause errors (only render/solve)",
    action='store_true'
)

# Render args
parser.add_argument(
    "-r", "--renderer",
    help="rendering method"
)

parser.add_argument(
    "-A", "--renderer-args",
    help="additional arguments for the renderer. check the renderer docs for supported renderer args."
)

args = parser.parse_args()

l = custom_formatter.get_formatted_logger()

match args.verbose.upper(): # the type of flag is str, so we're sure it has .upper()
    case "NOTSET" | "N":
        l.setLevel(0)
    case "DEBUG" | "D":
        l.setLevel(10)
    case "INFO" | "I":
        l.setLevel(20)
    case "WARNING" | "W":
        l.setLevel(30)
    case "ERROR" | "E":
        l.setLevel(40)
    case "CRITICAL" | "C":
        l.setLevel(50)
    case _:
        l.warning("Unknown logging level '%s'. Defaulting to 'WARNING'", args.verbose.upper())

# l.debug("Debug")
# l.info("Info")
# l.warn("Warning")
# l.warning("Warning")
# l.error("Error")
# l.critical("Critical")

def list_renderers(directory) -> list:
    """
    Get all .py files in /renderers/ and check if they can be used as renderers
    """
    renderers_dir = directory

    # Check if dir exists
    if not pathlib.Path(directory).is_dir():
        l.error("%s is not a directory. Skipping renderers...")
        return [] # Return empty list, i.e. no renderers found.

    # List of all found .py files
    py_files_list = []

    # Get all files and dirs in dir
    for filename in os.listdir(renderers_dir):
        l.debug("Analyzing %s", filename)
        f = os.path.join(renderers_dir, filename)

        #print(f)
        if os.path.isfile(f) and f.lower().endswith(".py"):
            py_files_list.append(f)
            l.debug("%s is a .py file, appending to list", f)

    valid_modules_list = []

    # Try to import and check them
    for file in py_files_list:
        # Try to extract stem from path
        name = pathlib.Path(file).stem

        # Import module
        try:
            spec = importlib.util.spec_from_file_location(name, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            l.debug("Successfully imported %s from %s", name, file)
        except Exception as e: # pylint: disable=broad-exception-caught
            l.debug("Can't import %s from %s: unknown error (%s). Skipping", name, file, e)
            continue

        try:
            _factory = module.RendererFactory()
        except AttributeError as e:
            l.debug("Imported module has no RendererFactory. Skipping (%s)", e)
            continue

        # If we're here, then the imported module is probably valid.
        # TODO: add version check?

        valid_modules_list.append({"name": module.__name__, "file": file})

    return valid_modules_list

if __name__ == "__main__":
    ## Not required now since mode is positional
    # if args.mode is None:
    #     l.critical("Missing mode argument. Try -h or --help")
    #     sys.exit(1)

    match args.mode.lower():
        case "list" | "l":
            l.debug("list mode")

            ### Renderers
            # l.debug(str(pathlib.Path(__file__).parent.resolve().joinpath("./renderers")))
            successful_renderers = list_renderers(str(pathlib.Path(__file__).parent.resolve().joinpath("./renderers")))

            print(f"Found {len(successful_renderers)} renderer(s) in /renderers/")
            for renderer in successful_renderers:
                print(f"\t{renderer['name']} ({renderer['file']})")

        case "render" | "r":
            l.debug("render mode")
        case _:
            l.critical("Unknown mode: %s. Supported modes: render, list. Try -h or --help", args.mode)
    