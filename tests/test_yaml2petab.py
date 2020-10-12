import os
import unittest

import yaml2sbml.yaml2PEtab as yaml2PEtab


class TestYaml2PEtab(unittest.TestCase):
    """
    TestCase class for testing ODE import from a generic yaml file and conversion to SBML.
    """

    def setUp(self):
        this_dir, _ = os.path.split(__file__)
        self.test_folder = os.path.join(this_dir, 'test_yaml2sbml')

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
    suite.addTest(TestYaml2PEtab())
    unittest.main()
