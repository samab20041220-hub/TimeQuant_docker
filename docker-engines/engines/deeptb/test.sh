#!/bin/bash
set -e
echo "[Test] Verifying DeePTB..."
python3 -c "import dptb; print('DeePTB (dptb) version:', getattr(dptb, '__version__', 'OK'))"
echo "DeePTB OK" > output.log
