import setuptools
import os

ENTRY_POINTS = {
    'console_scripts': [
        'yaml2sbml = yaml2sbml.yaml2sbml:main',
        'yaml2petab = yaml2sbml.yaml2PEtab:main',
        'yaml2sbml_validate = yaml2sbml.yaml_validation:main'
    ]
}

# read version
with open(os.path.join(os.path.dirname(__file__),
          "yaml2sbml", "version.py")) as f:
    version = f.read().split('\n')[0].split("'")[-2]

# read README as long_description
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setuptools.setup(
    name="yaml2sbml",
    version=version,
    author="Jakob Vanhoefer, Marta R. A. Matos",
    author_email="marta.ra.matos@gmail.com",
    description="A small package to convert ODEs specified in "
                "a YAML file to SBML/PEtab.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yaml2sbml-dev/yaml2sbml",
    packages=setuptools.find_packages(),
    install_requires=["python-libsbml>=5.18.0",
                      "PyYAML>=5.1",
                      "pandas>=1.0.1",
                      "petab>=0.1.4"],
    tests_require=["amici>=0.11.10",
                   "pypesto>=0.2.2"
                   "numpy>=1.19.4",
                   "matplotlib>=3.1.0",
                   "flake8>=3.7.2",
                   "nbmake>=0.1.0",
                   "scipy>=1.6.0"],
    extras_require={
        "examples": [
            "amici>=0.11.10",
            "numpy>=1.19.4",
            "matplotlib>=3.1.0",
            "scipy>=1.6.0"],
        "doc": [
            "sphinx>=3.4.3",
            "nbsphinx>=0.8.0",
            "nbconvert>=6.0.7",
            "sphinx-rtd-theme>=0.5.1",
            "sphinx_autodoc_typehints>=1.11.1"]},
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points=ENTRY_POINTS,
    include_package_data=True
)
