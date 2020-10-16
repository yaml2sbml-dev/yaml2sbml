# yaml2sbml

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/dc25c9a84ba54710bbb23a6e08ab5d22)](https://www.codacy.com/manual/martamatos/yaml2sbml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yaml2sbml-dev/yaml2sbml&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.com/yaml2sbml-dev/yaml2sbml.svg?branch=master)](https://travis-ci.com/yaml2sbml-dev/yaml2sbml)
[![Coverage Status](https://coveralls.io/repos/github/yaml2sbml-dev/yaml2sbml/badge.svg?branch=yaml_validation)](https://coveralls.io/github/yaml2sbml-dev/yaml2sbml?branch=yaml_validation)

## Table of contents

* [Introduction](#introduction)

* [Installation](#installation)

* [Usage](#usage)

  * [Command line interface](#Command_line_interface)

  * [Python](#Python)

* [Known issues and limitations](#known-issues-and-limitations)

## Introduction

yaml2sbml is a small package to convert an ODE model specified in a yaml file into an [**SBML**](http://www.sbml.org/) for ODE simulation and into [**PEtab**](https://github.com/martamatos/yaml2sbml) for parameter fitting. These file formats can be used with other packages.

* [format_documentation.md](format_documentation.md) provides a documentation of the format of the input yaml. 

* Examples can be found in the `examples` folder.

## Installation

To install go to the main folder and do:

```pip install .```

## Requirements

 * Python 3.6+
 * python-libsbml>=5.18.0
 * PyYAML>=5.3
 * pandas >= 1.0.1 
 * PEtab >= 0.1.4

#### Requirements files

 * `requirements.txt` 

#### How to get Python 3.6+

If you don't have Python 3.6 or higher in your system, the best way to get it is either using pyenv or conda.

With conda you can create a virtual environment with a specific python version. To do so start by installing miniconda if you don't have any sort of conda installed yet, and then create a virtual environment using a specific version of python:

``` conda create -n <virtual_env_name> python=3.7```

To activate the virtual environment do

``` source activate <virtual_env_ńame>```

To install packages use either pip or conda: 

``` conda/pip install <package_name> ```

## Usage

You can either call `yaml2sbml` via its [command line interface](#Command_line_interface) or within your [python code](#Python): 

### Command line interface

#### yaml2sbml command

To convert an ODE model encoded in a yaml file to SBML using the terminal, go to the `yaml2sbml` folder and run:

```shell
 yaml2sbml <yaml_input_file> <sbml_output_file>
```

For instance, using the yaml file in the examples folder:

```shell
 yaml2sbml ../examples/ode_input1.yaml ../examples/sbml_out.xml
```

#### yaml2PEtab command

If you want to generate PEtab parameter, observable and condition tables, additionally to the SBML file using the terminal, go to the `yaml2sbml` folderand run:

```shell
 yaml2petab <yaml_input_file> <petab_output_directory> <model_name>
```

For instance, again using the yaml file in the examples folder:
```shell
 yaml2petab ../examples/ode_input1.yaml ../examples/ example_model.xml
```

### Python

Alternatively you can call `yaml2sbml` within your python code via

```python
import yaml2sbml

yaml2sbml.yaml2sbml(yaml_file, sbml_file)
```

Here all inputs ar given as strings.

To generate PEtab files call `yaml2petab` via

```python
import yaml2sbml

yaml2sbml.yaml2petab(yaml_file,
                     output_dir,
                     model_name)
```
Here `yaml_file, output_dir` and `model_name` are strings.

## Known issues and limitations

* **Compartments** are not supported.
* **Units** are not supported, all quantities are dimensionless.
* Specification of PEtab **data tables** are not in the scope of this tool. 
