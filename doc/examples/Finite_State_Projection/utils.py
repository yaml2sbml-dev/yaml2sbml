import amici
import amici.plotting

import importlib
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def plot_AMICI(sbml_dir: str,
               t: np.ndarray,
               r_max: int,
               p_max: int):
    """
    Compiles, simulates and plots the AMICI model for the FSP example.
    """
    n_t = len(t)
    # compile and Simulate model
    simulation, model = compile_and_simulate(sbml_dir,
                                             t,
                                             r_max,
                                             p_max)

    def get_obs_idx_by_id(obs_id: str):
        try:
            return model.getObservableIds().index(obs_id)
        except ValueError:
            raise IndexError(f'No observable with id {obs_id}')

    for i in range(n_t):

        r_marginal = [simulation.y[i, get_obs_idx_by_id(f'x_r{r}')] for r in range(r_max)]
        p_marginal = [simulation.y[i, get_obs_idx_by_id(f'x_p{p}')] for p in range(p_max)]
        # rna
        plt.subplot(n_t, 2, 2*i+1)
        plt.fill_between(np.arange(r_max), 0, r_marginal, facecolor='blue', alpha=0.5)
        plt.plot(r_marginal)
        plt.ylabel(f't={int(t[i])}')
        plt.yticks([])
        plt.xlim(0, r_max-1)
        plt.ylim(0, 0.3)

        if i < n_t-1:
            plt.tick_params(labelbottom=False)
        else:
            plt.xlabel('mRNA abundance')

        # protein
        plt.subplot(n_t, 2, 2*(i+1))
        plt.fill_between(np.arange(p_max), 0, p_marginal, facecolor='blue', alpha=0.5)
        plt.plot(p_marginal)
        plt.yticks([ ])
        plt.xlim(0, p_max-1)
        plt.ylim(0, 0.2)
        if i < n_t-1:
            plt.tick_params(labelbottom=False)
        else:
            plt.xlabel('protein abundance')

    plt.subplots_adjust(wspace=0.07, hspace=0.1)
    plt.show()


def compile_and_simulate(sbml_dir: str,
                         t: np.ndarray,
                         r_max: int,
                         p_max: int):
    """
    Utility function, that compiles and simulates the FSP model.
    """
    model_name = 'Gene_regulation_FSP'

    # define marginal rna concentrations
    observables_rna = {f'x_r{r}': get_marginal_rna_obs(r, p_max)
                       for r in range(r_max)}

    # define marginal protein concentrations
    observables_protein = {f'x_p{p}': get_marginal_protein_obs(p, r_max)
                           for p in range(p_max)}

    observables = {**observables_rna, **observables_protein}

    sbml_importer = amici.sbml_import.SbmlImporter(sbml_dir)
    sbml_importer.sbml2amici(
        model_name=model_name,
        output_dir=os.path.join('amici_models', model_name),
        observables=observables)

    # Import the compiled model.
    sys.path.insert(0,
                    os.path.abspath(os.path.join('amici_models', model_name)))
    model_module = importlib.import_module(model_name)
    model = model_module.getModel()

    # Simulate.
    model.setTimepoints(t)
    solver = model.getSolver()
    simulation = amici.runAmiciSimulation(model, solver)

    return simulation, model


def get_marginal_rna_obs(r: int, p_max: int):
    """
    Returns a dict of containing the observable for the given marginalized
    rna abundance of r in AMICI.
    """
    marginal = ''
    for p in range(p_max-1):
        marginal += f'x_{r}_{p} + '
    marginal += f'x_{r}_{p_max-1}'

    return {'name': f'x_r{r}', 'formula': marginal}


def get_marginal_protein_obs(p: int, r_max: int):
    """
    Returns a dict of containing the observable for the given marginalized
    protein abundance of p in AMICI.
    """
    marginal = ''
    for r in range(r_max-1):
        marginal += f'x_{r}_{p} + '
    marginal += f'x_{r_max-1}_{p}'

    return {'name': f'x_p{p}', 'formula': marginal}
