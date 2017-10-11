#!/bin/bash
command -v python >/dev/null 2>&1 && echo "Running tests for python" && PYTHONPATH=../ PYTHON=python python -m unittest discover
command -v python2 >/dev/null 2>&1 && echo "Running tests for python2" && PYTHONPATH=../ PYTHON=python2 python2 -m unittest discover
command -v python3 >/dev/null 2>&1 && echo "Running tests for python3" && PYTHONPATH=../ PYTHON=python3 python3 -m unittest discover
