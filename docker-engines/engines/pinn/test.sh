#!/bin/bash
set -e
echo "[Test] Verifying PINN (DeepXDE)..."
python3 -c "import deepxde; print('DeepXDE version:', deepxde.__version__)"
echo "PINN OK" > output.log
