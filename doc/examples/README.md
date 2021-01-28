# yaml2sbml examples

The [`yaml2sbml`](https://github.com/yaml2sbml-dev/yaml2sbml) package translates ODEs specified in YAML into [SBML](http://sbml.org/) for model simulation and [PEtab](https://github.com/PEtab-dev/PEtab) for parameter fitting. This folder contains several example notebooks for the usage of `yaml2sbml`.

# Scope of the Notebooks

* [Lotka Volterra Notebooks]
    * [Lotka Volterra (Python) ](./Lotka_Volterra/Lotka_Volterra_python/Lotka_Volterra.ipynb)
        * Introduces the input format, syntax & capabilities of `yaml2sbml`
        * Showcases ODE simulation & parameter fitting using [AMICI](https://github.com/AMICI-dev/AMICI) & [pyPESTO](https://github.com/ICB-DCM/pyPESTO)
    * [Lotka Volterra CLI](./Lotka_Volterra/Lotka_Volterra_CLI/Lotka_Volterra_CLI.ipynb)
        * Shows the command line interface of `yaml2sbml`
    * [Lotka Volterra Model Editor](./Lotka_Volterra/Lotka_Volterra_Model_Editor/Lotka_Volterra_Model_Editor.ipynb)
        * Shows model construction using the model editor of `yaml2sbml`
* [Sorensen](./Sorensen/yaml2sbml_Sorensen.ipynb)
    * Application example, model of glucose and insulin metabolism
    * Shows the extension of an existing YAML model by the model editor
* [Finite State Projection](./Finite_State_Projection/Finite_State_Projection.ipynb)
    * Application example of a stochastic gene transcription model having hundreds of states.
    * Generates a complex and realistic model within a few lines of python.
* [Format Features](./Format_Features/Format_Features.ipynb)
    * several didactic examples, that show individual features of `yaml2sbml`:
        * Time-dependent right hand sides
        * Step functions in the right hand side
        * Function definitions
