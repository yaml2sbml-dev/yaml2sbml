Installation
============

This package requires Python 3.6 or later. Miniconda_ provides a small
installation.

Install from PyPI
-----------------

Install yaml2sbml from PyPI_ via::

    pip install yaml2sbml

Install from GitHub
-------------------

To work with the latest development version, install yaml2sbml from
GitHub_ via::

    pip install https://github.com/yaml2sbml-dev/yaml2sbml/archive/develop.zip

or clone the repository and install from local via::

    git clone https://github.com/yaml2sbml-dev/yaml2sbml
    cd yaml2sbml
    git checkout develop
    pip install -e .

where ``-e`` is short for ``--editable`` and links the installed package to
the current location, such that changes there take immediate effect.

Additional dependencies for running the examples
------------------------------------------------

The notebooks come with additional dependencies. Information on the
installation of the ODE simulator `AMICI <https://github.com/AMICI-dev/AMICI>`_ is given in its
`installation guide <https://github.com/AMICI-dev/AMICI/blob/master/INSTALL.md>`_.
Further dependencies can be installed via::

    pip install yaml2sbml[examples]

.. _Miniconda: http://conda.pydata.org/miniconda.html
.. _PyPI: https://pypi.org/project/yaml2sbml
.. _GitHub: https://github.com/yaml2sbml-dev/yaml2sbml
