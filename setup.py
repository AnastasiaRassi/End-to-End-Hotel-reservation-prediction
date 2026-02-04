from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="HOTEL-RES-PREDICTIONS",
    version="0.1",
    author="Anastasia Al Rassi",
    packages=find_packages(),
    install_requires= requirements,
)