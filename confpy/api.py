"""Imports of all config related objects and features for ease of use."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from .core.config import Configuration
from .core.namespace import Namespace
from .core.namespace import AutoNamespace
from .options.boolopt import BoolOption
from .options.listopt import ListOption
from .options.numopt import IntegerOption
from .options.numopt import FloatOption
from .options.stropt import StringOption
from .options.stropt import PatternOption
from .parser import parse_options


__all__ = (
    'Configuration',
    'Namespace',
    'AutoNamespace',
    'BoolOption',
    'ListOption',
    'IntegerOption',
    'FloatOption',
    'StringOption',
    'PatternOption',
    'parse_options',
)
