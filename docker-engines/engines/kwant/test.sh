#!/bin/bash
set -e
echo "[Test] Verifying Kwant..."
python3 -c "import kwant; print('Kwant version:', kwant.__version__)"
echo "Kwant OK" > output.log
