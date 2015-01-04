"""Descriptor utilities."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


def is_descriptor(obj):
    """True if the object is a descriptor else False."""
    return (
        hasattr(obj, '__get__') or
        hasattr(obj, '__set__') or
        hasattr(obj, '__delete__')
    )


class LateDescriptorBinding(object):

    """Allow for binding of descriptors after class definition.

    Descriptors are only handled appropriately if they are present when the
    class is defined. This class adds custom getattr and setattr behaviour
    to allow for the late binding of descriptors after instance init.
    """

    @property
    def _descriptors(self):
        """Get a dictionary of descriptors bound to the object after init.

        This property will lazy create a dictionary on a hidden attribute
        which contains all late bound descriptors. This is done to bypass
        any need for subclasses to properly call super().__init__() in order
        to generate the attributes needed.
        """
        if '___descriptors' not in self.__dict__:
            self.__dict__['___descriptors'] = self.__dict__.get(
                '___descriptors',
                {},
            )
        return self.__dict__['___descriptors']

    def __getattr__(self, name):
        """Resolve late bound descriptors on __getattr__."""
        if name in self._descriptors:

            return self._descriptors[name].__get__(self, self.__class__)

        raise AttributeError(
            "'{0}' object has no attribute '{1}'".format(
                self.__class__.__name__,
                name,
            )
        )

    def __setattr__(self, name, value):
        """Resolve late bound descriptors on __setattr__."""
        if is_descriptor(value):

            # Place descriptors assigned to an instance attribute in the dict.
            self._descriptors[name] = value
            return None

        # If assigning to a late bound descriptor, call the __set__ method.
        if name in self._descriptors:

            return self._descriptors[name].__set__(self, value)

        # Default to standard behaviour.
        return super(LateDescriptorBinding, self).__setattr__(name, value)

    def __delattr__(self, name):
        """Resolve late bound descriptors on __delattr__."""
        if name in self._descriptors:

            return self._descriptors[name].__delete__(self)

        return super(LateDescriptorBinding, self).__delattr__(name)
