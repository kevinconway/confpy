"""Tests for list options."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.options import boolopt
from confpy.options import listopt


def test_list_coerce():
    """Test if list values are converted to lists of options."""
    opt = listopt.ListOption(option=boolopt.BoolOption())

    opt.__set__(None, (True, False, "yes", "no"))
    result = tuple(opt.__get__())
    assert result[0] is True
    assert result[1] is False
    assert result[2] is True
    assert result[3] is False


def test_list_string_coerce():
    """Test if string values are converted to lists of options."""
    opt = listopt.ListOption(option=boolopt.BoolOption())

    opt.__set__(None, "TRUE,FALSE   ,yes,no")
    result = tuple(opt.__get__())
    assert result[0] is True
    assert result[1] is False
    assert result[2] is True
    assert result[3] is False


def test_list_default():
    """Test if default values are registered with a list option."""
    opt = listopt.ListOption(
        option=boolopt.BoolOption(), default="true,false,yes,no"
    )

    result = tuple(opt.__get__())
    assert result[0] is True
    assert result[1] is False
    assert result[2] is True
    assert result[3] is False


def test_list_default_none():
    """Test that there is no exception when default is NOne."""
    opt = listopt.ListOption(option=boolopt.BoolOption())

    result = tuple(opt.__get__())
    assert result is not None
    assert iter(result)
