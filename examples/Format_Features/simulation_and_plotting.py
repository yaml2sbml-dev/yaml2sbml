import amici
import amici.plotting
import os
import sys
import importlib
import numpy as np


def compile_and_simulate_in_AMICI(sbml_name: str):
    """
    Compiles, simulates and plots the SBML in AMICI.

    :param yaml_name:
    :return:
    """
    model_name = os.path.splitext(sbml_name)[0]
    model_output_dir = 'AMICI_models'

    sbml_importer = amici.SbmlImporter(sbml_name)
    sbml_importer.sbml2amici(model_name,
                             model_output_dir)

    # import model
    sys.path.insert(0, os.path.abspath(model_output_dir))
    model_module = importlib.import_module(model_name)

    # create model + solver instance
    model = model_module.getModel()
    solver = model.getSolver()

    # Define time points ans run simulation using default model parameters/solver options
    model.setTimepoints(np.linspace(0, 5, 101))
    rdata = amici.runAmiciSimulation(model, solver)

    return rdata

