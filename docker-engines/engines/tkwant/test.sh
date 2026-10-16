#!/bin/bash
set -e
echo "[Test] Verifying TKwant..."
python3 -c "import tkwant; print('TKwant version:', tkwant.__version__)"
echo "TKwant OK" > output.log
