#!/usr/bin/env bash

mkdir test_output

# test yaml2sbml
yaml2sbml ./test_yaml2sbml/ode_input1.yaml test_output/test_sbml.xml

# test yaml2petab for both versions of the petab yaml flag
yaml2petab ./test_yaml2sbml/ode_input2.yaml test_output petab_test_sbml.xml -y test_yaml.yml
yaml2petab ./test_yaml2sbml/ode_input2.yaml test_output petab_test_sbml.xml --petab_yaml test_yaml.yml

# test validator
yaml2sbml_validate ./test_yaml2sbml/ode_input1.yaml

rm -r test_output

