import amici
import amici.plotting
import matplotlib.pyplot as plt
import os
import sys
import importlib
import numpy as np


def simulate_AMICI(sbml_name: str):
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
    amici_model = model_module.getModel()
    solver = amici_model.getSolver()

    # Define time points ans run simulation using default model parameters/solver options
    amici_model.setTimepoints(np.linspace(0, 5, 101))
    rdata = amici.runAmiciSimulation(amici_model, solver)

    return amici_model, rdata


def plot_AMICI(amici_model,
               rdata,
               title: str):
    """
    Plots the AMICI simulation from the given rdata...
    """

    fig, ax = plt.subplots()
    amici.plotting.plotStateTrajectories(rdata, ax=ax)

    # state axis
    ax.set_ylabel('x')

    # format time axis
    ax.set_xlabel('t')
    ax.set_xlim(0, 5)

    # legend + title
    if len(amici_model.getStateIds()) > 1:
        ax.legend(amici_model.getStateNames())
    else:
        ax.get_legend().remove()

    ax.set_title(label=title)

    plt.show()
