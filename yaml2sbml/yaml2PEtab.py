import argparse
import os
import pandas as pd
import libsbml as sbml

from . import yaml2sbml


def create_petab_from_yaml(yaml_dict: dict,
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

    # create PEtab observable file, if observables are present in the yaml file.
    observable_table = _create_observable_table(yaml_dict['observables'])

    if observable_table is not None:
        observable_table.to_csv(os.path.join(output_dir, 'observable_table.tsv'), sep='\t')

    parameter_table = _create_parameter_table(yaml_dict['parameters'])
    parameter_table.to_csv(os.path.join(output_dir, 'parameter_table.tsv'), sep='\t')


def _create_observable_table(observable_block_dict: dict):
    """
    Creates an observable table from the observable block given by
    yaml_dict['observable'].

    Arguments:
        observable_block_dict: yaml_dict['parameters'].

    Returns:
        observable_table: pandas data frame containing the observable table.
            (if observable block is not empty, else None)

    Raises:

    """

    if observable_block_dict:

        observable_table = pd.DataFrame({'observableId': [],
                                         'observableName': [],
                                         'observableFormula': [],
                                         'observableTransformation': [],
                                         'noiseFormula': [],
                                         'noiseDistribution': []})
        for observable in observable_block_dict:
            _petab_table_add_row(observable_table, observable)

        return observable_table

    else:
        return None


def _create_parameter_table(parameter_block_dict: dict):
    """
    Creates a parameter table from the parameter block given by
    yaml_dict['parameters'].

    Arguments:
        parameter_block_dict: yaml_dict['parameters'].

    Returns:
        parameter_table: pandas data frame containing the parameter table.

    Raises:

    """
    parameter_table = pd.DataFrame({'parameterId': [],
                                    'parameterName': [],
                                    'parameterScale': [],
                                    'lowerBound': [],
                                    'upperBound': [],
                                    'nominalValue': [],
                                    'estimate': []})

    for parameter in parameter_block_dict:
        _petab_table_add_row(parameter_table, parameter)

    parameter_table.loc[:, 'estimate'] = pd.to_numeric(parameter_table.loc[:, 'estimate'], downcast='integer')

    return parameter_table


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
    parser.add_argument('petab_output', type=str)

    args = parser.parse_args()

    print(f'Path to yaml file: {args.yaml_file}')
    print(f'Output directory: {args.model_name}')
    print(f'Path to sbml/petab files: {args.model_name}')

    print('Converting...')

    # TODO
    yaml2sbml.yaml2sbml(args.yaml_file,
                        args.output_dir,
                        args.model_name,
                        'y' in args.petab_output)


# TODO
def yaml2sbml(yaml_file: str,
              output_dir: str,
              model_name: str,
              petab: bool = True):
    """
    Takes in a yaml file with the ODE specification, parses it, converts it into SBML format, and writes the SBML file.

    Arguments:
        yaml_file : path to the yaml file with the ODEs specification
        output_dir: path the output file(s) are be written out
        model_name: name of SBML model (e.g. lokta_volterra leads to a model named lokta_volterra.xml)
        petab: flag, if the PEtab observable/parameter tables should be generated as well

    Returns:

    Raises:

    """

    if model_name.endswith('.xml'):
        sbml_file = os.path.join(output_dir, model_name)
    else:
        sbml_file = os.path.join(output_dir, model_name + '.xml')

    sbml_as_string = parse_yaml(yaml_file, output_dir, petab)

    # write sbml file
    with open(sbml_file, 'w') as f_out:
        f_out.write(sbml_as_string)


def parse_yaml(yaml_file: str, output_dir: str, petab: bool) -> str:
    """
    Takes in a yaml file with the specification of ODEs, parses it, and returns the corresponding SBML string.

    Arguments:
        yaml_file: path to the yaml file with the ODEs specification
        output_dir: path to the directory, where the output is written
        petab: flag, that indicates weather petab files should be written

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
    _convert_yaml_blocks_to_sbml(model, yaml_dic)

    if petab:
        yaml2PEtab.create_petab_from_yaml(yaml_dic, output_dir)

    sbml_string = sbml.writeSBMLToString(document)

    return sbml_string
