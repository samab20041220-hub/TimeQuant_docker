#!/bin/bash
set -e
echo "[Test] Verifying PySCF..."
python3 -c "import pyscf; print('PySCF version:', pyscf.__version__)"
echo "PySCF OK" > output.log
