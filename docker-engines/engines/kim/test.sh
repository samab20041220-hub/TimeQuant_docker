#!/bin/bash
set -e
echo "[Test] Verifying OpenKIM..."
which kim-api-collections-management
kim-api-collections-management list
echo "OpenKIM OK" > output.log
