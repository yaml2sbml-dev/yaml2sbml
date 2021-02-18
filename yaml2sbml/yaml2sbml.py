"""Translate ODEs in the YAML format into SBML."""
import argparse
import warnings

import libsbml as sbml
import yaml
from yaml.scanner import ScannerError

from .yaml_validation import _validate_yaml_from_dict


def yaml2sbml(yaml_dir: str, sbml_dir: str):
    """
    Parse a YAML file with the specification of ODEs and write it to SBML.

    SBML is written within this function.

    Arguments:
        yaml_file : path to the yaml file with the ODEs specification
        sbml_file: path to the SBML file to be written out
    """
    sbml_as_string = _parse_yaml(yaml_dir)

    # write sbml file
    with open(sbml_dir, 'w') as f_out:
        f_out.write(sbml_as_string)


def _parse_yaml(yaml_dir: str) -> str:
    """
    Parse a YAML file with the specification of ODEs to SBML.

    The SBML is returned as string.

    Arguments:
        yaml_dir: path to the yaml file with the ODEs specification

    Returns:
        sbml_string: a string containing the ODEs in SBML format

    Raises:
        SystemExit
    """
    yaml_dict = _load_yaml_file(yaml_dir)
    _validate_yaml_from_dict(yaml_dict)
    sbml_string = _parse_yaml_dict(yaml_dict)

    return sbml_string


def _parse_yaml_dict(yaml_dict) -> str:
    """
    Generate a string, containing the SBML from a yaml_dict.

    Arguments:
        yaml_dict: dictionary, containing to the yaml file with the ODEs
                   specification.

    Returns:
        sbml_string: a string containing the ODEs in SBML format.

    """
    try:
        document = sbml.SBMLDocument(3, 1)
    except ValueError:
        raise SystemExit('Could not create SBMLDocument object')

    model = document.createModel()
    model = _create_compartment(model)

    _convert_yaml_blocks_to_sbml(model, yaml_dict)

    # check consistency and give warnings for errors in SBML:
    if document.checkConsistency():

        for error_num in range(document.getErrorLog().getNumErrors()):
            if not document.getErrorLog().getError(error_num).isWarning():
                warnings.warn(
                    document.getErrorLog().getError(error_num).getMessage(),
                    RuntimeWarning)

    sbml_string = sbml.writeSBMLToString(document)

    return sbml_string


def _create_compartment(model: sbml.Model):
    """
    Create a default compartment for the model.

    yaml2sbml doesn't support multiple compartments.

    Arguments:
        model: SBML model

    Returns:
        model: SBML model with added compartment
    """
    c = model.createCompartment()
    c.setId('Compartment')
    c.setConstant(True)
    c.setSize(1)

    return model


def _load_yaml_file(yaml_file: str) -> dict:
    """
    Load YAML file from a dictionary.

    Arguments:
        yaml_file: directory YAML model

    Returns:
        yaml_dic: dictionary with parsed yaml file contents
    Raises:
        RuntimeError, if yaml can not be parsed, e.g. to incorrectly
            formatted entries
    """
    try:

        with open(yaml_file, 'r') as f_in:
            yaml_contents = f_in.read()
            yaml_dict = yaml.full_load(yaml_contents)

    except ScannerError:
        raise RuntimeError('YAML file can not be parsed due to a Scanner '
                           'Error. This commonly happens if formulas are '
                           'starting with a minus. Please set them inside of '
                           'brackets "(...)" or quotation marks.')
    return yaml_dict


def _convert_yaml_blocks_to_sbml(model: sbml.Model, yaml_dic: dict):
    """
    Convert each block in the yaml dictionary to SBML.

    Arguments:
        model: SBML model
        yaml_dic: dictionary with yaml contents

    Returns:
        model: SBML model with added entities
    """
    function_dict = {'time': _read_time_block,
                     'parameters': _read_parameters_block,
                     'assignments': _read_assignments_block,
                     'functions': _read_functions_block,
                     'observables': _read_observables_block,
                     'odes': _read_odes_block,
                     'conditions': _read_conditions_block}

    for block in yaml_dic:
        function_dict[block](model, yaml_dic[block])

    return model


