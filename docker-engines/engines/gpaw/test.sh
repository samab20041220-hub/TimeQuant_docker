#!/bin/bash
set -e
echo "[Test] Verifying GPAW..."
gpaw info 2>&1 | head -n 10 || python3 -c "import gpaw; print('GPAW version:', gpaw.__version__)"
echo "GPAW OK" > output.log
