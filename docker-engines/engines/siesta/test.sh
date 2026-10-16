#!/bin/bash
set -e
echo "[Test] Verifying SIESTA..."
which siesta || which /opt/conda/bin/siesta
echo "SIESTA OK" > output.log
