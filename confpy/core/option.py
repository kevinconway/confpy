"""Classes for creating validated configuration options."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


class Option(object):

    """Base class for all validated options."""

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
    def description(self):
        """Get the human description of the options."""
        return self.__doc__

    @property
    def default(self):
        """Get the default value of the property."""
        return self._default

    @property
    def required(self):
        """Get whether or not the value is required."""
        return self._required

    @property
    def value(self):
        """Get the current value of the option.

        If the value is unset the default value will be used instead.
        """
        return self._value if self._value is not None else self._default

    @value.setter
    def value(self, val):
        """Set the value of the option.
        Args:
            val: The value to set the option to.

        Raises:
            TypeError: If the value is not a string or appropriate native type.
            ValueError: If the value is a string but cannot be coerced.
        """
        self._value = self.coerce(val)

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
        """Proxy the request to the 'value' property."""
        return self.value

    def __set__(self, obj, value):
        """Proxy the request to the 'value' property."""
        self.value = value
