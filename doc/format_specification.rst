Input Format for yaml2sbml
==========================


General scope
-------------

*  `yaml2sbml`: Translates ODEs (Initial value problems) of the form `x' = f(t, x, p)` with time `t`, states `x` and (potentially) unknown parameters `p` into a SBML file for simulation purpose.

*  `yaml2PEtab`: Defines a fitting problem of the form `y(t_i) = h(x(t_i), p) + eps_i` with independent Normal or Laplace distributed error terms `eps`. `h` denotes the mapping from system states to observables. PEtab allows to formulate MLE and MAP based fitting problems.

General remarks
---------------

* All identifiers of states, parameters etc. need to be valid SBML identifiers. Therefore identifiers must consist only of upper and lower case letters, digits and underscores, and must not start with a digit.
* Mathematical equations are parsed by `libsbml`s `parseL3Formula`. Hence see it's `documentation <http://sbml.org/Special/Software/libSBML/docs/formatted/python-api/namespacelibsbml.html#ae79acc3be958963c55f1d03944add36b>`_ and the corresponding section of the format specification.
* Equations starting with a minus must be surrounded by brackets or quotation marks, since a leading minus also has a syntactic meaning in YAML and the YAML file will not be valid otherwise.

time \[optional\]
-----------------


.. code-block:: yaml

  time:
    variable: t


Defines a **time variable**, in case the right hand side of the ODE is time-dependent.
  

  
parameters \[optional\]
-----------------------

.. code-block:: yaml

  parameters: 
    - parameterId: p_1
      nominalValue: 1
    
    - parameterId: p_2
      ...     


Defines a **parameter**. `nominalValue` is optional for SBML/PEtab generation, but will be needed for model simulation. Further optional entries are `parameterName, parameterScale, lowerBound, upperBound, estimate` and entries regarding priors. These entries will be written in the corresponding column of the _parameter table_ by `yaml2PEtab.`

For a detailed description see the documentation of the `PEtab parameter table <https://github.com/PEtab-dev/PEtab/blob/master/doc/documentation_data_format.rst#parameter-table>`_ "PEtab parameter table documentation"). 

Further entries are possible and will be written to the _parameter table_ as well but are currently not part of the PEtab standard. 



odes
----

.. code-block:: yaml

  odes:
      - stateId: x_1
        rightHandSide: p_1 * x_1
        initialValue: 1

      - stateId: x_2
        ...      


Defines the **ODE**. An ODE consists of a `stateId` (string), a `rightHandSide` (string, encoding a mathematical expression), and an `initial value`. Initial values can be either numerical values or parameter Ids. 

For a more detailed description of the parsing of mathematical expressions ( for  `rightHandSide`) we refer to the [corresponding section](#parsing-of-mathematical-equations) of this documentation.



assignments \[optional\]
------------------------

.. code-block:: yaml

  assignments:
      - assignmentId: sum_of_states
        formula: x_1 + x_2

      - assignmentId: ...
        ...


**Assigns** the term `assignmentId` to the value given in `formula`. The value is dynamically updated and can depend on parameters, states and time. In the SBML assignments are represented via parameter assignment rules.

For a more detailed description of the parsing of mathematical expressions (e.g. for `formula`) we refer to the [corresponding section](#parsing-of-mathematical-equations) of this documentation.



functions \[optional\]
----------------------

.. code-block:: yaml

  functions:
      - functionId: g_1
        arguments: x_1, s
        formula: s * x_1 + 1

      - functionId: g_2
        ...

Defines a **function**, that can be called in other parts of the ODE definitions, e.g. in the example above via  `g_1(x_1, s)`. 

**Please note**, that all unknowns appearing in the formula (e.g. also parameters or the time variable) also have to be arguments of the function.  

For a more detailed description of the parsing of mathematical expressions (e.g. for  `formula`) we refer to the [corresponding section](#parsing-of-mathematical-equations) of this documentation.



observables \[optional\]
------------------------

.. code-block:: yaml

  observables:

      - observableId: Obs_1
        observableFormula: x_1 + x_2

        noiseFormula: noiseParameter1
        noiseDistribution: normal

      - observableId: Obs_2
        ...

Defines the **observables**. Observables are not part of the SBML standard and hence only influence the _observable table_ generated in `yaml2PEtab`. The entries are written to the corresponding columns of the PEtab observable table. According to the PEtab standard, an observable table can take the following entries:  `observableId, observableName, observableFormula, observableTransformation, noiseFormula, noiseDistribution`. 

For a detailed discussion see the `corresponding part of the PEtab documentation <https://github.com/PEtab-dev/PEtab/blob/master/doc/documentation_data_format.rst#observables-table>`_.



conditons \[optional\]
----------------------

.. code-block:: yaml

  conditions:

      - conditionId: condition1
        p_1: 1
        x_1: 2
        ...


Conditions allows to set parameters or initial conditions of states to a numeric value/unknown parameter. This allows to specify different experimental setups in the data generation (e.g. different initial conditions for different runs of an experiment). 

The "trivial condition table" (if only one setup exist) is generated by:

.. code-block:: yaml

  conditions:
        - conditionId: condition1


For a detailed discussion see the `corresponding part of the PEtab documentation <https://github.com/PEtab-dev/PEtab/blob/master/doc/documentation_data_format.rst#condition-table>`_.



Parsing of mathematical equations
---------------------------------

 Throughout `yaml2sbml` formulas are parsed by `libsbml's` `parseL3Formula` function. Further information on the syntax are given by:

*  the `working with math <http://sbml.org/Special/Software/libSBML/docs/formatted/python-api/libsbml-math.html>`_ - section of the `libsbml` documentation.
*  the `documentation <http://sbml.org/Special/Software/libSBML/docs/formatted/python-api/namespacelibsbml.html#ae79acc3be958963c55f1d03944add36b>`_ of `libsbml.parseL3Formula`.


This gives access to e.g.:

*  +, -, *, / and power,
*  trigonometric/hyperbolic functions, 
*  exponential/logarithmic functions,
*  piecewise defined functions,
*  boolean expressions like "<".
