#!/bin/bash
set -e
echo "[Test] Verifying BoltzTraP2..."
python3 -c "import BoltzTraP2; print('BoltzTraP2 OK')"
echo "BoltzTraP2 OK" > output.log
