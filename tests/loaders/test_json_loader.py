"""Tests for json configuration files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from confpy.core import config
from confpy.core import namespace
from confpy.loaders import json
from confpy.options import boolopt
from confpy.options import numopt
from confpy.options import stropt


@pytest.fixture
def conf_body():
    """Return a static configuration file body."""
    return """
    {
        "test_json_loader": {
            "test": true,
            "many": 10,
            "letter": "a"
        }
    }
    """


@pytest.fixture
def JsonFile(conf_body):
    """Return a JsonFile class which has a fixture for the content property."""
    class JsonTestFile(json.JsonFile):

        @property
        def content(self):
            return conf_body

    return JsonTestFile


def test_json_file_creates_config_objects(JsonFile):
    """Test that parsing JSON files loads options."""
    config.Configuration(
        test_json_loader=namespace.NameSpace(
            test=boolopt.BoolOption(),
            many=numopt.IntegerOption(),
            letter=stropt.StringOption(),
        ),
    )
    generated_conf = JsonFile(path='test').config

    assert generated_conf.test_json_loader.test is True
    assert generated_conf.test_json_loader.many == 10
    assert generated_conf.test_json_loader.letter == 'a'
