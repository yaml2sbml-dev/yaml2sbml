# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'yaml2sbml'
copyright = '2021, The yaml2sbml authors'
author = 'Jakob Vanhoefer, Marta R. A. Matos, Dilan Pathirana, Yannik Schälte'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
import yaml2sbml
version = yaml2sbml.__version__
# The full version, including alpha/beta/rc tags.
release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'sphinx_autodoc_typehints',
              'nbsphinx',
              'sphinx.ext.mathjax',
              # link to code
              'sphinx.ext.viewcode',
              # link to other projects' docs
              'sphinx.ext.intersphinx',
              # code highlighting in jupyter cells
              'IPython.sphinxext.ipython_console_highlighting',
              ]

# links for intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/devdocs/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'petab': ('https://petab.readthedocs.io/en/stable/', None),
    'amici': ('https://amici.readthedocs.io/en/latest/', None),
}

# Add any paths that contain templates here, relative to this directory.
#templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']
