"""Loader for Python files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from ..core import config
from . import base


class PythonFile(base.ConfigurationFile):

    """Configuration file parser for Python files.

    Unlike static format configuration files, Python files are expected to
    generate side-effects by interacting in some way with the Configuration
    singleton.
    """

    def __init__(self, *args, **kwargs):
        super(PythonFile, self).__init__(*args, **kwargs)
        self._parsed = None

    @property
    def parsed(self):
        """Get the code object which represents the compiled Python file.

        This property is cached and only parses the content once.
        """
        if not self._parsed:

            self._parsed = compile(self.content, self.path, 'exec')

        return self._parsed

    @property
    def config(self):
        """Get a Configuration object from the file contents."""
        exec(self.parsed, {}, None)
        return config.Configuration()

    @property
    def namespaces(self):
        """Get an empty iterable.

        An iterable of namespaces cannot be generated from Python files.
        """
        return ()

    def items(self, namespace):
        """Get an empty iterable.

        An iterable of items cannot be generated from Python files.
        """
        return ()
