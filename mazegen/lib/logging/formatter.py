"""
This module contains a custom formatter for logging.
"""

import sys
import logging
from colorama import Fore, Style

class CustomFormatter(logging.Formatter):
    def format(self, record):
        # [E] Error
        # (module) [W] Warning
        log = "" # Record

        # Add logger name if it's not root
        if record.name != "root":
            log += f"({record.name}) "

        # Add severity
        match record.levelno:
            case 0: # NOTSET
                log += "[N/A] "
            case 10: # DEBUG
                log += Fore.BLUE + "[D] " + Fore.RESET
            case 20: # INFO
                log += Fore.BLUE + "[i] " + Fore.RESET
            case 30: # WARNING
                log += Fore.YELLOW + "[W] " + Fore.RESET
            case 40: # ERROR
                log += Fore.RED + "[ERR] " + Fore.RESET
            case 50:
                log += Style.BRIGHT + Fore.RED + "[CRITICAL] " + Style.NORMAL

        # Add message
        log += record.getMessage() + Style.RESET_ALL

        return log

def get_formatted_logger(name = "root"):
    """
    Return a named logger that already has a StreamHandler attached to it.
    """
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(CustomFormatter())

    l = logging.getLogger(name)
    l.addHandler(logging_handler)

    return l
