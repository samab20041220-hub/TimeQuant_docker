#!/bin/bash
set -e
echo "[Test] Verifying WannierBerri..."
python3 -c "import wannierberri; print('WannierBerri version:', wannierberri.__version__)"
echo "WannierBerri OK" > output.log
