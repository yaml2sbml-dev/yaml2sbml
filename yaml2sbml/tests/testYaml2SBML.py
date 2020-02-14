import os
import unittest

from yaml2sbml.yaml2sbml import parse_yaml


class TestYamlImport(unittest.TestCase):
    """
    TestCase class for testing ODE import from a generic yaml file and conversion to SBML.
    """

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_yaml2sbml')

    def test_yaml_import(self):
        ode_file = os.path.join(self.test_folder, 'ode_input1.yaml')
        expected_result_file = os.path.join(self.test_folder, 'true_sbml_output1.xml')

        sbml_contents = parse_yaml(ode_file)

        with open(expected_result_file, 'r') as f_in:
            expected_sbml_contents = f_in.read()

        with open(os.path.join(self.test_folder, 'sbml_test.xml'), 'w') as f_out:
            f_out.write(sbml_contents)

        self.assertEqual(expected_sbml_contents, sbml_contents)

        os.remove(os.path.join(self.test_folder, 'sbml_test.xml'))

    def test_yaml_import_observables(self):
        ode_file = os.path.join(self.test_folder, 'ode_input2.yaml')
        expected_result_file = os.path.join(self.test_folder, 'true_sbml_output2.xml')

        sbml_contents = parse_yaml(ode_file)

        with open(expected_result_file, 'r') as f_in:
            expected_sbml_contents = f_in.read()

        with open(os.path.join(self.test_folder, 'sbml_test.xml'), 'w') as f_out:
            f_out.write(sbml_contents)

        self.assertEqual(expected_sbml_contents, sbml_contents)

        os.remove(os.path.join(self.test_folder, 'sbml_test.xml'))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestYamlImport())
    unittest.main()
