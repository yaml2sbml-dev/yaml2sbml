import argparse
import warnings

import libsbml as sbml
import yaml


def yaml2sbml(yaml_file: str, sbml_file: str):
    """
    Takes in a yaml file with the ODE specification, parses it, converts it into SBML format, and writes the SBML file.

    Arguments:
        yaml_file : path to the yaml file with the ODEs specification
        sbml_file: path to the SBML file to be written out

    Returns:

    Raises:

    """
    sbml_as_string = parse_yaml(yaml_file)

    # write sbml file
    with open(sbml_file, 'w') as f_out:
        f_out.write(sbml_as_string)


def parse_yaml(yaml_file: str) -> str:
    """
    Takes in a yaml file with the specification of ODEs, parses it, and returns the corresponding SBML string.

    Arguments:
        yaml_file: path to the yaml file with the ODEs specification

    Returns:
        sbml_string: a string containing the ODEs in SBML format

    Raises:
        SystemExit
    """
    try:
        document = sbml.SBMLDocument(3, 1)
    except ValueError:
        raise SystemExit('Could not create SBMLDocument object')

    model = document.createModel()
    model = _create_compartment(model)

    yaml_dic = _load_yaml_file(yaml_file)
    model = _convert_yaml_blocks_to_sbml(model, yaml_dic)

    sbml_string = sbml.writeSBMLToString(document)

    return sbml_string


def _create_compartment(model):
    """
    Creates a default compartment for the model.
    We don't support multiple compartments at the moment.

    Arguments:
        model: SBML model

    Returns:
        model: SBML model with added compartment

    Raises:

    """
    c = model.createCompartment()
    c.setId('Compartment')
    c.setConstant(True)

    return model


def _load_yaml_file(yaml_file: str) -> dict:
    """
    Loads yaml file and returns the resulting dictionary.

    Arguments:
        yaml_file: SBML model

    Returns:
        yaml_dic: dictionary with parsed yaml file contents

    Raises:

    """
    with open(yaml_file, 'r') as f_in:
        yaml_contents = f_in.read()
        yaml_dic = yaml.full_load(yaml_contents)

    return yaml_dic


def _convert_yaml_blocks_to_sbml(model, yaml_dic: dict):
    """
    Converts each block in the yaml dictionary to SBML.

    Arguments:
        model: SBML model
        yaml_dic: dictionary with yaml contents

    Returns:
        model: SBML model with added entities

    Raises:

    """
    function_dict = {'time': read_time_block,
                     'constants': read_constants_block,
                     'parameters': read_parameters_block,
                     'states': read_states_block,
                     'assignments': read_assignments_block,
                     'functions': read_functions_block,
                     'odes': read_odes_block,
                     'observables': read_observables_block,
                     'noise': read_noise_block,
                     'events': read_events_block}

    for block in yaml_dic:
        function_dict[block](model, yaml_dic[block])

    return model


def read_time_block(model, time_dic: dict):
    """
    Reads and processes the time block.
    If time units are not given they're set to seconds.

    Arguments:
        model: SBML model to which the rate rule will be added.
        time_dic: a dictionary with the time block in the ODE yaml file.

    Returns:

    Raises:

    """
    create_time(model, time_dic['variable'])


def create_time(model, time_var: str):
    """
    Creates the time variable, add assignment to 'time'

    Arguments:
        model: the SBML model to which the species will be added.
        time_var: str, the time variable

    Returns:

    Raises:

    """
    time_parameter = model.createParameter()
    time_parameter.setId(time_var)
    time_parameter.setName(time_var)
    time_parameter.setConstant(False)

    time_assignment = model.createAssignmentRule()
    time_assignment.setVariable(time_var)
    time_assignment.setMath(sbml.parseL3Formula('time'))


