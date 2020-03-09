import argparse
import os
import pandas as pd
import warnings

import libsbml as sbml
import petab


from . import yaml2sbml


def yaml2petab(yaml_file: str,
               output_dir: str,
               model_name: str):
    """
    Takes in a yaml file with the ODE specification, parses it, converts
    it into SBML format, and writes the SBML file.

    Arguments:
        yaml_file : path to the yaml file with the ODEs specification
        output_dir: path the output file(s) are be written out
        model_name: name of SBML model

    Returns:

    Raises:

    """
    if model_name.endswith('.xml') or model_name.endswith('.sbml'):
        sbml_dir = os.path.join(output_dir, model_name)
    else:
        sbml_dir = os.path.join(output_dir, model_name + '.xml')

    sbml_as_string = yaml2sbml.parse_yaml(yaml_file)

    with open(sbml_dir, 'w') as f_out:
        f_out.write(sbml_as_string)

    # create petab tsv files:
    yaml_dict = yaml2sbml.load_yaml_file(yaml_file)
    create_petab_tables_from_yaml(yaml_dict, output_dir)


def create_petab_tables_from_yaml(yaml_dict: dict,
                                  output_dir: str):
    """
    Parses the yaml dict to a PEtab observable/parameter table.

    Arguments:
        yaml_dict: dict, that contains the yaml file.
        output_dir: directory, where the PEtab tables should be written.

    Returns:
        parameter_table: pandas data frame containing the observable table.

    Raises:

    """
    parameter_table = _create_parameter_table(yaml_dict)
    parameter_table.to_csv(os.path.join(output_dir, 'parameter_table.tsv'), sep='\t', index=False)

    # create PEtab observable table, if observables are present in the yaml file.
    if 'observables' in yaml_dict.keys():
        observable_table = _create_observable_table(yaml_dict)
        observable_table.to_csv(os.path.join(output_dir, 'observable_table.tsv'), sep='\t', index=False)

    # create PEtab condition table, if conditions are present in the yaml file.
    if 'conditions' in yaml_dict.keys():
        condition_table = _create_condition_table(yaml_dict)
        condition_table.to_csv(os.path.join(output_dir, 'condition_table.tsv'), sep='\t', index=False)


def _create_parameter_table(yaml_dict: dict):
    """
    Creates a parameter table from the parameter block in the given yaml_dict.

    Arguments:
        yaml_dict

    Returns:
        parameter_table: pandas data frame containing the parameter table.

    Raises:

    """
    mandatory_id_list = ['parameterId', 'parameterName', 'parameterScale',
                         'lowerBound', 'upperBound', 'nominalValue', 'estimate']

    optional_id_list = ['initializationPriorType', 'initializationPriorParameters',
                        'objectivePriorType', 'objectivePriorParameters']

    return _create_petab_table(yaml_dict['parameters'], mandatory_id_list, optional_id_list)


def _create_observable_table(yaml_dict: dict):
    """
    Creates an observable table from the observable block  in the given yaml_dict.

    Arguments:
        yaml_dict

    Returns:
        observable_table: pandas data frame containing the observable table.
            (if observable block is not empty, else None)

    Raises:

    """
    mandatory_id_list = ['observableId', 'observableFormula', 'noiseFormula']

    optional_id_list = ['observableName', 'observableTransformation', 'noiseDistribution']

    return _create_petab_table(yaml_dict['observables'], mandatory_id_list, optional_id_list)


def _create_condition_table(yaml_dict: dict):
    """
    Creates a condition table from the observable block  in the given yaml_dict.

    Arguments:
        yaml_dict

    Returns:
        condition_table: pandas data frame containing the condition table.
            (if condition block is not empty, else None)

    Raises:

    """
    mandatory_id_list = ['conditionId']

    optional_id_list = ['conditionName'] + \
                       [param['parameterId'] for param in yaml_dict['parameters']] + \
                       [ode['stateId'] for ode in yaml_dict['odes']]

    return _create_petab_table(yaml_dict['conditions'], mandatory_id_list, optional_id_list)


def validate_petab_tables(sbml_dir: str, output_dir: str):
    """
    Validates the petab tables via petab.lint. Throws an error,
    if the petab tables do not follow petab format standard.

    Arguments:
        sbml_dir: directory of the sbml
        output_dir: output directory for petab files

    Returns:

    Raises:
        Errors are raised by lint, if PEtab files are invalid...

    """
    model = sbml.readSBML(sbml_dir)

    parameter_file_dir = os.path.join(output_dir, 'parameter_table.tsv')
    observable_file_dir = os.path.join(output_dir, 'observable_table.tsv')

    if os.path.exists(observable_file_dir):
        observable_df = pd.read_csv(observable_file_dir, sep='\t', index_col='observableId')
        petab.lint.check_observable_df(observable_df)

    else:
        observable_df = None

    parameter_df = pd.read_csv(parameter_file_dir, sep='\t', index_col='parameterId')
    petab.lint.check_parameter_df(parameter_df,
                                  sbml_model=model,
                                  observable_df=observable_df)


def _create_petab_table(block_list: list,
                        mandatory_id_list: list,
                        optional_id_list: id):
    """
    Creates a PEtab table from the block_list in the yaml_dict.

    Arguments:
        block_list: entry from yaml_dict.
        mandatory_id_list: list of mandatory ids in the PEtab table
        optional_id_list: list of optional ids in the PEtab table

    Returns:
        petab_table: pandas data frame containing the petab table.

    Raises:

    """

    petab_table = pd.DataFrame({col_id: [] for col_id in mandatory_id_list})

    for row in block_list:
        _petab_table_add_row(petab_table, row)

    # check if every column is part of PEtab standard.
    for col_name in petab_table.head():
        if not (col_name in mandatory_id_list or col_name in optional_id_list):
            warnings.warn(f'PEtab warning: {col_name} is not part of the PEtab standard.')
    return petab_table


def _petab_table_add_row(petab_table: pd.DataFrame, row_dict: dict):
    """
    Adds a row defined by row_dict to the petab_table given by petab_table.
    In the end the last row of petab_table has the entries

        petab_table[-1, key] = row_dict[key]

    for all keys of row_dict.

    Arguments:
        petab_table: pd.DataFrame containing the current petab table.
        row_dict: dict, that contains the values of the new row.

    Returns:

    Raises:

    """
    n_rows = petab_table.shape[0]

    for key in row_dict.keys():
        petab_table.loc[n_rows + 1, key] = row_dict[key]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Takes in an ODE model in .yaml and converts it to a PEtab file.')
    parser.add_argument('yaml_file', type=str)
    parser.add_argument('output_dir', type=str)
    parser.add_argument('model_name', type=str)

    args = parser.parse_args()

    print(f'Path to yaml file: {args.yaml_file}')
    print(f'Output directory: {args.output_dir}')
    print(f'Path to sbml/petab files: {args.model_name}')

    print('Converting...')

    yaml2petab(args.yaml_file,
               args.output_dir,
               args.model_name)
