#!/bin/bash

rm -rf build dist backend.egg-info

python3 setup.py sdist bdist_wheel

pip install .

debiai-start
