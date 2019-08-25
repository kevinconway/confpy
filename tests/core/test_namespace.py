"""Tests for namespace objects."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.core import namespace
from confpy.options import boolopt


def test_namespace_descriptor_binding():
    """Test that option descriptors are bound to a namespace on init."""
    ns = namespace.Namespace(test=boolopt.BoolOption())
    assert ns.test is None
    ns.test = True
    assert ns.test is True
    ns.test = "no"
    assert ns.test is False


def test_namespace_auto_generate():
    """Test if AutoNamespace can generate new options dynamically."""
    ns = namespace.AutoNamespace(
        type=boolopt.BoolOption, test_1=boolopt.BoolOption()
    )
    assert ns.test_1 is None
    ns.test_1 = True
    assert ns.test_1 is True
    ns.test_2 = False
    assert ns.test_2 is False
    assert "test_2" in ns._options
    assert hasattr(ns._options["test_2"], "__get__")
