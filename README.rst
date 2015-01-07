======
confpy
======

*Config file parsing and option management.*

Defining Configuration Options
==============================

.. code-block:: python

    # Example conf.py

    from confpy.api import Configuration
    from confpy.api import Namespace
    from confpy.api import StringOption

    cfg = Configuration(
        http_options=Namespace(
            description="Options related to HTTP functions.",
            endpoint=StringOption(
                description="The HTTP endpoint to fetch.",
                default="https://some-api.com",
                required=True,
            ),
        ),
    )

The above models a configuration file with one section named "http_options"
which contains on option named "endpoint". Any number of options can be added
to a namespace and any number of namespaces can be added to a configuration

All options have the same core keyword arguments. You may set a default value
for the option using the 'default' keyword and mark the option as required with
the 'required' keyword. Marking an option as required which already has a
default value is redundant and will have no effect.

The description keyword arguments may be given as shown above. These do not
directly impact the functionality of the object. Instead, descriptions are used
when generating sample config files to help document what different options
represent.

Configuration definitions like the one above can be defined anywhere within
your code. However, it is strongly recommended that you have one module, or
very few modules, in your project which contain *only* these definitions.
They should be separate from all other code and logic in your project. This is
suggested because these definitions must be loaded into a Python process
*before* they are used by other code. Techniques for doing this are below in
the 'Loading Configuration Options' section.

Using Options In Your Code
==========================

Any module which imports your configuration definition can access the options
you have defined. Continuing the example from above:

.. code-block:: python

    # some other python file in your project
    from myproject.conf import cfg

    def get_api_data(endpoint=None):
        endpoint = endpoint or cfg.http_options.endpoint
        return requests.get(endpoint)

All confpy options are automatically converted to the appropriate Python type
based on the option used. Accessing the option through its namespace will
retrieve the currently set configuration value.

Loading Configuration Options
=============================

Once the options are defined and used in the code they must be set before they
are useful. Setting values can be done with one, or more, configuration files,
environment variables, and command line arguments. Here are all of the ways to
define the "endpoint" option from our example:

Example INI:

.. code-block::

    [http_options]
    endpoint = "https://some-other-api.com"


Example JSON:

.. code-block:: javascript

    {
        "http_options": {
            "endpoint": "https://some-other-api.com"
        }
    }


Example Python:

.. code-block:: python

    from myproject.conf import cfg
    cfg.http_options.endpoint = "https://some-other-api.com"


Example Env Var:

.. code-block:: shell

    # Note: The CONFPY prefix is configurable.
    export CONFPY_HTTP_OPTIONS_ENDPOINT="https://some-other-api.com"


Example CLI Flag:

.. code-block:: shell

    some_executable --http_options_endpoint="https://some-other-api.com"

All of the above examples set the same option to the same value. Any
combination of these may be used to set or overwrite options. The option parser
will follow a simple pattern for setting and overwrite option values.
Configuration files are parsed first with later files overwriting values from
earlier files. Environment variables are parsed next and can overwrite any
values set by configuration files. CLI flags are parsed last and can overwrite
any value set.

In order to bring these values into your Python process you need to add a line
in your "main" (or equivalent) method which imports your configuration
definition and another line which parses and loads the option values. As stated
above, the importing of configuration definitions must happen before all other
code logic. After the definitions are loaded, but before any other project
code, the option values must also be parsed and loaded. For example:

.. code-block:: python

    def main():

        from myproject.conf import cfg
        # import other configuration definitions if needed.

        from confpy.api import parse_options
        # Files are loaded in order. Later values can overwrite earlier values.
        # Pass an 'env_prefix' keyword argument to change the prefix used
        # in environment variables.
        parse_options(files=('example.ini', 'example.json', 'example.py'))

        # start your service or WSGI app or CLI call.
        from myproject.wsgi import app
        print(cfg.my_options.http_endpoint)
        app.run(8888)

Option Types
============

Values from configuration files are automatically converted to the appropriate
Python type based on the option object used in the configuration definition.
The currently available types are:

-   BoolOption(description=None, required=False, default=None)

    An option which represents a True or False value. The text values of
    'yes', 'true', and '1' are converted to True. The text values of 'no',
    'false', and '0' are converted to False. All values are case-insensitive.

-   ListOption(description=None, option=None, required=False, default=None)

    An option which represents a list of values. The 'option' parameter must
    be an option object which will be used to load/validate each item in the
    list.

-   IntegerOption(description=None, required=False, default=None)

    An option which represents an integer value.

-   FloatOption(description=None, required=False, default=None)

    An option which represents a floating point value.

-   StringOption(description=None, required=False, default=None)

    An option which represents any string value.

-   PatternOption(description=None, pattern=None, required=False, default=None)

    An option which represents a string constrained by a regex pattern. The
    'pattern' attribute must be a string which represent the regexp to use.

Generating Sample Configuration Files
=====================================

There is a programmatic API for generating sample configurations in the
'confpy.example' module. However, the easiest way to generate samples is by
using the 'confpy-generate' script that is installed with this package.

::

    $ confpy-generate --help
    usage: confpy-generate [-h] [--module MODULE] [--file FILE]
                           [--format {JSON,INI}]

    Confpy example generator.

    optional arguments:
      -h, --help           show this help message and exit
      --module MODULE      A python module which should be imported.
      --file FILE          A python file which should be evaled.
      --format {JSON,INI}  The output format of the configuration file.

Multiple '--module' and '--file' flags may be added to load additional
configuration definitions before generating the sample. Module should be
importable on the Python path while files must be paths for which the current
user has read permissions. By default the generator will create a JSON file.
Use the '--format' flag to override this behaviour. Our running example would
generate the following:

::

    confpy-generate --module="myproject.conf"
    {
        "http_options": {
            "endpoint": "https://some-api.com"
        }
    }

    confpy-generate --module="myproject.conf" --format="INI"
    # Options related to HTTP functions.
    [http_options]
    endpoint = "https://some-api.com" # The HTTP endpoint to fetch.

While developing, it may be easier to use the file path rather than the module
path if your file is not installed on the Python path.

::

    confpy-generate --file ./my_project/conf.py

Testing
=======

All tests are organized in the 'tests' subdirectory. The layout of the test
modules is paired one-to-one with the modules they test. For example, the tests
for confpy.core.config are found in tests/core/test_config.py. Attempt to
maintain this organization when adding new tests.

This repository comes with a tox.ini file which is configured to run a fairly
exhaustive set of tests. All the current unit tests run, and pass, under Python
2.6, 2.7, 3.2, 3.3, and 3.4 interpreters. Running the default tox command will
attempt to run the tests in all these environments. In addition, tox is also
configured to run PEP8, PyFlakes, and PyLint checks. The PyLint checks will
make use of the .pylintrc file also included in this repository.

License
=======

::

    (MIT License)

    Copyright (C) 2015 Kevin Conway

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.


Contributing
============

All contributions to this project are protected under the agreement found in
the `CONTRIBUTING` file. All contributors should read the agreement but, as
a summary::

    You give us the rights to maintain and distribute your code and we promise
    to maintain an open source distribution of anything you contribute.
