import os

import jsonschema

from yaml2sbml.yaml2sbml import load_yaml_file

SCHEMA = os.path.join(os.path.abspath(os.path.dirname(__file__)),
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

    schema = load_yaml_file(SCHEMA)
    yaml_in = load_yaml_file(yaml_file)

    jsonschema.validate(instance=yaml_in, schema=schema)