def read_constants_block(model, constant_list: list):
    """
    Reads and processes the constants block in the ODE yaml file.
    In particular, it reads the constants and adds them to the given SBML model.
    The expected format for constant_dic definition is
    {'id': <constant_id>, 'value': <value>}

    Arguments:
        model: the SBML model
        constant_list: block containing the constant definitions

    Returns:

    Raises:

    """
    for constant_def in constant_list:
        create_parameter(model, constant_def['id'], True, constant_def['value'])


def read_parameters_block(model, parameter_list: list):
    """
    Reads and processes the parameters block in the ODE yaml file.
    In particular, it reads the parameters and adds them to the given SBML model.
    The expected format for parameter definition is
    {'id': <parameter_id>, 'value': <value>}

    Arguments:
        model: the SBML model
        parameter_list: block containing the parameter definitions

    Returns:

    Raises:

    """
    for parameter_def in parameter_list:
        create_parameter(model, parameter_def['id'], True, parameter_def['value'])


def create_parameter(model, id: str, constant: bool, value: str):
    """
    Creates a parameter or constant and adds it to the given SBML model.
    The difference between parameter and constant is only whether the parameter is set as constant or not. If it is
    set as constant then it is a constant, otherwise it is a parameter that can be optimized.
    Units are set as dimensionless by default.

    Arguments:
        model: the SBML model to which the parameter/constant will be added.
        id: the parameter/constant ID
        constant: whether the parameter is actually a constant or not.
        value: the parameter or constant value

    Returns:

    Raises:

    """
    k = model.createParameter()
    k.setId(id)
    k.setName(id)
    k.setConstant(constant)
    k.setValue(float(value))

    k.setUnits('dimensionless')


def read_states_block(model, state_list: list):
    """
    Reads and processes the states block in the ODE yaml file.
    In particular, it reads the states and adds them to the given SBML file as species.
    The expected format of a state definition is:
    {'id': <state_id>, 'value': <value>}

    Arguments:
        model: the SBML model
        state_list: a list of dictionaries where each entry is a state definition

    Returns:

    Raises:

    """
    for state_def in state_list:
        create_species(model, state_def['id'], state_def['initial_value'])


def create_species(model, species_id: str, initial_amount: str):
    """
    Creates a species and adds it to the given SBML model.
    Units are set as dimensionless by default.

    Arguments:
        model: the SBML model to which the species will be added.
        species_id: the species ID
        initial_amount: the species initial amount

    Returns:
        s: the SBML species

    Raises:

    """
    s = model.createSpecies()
    s.setId(species_id)
    s.setInitialAmount(float(initial_amount))
    s.setConstant(False)
    s.setBoundaryCondition(False)
    s.setHasOnlySubstanceUnits(False)
    s.setCompartment('Compartment')

    s.setSubstanceUnits('dimensionless')

    return s


def read_assignments_block(model, assignment_list: list):
    """
    Reads and processes the assignments block in the ODE yaml file.
    In particular, it reads the assignments and adds them to the given SBML file.
    The expected format of a state definition is:
    {'id': <state_id>, 'formula': <formula>}
    This is used to assign a formula (probably time-dependent) to a variable.

    Arguments:
        model: the SBML model
        assignment_list: a list of dictionaries where each entry is an assignment definition

    Returns:

    Raises:

    """

    for assignment_def in assignment_list:
        create_assignment(model, assignment_def['id'], assignment_def['formula'])


def create_assignment(model, assignment_id: str, formula: str):
    """
    Creates an  assignment rule, that assigns id to formula.

    Arguments:
        model: SBML model to which the assignment rule will be added.
        assignment_id: str, the id of the assignment rule
        formula: str: contains the equation for the assignment rule
    Returns:

    Raises:

    """
    assignment_parameter = model.createParameter()
    assignment_parameter.setId(assignment_id)
    assignment_parameter.setName(assignment_id)
    assignment_parameter.setConstant(False)
    assignment_parameter.setUnits('dimensionless')

    assignment_rule = model.createAssignmentRule()
    assignment_rule.setVariable(assignment_id)
    assignment_rule.setMath(sbml.parseL3Formula(formula))


