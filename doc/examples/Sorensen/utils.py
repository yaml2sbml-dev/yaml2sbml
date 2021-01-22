import amici
import amici.plotting

import importlib
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def simulate_and_plot_sorensen(sbml_dir: str):
    """
    Plots and simulates the Sorensen model.
    This function is highly specific to the Sorensen model.

    Parameters:
    -----------
    sbml_dir:
        path to the SBML model.
    """
    model = compile_model(sbml_dir)

    # Simulate.
    model.setTimepoints(np.linspace(0, 300, 3001))
    solver = model.getSolver()
    simulation = amici.runAmiciSimulation(model, solver)

    # Reproduce the figure.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    amici.plotting.plotObservableTrajectories(
        simulation,
        observable_indices=[0],
        model=model,
        ax=ax1,
    )
    ax1.set_xlabel('Time [min]')
    ax1.set_ylabel('Blood glucose concentration [mg/dL]')
    ax1.set_title('Blood Glucose Concentration')
    ax1.get_legend().remove()

    amici.plotting.plotObservableTrajectories(
        simulation,
        observable_indices=[1],
        model=model,
        ax=ax2,
    )
    ax2.set_xlabel('Time [min]')
    ax2.set_ylabel('Plasma insulin concentration [mU/L]')
    ax2.set_title('Plasma Insulin Concentration')
    ax2.get_legend().remove()

    plt.show()


def compile_model(sbml_dir: str):
    """
    Compiles the Sorensen model and specifies the observables.

    Parameters:
    -----------
    sbml_dir:
        path to the SBML model.
    """
    # observables are defined, as specifying a whole PEtab problem including
    # observables would mean a huge overhead.

    # Define the variables that will be plotted to reproduce the figure from
    # the original thesis.
    observables = {
        'blood_glucose': {
            'name': 'Blood glucose concentration [mg/dL]',
            # GlucPV: model state for glucose in the peripheral vascular space.
            # Multiplied by 18.0156 to convert [mmol/L] to [mg/dL].
            # Multiplied by 0.84 as described in Panunzi et al. 2020 [2].
            'formula': 'GlucPV * 18.0156 * 0.84',
        },
        'plasma_insulin': {
            'name': 'Plasma insulin concentration [mU/L]',
            # InsuPV: model state for insulin in the peripheral vascular space.
            # Multiplied by 0.144 to convert [pM] to [mU/L].
            'formula': 'InsuPV * 0.144',
        }
    }

    # Compile the model with AMICI.
    sbml_importer = amici.sbml_import.SbmlImporter('Fig71_Sorensen1985.xml')
    sbml_importer.sbml2amici(
        model_name='Fig71_Sorensen1985',
        output_dir=os.path.join('amici_models', 'Fig71_Sorensen1985'),
        observables=observables,
    )

    # Import the compiled model.
    sys.path.insert(
        0,
        os.path.abspath(os.path.join('amici_models', 'Fig71_Sorensen1985'))
    )
    model_module = importlib.import_module('Fig71_Sorensen1985')

    return model_module.getModel()
