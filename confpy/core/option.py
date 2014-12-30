"""Classes for creating validated configuration options."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Option(object):

    """Base class for all validated options.

    Attributes:
        default (optional): The default value for the options.
        required (bool): Whether or not the option is required.
    """

    def __init__(self, description=None, default=None, required=False):
        """Initialize the option with some basic metadata.

        Args:
            description (str, optional): A human readable description of what
                the option represents.
            default (optional): The default value to use if unset.
            required (bool, optional): Whether or not the value must be set.
        """
        self.__doc__ = description
        self._default = default
        self._value = default
        self._required = bool(required)

    @property
    def default(self):
        """Get the default value of the property."""
        return self._default

    @property
    def required(self):
        """Get whether or not the value is required."""
        return self._required

    def coerce(self, value):
        """Convert a string to the appropriate Python value.

        If the value is already the appropriate Python value it should be
        returned without change.

        Args:
            value (str): The string value to coerce.

        Raises:
            TypeError: If the value is not string or appropriate native type.
            ValueError: If the value cannot be converted.

        Returns:
            object: Some Python value.
        """
        return value

    def __get__(self, obj=None, objtype=None):
        """Get the current value of the option.

        Returns:
            object: The current value of the option.

            If the value is unset, a default option is defined, and the
            option is not required then the default value will be returned.

        Raises:
            AttributeError: If the value is unset and required.
        """
        if self.required and self._value is None:

            raise AttributeError("Attempted to access an unset option.")

        if not self.required and self._value is None:

            return self.default

        return self._value

    def __set__(self, obj, value):
        """Set the current value of the option.

        Raises:
            TypeError: If the value is not a string or appropriate native type.
            ValueError: If the value is a string but cannot be coerced.
        """
        self._value = self.coerce(value)
