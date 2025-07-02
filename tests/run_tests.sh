#!/bin/bash

# Ensure we're in the tests directory
cd "$(dirname "$0")"

# Go up one level to the project root and run all tests with correct module path
PYTHONPATH=.. python3 -m pytest .
