import os
import pandas as pd


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
