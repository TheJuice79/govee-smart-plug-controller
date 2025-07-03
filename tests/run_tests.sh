#!/bin/bash

# Exit if any command fails
set -e

# Get the script directory and go there
cd "$(dirname "$0")"

# Print current path (for debug)
echo "Running tests from: $(pwd)"

# Run pytest with correct module resolution
PYTHONPATH=.. pytest .
