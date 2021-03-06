yaml2sbml
=========

.. image:: https://github.com/yaml2sbml-dev/yaml2sbml/workflows/CI/badge.svg
   :target: https://github.com/yaml2sbml-dev/yaml2sbml/actions
   :alt: Build status
.. image:: https://codecov.io/gh/yaml2sbml-dev/yaml2sbml/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/yaml2sbml-dev/yaml2sbml
   :alt: Code coverage
.. image:: https://readthedocs.org/projects/yaml2sbml/badge/?version=latest
   :target: https://yaml2sbml.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://app.codacy.com/project/badge/Grade/632acdc8d4ef4f50bf69892b8862fd24
   :target: https://www.codacy.com/gh/yaml2sbml-dev/yaml2sbml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yaml2sbml-dev/yaml2sbml&amp;utm_campaign=Badge_Grade
   :alt: Code quality

:Release: |version|
:Source code: https://github.com/yaml2sbml-dev/yaml2sbml

.. image:: logo/logo_yaml2sbml_long.png
   :alt: yaml2sbml logo
   :align: center
   :scale: 20 %

**yaml2sbml** allows the user to convert a system of ODEs specified in a YAML_
file to SBML_.
In addition, if experimental data is provided in the YAML file, it can also be
converted to PEtab_.

.. toctree::
   :caption: Main
   :maxdepth: 1
   :hidden:

   install
   format_specification
   examples/examples
   api_doc

.. toctree::
   :caption: About
   :maxdepth: 1
   :hidden:

   release_notes
   license
   log
   logo
   contact

.. toctree::
   :caption: Developers
   :maxdepth: 1
   :hidden:

   contribute
   deploy

.. _YAML: https://yaml.org
.. _SBML: http://sbml.org
.. _PEtab: https://petab.readthedocs.io/en/stable/
