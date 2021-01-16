import os
import unittest


from yaml2sbml.yaml_validation import validate_yaml
from jsonschema.exceptions import ValidationError


class TestYamlValidation(unittest.TestCase):

    def setUp(self):
        this_dir, _ = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_yaml2sbml')

    def test_validate_yaml_valid_1(self):
        # Test validation for a valid yaml model.
        file_in = os.path.join(self.test_folder, 'ode_input1.yaml')
        validate_yaml(file_in)

    def test_validate_yaml_valid_2(self):
        # Test validation for a second valid yaml model.
        file_in = os.path.join(self.test_folder, 'ode_input2.yaml')
        validate_yaml(file_in)

    def test_validate_yaml_typos(self):
        # Test if Error is thrown due to typos.
        file_in = os.path.join(self.test_folder, 'ode_input_typos.yaml')
        with self.assertRaises(ValidationError):
            validate_yaml(file_in)

    def test_validate_yaml_typos_required(self):
        # Test if Error is thrown due to typos.
        file_in = os.path.join(self.test_folder,
                               'ode_input_typos_required.yaml')
        with self.assertRaises(ValidationError):
            validate_yaml(file_in)

    def test_validate_yaml_empty_section(self):
        # Test if Error is thrown due to empty observable section.
        file_in = os.path.join(self.test_folder,
                               'ode_input_empty_section.yaml')
        with self.assertRaises(ValidationError):
            validate_yaml(file_in)

    def test_catch_invalid_time_block_missing_variable_key(self):
        # Test time block without kew word "variable".
        file_in = os.path.join(self.test_folder,
                               'ode_input_invalid_time_1.yaml')
        with self.assertRaises(ValidationError):
            validate_yaml(file_in)

    def test_catch_invalid_time_block_as_array(self):
        # Test time block as array instead of single object.
        file_in = os.path.join(self.test_folder,
                               'ode_input_invalid_time_2.yaml')
        with self.assertRaises(ValidationError):
            validate_yaml(file_in)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestYamlValidation())
    unittest.main()
