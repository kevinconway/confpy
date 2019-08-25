"""Tests for number options."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from confpy.options import numopt


def test_integer_coerce():
    """Test if text values are converted to integer."""
    opt = numopt.IntegerOption()

    opt.__set__(None, 0)
    assert opt.__get__() == 0
    opt.__set__(None, "1")
    assert opt.__get__() == 1
    opt.__set__(None, "10")
    assert opt.__get__() == 10


def test_integer_coerce_fail():
    """Test if coercion fails with ValueError on invalid integer."""
    opt = numopt.IntegerOption()

    with pytest.raises(ValueError):

        opt.__set__(None, "notanumber")


def test_float_coerce():
    """Test if text values are converted to floats."""
    opt = numopt.FloatOption()

    opt.__set__(None, 0)
    assert opt.__get__() == 0.0
    opt.__set__(None, "5.4")
    assert opt.__get__() == 5.4


def test_float_coerce_fail():
    """Test if coercion fails with ValueError on invalid floats."""
    opt = numopt.FloatOption()

    with pytest.raises(ValueError):

        opt.__set__(None, "notanumber")
