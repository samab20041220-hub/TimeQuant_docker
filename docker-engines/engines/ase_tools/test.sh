#!/bin/bash
set -e
echo "[Test] Verifying ASE & PyMatGen..."
python3 -c "import ase; import pymatgen; print('ASE version:', ase.__version__)"
echo "ASE Tools OK" > output.log
