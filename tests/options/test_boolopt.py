"""Tests for boolean options."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.options import boolopt


def test_bool_coerce():
    """Test if text values are converted to booleans."""
    opt = boolopt.BoolOption()

    opt.__set__(None, "1")
    assert opt.__get__() is True
    opt.__set__(None, "yes")
    assert opt.__get__() is True
    opt.__set__(None, "TRUE")
    assert opt.__get__() is True

    opt.__set__(None, "0")
    assert opt.__get__() is False
    opt.__set__(None, "no")
    assert opt.__get__() is False
    opt.__set__(None, "FALSE")
    assert opt.__get__() is False
