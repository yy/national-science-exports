""" setup script for national science production project. """
from setuptools import find_packages, setup

setup(
    name="nsp",
    version="0.1",
    description="package for the national science production project",
    author="Lili Miao, Dakota Murray, YY Ahn",
    packages=find_packages(exclude=("tests",)),
    install_requires=["numpy", "pandas", "networkx", "matplotlib"],
)
