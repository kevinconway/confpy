"""Configuration file parser API."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from . import exc
from .loaders import ini
from .loaders import json
from .loaders import pyfile


FILE_TYPES = {
    "ini": ini.IniFile,
    "json": json.JsonFile,
    "py": pyfile.PythonFile,
}


def get_config(path):
    """Get a ConfigFile object based on a file path.

    This method will inspect the file extension and return the appropriate
    ConfigFile subclass initialized with the given path.

    Args:
        path (str): The file path which represents the configuration file.

    Returns:
        confpy.loaders.base.ConfigurationFile: The subclass which is
            specialized for the given file path.

    Raises:
        UnrecognizedFileExtension: If there is no loader for the path.
    """
    extension = path.split('.')[-1]
    conf_type = FILE_TYPES.get(extension)
    if not conf_type:

        raise exc.UnrecognizedFileExtension(
            "Cannot parse file of type {0}. Choices are {1}.".format(
                extension,
                FILE_TYPES.keys(),
            )
        )

    return conf_type(path=path)


def parse_files(files):
    """Parse a list of files in order and return a configuration object.

    Args:
        files (iter of str): File paths which identify configuration files.

    Returns:
        confpy.core.config.Configuration: The loaded configuration object.

    Raises:
        MissingRequiredOption: If a required option is not defined in any file.
        NamespaceNotRegistered: If a file contains a namespace which is not
            defined.
        OptionNotRegistered: If a file contains an option which is not defined
            but resides under a valid namespace.
        UnrecognizedFileExtension: If there is no loader for a path.
    """
    for config_file in files:

        cfg = get_config(path=config_file).config

    return cfg
