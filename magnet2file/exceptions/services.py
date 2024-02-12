"""
This module defines the custom exception classes for services in the magnet2file package.
"""


class MissingServiceError(Exception):
    """Exception raised when a required service is missing.

    Attributes:
        None
    """
