#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "======================================================"
echo " Starting Wordle Web Application (Python Server)     "
echo " Python version: $(python3 --version 2>&1)           "
echo " Press Ctrl+C to stop the server                      "
echo "======================================================"

python3 server.py "$@"
