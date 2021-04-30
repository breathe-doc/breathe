#!/bin/sh

export PYTHONPATH="../${PYTHONPATH:+:$PYTHONPATH}"

python3 -m pytest -v
