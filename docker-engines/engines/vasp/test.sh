#!/bin/bash
set -e
echo "[Test] Verifying VASP (BYOB wrapper)..."
which vasp_std
vasp_std
echo "VASP BYOB OK" > output.log
