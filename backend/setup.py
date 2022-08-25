# coding: utf-8

from setuptools import setup, find_packages

NAME = "debiai-backend"
VERSION = "0.16.0"

# To setup the project, run the command:
#
# python setup.py install
# or
# pip install . (after cd to this folder)
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

with open('requirements.txt', 'r') as file:
    REQUIRES = file.read().split('\n')

setup(
    name=NAME,
    version=VERSION,
    license="Apache License 2.0",
    description="ML :: DebiAI :: Impl :: Python",
    author_email="",
    url="",
    keywords=["DebiAI", "ML", "Python", "Data analysis"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)
