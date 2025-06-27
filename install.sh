#!/bin/bash
set -e

python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
cd src
python install.py

cd ../keys
chmod +x genkeys.sh
source ./genkeys.sh
