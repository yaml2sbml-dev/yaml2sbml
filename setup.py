import setuptools

ENTRY_POINTS = {
    'console_scripts': [
        'yaml2sbml = yaml2sbml.yaml2sbml:main',
        'yaml2petab = yaml2sbml.yaml2PEtab:main'
    ]
}

setuptools.setup(
    name="yaml2sbml",
    version="0.1.1",
    author="Jakob Vanhoefer, Marta R. A. Matos",
    author_email="marta.ra.matos@gmail.com",
    description="A small package to convert ODEs specified in a yaml file to SBML/PEtab.",
    url="https://github.com/martamatos/yaml2sbml",
    packages=setuptools.find_packages(),
    install_requires=["python-libsbml>=5.18.0",
                      "PyYAML>=5.1",
                      "pandas>=1.0.1",
                      "petab>=0.1.4"],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points=ENTRY_POINTS
)
