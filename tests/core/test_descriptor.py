"""Tests for descriptor objects."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from confpy.core import descriptor


class TestDescriptor(object):

    def __init__(self, value=None):
        self._value = value

    def __get__(self, obj=None, objtype=None):
        return self._value

    def __set__(self, obj, value):
        self._value = value

    def __delete__(self, obj):
        self._value = False


def test_late_descriptor_binding():
    """Test that the LateDescriptorBinding base binds late descriptors."""
    test_value = object()

    class T(descriptor.LateDescriptorBinding):

        def __init__(self):

            self.test = TestDescriptor(value=test_value)

    instance = T()
    assert instance.test is test_value
    instance.test = True
    assert instance.test is True
    del instance.test
    assert instance.test is False
