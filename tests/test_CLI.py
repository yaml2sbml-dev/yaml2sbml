import os
import shutil
from pytest_console_scripts import script_runner


def test_yaml2sbml_cli(script_runner):
    """Test the command line command `yaml2sbml`."""
    path = os.path.dirname(os.path.abspath(__file__))

    yaml_dir = os.path.join(path, 'test_yaml2sbml/ode_input1.yaml')
    sbml_dir = os.path.join(path, 'test_sbml.xml')

    script_runner.run('yaml2sbml', yaml_dir, sbml_dir)

    os.remove(sbml_dir)


def test_yaml2petab_cli(script_runner):
    """Test the command line command yaml2petab."""
    path = os.path.dirname(os.path.abspath(__file__))
    yaml_dir = os.path.join(path, 'test_yaml2sbml/ode_input2.yaml')
    output_dir = os.path.join(path, 'test_output')
    model_name = 'petab_test_sbml.xml'

    # run with no optional Arguments
    script_runner.run('yaml2petab', yaml_dir, output_dir, model_name)

    # run with optional Arguments
    script_runner.run('yaml2petab', yaml_dir, output_dir, model_name, '-y test_yaml.yml')

    # delete the generated files
    shutil.rmtree(output_dir)


def test_yaml2sbml_validate_cli(script_runner):
    """Test the command line command yaml2sbml_validate"""

    path = os.path.dirname(os.path.abspath(__file__))
    yaml_dir = os.path.join(path, 'test_yaml2sbml/ode_input1.yaml')

    script_runner.run('yaml2sbml_validate', yaml_dir)
