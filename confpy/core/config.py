"""Classes for creating configuration files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import compat
from . import namespace as ns


class Configuration(object):

    """A configuration file.

    Instances of this class act as a global singleton by sharing a dictionary
    of values which is attached to the class. All subclasses will also express
    this behaviour. However, if a subclass wishes to maintain a dictionary
    separate from this parent it should overwrite the '_NAMESPACES' attribute
    with a new class dictionary.
    """

    _NAMESPACES = {}

    def __init__(self, **namespaces):
        """Initialize a configuration with a series of namespaces.

        Args:
            **namespaces: Each keyword should be a Namespace object which will
                be added to the configuration file.

        Raises:
            TypeError: If an entry is not a Namespace object.
            ValueError: If the namespace is already registered.
        """
        super(Configuration, self).__init__()
        for key, entry in compat.iteritems(namespaces):

            self.register(key, entry)

    def get(self, name, default=None):
        """Fetch a namespace from the dictionary.

        Args:
            name (str): The name of the section/namespace.
            default: The value to return if the name is missing.

        Returns:
            namespace.Namespace: The namespace registered under the given name.
        """
        return self._NAMESPACES.get(name, default)

    def register(self, name, namespace):
        """Register a new namespace with the Configuration object.

        Args:
            name (str): The name of the section/namespace.
            namespace (namespace.Namespace): The Namespace object to store.

        Raises:
            TypeError: If the namespace is not a Namespace object.
            ValueError: If the namespace is already registered.
        """
        if name in self._NAMESPACES:

            raise ValueError("Namespace {0} already exists.".format(name))

        if not isinstance(namespace, ns.Namespace):

            raise TypeError("Namespaces must be of type Namespace.")

        self._NAMESPACES[name] = namespace

    def namespaces(self):
        """Get an iterable of two-tuples containing name and namespace.

        The name in this case is the name given at registration time which is
        used to identify a namespace and look it up on the object. The
        namespace is the actual Namespace object.
        """
        return iter(compat.iteritems(self._NAMESPACES))

    def __iter__(self):
        """Proxy iter attempts to the 'namespaces' method."""
        return self.namespaces()

    def __setattr__(self, name, value):
        """Proxy all attribute sets to the 'register' method."""
        self.register(name, value)

    def __getattr__(self, name):
        """Lookup missing attributes in the _NAMESPACES dictionary."""
        attr = self.get(name)
        if not attr:

            raise AttributeError("Namespace {0} does not exist.".format(name))

        return attr
