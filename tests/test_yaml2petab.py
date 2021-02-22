import os
import shutil
import unittest

import yaml2sbml.yaml2PEtab as yaml2PEtab


class TestYaml2PEtab(unittest.TestCase):
    """
    TestCase class for testing ODE import from a generic yaml file
    and conversion to PEtab.
    """

    def setUp(self):
        this_dir, _ = os.path.split(__file__)
        self.input_folder = os.path.join(this_dir, 'test_yaml2sbml')
        self.output_folder = os.path.join(this_dir, 'test_yaml2sbml_output')

    def tearDown(self):
        shutil.rmtree(self.output_folder)

    def test_petab_export(self):
        """
        Test PEtab export
        """
        input_yaml_dir = os.path.join(self.input_folder, 'ode_input2.yaml')

        yaml2PEtab.yaml2petab(input_yaml_dir,
                              self.output_folder,
                              'sbml_test.xml')

        yaml2PEtab.validate_petab_tables(
            os.path.join(self.output_folder, 'sbml_test.xml'),
            self.output_folder)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestYaml2PEtab())
    unittest.main()
