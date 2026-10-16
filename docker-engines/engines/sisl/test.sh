#!/bin/bash
set -e
echo "[Test] Verifying sisl..."
python3 -c "import sisl; print('sisl version:', sisl.__version__)"
echo "sisl OK" > output.log
