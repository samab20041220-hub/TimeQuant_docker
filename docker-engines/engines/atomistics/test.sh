#!/bin/bash
set -e
echo "[Test] Verifying Atomistics..."
python3 -c "import atomistics; print('Atomistics version:', getattr(atomistics, '__version__', 'OK'))"
echo "Atomistics OK" > output.log
