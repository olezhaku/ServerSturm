#!/bin/bash
set -e

cd ServerSturm
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
cd src
python install.py
