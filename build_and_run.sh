#!/bin/bash

echo "Nettoyage des anciennes constructions..."
rm -rf build dist backend.egg-info

echo "Construction du package..."
python3 setup.py sdist bdist_wheel

echo "Installation du package localement..."
pip install .

debiai-start
