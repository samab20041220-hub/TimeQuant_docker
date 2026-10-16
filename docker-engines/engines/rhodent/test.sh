#!/bin/bash
set -e
echo "[Test] Verifying Rhodent..."
python3 -c "import rhodent; print('Rhodent version:', getattr(rhodent, '__version__', 'OK'))"
echo "Rhodent OK" > output.log
