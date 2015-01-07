======
confpy
======

*Config file parsing and option management.*

Usage
=====

Creating Configuration Options
------------------------------

While you can create and register configuration options anywhere within your
code, it is strongly recommended that you place all option definitions within
one file or a small number of files which are separate from other logic in
your project. In order for your options to be parsed from configuration files
the module which defines the options must be loaded before the code which
uses those options.

The suggestion is that you create a single 'conf.py' module in the top level
of your Python package which contains all the option definitions for your
project.

To define the options in your 'conf.py' file you create an instance of the
'confpy.core.config.Configuration' object and pass in one or more
'confpy.core.namespace.NameSpace' objects which, in turn, contain on or more
'confpy.core.option.Option' subclasses.

.. code-block:: python

    # Example conf.py

    from confpy.core import config
    from confpy.core import namespace
    from confpy.options import stropt

    cfg = config.Configuration(
        my_options=namespace.NameSpace(
            description="Options for my new service.",
            http_endpoint=stropt.StringOption(
                description="The HTTP endpoint to curl.",
                default="https://some-api.com",
            )
        )
    )

Using Configuration Options
---------------------------

Any module which imports your 'conf.py' module can access your options through
the Configuration instance stored in 'cfg'.

.. code-block:: python

    # some other python file in your project
    from myproject.conf import cfg

    def get_api_data():
        return curl(endpoint=cfg.my_options.http_endpoint)

All confpy options are automatically converted to the appropriate Python type
based on the option used. Accessing the option through its namespace will
retrieve the currently set configuration value.

Setting Configuration Options
-----------------------------

Once the options are registered and used in the code they need to be set using
a configuration file. Currently confpy supports using INI, JSON, and Python
configuration files to set options. Alternatively, options my also be set using
environment variables.

Example INI:

.. code-block::

    [my_options]
    http_endpoint = "https://some-other-api.com"


Example JSON:

.. code-block:: javascript

    {
        "my_options": {
            "http_endpoint": "https://some-other-api.com"
        }
    }


Example Python:

.. code-block:: python

    from myproject.conf import cfg
    cfg.my_options.http_endpoint = "https://some-other-api.com"


Example Env Var:

.. code-block:: shell

    # Note: The CONFPY prefix is configurable.
    export CONFPY_MY_OPTIONS_HTTP_ENDPOINT="https://some-other-api.com"

Each of the above files accomplishes the same thing. Any format can be used. In
order to load these files and set the values they must be parsed using the
'confpy.parser.parse_options' helper. This should be run after option
definitions, but before other code execution. Typically this would take place
somewhere in the equivalent of your "main" method like starting a WSGI server,
handling a CLI call, or starting your service.

.. code-block:: python

    def main():

        from myproject.conf import cfg
        # import other configuration definitions if needed.

        from confpy.parser import parse_options
        # Files are loaded in order. Later values can overwrite earlier values.
        # Pass an 'env_prefix' keyword argument to change the prefix used
        # in environment variables.
        parse_options(files=('example.ini', 'example.json', 'example.py'))

        # start your service or WSGI app or CLI call.
        print(cfg.my_options.http_endpoint)


Generating Sample Configuration Files
-------------------------------------

There is a sample generator in the 'confpy.example' module which can generate
a configuration file containing all the options registered with confpy.

Testing
=======

All tests are organized in the 'tests' subdirectory. The layout of the test
modules is paired one-to-one with the modules they test. For example, the tests
for confpy.core.config are found in tests/core/test_config.py. Attempt to
maintain this organization when adding new tests.

This repository comes with a tox.ini file which is configured to run a fairly
exhaustive set of tests. All the current unit tests run, and pass, under Python
2.6, 2.7, 3.2, 3.3, and 3.4 interpreters. Running default tox command will
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
