Deploy
======

New production releases should be created every time the ``main`` branch is
updated.

Versions
--------

On every merge to ``main``, the version number in ``yaml2sbml/version.py`` should
be incremented. We use version numbers ``A.B.C``, where roughly

* ``C`` is increased for bug fixes,
* ``B`` is increased for new features and minor API breaking changes,
* ``A`` is increased for major API breaking changes.

as suggested by the
`Python packaging guide <https://packaging.python.org>`_.

Create a new release
--------------------

After new commits have been added via pull requests to the ``develop`` branch,
changes can be merged to ``main`` and a new version of yaml2sbml can be
released.

Merge into main
~~~~~~~~~~~~~~~

1. create a pull request from develop to main,
2. check that all tests pass,
3. check that the documentation is up-to-date,
4. update the version number in ``yaml2sbml/version.py`` (see above),
5. update the release notes in ``doc/release_notes.rst``,
6. request a code review.

To be able to actually perform the merge, sufficient rights may be required.
Also, at least one review is required.

Create a release on GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~

After merging into ``main``, create a new release on GitHub. This can be done
either directly on the project GitHub website, or via the CLI as described
in
`Git Basics - Tagging <https://git-scm.com/book/en/v2/Git-Basics-Tagging>`_.
In the release form,

* specify a tag with the new version as specified in ``yaml2sbml/version.py``,
* include the latest additions to ``doc/release_notes.rst`` in the release
  description.

Upload to PyPI
--------------

The upload to the python package index PyPI has been automatized via GitHub
Actions, specified in ``.github/workflows/deploy.yml``,
and is triggered whenever a new release tag is created.

To manually upload a new version to PyPI, proceed as follows:
First, create a so-called "wheel" via::

    python setup.py sdist bdist_wheel

A wheel is essentially a zip archive which contains the source code
and the binaries (if any).

Then upload the archive::

    twine upload dist/yaml2sbml-x.y.z-py3-non-any.wheel

replacing x.y.z by the respective version number.

See also the
`section on distributing packages 
<https://packaging.python.org/tutorials/distributing-packages>`_
of the Python packaging guide.
