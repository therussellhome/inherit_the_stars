#!/bin/bash

if [ -f "/usr/local/bin/coverage" ]; then
    coverage run --omit=stars/test/* -m unittest discover -v ; coverage report --skip-covered
else
    python3 -m unittest discover -v
fi
