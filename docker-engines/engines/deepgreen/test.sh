#!/bin/bash
set -e
echo "[Test] Verifying DeepGreen / GreenLearning..."
python3 -c "import greenlearning; print('GreenLearning OK')"
echo "DeepGreen OK" > output.log
