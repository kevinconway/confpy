"""Command line applications for confpy."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

from .core import config
from .loaders import pyfile
from . import example


def generate_example():
    """Generate a configuration file example.

    This utility will load some number of Python modules which are assumed
    to register options with confpy and generate an example configuration file
    based on those options.
    """
    cmd_args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Confpy example generator.')
    parser.add_argument(
        '--module',
        action='append',
        help='A python module which should be imported.',
    )
    parser.add_argument(
        '--file',
        action='append',
        help='A python file which should be evaled.',
    )
    parser.add_argument(
        '--format',
        default='JSON',
        choices=('JSON', 'INI'),
        help='The output format of the configuration file.',
    )

    args = parser.parse_args(cmd_args)

    for module in args.module or ():

        __import__(module)

    for source_file in args.file or ():

        cfg = pyfile.PythonFile(path=source_file).config

    cfg = config.Configuration()

    print(example.generate_example(cfg, ext=args.format))
