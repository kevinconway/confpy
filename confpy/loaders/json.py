"""Loader for JSON format files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json

from . import base


class JsonFile(base.ConfigurationFile):

    """Configuration file parser for JSON style files."""

    def __init__(self, *args, **kwargs):
        super(JsonFile, self).__init__(*args, **kwargs)
        self._parsed = None

    @property
    def parsed(self):
        """Get the JSON dictionary object which represents the content.

        This property is cached and only parses the content once.
        """
        if not self._parsed:

            self._parsed = json.loads(self.content)

        return self._parsed

    @property
    def namespaces(self):
        """Get an iterable of str representing namespaces within the config."""
        return self.parsed.keys()

    def items(self, namespace):
        """Get a dictionary of entries under a given namespace."""
        return self.parsed.copy().get(namespace, {})
