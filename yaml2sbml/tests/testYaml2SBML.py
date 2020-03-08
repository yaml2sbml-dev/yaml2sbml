import os
import unittest

from yaml2sbml.yaml2sbml import parse_yaml
import yaml2sbml.yaml2PEtab as yaml2PEtab


class TestYamlImport(unittest.TestCase):
    """
    TestCase class for testing ODE import from a generic yaml file and conversion to SBML.
    """

    def setUp(self):
        this_dir, this_filename = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_yaml2sbml')

    def test_yaml_import(self):
        """
        Test yaml import/SBML generation...
        """
        ode_file = os.path.join(self.test_folder, 'ode_input2.yaml')
        expected_result_file = os.path.join(self.test_folder, 'true_sbml_output.xml')

        sbml_contents = parse_yaml(ode_file)

        with open(expected_result_file, 'r') as f_in:
            expected_sbml_contents = f_in.read()

        with open(os.path.join(self.test_folder, 'sbml_test.xml'), 'w') as f_out:
            f_out.write(sbml_contents)

        self.assertEqual(expected_sbml_contents, sbml_contents)

        os.remove(os.path.join(self.test_folder, 'sbml_test.xml'))

    def test_yaml_import_observables(self):
        ode_file = os.path.join(self.test_folder, 'ode_input2.yaml')
        expected_result_file = os.path.join(self.test_folder, 'true_sbml_output.xml')

        sbml_contents = parse_yaml(ode_file)

        with open(expected_result_file, 'r') as f_in:
            expected_sbml_contents = f_in.read()

        with open(os.path.join(self.test_folder, 'sbml_test.xml'), 'w') as f_out:
            f_out.write(sbml_contents)

        self.assertEqual(expected_sbml_contents, sbml_contents)

        os.remove(os.path.join(self.test_folder, 'sbml_test.xml'))

    def test_petab_export(self):
        """
        Test PEtab export
        """
        ode_file = os.path.join(self.test_folder, 'ode_input2.yaml')

        yaml2PEtab.yaml2petab(ode_file,
                              self.test_folder,
                              'sbml_test.xml')

        yaml2PEtab.validate_petab_tables(os.path.join(self.test_folder, 'sbml_test.xml'),
                                         self.test_folder)

        for file in ['observable_table.tsv', 'parameter_table.tsv', 'condition_table.tsv', 'sbml_test.xml']:
            os.remove(os.path.join(self.test_folder, file))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestYamlImport())
    unittest.main()
