"""Configuration file parser API."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import sys

from . import exc
from .loaders import ini
from .loaders import json
from .loaders import pyfile


FILE_TYPES = {
    "ini": ini.IniFile,
    "json": json.JsonFile,
    "py": pyfile.PythonFile,
}


def configfile_from_path(path):
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


def configuration_from_paths(paths):
    """Get a Configuration object based on multiple file paths.

    Args:
        paths (iter of str): An iterable of file paths which identify config
            files on the system.

    Returns:
        confpy.core.config.Configuration: The loaded configuration object.

    Raises:
        NamespaceNotRegistered: If a file contains a namespace which is not
            defined.
        OptionNotRegistered: If a file contains an option which is not defined
            but resides under a valid namespace.
        UnrecognizedFileExtension: If there is no loader for a path.
    """
    for path in paths:

        cfg = configfile_from_path(path).config

    return cfg


def set_environment_var_options(config, env=None, prefix='CONFPY'):
    """Set any configuration options which have an environment var set.

    Args:
        config (confpy.core.config.Configuration): A configuration object which
            has been initialized with options.
        env (dict): Optional dictionary which contains environment variables.
            The default is os.environ if no value is given.
        prefix (str): The string prefix prepended to all environment variables.
            This value will be set to upper case. The default is CONFPY.

    Returns:
        confpy.core.config.Configuration: A configuration object with
            environment variables set.

    The pattern to follow when setting environment variables is:

        <PREFIX>_<SECTION>_<OPTION>

    Each value should be upper case and separated by underscores.
    """
    env = env or os.environ
    for section_name, section in config:

        for option_name, _ in section:

            var_name = '{0}_{1}_{2}'.format(
                prefix.upper(),
                section_name.upper(),
                option_name.upper(),
            )
            env_var = env.get(var_name)
            if env_var:

                setattr(section, option_name, env_var)

    return config


def set_cli_options(config, arguments=None):
    """Set any configuration options which have a CLI value set.

    Args:
        config (confpy.core.config.Configuration): A configuration object which
            has been initialized with options.
        arguments (iter of str): An iterable of strings which contains the CLI
            arguments passed. If nothing is give then sys.argv is used.

    Returns:
        confpy.core.config.Configuration: A configuration object with CLI
            values set.

    The pattern to follow when setting CLI values is:

        <section>_<option>

    Each value should be lower case and separated by underscores.
    """
    arguments = arguments or sys.argv[1:]
    parser = argparse.ArgumentParser()
    for section_name, section in config:

        for option_name, _ in section:

            var_name = '{0}_{1}'.format(
                section_name.lower(),
                option_name.lower(),
            )
            parser.add_argument('--{0}'.format(var_name))

    args, _ = parser.parse_known_args(arguments)
    args = vars(args)
    for section_name, section in config:

        for option_name, _ in section:

            var_name = '{0}_{1}'.format(
                section_name.lower(),
                option_name.lower(),
            )
            value = args.get(var_name)
            if value:

                setattr(section, option_name, value)

    return config


def check_for_missing_options(config):
    """Iter over a config and raise if a required option is still not set.

    Args:
        config (confpy.core.config.Configuration): The configuration object
            to validate.

    Raises:
        MissingRequiredOption: If any required options are not set in the
            configuration object.

    Required options with default values are considered set and will not cause
    this function to raise.
    """
    for section_name, section in config:

        for option_name, option in section:

            if option.required and option.value is None:

                raise exc.MissingRequiredOption(
                    "Option {0} in namespace {1} is required.".format(
                        option_name,
                        section_name,
                    )
                )

    return config


def parse_options(files, env_prefix='CONFPY'):
    """Parse configuration options and return a configuration object.

    Args:
        files (iter of str): File paths which identify configuration files.
            These files are processed in order with values in later files
            overwriting values in earlier files.
        env_prefix (str): The static prefix prepended to all options when set
            as environment variables. The default is CONFPY.

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
    return check_for_missing_options(
        config=set_cli_options(
            config=set_environment_var_options(
                config=configuration_from_paths(
                    paths=files,
                ),
                prefix=env_prefix,
            ),
        )
    )
