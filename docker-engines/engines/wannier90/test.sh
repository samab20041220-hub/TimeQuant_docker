#!/bin/bash
set -e
echo "[Test] Verifying Wannier90..."
if which wannier90.x >/dev/null 2>&1; then
    which wannier90.x
elif which wannier90 >/dev/null 2>&1; then
    which wannier90
else
    echo "Wannier90 binary not found" && exit 1
fi
echo "Wannier90 OK" > output.log
