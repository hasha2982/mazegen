"""This module contains a custom formatter for logging."""

import sys
import logging
from colorama import Fore, Style

class CustomFormatter(logging.Formatter):
    """This class is used to format LogRecords. Inherited from logging.Formatter"""
    def format(self, record: logging.LogRecord) -> str:
        """Return a formatted LogRecord as a string
        
        Example output
            * root, WARNING:
              [W] Warning
            * foo, ERROR:
              (foo) [ERR] Error
            * bar, NOTSET:
              (bar) [N/A] NOTSET

        Arguments
            * record: logging.LogRecord - the record that will be formatted
        
        Returns
            * str - the formatted string
        """
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
    """Return a named logger with a StreamHandler attached to it.

    Arguments
        * name: str - logger's name (defaults to "root")
    
    Returns
        * named Logger with CustomFormatter and propagate = False 
    """
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(CustomFormatter())

    l = logging.getLogger(name)
    l.propagate = False # Fix #22

    l.addHandler(logging_handler)

    return l
