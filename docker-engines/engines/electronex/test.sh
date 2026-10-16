#!/bin/bash
set -e
echo "[Test] Verifying ELEQTRONeX / electronex..."
python3 -c "import electronex; print('electronex version:', getattr(electronex, '__version__', 'OK'))"
echo "ELEQTRONeX OK" > output.log
