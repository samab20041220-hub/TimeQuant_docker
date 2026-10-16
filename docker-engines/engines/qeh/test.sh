#!/bin/bash
set -e
echo "[Test] Verifying QEH..."
python3 -c "import qeh; print('QEH version:', getattr(qeh, '__version__', 'OK'))"
echo "QEH OK" > output.log
