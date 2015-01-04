"""Tests for Python configuration files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from confpy.core import config
from confpy.core import namespace
from confpy.loaders import pyfile
from confpy.options import boolopt
from confpy.options import numopt
from confpy.options import stropt


@pytest.fixture
def conf_body():
    """Return a static configuration file body."""
    return """
from confpy.core import config
cfg = config.Configuration()
cfg.test_python_loader.test = True
cfg.test_python_loader.many = 10
cfg.test_python_loader.letter = 'a'
"""


@pytest.fixture
def PythonFile(conf_body):
    """Return a PythonFile class which has a fixture for the content."""
    class PythonTestFile(pyfile.PythonFile):

        @property
        def content(self):
            return conf_body

    return PythonTestFile


def test_python_file_creates_config_objects(PythonFile):
    """Test that execing Python files loads options."""
    config.Configuration(
        test_python_loader=namespace.NameSpace(
            test=boolopt.BoolOption(),
            many=numopt.IntegerOption(),
            letter=stropt.StringOption(),
        ),
    )
    generated_conf = PythonFile(path='test').config

    assert generated_conf.test_python_loader.test is True
    assert generated_conf.test_python_loader.many == 10
    assert generated_conf.test_python_loader.letter == 'a'
