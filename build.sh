#!/bin/bash

REPO_NAME="Static-Site-Generator"

echo "Building site for production with base path /$REPO_NAME/"
python3 src/main.py "/$REPO_NAME/"
