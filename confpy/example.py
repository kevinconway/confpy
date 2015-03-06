"""Configuration file example generator."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys

try:

    import jinja2

except ImportError as exc:

    raise exc

except Exception as exc:

    if sys.version_info[0] == 3 and sys.version_info[1] == 2:

        raise ImportError(
            "Example generator cannot be imported in Python 3.2.X."
        )

    raise exc


ENV = jinja2.Environment(
    loader=jinja2.PackageLoader('confpy', 'templates'),
)


def generate_example_ini(config):
    """Generate an INI file based on the given Configuration object.

    Args:
        config (confpy.core.configuration.Configuration): The configuration
            object on which to base the example.

    Returns:
        str: The text of the example INI file.
    """
    return generate_example(config, ext='INI')


def generate_example_json(config):
    """Generate an JSON file based on the given Configuration object.

    Args:
        config (confpy.core.configuration.Configuration): The configuration
            object on which to base the example.

    Returns:
        str: The text of the example JSON file.
    """
    return generate_example(config, ext='JSON')


def generate_example(config, ext='json'):
    """Generate an example file based on the given Configuration object.

    Args:
        config (confpy.core.configuration.Configuration): The configuration
            object on which to base the example.
        ext (str): The file extension to render. Choices: JSON and INI.

    Returns:
        str: The text of the example file.
    """
    template_name = 'example.{0}'.format(ext.lower())
    template = ENV.get_template(template_name)
    return template.render(config=config)
