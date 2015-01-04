"""Integration test suite for loading and parsing files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import pytest

from confpy import parser
from confpy.core import config
from confpy.core import namespace
from confpy.options import boolopt


@pytest.fixture
def config_path():
    """Get the path to the config file directory."""
    return os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            'config_files',
        )
    )


@pytest.fixture
def ini_file(config_path):
    """Get the path to an INI configuration file."""
    return os.path.join(
        config_path,
        'conf.ini',
    )


@pytest.fixture
def json_file(config_path):
    """Get the path to an INI configuration file."""
    return os.path.join(
        config_path,
        'conf.json',
    )


@pytest.fixture
def py_file(config_path):
    """Get the path to an INI configuration file."""
    return os.path.join(
        config_path,
        'conf.py',
    )


def test_parse_files(ini_file, json_file, py_file):
    """Test that files can be loaded from path."""
    config.Configuration(
        test_ini_parse=namespace.Namespace(
            ini_loaded=boolopt.BoolOption(),
        ),
        test_json_parse=namespace.Namespace(
            json_loaded=boolopt.BoolOption(),
        ),
        test_python_parse=namespace.Namespace(
            python_loaded=boolopt.BoolOption(),
        ),
    )

    cfg = parser.parse_files(files=(ini_file, json_file, py_file))

    assert cfg.test_ini_parse.ini_loaded is True
    assert cfg.test_json_parse.json_loaded is True
    assert cfg.test_python_parse.python_loaded is True
