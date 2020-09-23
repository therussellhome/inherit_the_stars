#!/bin/bash

if [ -f "/usr/local/bin/coverage" ]; then
    coverage run --omit=*/test/* -m unittest discover -v ; coverage report --skip-covered --show-missing
else
    python3 -m unittest discover -v
fi
