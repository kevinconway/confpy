"""Py2/Py3 compatibility helpers."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

try:

    import __builtin__ as builtins

except ImportError:

    import builtins

import itertools


if hasattr(builtins, 'xrange'):

    range = builtins.xrange

else:

    range = builtins.range

if not hasattr(builtins, 'unicode'):

    unicode = builtins.str

else:

    unicode = builtins.unicode

if not hasattr(builtins, 'basestring'):

    basestring = unicode

else:

    basestring = builtins.basestring

if not hasattr(builtins, 'long'):

    long = builtins.int

else:

    long = builtins.long

if hasattr(itertools, 'izip'):

    zip = itertools.izip

else:

    zip = builtins.zip


def iteritems(dictionary):
    """Replacement to account for iteritems/items switch in Py3."""
    if hasattr(dictionary, 'iteritems'):

        return dictionary.iteritems()

    return dictionary.items()
