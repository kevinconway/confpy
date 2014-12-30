"""Tests for Configuration objects."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

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


def test_config_class_namespace_setting():
    """Test that namespaces are bound to a config after init."""
    ns = namespace.NameSpace(description="class test")
    config.Configuration.class_test = ns
    config.Configuration.class_test = ns

    assert config.Configuration.class_test is ns
    assert config.Configuration.class_test.description == "class test"


def test_config_combo_namespaces():
    """Test that both instances and the class can reach namespaces."""
    set_by_class = namespace.NameSpace()
    set_by_instance = namespace.NameSpace()
    config.Configuration.set_by_class = set_by_class
    instance = config.Configuration(set_by_instance=set_by_instance)

    assert instance.set_by_instance is set_by_instance
    assert instance.set_by_class is set_by_class

    assert config.Configuration.set_by_class is set_by_class
    assert config.Configuration.set_by_instance is set_by_instance
