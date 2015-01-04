"""Tests for Configuration objects."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from confpy.core import config
from confpy.core import namespace


def test_config_instance_namespace_setting():
    """Test that namespaces are bound to a config on init."""
    ns = namespace.NameSpace(description="test")
    conf = config.Configuration(
        test=ns,
    )

    assert conf.test is ns
    assert conf.test.description == "test"


def test_config_subclasses_are_not_affected_by_parent():
    """Test that Configuration subclasses to not recieve parent namespaces."""
    ns = namespace.NameSpace(description="modified")
    class TestConfiguration(config.Configuration):
        _NAMESPACES = {}

    parent = config.Configuration(
        modified=ns,
    )
    child = TestConfiguration()

    assert parent.modified is ns
    with pytest.raises(AttributeError):

        child.modified
