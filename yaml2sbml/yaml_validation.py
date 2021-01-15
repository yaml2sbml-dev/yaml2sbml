import os
import yaml
import jsonschema
import argparse

SCHEMA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "yaml_schema.yaml")


def validate_yaml(yaml_file: str):
    """
    Validates the syntax of the yaml file.

    Arguments:
        yaml_file: path to yaml file to be validated

    Returns:
        jsonschema.validate

    Raises:

    """
    # read in yaml_file
    with open(yaml_file, 'r') as f_in:
        yaml_contents = f_in.read()
        yaml_in = yaml.full_load(yaml_contents)

    _validate_yaml_from_dict(yaml_in)
    print('YAML file is valid ✅')


def _validate_yaml_from_dict(yaml_dict: dict):
    """
    Validates the syntax of the yaml file, using a dict as input.

    Arguments:
        yaml_dict: yaml model as dict.

    Returns:
        jsonschema.validate

    Raises:

    """
    # read in SCHEMA
    with open(SCHEMA, 'r') as f_in:
        yaml_contents = f_in.read()
        schema = yaml.full_load(yaml_contents)

    jsonschema.validate(instance=yaml_dict, schema=schema)


def main():
    """
    Function called by the CLI.
    """
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
