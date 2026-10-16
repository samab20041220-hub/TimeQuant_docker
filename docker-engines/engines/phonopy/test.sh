#!/bin/bash
set -e
echo "[Test] Verifying Phonopy..."
python3 -c "import phonopy; print('Phonopy version:', phonopy.__version__)"
echo "Phonopy OK" > output.log
