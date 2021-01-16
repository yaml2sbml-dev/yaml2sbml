import os
import unittest

from yaml2sbml.yaml2sbml import _parse_yaml


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
        ode_file = os.path.join(self.test_folder, 'ode_input1.yaml')
        expected_result_file = os.path.join(self.test_folder,
                                            'true_sbml_output.xml')

        sbml_contents = _parse_yaml(ode_file)

        with open(expected_result_file, 'r') as f_in:
            expected_sbml_contents = f_in.read()

        sbml_test_dir = os.path.join(self.test_folder, 'sbml_test.xml')
        with open(sbml_test_dir, 'w') as f_out:
            f_out.write(sbml_contents)

        self.assertEqual(expected_sbml_contents, sbml_contents)

        os.remove(sbml_test_dir)

    def test_yaml_import_observables(self):
        """
        Test yaml import/export for a model containing observables
        (that are not translated).
        """
        ode_file = os.path.join(self.test_folder, 'ode_input2.yaml')

        expected_result_file = \
            os.path.join(self.test_folder, 'true_sbml_output.xml')

        test_sbml_dir = os.path.join(self.test_folder, 'sbml_test.xml')

        sbml_contents = _parse_yaml(ode_file)

        with open(expected_result_file, 'r') as f_in:
            expected_sbml_contents = f_in.read()

        with open(test_sbml_dir, 'w') as f_out:
            f_out.write(sbml_contents)

        self.assertEqual(expected_sbml_contents, sbml_contents)

        os.remove(test_sbml_dir)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestYaml2SBML())
    unittest.main()