def _read_time_block(model: sbml.Model, time_dic: dict):
    """
    Read and process the time block.

    Arguments:
        model: SBML model to which the rate rule will be added.
        time_dic: a dictionary with the time block in the ODE yaml file.
    """
    if time_dic['variable'] == 'time':
        return
    else:
        _create_time(model, time_dic['variable'])


def _create_time(model: sbml.Model, time_var: str):
    """
    Create the time variable, add assignment to 'time'.

    Arguments:
        model: the SBML model to which the species will be added.
        time_var: str, the time variable
    """
    time_parameter = model.createParameter()
    time_parameter.setId(time_var)
    time_parameter.setName(time_var)
    time_parameter.setConstant(False)

    time_assignment = model.createAssignmentRule()
    time_assignment.setVariable(time_var)
    time_assignment.setMath(sbml.parseL3Formula('time'))


def _read_parameters_block(model: sbml.Model, parameter_list: list):
    """
    Read and process the parameters block in the YAML file.

    The expected format for parameter definition is
    {'parameterId': <parameterId>, 'nominalValue': <nominalValue>}

    Arguments:
        model: the SBML model
        parameter_list: block containing the parameter definitions
    """
    for parameter_def in parameter_list:
        if 'nominalValue' in parameter_def.keys():
            _create_parameter(model,
                              parameter_def['parameterId'],
                              parameter_def['nominalValue'])
        else:
            _create_parameter(model, parameter_def['parameterId'])


def _create_parameter(model: sbml.Model, parameter_id: str, value: str = None):
    """
    Create a parameter and add it to the given SBML model.

    Units are set as dimensionless by default.

    Arguments:
        model: the SBML model to which the parameter will be added.
        parameter_id: the parameter ID
        value: the parameter value, if value is None, no parameter is set.
    """
    k = model.createParameter()
    k.setId(parameter_id)
    k.setName(parameter_id)
    k.setConstant(True)

    if value is not None:
        k.setValue(float(value))

    k.setUnits('dimensionless')


def _read_assignments_block(model: sbml.Model, assignment_list: list):
    """
    Read and process the assignments block in the YAML file.

    The expected format of a state definition is:
    {'assignmentId': <assignmentId>, 'formula': <formula>}

    This is used to assign a formula (possibly time-dependent) to a variable.

    Arguments:
        model: the SBML model
        assignment_list: a list of dictionaries where each entry is an
                         assignment definition
    """
    for assignment_def in assignment_list:
        _create_assignment(model,
                           assignment_def['assignmentId'],
                           assignment_def['formula'])


def _create_assignment(model: sbml.Model, assignment_id: str, formula: str):
    """
    Create an assignment rule, that assigns <id> to <formula>.

    Arguments:
        model: SBML model to which the assignment rule will be added.
        assignment_id: str, the id of the assignment rule
        formula: str: contains the equation for the assignment rule
    """
    assignment_parameter = model.createParameter()
    assignment_parameter.setId(assignment_id)
    assignment_parameter.setName(assignment_id)
    assignment_parameter.setConstant(False)
    assignment_parameter.setUnits('dimensionless')

    assignment_rule = model.createAssignmentRule()
    assignment_rule.setVariable(assignment_id)
    assignment_rule.setMath(sbml.parseL3Formula(formula))


def _read_functions_block(model: sbml.Model, functions_list: list):
    """
    Read and process the functions block in the YAML file.

    The expected format of a function definition is:
        {'functionId': <functionId>,
         'arguments': <arguments>,
         'formula' : <formula>}

    Arguments:
        model: a SBML model
        functions_list: a list of dictionaries where each entry is a
                        function definition
    """
    for function_def in functions_list:
        _create_function(model,
                         function_def['functionId'],
                         function_def['arguments'],
                         function_def['formula'])


