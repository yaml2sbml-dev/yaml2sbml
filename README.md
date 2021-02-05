# yaml2sbml

[![CI](https://github.com/yaml2sbml-dev/yaml2sbml/workflows/CI/badge.svg)](https://github.com/yaml2sbml-dev/yaml2sbml/actions)
[![codecov](https://codecov.io/gh/yaml2sbml-dev/yaml2sbml/branch/master/graph/badge.svg)](https://codecov.io/gh/yaml2sbml-dev/yaml2sbml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/632acdc8d4ef4f50bf69892b8862fd24)](https://www.codacy.com/gh/yaml2sbml-dev/yaml2sbml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yaml2sbml-dev/yaml2sbml&amp;utm_campaign=Badge_Grade)

## Table of contents

* [About](#about)

* [Installation](#installation)

* [Getting Started](#getting-started)

* [Contact](#contact)

## About

`yaml2sbml` is a small package in Python to convert an ODE model specified in a yaml file into an 
[**SBML**](http://www.sbml.org/) for ODE simulation and into 
[**PEtab**](https://github.com/PEtab-dev/PEtab) for parameter fitting. `yaml2sbml` offers:


* Functionality to translate ODE models in YAML into SBML and PEtab.
* A format validator for the input YAML.
* A Python and a command line interface for translation and validation functionality.
* A model editor, that allows to generate, import and export a YAML models.

## About

`yaml2sbml` is a small package in Python to convert an ODE model specified in a yaml file into an 
[**SBML**](http://www.sbml.org/) for ODE simulation and into 
[**PEtab**](https://github.com/martamatos/yaml2sbml) for parameter fitting. `yaml2sbml` offers:

* Functionality to translate ODE models in YAML into SBML and PEtab.
* A format validator for the input YAML.
* A Python and a command line interface for translation and validation functionality.
* A model editor, that allows to generate, import and export a YAML models.

## Installation

To install open your terminal and run:

```shell
# clone the repository
git clone https://github.com/yaml2sbml-dev/yaml2sbml

# go to the folder of yaml2bsml
cd yaml2sbml 

# install
pip install .
```

## Getting Started

* The documentation of the tool is hosted on [read the docs](https://yaml2sbml.readthedocs.io/en/latest/)
* The [format documentation](doc/format_documentation.md) describes the input YAML. 

* Jupyter notebooks containging examples can be found under [`doc/examples`](doc/examples).  Most notably:
    * [Lotka_Volterra.ipynb](doc/examples/Lotka_Volterra/Lotka_Volterra_python/Lotka_Volterra.ipynb), a simple example showing the Python package.
    * [Lotka_Volterra_CLI.ipynb](doc/examples/Lotka_Volterra/Lotka_Volterra_CLI/Lotka_Volterra_CLI.ipynb), a simple example showing the command line interface.

## Contact
If you have a question regarding the tool: Please drop us an issue or a message, we are happy to help.