def read_functions_block(model, functions_list: list):
    """
    Reads and processes the functions block in the ODE yaml file.
    In particular, it reads the functions and adds them to the given SBML file as functionDefinitions.
    The expected format of a function definition is:
    {'id': <state_id>, 'arguments': <arguments>,  'formula' : <formula>}

    Arguments:
        model: a SBML model
        functions_list: a list of dictionaries where each entry is a function definition

    Returns:

    Raises:

    """
    for function_def in functions_list:
        create_function(model, function_def['id'], function_def['arguments'], function_def['formula'])


def create_function(model, function_id: str, arguments: str, formula: str):
    """
    Creates a functionDefinition and adds it to the given SBML model.

    Arguments:
        model: SBML model to which the function will be added.
        function_id: the function id/name
        arguments: the arguments of the function (species AND parameters)
        formula: the formula of the function

    Returns:

    Raises:

    """
    f = model.createFunctionDefinition()
    f.setId(function_id)
    math = sbml.parseL3Formula('lambda(' + arguments + ', ' + formula + ')')
    f.setMath(math)


def read_odes_block(model, odes_list: list):
    """
    Reads and processes lines in the odes block in the ODE yaml file.
    In particular, it reads the odes and adds them to the given SBML file as rateRules.
    The expected format of an ode definition is: {'id': <state_variable>, 'right_hand_side' : <right_hand_side>}

    Arguments:
        model: a SBML model
        odes_list: block of ODE definitions

    Returns:

    Raises:

    """
    for ode_def in odes_list:
        create_rate_rule(model, ode_def['state'], ode_def['right_hand_side'])


def create_rate_rule(model, species: str, formula: str):
    """
    Creates a SBML rateRule for a species and adds it to the given model.
    This is where the ODEs from the text file are encoded.

    Arguments:
        model: SBML model to which the rate rule will be added.
        species: the species name of the ODE
        formula: the right-hand-side of the ODE

    Returns:

    Raises:

    """
    r = model.createRateRule()
    r.setId('d/dt_' + species)
    r.setVariable(species)
    math_ast = sbml.parseL3Formula(formula)
    r.setMath(math_ast)


def read_observables_block(model, observable_list: list):
    """
    Reads an processes the observables block in the ODE yaml file.
    In particular it generates the Observables in the SBML file.
    The expected format is: {'id': <observable_id>, 'formula': <observable_formula>}

    Arguments:
        model: SBML model (libsbml)
        observable_list: observables block containing all observable definitions.

    Returns:

    Raises:

    """
    try:
        for observable_def in observable_list:
            create_observable(model, observable_def['id'], observable_def['formula'])
    except TypeError:
        pass


def create_observable(model, observable_id: str, formula: str):
    """
    Creates a parameter with the name observable_id and an assignment rule, that assigns the parameter to
    the equation given in formula.
    Units are set as dimensionless by default.

    Arguments:
        model: SBML model to which the rate rule will be added.
        observable_id: str, the id of the observable
        formula: str: contains the equation for the observable

    Returns:

    Raises:

    """
    obs_param = model.createParameter()
    obs_param.setId('observable_' + observable_id)
    obs_param.setName(observable_id)
    obs_param.setConstant(False)
    obs_param.setUnits('dimensionless')

    obs_assignment_rule = model.createAssignmentRule()
    obs_assignment_rule.setVariable('observable_' + observable_id)
    obs_assignment_rule.setMath(sbml.parseL3Formula(formula))


def read_noise_block(model, line):
    warnings.warn('Noise not supported yet')


# TODO read_events_block
def read_events_block(model, line):
    warnings.warn('Events not supported yet')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Takes in an ODE model in .yaml and converts it to SBML.')
    parser.add_argument('yaml_file', type=str)
    parser.add_argument('sbml_file', type=str)

    args = parser.parse_args()
    print(f'Path to yaml file: {args.yaml_file}')
    print(f'Path to sbml file: {args.sbml_file}')
    print('Converting...')

    yaml2sbml(args.yaml_file, args.sbml_file)