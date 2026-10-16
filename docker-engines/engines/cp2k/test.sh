#!/bin/bash
set -e
echo "[Test] Verifying CP2K..."
which cp2k
cp2k --version
echo "CP2K OK" > output.log
