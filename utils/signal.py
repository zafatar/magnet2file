"""This module contains a signal handler for system signals"""

import sys

from signal import signal, SIGINT

import logging

logger = logging.getLogger(__name__)


def add_sigint_handler(signal_received=SIGINT):
    """This adds a handler to a system signal

    Args:
        signal_received (Signal): Signal type
        handler (Handler): Handler method
    """
    signal(signal_received, handler)


def handler(signal_received, frame):
    """This is a handler method which runs with a system signal

    Args:
        signal_received (Signal): Signal type
        frame (Frame): Frame which received the signal
    """
    logger.info("%s - %s", signal_received, frame)

    # Handle any cleanup here
    print("\n\nExiting...\nBye.\n")
    sys.exit()
