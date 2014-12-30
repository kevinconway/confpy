"""Loader for INI format files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

try:

    from ConfigParser import SafeConfigParser as ConfigParser

except ImportError:

    from configparser import ConfigParser

import io

from . import base


class IniFile(base.ConfigurationFile):

    """Configuration file parser for INI style files."""

    def __init__(self, *args, **kwargs):
        super(IniFile, self).__init__(*args, **kwargs)
        self._parsed = None

    @property
    def parsed(self):
        """Get the ConfigParser object which represents the content.

        This property is cached and only parses the content once.
        """
        if not self._parsed:

            self._parsed = ConfigParser()
            self._parsed.readfp(io.StringIO(self.content))

        return self._parsed

    @property
    def namespaces(self):
        """Get an iterable of str representing namespaces within the config."""
        return self.parsed.sections()

    def items(self, namespace):
        """Get a dictionary of entries under a given namespace."""
        return dict(self.parsed.items(namespace))
