#!/bin/bash
set -e
echo "[Test] Verifying HetDB / HetBuilder..."
python3 -c "import hetbuilder; print('HetBuilder version:', getattr(hetbuilder, '__version__', 'OK'))"
echo "HetDB OK" > output.log
