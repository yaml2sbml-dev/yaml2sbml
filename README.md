![yaml2sbml logo](https://github.com/yaml2sbml-dev/yaml2sbml/blob/master/doc/logo/logo_yaml2sbml_long.png?raw=true)

[![CI](https://github.com/yaml2sbml-dev/yaml2sbml/workflows/CI/badge.svg)](https://github.com/yaml2sbml-dev/yaml2sbml/actions)
[![codecov](https://codecov.io/gh/yaml2sbml-dev/yaml2sbml/branch/master/graph/badge.svg)](https://codecov.io/gh/yaml2sbml-dev/yaml2sbml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/632acdc8d4ef4f50bf69892b8862fd24)](https://www.codacy.com/gh/yaml2sbml-dev/yaml2sbml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yaml2sbml-dev/yaml2sbml&amp;utm_campaign=Badge_Grade)

## Table of contents

* [About](#about)

* [Installation](#installation)

* [Getting Started](#getting-started)

* [Basic Syntax](#basic-syntax)

* [Contact](#contact)


## About

`yaml2sbml` is a small package in Python to convert an ODE model specified in a YAML file into 
[**SBML**](http://www.sbml.org/) for ODE simulation and into 
[**PEtab**](https://github.com/martamatos/yaml2sbml) for parameter fitting. `yaml2sbml` offers:

* Translate ODE models specified in YAML into SBML/PEtab via a Python and a command line interface.
* A format validator for the input YAML.
* A model editor that allows to generate, import and export YAML models.

## Installation

`yaml2sbml`can be installed from PyPI with

```shell
pip install yaml2sbml
```
For more infos see the [docs](https://yaml2sbml.readthedocs.io/en/latest/).

## Getting Started

* The documentation of the tool is hosted on [Read the Docs](https://yaml2sbml.readthedocs.io/en/latest/).
* The [format documentation](https://github.com/yaml2sbml-dev/yaml2sbml/blob/main/doc/format_specification.rst) describes the input YAML. 

* Jupyter notebooks containging examples can be found under [`doc/examples`](https://github.com/yaml2sbml-dev/yaml2sbml/tree/main/doc/examples).  Most notably:
    * [Lotka_Volterra.ipynb](https://github.com/yaml2sbml-dev/yaml2sbml/tree/main/doc/examples/Lotka_Volterra/Lotka_Volterra_python/Lotka_Volterra.ipynb) showing the Python package.
    * [Lotka_Volterra_CLI.ipynb](https://github.com/yaml2sbml-dev/yaml2sbml/tree/main/doc/examples/Lotka_Volterra/Lotka_Volterra_CLI/Lotka_Volterra_CLI.ipynb) showing the command line interface.
    * [Lotka_Volterra_Model_Editor.ipynb](https://github.com/yaml2sbml-dev/yaml2sbml/tree/main/doc/examples/Lotka_Volterra/Lotka_Volterra_Model_Editor/Lotka_Volterra_Model_Editor.ipynb) showing the Model Editor.

## Basic Syntax

### Python

A YAML model can be translated to SBML/PEtab in Python via
```python
import yaml2sbml

# SBML conversion
yaml2sbml.yaml2sbml(input_yaml_dir, output_sbml_dir)

#PEtab conversion
yaml2sbml.yaml2petab(input_yaml_dir, 
                     output_petab_dir,
                     sbml_name)
```
### Command Line Interface

And in the command line via 
```shell
# SBML conversion
yaml2sbml <yaml_input_file> <sbml_output_file>

#PEtab conversion
yaml2petab <yaml_input_file> <petab_output_directory> <model_name>
```

### Format Validation

Format validation is possible in Python via `yaml2sbml.validate_yaml` and in the command line via `yaml2sbml_validate`.

## Contact
If you have a question regarding the tool: Please drop us an [issue](https://github.com/yaml2sbml-dev/yaml2sbml/issues/new) or a [mail](mailto:jakob.vanhoefer@uni-bonn.de), we are happy to help.
