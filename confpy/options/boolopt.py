"""Classes for creating boolean options."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from ..core import option


class BoolOption(option.Option):

    """An option which represents a boolean value."""

    def coerce(self, value):
        """Convert text values into boolean values.

        True values are (case insensitive): 'yes', 'true', '1'. False values
        are (case insensitive): 'no', 'false', '0'.

        Args:
            value (str or bool): The value to coerce.

        Raises:
            TypeError: If the value is not a bool or string.
            ValueError: If the value is not bool or an acceptable value.

        Returns:
            bool: The True/False value represented.
        """
        if isinstance(value, bool):

            return value

        if not hasattr(value, 'lower'):

            raise TypeError('Value is not bool or string.')

        if value.lower() in ('yes', 'true', '1'):

            return True

        if value.lower() in ('no', 'false', '0'):

            return False

        raise ValueError('Could not coerce {0} to a bool.'.format(value))
