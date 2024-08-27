"""
Importing the Enum class from the enum module.

This import is used to define enumeration classes that provide a set of symbolic names
(bound to unique, constant values) for use in the application. Enumerations are useful
for defining sets of related constants and improving code readability.

Usage:
    This module import is used in defining error message constants, configuration options,
    and other sets of named values.
"""

from enum import Enum


class ErrorMessages(Enum):
    """
    Enumeration for standardized error messages used throughout the application.

    Attributes:
        TRANSACTION_NOT_FOUND (str): Error message indicating that a requested transaction was not found.
    """

    ERROR_CREATING_USER = "User already exists"
    INVALID_CREDENTIALS = "Credentials are invalid"
    ERROR_LOGGING_IN = "Error logging in"

    ERROR_CREATING_CATEGORY = "Error Creating Category"
    CATEGORY_NOT_FOUND = "Category not found!"
    CATEGORY_ALREADY_EXISTS = "Category already exist"
    ERROR_RETRIEVING_CATEGORY = "Error retrieving category"
    ERROR_RETRIEVING_CATEGORIES = "Error retrieving categories"
    ERROR_UPDATING_CATEGORY = "Error updating categories"
    ERROR_DELETING_CATEGORY = "Error deleting category"
