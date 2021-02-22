import os
import shutil

import unittest
import tempfile

from yaml2sbml.YamlModel import YamlModel
from yaml2sbml.yaml_validation import validate_yaml


class TestYamlModel(unittest.TestCase):
    """TestCase class for testing YamlModel."""

    def setUp(self):
        # input directory
        this_dir, _ = os.path.split(__file__)
        self.test_input_folder = os.path.join(this_dir, 'test_yaml2sbml')

        # temporary output directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # remove temporary directory
        shutil.rmtree(self.test_dir)

    def test_load_and_write(self):
        """
        Test loading and writing.
        """
        # read in yaml
        yaml_dir = os.path.join(self.test_input_folder, 'ode_input2.yaml')
        model = YamlModel.load_from_yaml(yaml_dir)

        # save and read in again
        saved_yaml_file = os.path.join(self.test_dir, 'test_yaml.yml')
        model.write_to_yaml(saved_yaml_file)
        reloaded_model = YamlModel.load_from_yaml(saved_yaml_file)

        # check if save+reload did change the model
        self.assertDictEqual(model._yaml_model, reloaded_model._yaml_model)

    def test_time(self):
        """
        Test all functionality regarding the time keyword.
        """
        model = YamlModel()
        time_var = 't'

        self.assertFalse(model.is_set_time())

        model.set_time(time_var)

        self.assertTrue(model.is_set_time())
        self.assertEqual(model.get_time(), time_var)

        model.delete_time()
        self.assertFalse(model.is_set_time())

    def test_parameter(self):
        """
        Test all functionality regarding the 'parameters' keyword.
        """
        model = YamlModel()
        parameter_id = 'p1'
        model.add_parameter(parameter_id,
                            nominal_value=0,
                            lower_bound=-2,
                            upper_bound=2)

        # test get_parameter_by_id
        self.assertIsInstance(model.get_parameter_by_id(parameter_id), dict)

        # test overwrite
        with self.assertRaises(ValueError):
            model.add_parameter(parameter_id=parameter_id)

        # now over write parameter
        model.add_parameter(parameter_id=parameter_id,
                            overwrite=True)

        # test get_parameter_ids
        self.assertListEqual(model.get_parameter_ids(),
                             [parameter_id])

        # test delete
        model.delete_parameter(parameter_id)
        self.assertListEqual(model.get_parameter_ids(), [])

    def test_ode(self):
        """
        Test all functionality regarding the 'odes' keyword.
        """
        model = YamlModel()

        state_id = 's1'
        right_hand_side = '1'
        initial_value = 0

        model.add_ode(state_id, right_hand_side, initial_value)

        # test get_ode_by_id
        self.assertIsInstance(model.get_ode_by_id(state_id), dict)

        # test overwrite
        with self.assertRaises(ValueError):
            model.add_ode(state_id, right_hand_side, initial_value)

        # now over write ode/state
        model.add_ode(state_id,
                      right_hand_side,
                      initial_value,
                      overwrite=True)

        # test get_ode_ids
        self.assertListEqual(model.get_ode_ids(),
                             [state_id])

        # test delete
        model.delete_ode(state_id)
        self.assertListEqual(model.get_ode_ids(), [])

    def test_assignment(self):
        """
        Test all functionality regarding the 'assignments' keyword.
        """
        model = YamlModel()

        assignment_id = 's1'
        formula = '1+2'

        model.add_assignment(assignment_id, formula)

        # test get_assignment_by_id
        self.assertIsInstance(model.get_assignment_by_id(assignment_id), dict)

        # test overwrite
        with self.assertRaises(ValueError):
            model.add_assignment(assignment_id, formula)

        # now over write assignment
        model.add_assignment(assignment_id, formula, overwrite=True)

        # test get_assignment_ids
        self.assertListEqual(model.get_assignment_ids(),
                             [assignment_id])

        # test delete
        model.delete_assignment(assignment_id)
        self.assertListEqual(model.get_assignment_ids(), [])

    def test_function(self):
        """
        Test all functionality regarding the 'functions' keyword.
        """
        model = YamlModel()

        function_id = 'f'
        arguments = 'x1, x2'
        formula = 'x1 + x2'

        model.add_function(function_id, arguments, formula)

        # test get_function_by_id
        self.assertIsInstance(model.get_function_by_id(function_id), dict)

        # test overwrite
        with self.assertRaises(ValueError):
            model.add_function(function_id, arguments, formula)

        # now over write function
        model.add_function(function_id, arguments, formula, overwrite=True)

        # test get_function_ids
        self.assertListEqual(model.get_function_ids(),
                             [function_id])

        # test delete
        model.delete_function(function_id)
        self.assertListEqual(model.get_function_ids(), [])

    def test_observable(self):
        """
        Test all functionality regarding the 'observables' keyword.
        """
        model = YamlModel()

        observable_id = 'obs'
        observable_formula = 's*x'
        noise_formula = 'noiseParameter_1'
        observable_name = 'obs_name'

        model.add_observable(observable_id,
                             observable_formula,
                             noise_formula,
                             observable_name=observable_name)

        # test get_observable_by_id
        self.assertIsInstance(model.get_observable_by_id(observable_id), dict)

        # test overwrite
        with self.assertRaises(ValueError):
            model.add_observable(observable_id,
                                 observable_formula,
                                 noise_formula,
                                 observable_name=observable_name)

        # now over write observable
        model.add_observable(observable_id,
                             observable_formula,
                             noise_formula,
                             overwrite=True,
                             observable_name=observable_name)

        # test get_observable_ids
        self.assertListEqual(model.get_observable_ids(),
                             [observable_id])

        # test delete
        model.delete_observable(observable_id)
        self.assertListEqual(model.get_observable_ids(), [])

    def test_condition(self):
        """
        Test all functionality regarding the 'conditions' keyword.
        """
        model = YamlModel()

        condition_id = 'cond'
        condition_name = 'cond'
        condition_dict = {'x1': 42}

        model.add_condition(condition_id,
                            condition_dict,
                            condition_name=condition_name)

        # test get_condition_by_id
        self.assertIsInstance(model.get_condition_by_id(condition_id), dict)

        # test overwrite
        with self.assertRaises(ValueError):
            model.add_condition(condition_id,
                                condition_dict,
                                condition_name=condition_name)

        # now over write condition
        model.add_condition(condition_id,
                            condition_dict,
                            condition_name=condition_name,
                            overwrite=True)

        # test get_condition_ids
        self.assertListEqual(model.get_condition_ids(),
                             [condition_id])

        # test delete
        model.delete_condition(condition_id)
        self.assertListEqual(model.get_condition_ids(), [])

    def test_valid_model(self):
        """Test whether the resulting models are valid."""
        model = YamlModel()

        model.set_time('t')
        model.add_ode(state_id='x',
                      right_hand_side='k_1 * x + t',
                      initial_value=0)
        model.add_parameter(parameter_id='k_1',
                            nominal_value=1)

        model.validate_model()

    def test_minus_in_formula(self):
        """Test writing a model for a right hand side starting with a minus."""
        model = YamlModel()

        model.add_ode(state_id='x',
                      right_hand_side='-x',
                      initial_value=1)

        model.validate_model()

        yaml_dir = os.path.join(self.test_dir, 'test_minus_sign.yaml')
        model.write_to_yaml(yaml_dir)

        validate_yaml(yaml_dir)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestYamlModel())
    unittest.main()
