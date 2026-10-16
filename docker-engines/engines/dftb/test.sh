#!/bin/bash
set -e
echo "[Test] Verifying DFTB+..."
which dftb+ || which /opt/conda/bin/dftb+
echo "DFTB+ OK" > output.log
