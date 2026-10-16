#!/bin/bash
set -e
echo "[Test] Verifying Nanoworks..."
python3 -c "import nanoworks; print('Nanoworks version:', getattr(nanoworks, '__version__', 'OK'))"
echo "Nanoworks OK" > output.log
