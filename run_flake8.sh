#!/usr/bin/env bash

python3 -m flake8 \
    --exclude=build,doc,examples,source \
    --per-file-ignores='*/__init__.py:F401 test/*:T001,S101'
