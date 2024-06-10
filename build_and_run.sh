#!/bin/bash

# Nettoyage des anciennes constructions
echo "Nettoyage des anciennes constructions..."
rm -rf build dist backend.egg-info

# Construction du package
echo "Construction du package..."
python3 setup.py sdist bdist_wheel

# Installation du package localement
echo "Installation du package localement..."
pip install .

# Démarrage du serveur
echo "Démarrage du serveur..."
debiai-start
