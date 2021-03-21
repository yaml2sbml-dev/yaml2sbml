import os
import unittest

from yaml2sbml.yaml2sbml import yaml2sbml, _parse_yaml


class TestYaml2SBML(unittest.TestCase):
    """
    TestCase class for testing ODE import from a generic yaml file
    and conversion to SBML.
    """

    def setUp(self):
        this_dir, _ = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_yaml2sbml')

    def test_yaml_import(self):
        """
        Test yaml import/SBML generation...
        """
        yaml_dir = os.path.join(self.test_folder, 'ode_input1.yaml')
        expected_result_file = os.path.join(self.test_folder,
                                            'true_sbml_output.xml')

        sbml_test_dir = os.path.join(self.test_folder, 'sbml_test.xml')

        yaml2sbml(yaml_dir, sbml_test_dir)

        with open(expected_result_file, 'r') as f_in:
            expected_sbml = f_in.read()

        with open(sbml_test_dir, 'r') as f_out:
            observed_sbml = f_out.read()

        # check if lines coincide
        for line_true, line_tested in zip(expected_sbml.split('\n'),
                                          observed_sbml.split('\n')):

            # the line containing name & id will not match...
            if not line_true.startswith('  <model id='):
                self.assertEqual(line_true, line_tested)

        os.remove(sbml_test_dir)

    def test_yaml_import_observables(self):
        """
        Test yaml import/export for a model containing observables.
        """
        yaml_dir = os.path.join(self.test_folder, 'ode_input2.yaml')

        expected_result_file = \
            os.path.join(self.test_folder, 'true_sbml_output.xml')

        sbml_test_dir = os.path.join(self.test_folder, 'sbml_test.xml')

        # Call yaml2sbml with observables as assignments
        yaml2sbml(yaml_dir,
                  sbml_test_dir,
                  observables_as_assignments=True)

        # Call yaml2sbml with observables not translated
        yaml2sbml(yaml_dir, sbml_test_dir)

        with open(expected_result_file, 'r') as f_in:
            expected_sbml = f_in.read()

        with open(sbml_test_dir, 'r') as f_out:
            observed_sbml = f_out.read()

        for line_true, line_tested in zip(expected_sbml.split('\n'),
                                          observed_sbml.split('\n')):

            # the line containing name & id will not match...
            if not line_true.startswith('  <model id='):
                self.assertEqual(line_true, line_tested)

        os.remove(sbml_test_dir)

    def test_catch_invalid_sbml_identifier(self):
        """
        Check for invalid SBML identifiers.
        """
        yaml_dir = os.path.join(self.test_folder,
                                'ode_input_invalid_SBML_identifier.yaml')
        with self.assertRaises(RuntimeError):
            _parse_yaml(yaml_dir,
                        'Test_Model')

    def test_catch_invalid_math(self):
        """
        Check for strings that parseL3Formula can not parse.
        """
        yaml_dir = os.path.join(self.test_folder,
                                'ode_input_invalid_formula.yaml')
        with self.assertRaises(RuntimeError):
            _parse_yaml(yaml_dir,
                        'Test_Model')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestYaml2SBML())
    unittest.main()
