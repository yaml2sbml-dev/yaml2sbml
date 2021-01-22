import yaml
import os.path
from typing import Union
import copy

from .yaml2sbml import _parse_yaml_dict
from .yaml2PEtab import _yaml2petab
from .yaml_validation import _validate_yaml_from_dict


class YamlModel:
    """
    Functionality to set up, edit, load and write yaml models.
    """

    def __init__(self):
        """
        Set up yaml model.
        """
        self._yaml_model = {'time': {},
                            'odes': [],
                            'parameters': [],
                            'assignments': [],
                            'functions': [],
                            'observables': [],
                            'conditions': []}

    @staticmethod
    def load_from_yaml(yaml_file):
        """
        Creates a model instance from a yaml file.

        Arguments:
        yaml_dir:
            directory to the yaml file, that should be imported

        Returns:
        cls:
            new model
        """

        new_model = YamlModel()

        # read in yaml_file
        with open(yaml_file, 'r') as f_in:
            yaml_contents = f_in.read()
            yaml_dict_from_file = yaml.full_load(yaml_contents)

        for key in yaml_dict_from_file.keys():
            new_model._yaml_model[key] = yaml_dict_from_file[key]

        # check, if the model is valid
        new_model.validate_model()

        return new_model

    def write_to_yaml(self,
                      yaml_dir: str,
                      over_write: bool = False):
        """
        Write model to yaml file given as directory yaml_dir.

        Arguments:
        yaml_dir:
            path/file, where the yaml should be written
        over_write:
            Indicates, whether an existing yaml should be overwritten

        Returns:

        Raises:
            ValueError
            FileExistsError
        """
        if not (yaml_dir.endswith('.yaml') or yaml_dir.endswith('.yml')):
            raise ValueError('yaml_dir should contain path to the yaml '
                             'and hence end with .yaml or .yml')

        if (not over_write) and os.path.exists(yaml_dir):
            raise FileExistsError(f'Can not write yaml model. File {yaml_dir}'
                                  f' already exists. Consider to set '
                                  f'over_write=True.')

        reduced_model_dict = self._get_reduced_model_dict()

        # translate to string
        yaml_as_string = yaml.dump(reduced_model_dict,
                                   sort_keys=False,
                                   indent=6)

        # post-process: add empty line around blocks
        for key in self._yaml_model.keys():
            yaml_as_string = yaml_as_string.replace(f'{key}:',
                                                    f'\n{key}:')
        yaml_as_string = yaml_as_string.replace('-     ', '\n    - ')

        with open(yaml_dir, 'w') as file:
            file.write(yaml_as_string)

    def write_to_sbml(self,
                      sbml_dir: str,
                      over_write: bool = False):
        """
        Writes the model as an SBML file to the directory given in sbml_dir.

        Arguments:
        sbml_dir:
            path/file, where the sbml should be written
        over_write:
            Indicates, whether an existing yaml should be overwritten

        Returns:

        Raises:
            ValueError
            FileExistsError
        """
        # Check file ending.
        if not (sbml_dir.endswith('.xml') or sbml_dir.endswith('.sbml')):
            raise ValueError('sbml_dir should contain path to the sbml '
                             'and hence end with .xml or .sbml')

        if (not over_write) and os.path.exists(sbml_dir):
            raise FileExistsError(f'Can not write SBML model. File {sbml_dir}'
                                  f' already exists. Consider to set '
                                  f'over_write=True.')

        # generate SBML as string
        reduced_model_dict = self._get_reduced_model_dict()
        sbml_as_string = _parse_yaml_dict(reduced_model_dict)

        with open(sbml_dir, 'w') as f_out:
            f_out.write(sbml_as_string)

    def write_to_petab(self,
                       output_dir: str,
                       model_name: str,
                       petab_yaml_name: str = None,
                       measurement_table_name: str = None):
        """
        Writes the YamlModel as a petab problem. Equivalent to calling
        yaml2petab on the file produced by the yaml output.

        If a petab_yaml_name is given, a .yaml file is created, that organizes
        the petab problem. If additionally a measurement_table_file_name is
        specified, this file name is written into the created .yaml file.

        Arguments:
            output_dir: path the output file(s) are be written out
            model_name: name of SBML model
            petab_yaml_name: name of yaml organizing the PEtab problem.
            measurement_table_name: Name of measurement table
        """
        reduced_model_dict = self._get_reduced_model_dict()

        _yaml2petab(reduced_model_dict,
                    output_dir,
                    model_name,
                    petab_yaml_name,
                    measurement_table_name)

    def validate_model(self):
        """
        Validates the yaml model.

        Arguments:

        Returns:

        Raises:
            ValidationError
        """
        _validate_yaml_from_dict(self._yaml_model)

    def _get_reduced_model_dict(self) -> dict:
        """
        Returns a reduced model dict, where keys without an entry are deleted.
        (Returns a copy of the model dict!!)

        Arguments:

        Raises:

        Returns:
            reduced_model_dict
        """
        reduced_model_dict = {}

        for (key, val) in self._yaml_model.items():
            if val:
                reduced_model_dict[key] = copy.deepcopy(val)

        return reduced_model_dict

    # functionalities regarding the time
    def is_set_time(self):
        return 'time' in self._yaml_model.keys()

    def set_time(self,
                 time_variable: str):
        self._yaml_model['time'] = {'variable': time_variable}

    def get_time(self):
        if self.is_set_time():
            return self._yaml_model['time']['variable']
        else:
            return None

    # functions adding a value
    def add_parameter(self,
                      parameter_id: str,
                      over_write: bool = False,
                      nominal_value: float = None,
                      parameter_name: str = None,
                      parameter_scale: str = None,
                      lower_bound: float = None,
                      upper_bound: float = None,
                      estimate: float = None):
        """
        Adds a parameter. Overwrites an existing parameter with the same id,
        if over_write=True.
        """
        # if parameter exists: delete if overwrite
        if parameter_id in self.get_parameter_ids():
            if over_write:
                self.delete_parameter(parameter_id)
            else:
                raise ValueError('Could not add parameter with id'
                                 f' {parameter_id}: Parameter with the same'
                                 ' id already exists.')

        entry_dict = {'parameterId': parameter_id,
                      'nominalValue': nominal_value,
                      'parameterName': parameter_name,
                      'parameterScale': parameter_scale,
                      'lowerBound': lower_bound,
                      'upperBound': upper_bound,
                      'estimate': estimate}

        self._add_entry(entry_dict, 'parameters')

    def add_ode(self,
                state_id: str,
                right_hand_side: Union[float, str],
                initial_value: Union[float, str],
                over_write: bool = False):
        """
        Adds a state/ODE. Overwrites an existing state/ODE with the same id,
        if over_write=True.
        """
        # if state exists: delete if over_write
        if state_id in self.get_ode_ids():
            if over_write:
                self.delete_ode(state_id)
            else:
                raise ValueError(f'Could not add state/ODE with id {state_id}:'
                                 f' State with the same id already exists.')

        entry_dict = {'stateId': state_id,
                      'rightHandSide': right_hand_side,
                      'initialValue': initial_value}

        self._add_entry(entry_dict, 'odes')

    def add_assignment(self,
                       assignment_id: str,
                       formula: str,
                       over_write: bool = False):
        """
        Adds an assignment. Overwrites an existing assignment with the same id,
        if over_write=True.
        """
        # if assignment exists: delete if over_write
        if assignment_id in self.get_assignment_ids():
            if over_write:
                self.delete_assignment(assignment_id)
            else:
                raise ValueError('Could not add assignment with id '
                                 f'{assignment_id}: Assignment with the same '
                                 'id already exists.')

        entry_dict = {'assignmentId': assignment_id,
                      'formula': formula}

        self._add_entry(entry_dict, 'assignments')

    def add_function(self,
                     function_id: str,
                     arguments: str,
                     formula: str,
                     over_write: bool = False):
        """
        Adds a function. Overwrites an existing function with the same id,
        if over_write=True.
        """
        # if function exists: delete if over_write
        if function_id in self.get_function_ids():
            if over_write:
                self.delete_function(function_id)
            else:
                raise ValueError('Could not add function with id '
                                 f' {function_id}: Function with the same '
                                 'id already exists.')

        entry_dict = {'functionId': function_id,
                      'arguments': arguments,
                      'formula': formula}

        self._add_entry(entry_dict, 'functions')

    def add_observable(self,
                       observable_id: str,
                       observable_formula: str,
                       noise_formula: str,
                       over_write: bool = False,
                       observable_name: str = None,
                       observable_transformation: str = None,
                       noise_distribution: str = None):
        """
        Adds an observable. Overwrites an existing observable with the same id,
        if over_write=True.
        """
        # if observable exists: delete if over_write
        if observable_id in self.get_observable_ids():
            if over_write:
                self.delete_observable(observable_id)
            else:
                raise ValueError('Could not add observable with id '
                                 f'{observable_id}: Observable with the same '
                                 'id already exists.')

        entry_dict = {'observableId': observable_id,
                      'observableName': observable_name,
                      'observableFormula': observable_formula,
                      'observableTransformation': observable_transformation,
                      'noiseFormula': noise_formula,
                      'noiseDistribution': noise_distribution}

        self._add_entry(entry_dict, 'observables')

    def add_condition(self,
                      condition_id: str,
                      condition_dict: dict,
                      over_write: bool = False,
                      condition_name: str = None):

        """
        Adds a condition. Overwrites an existing condition with the same id,
        if over_write=True.

        Arguments:
        condition_id:
            str, condition id
        condition_dict:
            dict, of the form {<parameter or state id>: <value>}.
            Corresponds to entries in the PEtab condition table.
            See details there.
        over_write:
            bool, indicates if an existing condition should be overwritten
        condition_name:
            Condition name. Optional.

        Returns:
        """
        # if condition exists: delete if over_write
        if condition_id in self.get_condition_ids():
            if over_write:
                self.delete_condition(condition_id)
            else:
                raise ValueError('Could not add condition with id '
                                 f' {condition_id}: Condition with the same '
                                 f'id already exists.')

        entry_dict = {'conditionId': condition_id,
                      'conditionName': condition_name,
                      **condition_dict}

        self._add_entry(entry_dict, 'conditions')

    def _add_entry(self,
                   entry_dict: dict,
                   block_key: str):
        """
        Adds the entry in 'entry_dict' to the block indexed by 'block_key'.
        If 'over_write=True', an existing value for that key is overwritten.

        Arguments:
        entry_dict:
            dict, that stores the new entry
        block_key:
            name, where the ids should be searched (e.g. 'parameters')

        Returns:
        """
        # filter out None values and append
        filtered_dict = _filter_none_values(entry_dict)
        self._yaml_model[block_key].append(filtered_dict)

    # functionalities to get ids
    def get_parameter_ids(self):
        """Returns a list with all parameter ids."""
        return self._get_ids('parameters', 'parameterId')

    def get_ode_ids(self):
        """Returns a list with all state ids."""
        return self._get_ids('odes', 'stateId')

    def get_assignment_ids(self):
        """Returns a list with all assignment ids."""
        return self._get_ids('assignments', 'assignmentId')

    def get_function_ids(self):
        """Returns a list with all function ids."""
        return self._get_ids('functions', 'functionId')

    def get_observable_ids(self):
        """Returns a list with all observable ids."""
        return self._get_ids('observables', 'observableId')

    def get_condition_ids(self):
        """Returns a list with all conditions ids."""
        return self._get_ids('conditions', 'conditionId')

    def _get_ids(self,
                 block_key: str,
                 index_key: str):
        """
        Returns all ids in the block named `block_key` in self._yaml_model.
        The ids have the key index_key.

        Arguments:
        block_key:
            name, where the ids should be searched (e.g. 'parameters')
        index_key:
            key of the identifier, in that block (e.g. 'parameterId')

        Returns:
        res:
            list of ids
        """
        return [element[index_key] for element in self._yaml_model[block_key]]

    # functionalities to get entry by Id:
    def get_parameter_by_id(self,
                            parameter_id: str):
        """returns dict for corresponding parameter."""
        if parameter_id not in self.get_parameter_ids():
            raise IndexError(f'Could not find parameter {parameter_id}.')

        return self._get_entry_by_id('parameters',
                                     'parameterId',
                                     parameter_id)

    def get_ode_by_id(self,
                      state_id: str):
        """returns dict for corresponding ODE/state."""
        if state_id not in self.get_ode_ids():
            raise IndexError(f'Could not find state/ODE {state_id}.')

        return self._get_entry_by_id('odes',
                                     'stateId',
                                     state_id)

    def get_assignment_by_id(self,
                             assignment_id: str):
        """returns dict for corresponding assignment."""
        if assignment_id not in self.get_assignment_ids():
            raise IndexError(f'Could not find assignment {assignment_id}.')

        return self._get_entry_by_id('assignments',
                                     'assignmentId',
                                     assignment_id)

    def get_function_by_id(self,
                           function_id: str):
        """returns dict for corresponding function."""
        if function_id not in self.get_function_ids():
            raise IndexError(f'Could not find function {function_id}.')

        return self._get_entry_by_id('functions',
                                     'functionId',
                                     function_id)

    def get_observable_by_id(self,
                             observable_id: str):
        """returns dict for corresponding observable."""
        if observable_id not in self.get_observable_ids():
            raise IndexError(f'Could not find observable {observable_id}.')

        return self._get_entry_by_id('observables',
                                     'observableId',
                                     observable_id)

    def get_condition_by_id(self,
                            condition_id: str):
        """returns dict for corresponding condition."""
        if condition_id not in self.get_condition_ids():
            raise IndexError(f'Could not find condition {condition_id}.')

        return self._get_entry_by_id('conditions',
                                     'conditionId',
                                     condition_id)

    def _get_entry_by_id(self,
                         block_key: str,
                         index_key: str,
                         entry_id: str):
        """
        Returns the entry with id 'entry_id' in the block named
        `block_key` in self._yaml_model. 'index_key' gives the name of the
        id-key.

        Arguments:
        block_key:
            Key of the block (e.g. 'parameters')
        index_key:
            key of the identifier in that block (e.g. 'parameterId')
        entry_id:
            Id of element, that should be returned

        Returns:
            Entry_dict. None, if entry is not found.
        """
        # check if block exists.
        for entry in self._yaml_model[block_key]:
            if entry[index_key] == entry_id:
                return entry

        return None

    # functionalities to delete entry by Id:
    def delete_parameter(self,
                         parameter_id: str):
        """
        Deletes a parameter. Raises a ValueError, if parameter does not exist.
        """
        if not self._delete_entry('parameters',
                                  'parameterId',
                                  parameter_id):

            raise ValueError(f'Could not delete parameter {parameter_id}. '
                             f'Invalid parameterId.')

    def delete_ode(self,
                   state_id: str):
        """
        Deletes a state + ODE. Raises a ValueError, if state does not exist.
        """
        if not self._delete_entry('odes',
                                  'stateId',
                                  state_id):

            raise ValueError(f'Could not delete ODE for state {state_id}. '
                             f'Invalid stateId.')

    def delete_assignment(self,
                          assignment_id: str):
        """
        Deletes an assignment. Raises a ValueError,
        if assignment does not exist.
        """
        if not self._delete_entry('assignments',
                                  'assignmentId',
                                  assignment_id):

            raise ValueError(f'Could not delete assignment {assignment_id}. '
                             f'Invalid assignmentId.')

    def delete_function(self,
                        function_id: str):
        """
        Deletes a function. Raises a ValueError, if function does not exist.
        """
        if not self._delete_entry('functions',
                                  'functionId',
                                  function_id):

            raise ValueError(f'Could not delete function {function_id}. '
                             f'Invalid functionId.')

    def delete_observable(self,
                          observable_id: str):
        """
        Deletes an observable. Raises a ValueError,
        if observable does not exist.
        """
        if not self._delete_entry('observables',
                                  'observableId',
                                  observable_id):

            raise ValueError(f'Could not delete observable {observable_id}. '
                             f'Invalid observableId.')

    def delete_condition(self,
                         condition_id: str):
        """
        Deletes a condition. Raises a ValueError, if condition does not exist.
        """
        if not self._delete_entry('conditions',
                                  'conditionId',
                                  condition_id):

            raise ValueError(f'Could not delete condition {condition_id}. '
                             f'Invalid conditionId.')

    def _delete_entry(self,
                      block_key: str,
                      index_key: str,
                      deleted_object_id: str):
        """
        Deletes the entry with id 'deleted_object_id' in the block named
        `block_key` in self._yaml_model. 'index_key' gives the name of the
        id-key.

        Arguments:
        block_key:
            Key of the block (e.g. 'parameters')
        index_key:
            key of the identifier in that block (e.g. 'parameterId')
        deleted_object_id:
            Id of element, that should be deleted

        Returns:
            Bool, that indicates, whether deletion was successful.
        """

        # Check if block exists
        for i, entry in enumerate(self._yaml_model[block_key]):

            # search for entry and delete
            if entry[index_key] == deleted_object_id:
                self._yaml_model[block_key].pop(i)
                return True

        return False


def _filter_none_values(d: dict):
    """
    Filters out the key-value pairs with None  as value.

    Arguments:
    d
        dictionary

    Returns:
        filtered dictionary.
    """
    return {key: value for (key, value) in d.items() if value is not None}
