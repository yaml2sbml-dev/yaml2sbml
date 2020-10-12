import os
import unittest


from yaml2sbml.yaml_validation import validate_yaml
from jsonschema.exceptions import ValidationError


class TestYamlValidation(unittest.TestCase):

    def setUp(self):
        this_dir, _ = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_yaml2sbml')

    def test_validate_yaml_valid_1(self):
        file_in = os.path.join(self.test_folder, 'ode_input1.yaml')
        validate_yaml(file_in)

    #Should throw an error because of extra fields in conditions
    def test_validate_yaml_valid_2(self):
        file_in = os.path.join(self.test_folder, 'ode_input2.yaml')
        validate_yaml(file_in)

    # Should throw an error because of typos
    def test_validate_yaml_typos(self):
        file_in = os.path.join(self.test_folder, 'ode_input_typos.yaml')
        with self.assertRaises(ValidationError):
            validate_yaml(file_in)

    def test_validate_yaml_typos_required(self):
        file_in = os.path.join(self.test_folder, 'ode_input_typos_required.yaml')
        with self.assertRaises(ValidationError):
            validate_yaml(file_in)

    def test_validate_yaml_empty_section(self):
        file_in = os.path.join(self.test_folder, 'ode_input_empty_section.yaml')
        with self.assertRaises(ValidationError):
            validate_yaml(file_in)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestYamlValidation())
    unittest.main()
