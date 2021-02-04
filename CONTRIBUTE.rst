Contribute
==========

Contribute documentation
------------------------

To make yaml2sbml easily usable, we are committed to documenting extensively.
This involves in particular documenting the functionality of methods and
classes, the purpose of single lines of code, and giving usage examples.
The documentation is hosted on
`yaml2sbml.readthedocs.io <https://yaml2sbml.readthedocs.io>`_
and updated automatically every time the master branch is updated.
To compile the documentation locally, use::

    cd doc
    make html

Contribute tests
----------------

Tests are located in the ``tests`` folder. All files starting with ``test_``
contain tests and are automatically run on GitHub Actions. Run them manually via::

    python3 -m pytest test

You can also run specific tests.

Tests can be written with `pytest <https://docs.pytest.org/en/latest/>`_
or the `unittest <https://docs.python.org/3/library/unittest.html>`_ module.

PEP8
~~~~

We try to respect the `PEP8 <https://www.python.org/dev/peps/pep-0008>`_
coding standards. We run `flake8 <https://flake8.pycqa.org>`_ as part of the
tests. If flake8 complains, the tests won't pass. You can run it via::

    ./run_flake8.sh

in Linux from the base directory, or directly from python. More, you can use
the tool `autopep8 <https://pypi.org/project/autopep8>`_ to automatically
fix various coding issues.

Contribute code
---------------

If you start working on a new feature or a fix, if not already done, please
create an issue on github shortly describing your plans and assign it to
yourself.

To get your code merged, please:

1. create a pull request to develop
2. if not already done in a commit message already, use the pull request
   description to reference and automatically close the respective issue
   (see https://help.github.com/articles/closing-issues-using-keywords/)
3. check that all tests pass
4. check that the documentation is up-to-date
5. request a code review
