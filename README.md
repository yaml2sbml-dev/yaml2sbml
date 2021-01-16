# yaml2sbml

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/dc25c9a84ba54710bbb23a6e08ab5d22)](https://www.codacy.com/manual/martamatos/yaml2sbml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yaml2sbml-dev/yaml2sbml&amp;utm_campaign=Badge_Grade)
![CI](https://github.com/yannikschaelte/yaml2sbml/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/yannikschaelte/yaml2sbml/branch/master/graph/badge.svg?token=AORT3GREQJ)](https://codecov.io/gh/yannikschaelte/yaml2sbml)

## Table of contents

* [About](#about)

* [Installation](#installation)

* [Getting Started](#getting-started)

## About

`yaml2sbml` is a small package to convert an ODE model specified in a yaml file into an 
[**SBML**](http://www.sbml.org/) for ODE simulation and into 
[**PEtab**](https://github.com/martamatos/yaml2sbml) for parameter fitting. `yaml2sbml` offers:

* Functionality to translate ODE models in YAML into SBML and PEtab.
* A format validator for the input YAML.
* A Python and a command line interface for translation and validation functionality.
* A model editor, that allows to generate, import and export a YAML models.

## Installation

To install go to the main folder and do:

```shell
# clone the repository
git clone https://github.com/yaml2sbml-dev/yaml2sbml

# go to the folder of yaml2bsml
cd yaml2sbml 

# install
pip install .
```

## Getting Started

The [format documentation](doc/format_documentation.md) describes the input YAML. 
Examples of jupyter notebooks can be found under [`doc/example`](doc/example). 
Most notably:
* [Lotka_Volterra.ipynb](dox/examples/Lotka_Volterra_python/Lotka_Volterra.ipynb), a simple example showing the python package.
* [Lotka_Volterra_CLI.ipynb](dox/examples/Lotka_Volterra_/Lotka_Volterra_CLI.ipynb), a simple example showing the command line interface.


## Contact
If you have a question regarding the tool: Please drop us an issue or a message, we are happy to help.
