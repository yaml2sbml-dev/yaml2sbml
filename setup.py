import setuptools
import os

ENTRY_POINTS = {
    'console_scripts': [
        'yaml2sbml = yaml2sbml.yaml2sbml:main',
        'yaml2petab = yaml2sbml.yaml2PEtab:main',
        'yaml2sbml_validate = yaml2sbml.yaml_validation:main'
    ]
}

# automatically extract version:
with os.path.join(os.path.dirname(__file__), 'yaml2sbml', 'version.py') as f:
    version = f.read().split("'")[1]

setuptools.setup(
    name="yaml2sbml",
    version=version,
    author="Jakob Vanhoefer, Marta R. A. Matos",
    author_email="marta.ra.matos@gmail.com",
    description="A small package to convert ODEs specified in "
                "a yaml file to SBML/PEtab.",
    url="https://github.com/martamatos/yaml2sbml",
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
                   "nbmake>=0.1.0", ],
    extras_require={'examples': ["amici>=0.11.10",
                                 "numpy>=1.19.4",
                                 "matplotlib>=3.1.0"]},
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points=ENTRY_POINTS,
    include_package_data=True
)
