#!/bin/bash
conda deactivate
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r requirements-init.txt
