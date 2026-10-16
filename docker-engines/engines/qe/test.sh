#!/bin/bash
set -e
echo "[Test] Verifying Quantum ESPRESSO..."
which pw.x
which ph.x
which pp.x
echo "QE OK" > output.log
