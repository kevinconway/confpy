"""Classes for creating configuration groups and namespaces."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import compat
from . import descriptor
from . import option


class NameSpace(descriptor.LateDescriptorBinding):

    """A collection of configuration options."""

    def __init__(self, description=None, **entries):
        """Initalize the NameSpace with options

        Args:
            description (str, optional): A human readable description of what
                the NameSpace contains.
            **entries: Each keyword should be an Option object which will be
                added to the NameSpace.

        Raises:
            TypeError: If an entry is not an Option object.
        """
        super(NameSpace, self).__init__()
        self.__doc__ = description
        for key, entry in compat.iteritems(entries):

            if not isinstance(entry, option.Option):

                raise TypeError("Entries must be an Option object.")

            setattr(self, key, entry)

    @property
    def description(self):
        """Get the description of what the namespace contains."""
        return self.__doc__

    def __get__(self, obj=None, objtype=None):
        """Return self as the __get__ value."""
        return self

    def __set__(self, obj, value):
        """Prevent overwriting of NameSpace objects."""
        raise AttributeError("Attempted to overwrite a NameSpace.")

    def __delete__(self, obj):
        """Prevent deleting of NameSpace objects."""
        raise AttributeError("Attempted to delete a NameSpace.")
