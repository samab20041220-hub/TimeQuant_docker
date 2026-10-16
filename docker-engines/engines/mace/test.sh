#!/bin/bash
set -e
echo "[Test] Verifying MACE..."
python3 -c "import mace; print('MACE version:', getattr(mace, '__version__', 'OK'))"
echo "MACE OK" > output.log
