"""Tests for string options."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import copy

import pytest

from confpy.options import stropt


def test_string_coerce():
    """Test if values are converted to strings."""
    opt = stropt.StringOption()

    opt.__set__(None, 0)
    assert opt.__get__() == "0"
    opt.__set__(None, "text")
    assert opt.__get__() == "text"
    opt.__set__(None, None)
    assert opt.__get__() == "None"


def test_pattern_coerce():
    """Test if values are converted to pattern matched strings."""
    opt = stropt.PatternOption(pattern="[a-z]")

    opt.__set__(None, "a")
    assert opt.__get__() == "a"
    opt.__set__(None, "b")
    assert opt.__get__() == "b"
    opt.__set__(None, "c")
    assert opt.__get__() == "c"


def test_pattern_coerce_fail():
    """Test if ValueError is raised when text does not match the pattern."""
    opt = stropt.PatternOption(pattern="[a-z]")

    with pytest.raises(ValueError):

        opt.__set__(None, "1")


def test_pattern_deepcopy():
    """Test if PatternOption can be deepcopied for ListOption."""
    opt = stropt.PatternOption(pattern="[a-z]")
    new_opt = copy.deepcopy(opt)

    assert new_opt is not opt
