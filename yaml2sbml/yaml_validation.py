import os
import yaml
import jsonschema

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
    # read in yaml_file
    with open(yaml_file, 'r') as f_in:
        yaml_contents = f_in.read()
        yaml_in = yaml.full_load(yaml_contents)

    _validate_yaml_from_dict(yaml_in)


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
