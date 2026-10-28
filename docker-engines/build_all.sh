#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$ROOT_DIR/engines"

if [ $# -gt 0 ]; then
    ENGINES="$@"
else
    ENGINES="$(ls -1 "$BASE_DIR")"
fi

echo "Building TimeQuant engines: $ENGINES"

for engine in $ENGINES; do
    if [ ! -d "$BASE_DIR/$engine" ]; then
        echo "Error: Engine directory '$BASE_DIR/$engine' does not exist." >&2
        exit 1
    fi
    echo "====================================="
    echo "Building engine: $engine"
    echo "====================================="
    docker build --network=host -f "$BASE_DIR/$engine/Dockerfile" -t timequant/engine-${engine}:latest "$ROOT_DIR"
    docker tag timequant/engine-${engine}:latest zorbeur/engine-${engine}:latest 2>/dev/null || true
    echo "Successfully built timequant/engine-${engine}:latest and zorbeur/engine-${engine}:latest"
done

echo "All engines built successfully!"
