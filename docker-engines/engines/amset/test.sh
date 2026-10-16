#!/bin/bash
set -e
echo "[Test] Verifying AMSET..."
python3 -c "import amset; print('AMSET version:', amset.__version__)"
echo "AMSET OK" > output.log
