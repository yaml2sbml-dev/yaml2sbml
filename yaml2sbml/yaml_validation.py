"""Validator of the input yaml."""
import os
import yaml
import jsonschema
from yaml.scanner import ScannerError
import argparse


SCHEMA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "yaml_schema.yaml")


def validate_yaml(yaml_dir: str):
    """
    Validate the syntax of the YAML file.

    Arguments:
        yaml_dir: path to YAML file to be validated

    Returns:
        jsonschema.validate
    """
    try:

        with open(yaml_dir, 'r') as f_in:
            yaml_contents = f_in.read()
            yaml_dict = yaml.full_load(yaml_contents)

    except ScannerError:
        raise RuntimeError('YAML file can not be parsed due to a Scanner '
                           'Error. This commonly happens if formulas begin '
                           'with a minus. Please set them inside of brackets '
                           '"(...)" or quotation marks.')

    _validate_yaml_from_dict(yaml_dict)
    print('YAML file is valid ✅')


def _validate_yaml_from_dict(yaml_dict: dict):
    """
    Validate the syntax of the YAML file, using a dict as input.

    Arguments:
        yaml_dict: YAML model as dict.

    Returns:
        jsonschema.validate
    """
    # read in SCHEMA
    with open(SCHEMA, 'r') as f_in:
        yaml_contents = f_in.read()
        schema = yaml.full_load(yaml_contents)

    jsonschema.validate(instance=yaml_dict, schema=schema)


def main():
    """Command-Line Interface."""
    parser = argparse.ArgumentParser(
        description='Validates a yaml model '
                    'so that it can be used by yaml2bsml.')

    parser.add_argument('yaml_file', type=str,
                        help='Directory of yaml file, that '
                             'should be validated.')

    args = parser.parse_args()

    print(f'Path to yaml file: {args.yaml_file}')
    print('Validating...')

    validate_yaml(args.yaml_file)


if __name__ == '__main__':
    main()
