#!/bin/bash
set -e
echo "[Test] Verifying Yambo..."
which yambo || which /opt/conda/bin/yambo
echo "Yambo OK" > output.log
