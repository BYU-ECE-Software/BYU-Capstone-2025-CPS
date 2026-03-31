#!/bin/bash

cd "$(dirname "$0")"

echo "Starting Capstone Labs at http://localhost:8080"

python3 -m http.server 8080