def _create_function(model: sbml.Model,
                     function_id: str,
                     arguments: str,
                     formula: str):
    """
    Create a function definition and add it to the SBML model.

    Arguments:
        model: SBML model to which the function will be added.
        function_id: the function id/name
        arguments: the arguments of the function (species AND parameters)
        formula: the formula of the function
    """
    f = model.createFunctionDefinition()
    f.setId(function_id)
    math = sbml.parseL3Formula('lambda(' + arguments + ', ' + formula + ')')
    f.setMath(math)


def _read_odes_block(model: sbml.Model, odes_list: list):
    """
    Read and process the odes block in the YAML file.

    In particular, read the odes and add a species for the corresponding
    state and the right hand side as rateRules to the given SBML file.

    The expected format of an ode definition is:
    {'stateId': <state_variable>, 'rightHandSide' : <right_hand_side>,
    'initialValue' = <initial_value>}

    Arguments:
        model: a SBML model
        odes_list: block of ODE definitions
    """
    for ode_def in odes_list:
        _create_species(model, ode_def['stateId'], ode_def['initialValue'])
        _create_rate_rule(model, ode_def['stateId'], ode_def['rightHandSide'])


def _create_species(model: sbml.Model, species_id: str, initial_amount: str):
    """
    Create a species and adds it to the SBML model.

    Units are set as dimensionless by default.

    Arguments:
        model: the SBML model to which the species will be added.
        species_id: the species ID
        initial_amount: the species initial amount

    Returns:
        s: the SBML species
    """
    s = model.createSpecies()
    s.setId(species_id)

    try:
        s.setInitialAmount(float(initial_amount))
    except ValueError:
        init = model.createInitialAssignment()
        init.setId('init_' + species_id)
        init.setSymbol(species_id)
        init.setMath(sbml.parseL3Formula(initial_amount))

    s.setConstant(False)
    s.setBoundaryCondition(False)
    s.setHasOnlySubstanceUnits(False)
    s.setCompartment('Compartment')

    s.setSubstanceUnits('dimensionless')

    return s


def _create_rate_rule(model: sbml.Model, species: str, formula: str):
    """
    Create an SBML rateRule for a species and add it to the SBML model.

    This is where the ODEs are encoded.

    Arguments:
        model: SBML model to which the rate rule will be added.
        species: the species name of the ODE
        formula: the right-hand-side of the ODE
    """
    r = model.createRateRule()
    r.setId('d/dt_' + species)
    r.setVariable(species)
    math_ast = sbml.parseL3Formula(formula)
    r.setMath(math_ast)


def _read_observables_block(model: sbml.Model, observable_list: list):
    """
    Read an process the observables block in the YAML file.

    Since the observables are not represented in the SBML, it only gives
    a warning to inform the user.

    Arguments:
        model: SBML model (libsbml)
        observable_list: observables block containing all
                         observable definitions.
    """
    warnings.warn(
        'Observables are not represented in the SBML and therefore only have '
        'an effect on the output when called via yaml2PEtab')


def _read_conditions_block(model: sbml.Model, conditions_list: list):
    """
    Read an process the conditions block in the YAML file.

    Since conditions are not represented in the SBML, it only gives
    a warning to inform the user.

    Arguments:
        model: SBML model (libsbml)
        conditions_list: conditions block containing all
                         conditions definitions.
    """
    warnings.warn(
        'Conditions are not represented in the SBML and therefore only have '
        'an effect on the output when called via yaml2PEtab')


def main():
    """Command Line Interface."""
    parser = argparse.ArgumentParser(
        description='Takes in an ODE model in .yaml and converts it to SBML.')
    parser.add_argument('yaml_file', type=str, help='Path to input YAML file.')
    parser.add_argument('sbml_file', type=str,
                        help='Path to output SBML file.')

    args = parser.parse_args()

    print(f'Path to yaml file: {args.yaml_file}')
    print(f'Path to sbml file: {args.sbml_file}')

    print('Converting...')

    yaml2sbml(args.yaml_file, args.sbml_file)


if __name__ == '__main__':
    main()
