"""Tests for namespace objects."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.core import namespace
from confpy.options import boolopt


def test_namespace_descriptor_binding():
    """Test that option descriptors are bound to a namespace on init."""
    ns = namespace.Namespace(
        test=boolopt.BoolOption(),
    )
    assert ns.test is None
    ns.test = True
    assert ns.test is True
    ns.test = 'no'
    assert ns.test is False
