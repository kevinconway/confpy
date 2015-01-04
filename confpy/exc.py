"""Configuration related exceptions."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class MissingRequiredOption(ValueError):

    """Represents a required option which has not been set after parsing."""


class NamespaceNotRegistered(AttributeError):

    """Represents an attempt to set values in a non-existent Namespace."""


class OptionNotRegistered(AttributeError):

    """Represents an attempt to set the value for a non-existent Option."""


class UnrecognizedFileExtension(ValueError):

    """Represents a file extension that cannot be parsed."""
