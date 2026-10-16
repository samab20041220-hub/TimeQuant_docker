#!/bin/bash
set -e
echo "[Test] Verifying QuTiP..."
python3 -c "import qutip; print('QuTiP version:', qutip.__version__)"
echo "QuTiP OK" > output.log
