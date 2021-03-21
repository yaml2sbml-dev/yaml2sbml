<img src="https://raw.githubusercontent.com/yaml2sbml-dev/yaml2sbml/main/doc/logo/logo_yaml2sbml_long.svg" alt="yaml2sbml logo"/>

[![CI](https://github.com/yaml2sbml-dev/yaml2sbml/workflows/CI/badge.svg)](https://github.com/yaml2sbml-dev/yaml2sbml/actions)
[![codecov](https://codecov.io/gh/yaml2sbml-dev/yaml2sbml/branch/master/graph/badge.svg)](https://codecov.io/gh/yaml2sbml-dev/yaml2sbml)
[![Documentation Status](https://readthedocs.org/projects/yaml2sbml/badge/?version=latest)](https://yaml2sbml.readthedocs.io/en/latest/?badge=latest)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/632acdc8d4ef4f50bf69892b8862fd24)](https://www.codacy.com/gh/yaml2sbml-dev/yaml2sbml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yaml2sbml-dev/yaml2sbml&amp;utm_campaign=Badge_Grade)
[![PyPI](https://badge.fury.io/py/yaml2sbml.svg)](https://badge.fury.io/py/yaml2sbml)

## Table of contents

* [About](#about)

* [Installation](#installation)

* [Getting Started](#getting-started)

* [Basic Syntax](#basic-syntax)

* [Contact](#contact)


## About

`yaml2sbml` is a small package in Python to convert an ODE model specified in a YAML file into 
[**SBML**](http://www.sbml.org/) for ODE simulation and into 
[**PEtab**](https://github.com/PEtab-dev/PEtab/) for parameter fitting. `yaml2sbml` offers:


* a translator of ODE models specified in YAML into SBML/PEtab via a Python and a command-line interface;
* a format validator for the input YAML; and
* a model editor, which provides a simplified interface to generate, import and export YAML models.

## Installation

`yaml2sbml` can be installed from PyPI with

```shell
pip install yaml2sbml
```
For more info see the [docs](https://yaml2sbml.readthedocs.io/en/latest/).

## Getting Started

* The documentation of the tool is hosted on [Read the Docs](https://yaml2sbml.readthedocs.io/en/latest/).
* The [format documentation](https://yaml2sbml.readthedocs.io/en/latest/format_specification.html) describes the input YAML. 

* Jupyter notebooks containing examples can be found under [`doc/examples`](https://github.com/yaml2sbml-dev/yaml2sbml/tree/main/doc/examples).  Most notably:
    * [Lotka_Volterra.ipynb](https://github.com/yaml2sbml-dev/yaml2sbml/tree/main/doc/examples/Lotka_Volterra/Lotka_Volterra_python/Lotka_Volterra.ipynb) showing the Python package,
    * [Lotka_Volterra_CLI.ipynb](https://github.com/yaml2sbml-dev/yaml2sbml/tree/main/doc/examples/Lotka_Volterra/Lotka_Volterra_CLI/Lotka_Volterra_CLI.ipynb) showing the command-line interface, and
    * [Lotka_Volterra_Model_Editor.ipynb](https://github.com/yaml2sbml-dev/yaml2sbml/tree/main/doc/examples/Lotka_Volterra/Lotka_Volterra_Model_Editor/Lotka_Volterra_Model_Editor.ipynb) demonstrates the Model Editor.

## Basic Syntax

### Python

A YAML model can be translated to SBML/PEtab in Python via
```python
import yaml2sbml

# SBML conversion
yaml2sbml.yaml2sbml(yaml_dir, sbml_dir)

#PEtab conversion
yaml2sbml.yaml2petab(yaml_dir, 
                     output_dir,
                     sbml_name)
```
### Command-Line Interface

and in the command-line via 
```shell
# SBML conversion
yaml2sbml <yaml_dir> <sbml_dir>

#PEtab conversion
yaml2petab <yaml_dir> <output_dir> <sbml_name>
```

### Format Validation

Format validation is possible in Python via `yaml2sbml.validate_yaml` and in the command-line via `yaml2sbml_validate`.

## Contact
If you have a question regarding the tool: Please drop us an [issue](https://github.com/yaml2sbml-dev/yaml2sbml/issues/new) or a [mail](mailto:jakob.vanhoefer@uni-bonn.de), we are happy to help.
