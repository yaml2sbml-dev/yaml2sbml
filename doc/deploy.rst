Deploy
======

New production releases should be created every time the master branch is
updated. The master is only updated from the develop branch.

Versioning scheme
-----------------

On every merge to master, the version number in ``yaml2sbml/version.py`` should
be incremented as described below.

For version numbers, we use ``A.B.C``, where

* ``C`` is increased for bug fixes,
* ``B`` is increased for new features and minor API breaking changes,
* ``A`` is increased for major API breaking changes.

Thus, we roughly follow the versioning scheme suggested
by the `Python packaging guide <https://packaging.python.org>`_.

Create a new release
--------------------

After new commits have been added via pull requests to the develop branch,
changes can be merged to master and a new version of yaml2sbml can be released.
Every merge to master should coincide with an incremented version number
and a git tag on the respective merge commit.

Merge into master
~~~~~~~~~~~~~~~~~

1. create a pull request from develop to master,
2. check that all tests pass,
3. check that the documentation is up-to-date,
4. adapt the version number in ``yaml2sbml/version.py`` (see above),
5. update the release notes in ``doc/release_notes.rst``,
6. request a code review,
7. merge into the origin master branch.

To be able to actually perform the merge, sufficient rights may be required.
Also, at least one review is required.

Create a release on GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~

After merging into master, create a new release on GitHub. This can be done
either directly on the project GitHub website, or via the CLI as described
in
`Git Basics - Tagging <https://git-scm.com/book/en/v2/Git-Basics-Tagging>`_.
In the release form,

* specify a tag with the new version as specified in ``yaml2sbml/version.py``,
* include the latest additions to ``doc/release_notes.rst`` in the release
  description.

Upload to PyPI
--------------

The upload to the python package index PyPI has been automatized via github
actions, as in ``.github/workflows/deploy.yml`` and is triggered whenever a
new release tag is created.

To manually upload a new version to pypi, proceed as follows:
First, a so called "wheel" is created via::

    python setup.py sdist bdist_wheel

A wheel is essentially a zip archive which contains the source code
and the binaries (if any).

This archive is uploaded using twine::

    twine upload dist/yaml2sbml-x.y.z-py3-non-any.wheel

replacing x.y.z by the respective version number.

For a more in-depth discussion see also the
`section on distributing packages 
<https://packaging.python.org/tutorials/distributing-packages>`_
of the Python packaging guide.
