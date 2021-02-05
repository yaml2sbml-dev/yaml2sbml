Contribute
==========

Documentation
-------------

To make yaml2sbml easily usable, we try to provide good documentation,
including code annotation and usage examples.
The documentation is hosted on
`yaml2sbml.readthedocs.io <https://yaml2sbml.readthedocs.io>`_
and updated automatically every time the ``main`` branch is updated.
To create the documentation locally, first install the requirements via::

    pip install .[doc]

and then compile the documentation via::

    cd doc
    make html

Test environment
----------------

We use the virtual testing tool `tox <https://tox.readthedocs.io/en/latest/>`_
for all unit tests, format and quality checks and notebooks.
Its configuration is specified in ``tox.ini``. To run it locally, first
install::

    pip install tox

and then simply execute::

    tox

To run only selected tests (see ``tox.ini`` for what is tested), use e.g.::

    tox -e pyroma,flake8

For continuous integration testing we use GitHub Actions. All tests are run
there on pull requests and required to pass. The configuration is specified
in `.github/workflows/ci.yml`.

Unit tests
----------

Unit tests are located in the ``tests`` folder. All files starting with
``test_`` contain tests and are automatically run on GitHub Actions.
Run them locally via::

    tox -e unittests

which boils mostly down to::

    python3 -m pytest tests

You can also run only specific tests.

Unit tests can be written with `pytest <https://docs.pytest.org/en/latest/>`_
or `unittest <https://docs.python.org/3/library/unittest.html>`_.

PEP8
----

We try to respect the `PEP8 <https://www.python.org/dev/peps/pep-0008>`_
coding standards. We run `flake8 <https://flake8.pycqa.org>`_ as part of the
tests. The flake8 plugins used are specified in ``tox.ini`` and the flake8
configuration given in ``.flake8``.
You can run it locally via::

    tox -e flake8

Pull requests
-------------

If you start working on a new feature or a fix, please create an issue on
GitHub shortly describing the issue and assign yourself.

To get your code merged, please:

1. create a pull request to develop
2. if not already done in a commit message, use the pull request
   description to reference and automatically close the respective issue
   (see https://help.github.com/articles/closing-issues-using-keywords/)
3. check that all tests pass
4. check that the documentation is up-to-date
5. request a code review
