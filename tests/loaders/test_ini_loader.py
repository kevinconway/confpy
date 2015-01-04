"""Tests for ini configuration files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from confpy.core import config
from confpy.core import namespace
from confpy.loaders import ini
from confpy.options import boolopt
from confpy.options import numopt
from confpy.options import stropt


@pytest.fixture
def conf_body():
    """Return a static configuration file body."""
    return """
[test_ini_loader]
test = yes
many = 10
letter = a
    """


@pytest.fixture
def IniFile(conf_body):
    """Return an IniFile class which has a fixture for the content property."""
    class IniTestFile(ini.IniFile):

        @property
        def content(self):
            return conf_body

    return IniTestFile


def test_ini_file_creates_config_objects(IniFile):
    """Test that parsing INI files loads options."""
    config.Configuration(
        test_ini_loader=namespace.Namespace(
            test=boolopt.BoolOption(),
            many=numopt.IntegerOption(),
            letter=stropt.StringOption(),
        ),
    )
    generated_conf = IniFile(path='test').config

    assert generated_conf.test_ini_loader.test is True
    assert generated_conf.test_ini_loader.many == 10
    assert generated_conf.test_ini_loader.letter == 'a'
