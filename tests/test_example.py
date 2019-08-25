"""Test suite for generating example config files."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from confpy.core import config
from confpy.core import namespace
from confpy.options import boolopt
from confpy.options import numopt
from confpy.options import stropt

example = pytest.importorskip("confpy.example")


@pytest.fixture(scope="module")
def cfg():
    """Get a configuration object with options set."""
    return config.Configuration(
        example_test_section=namespace.Namespace(
            description="section",
            example_empty=boolopt.BoolOption(),
            example_bool=boolopt.BoolOption(default=True, description="bool"),
            example_number=numopt.IntegerOption(default=10, description="int"),
            example_string=stropt.StringOption(default="a", description="str"),
        ),
        example_test_section_two=namespace.Namespace(
            description="section2", example_empty_two=boolopt.BoolOption()
        ),
    )


correct_ini = """# section
[example_test_section]
example_bool = True # bool
example_empty =
example_number = 10 # int
example_string = a # str

# section2
[example_test_section_two]
example_empty_two =

"""


def test_example_generator_ini(cfg):
    """Check if INI files are rendered appropriately."""
    text = example.generate_example_ini(cfg)
    assert text == correct_ini


correct_json = """{
   "example_test_section": {
        "example_bool": "True",
        "example_empty": null,
        "example_number": "10",
        "example_string": "a"
    },
   "example_test_section_two": {
        "example_empty_two": null
    }
}"""


def test_example_generator_json(cfg):
    """Check if JSON files are rendered appropriately."""
    text = example.generate_example_json(cfg)
    assert text == correct_json
