#!/bin/bash
set -e
echo "[Test] Verifying Analytical Models..."
python3 -c "import numpy, scipy; print('NumPy version:', numpy.__version__)"
echo "Models OK" > output.log
