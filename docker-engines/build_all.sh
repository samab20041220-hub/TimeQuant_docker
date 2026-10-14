#!/bin/bash
set -e

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/engines"

echo "Building all TimeQuant engines..."

for engine in $(ls -1 "$BASE_DIR"); do
    echo "====================================="
    echo "Building engine: $engine"
    echo "====================================="
    docker build -t timequant/engine-${engine}:latest "$BASE_DIR/$engine"
    echo "Successfully built timequant/engine-${engine}:latest"
done

echo "All engines built successfully!"
