"""
Maze generator and solver written in Python
Use mazegen -h for help.
"""

# TODO: #26 Import organization

import argparse
import textwrap # TODO: #24 textwrap.dedent?
import json

import colorama as co

try:
    from mazegen.lib.logging import formatter as custom_formatter
    from mazegen.lib import maze
    from mazegen.lib.rendering import toolkit as rendering_tk
except (ImportError, ModuleNotFoundError) as exc:
    print(f"Can't import mazegen! Please install mazegen with pip or add it to PYTHONPATH before using ({exc})")
    raise

co.init() # Init colorama

LATEST_MANIFEST = 0 # Latest supported manifest version.

# TODO: #27 Rewrite argument help
parser = argparse.ArgumentParser(
    prog="mazegen",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
    Maze generator and solver written in Python.
    Modes:
    render | r
        render .json maze file
    """)
)

# Logging
parser.add_argument(
    "-V", "--verbose",
    default="WARNING",
    type=str,
    help="set verbosity level. defaults to WARNING. available: NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL"
)

# All
# parser.add_argument(
#     "-m", "--mode",
#     type=str,
#     help="choose a mode (render/generate/solve)"
# )
parser.add_argument(
    "mode",
    help="selects mode. available: render/r"
)

# Render/solve
parser.add_argument(
    "-f", "--file",
    type=str,
    help="path to .json maze file to solve/render (only render/solve modes)"
)
parser.add_argument(
    "--ignore-version",
    help="ignore the maze .json file version. might cause errors (only render/solve modes)",
    action='store_true'
)

# Render args
parser.add_argument(
    "-r", "--renderer",
    type=str,
    help="path to the rendering module"
)

parser.add_argument(
    "-R", "--renderer-args",
    type=str,
    help="additional arguments for the renderer. check the renderer docs for supported renderer args. make sure to escape characters, like quotes"
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

# Mode functions
def render_mode():
    """Called when render mode is selected. Should not be called from outside __main__.py"""

    # Check if required args are set
    if (args.file is None) or (args.renderer is None):
        if args.file is None:
            l.critical("--file argument required for render mode")
        if args.renderer is None:
            l.critical("--renderer argument required for render mode")

        return

    # Import renderer
    try:
        renderer = rendering_tk.import_renderer(args.renderer)
    except ModuleNotFoundError:
        l.critical("Can't render: renderer '%s' not found", args.renderer, exc_info=True)
        return
    except ImportError:
        l.critical("Can't render: couldn't import renderer '%s'", args.renderer, exc_info=True)
        return
    except FileNotFoundError:
        l.critical("Can't render: Couldn't import renderer: file '%s' does not exist", args.renderer, exc_info=True)
        return

    if not renderer:
        l.critical("Can't render: module '%s' can't be used as a renderer")
        return

    # Check maze file
    try:
        with open(args.file, "r", encoding="utf8") as file:
            maze_json = file.read()
    except FileNotFoundError:
        l.critical("Can't render: Maze file '%s' not found", args.file, exc_info=True)
        return
    except OSError:
        l.critical("Can't render: Couldn't open maze file '%s'", args.file, exc_info=True)
        return

    # Parse Maze object
    try:
        maze_obj = maze.MazeFactory().init_from_json_str(maze_json, args.ignore_version)
    except maze.MazeFactoryError:
        l.critical("Can't render: Couldn't create a Maze object", exc_info=True)
        return

    # Parse additional args
    if args.renderer_args is None:
        additional_args = {}
    else:
        # Try to parse as JSON first
        try:
            additional_args = json.loads(args.renderer_args)
        except json.JSONDecodeError:
            l.info("Couldn't parse '%s' as a JSON string. Parsing as a JSON file...", args.renderer_args, exc_info=True)

            # Parse as file
            try:
                with open(args.renderer_args, "r", encoding="utf8") as file:
                    renderer_args_file = file.read()
                    try:
                        additional_args = json.loads(renderer_args_file)
                    except json.JSONDecodeError:
                        l.critical("Couldn't parse renderer args: File opened successfully, but the contents couldn't be parsed.", exc_info=True)
            except FileNotFoundError:
                l.critical("Couldn't parse renderer args: file '%s' not found", args.renderer_args)
                return
            except OSError:
                l.critical("Couldn't parse renderer args: couldn't open file '%s'", args.renderer_args, exc_info=True)
                return

    try:
        rendering_tk.render_maze_obj(renderer, maze_obj, additional_args)
    except rendering_tk.RenderingError as e:
        l.critical("RenderingError: %s", e)
        return

if __name__ == "__main__":
    ## Not required now since mode is positional
    # if args.mode is None:
    #     l.critical("Missing mode argument. Try -h or --help")
    #     sys.exit(1)

    match args.mode.lower():
        case "render" | "r":
            l.debug("render mode")
            render_mode()
        case _:
            l.critical("Unknown mode: %s. Supported modes: render. Try -h or --help", args.mode)
    