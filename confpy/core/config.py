"""Classes for creating configuration files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import compat
from . import descriptor
from . import namespace as ns


class Configuration(object):

    """A configuration file.

    All instances of this class modify a global dictionary which contains
    all namespaces registered within a Python process.
    """

    def __init__(self, **namespaces):
        """Initialize a file with a series of namespaces.

        Args:
            **namespace: Each keyword should be a Namespace object which will
                be added to the configuration file.

        Raises:
            TypeError: If an entry is not a Namespace object.
            ValueError: If the namespace is already registered.
        """
        super(Configuration, self).__init__()
        for key, entry in compat.iteritems(namespaces):

            self.register(key, entry)

    @descriptor.HybridMethod
    def register(ref, name, namespace):
        """Register a new namespace with the Configuration object.

        Args:
            name (str): The name of the section/namespace.
            namespace (namespace.Namespace): The Namespace object to store.

        Raises:
            TypeError: If the namespace is not a Namespace object.
            ValueError: If the namespace is already registered.
        """
        if isinstance(ref, Configuration):

            ref = type(ref)

        if not isinstance(namespace, ns.NameSpace):

            raise TypeError("Namespaces must be of type NameSpace.")

        if hasattr(ref, name):

            raise ValueError("NameSpace {0} already exists.".format(name))

        setattr(ref, name, namespace)

    @descriptor.HybridMethod
    def __setattr__(ref, name, value):
        """Set all attributes as class attributes.

        To support using Configuration as a singleton, all attributes added to
        instances are actually added to the class as class attributes.
        """
        if isinstance(ref, Configuration):

            ref = type(ref)

        return setattr(ref, name, value)

    @descriptor.HybridMethod
    def __delattr__(ref, name):
        """Delete all attributes as class attributes.

        Similar to __setattr__, this method must look to the class for
        attributes to remove rather than the instance.
        """
        if isinstance(ref, Configuration):

            ref = type(ref)

        return super(ref).__delattr__(name)
