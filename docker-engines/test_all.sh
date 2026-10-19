#!/bin/bash

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/engines"
FAILED_TESTS=()

if [ $# -gt 0 ]; then
    ENGINES="$@"
else
    ENGINES="$(ls -1 "$BASE_DIR")"
fi

echo "Testing TimeQuant engines: $ENGINES"

for engine in $ENGINES; do
    if [ ! -d "$BASE_DIR/$engine" ]; then
        echo "Error: Engine directory '$BASE_DIR/$engine' does not exist." >&2
        FAILED_TESTS+=($engine)
        continue
    fi
    echo "====================================="
    echo "Testing engine: $engine"
    echo "====================================="

    # Mount the engine directory (which contains both test.sh and the test/ directory) to /workspace
    ENGINE_DIR="$BASE_DIR/$engine"

    if [ -f "$ENGINE_DIR/test.sh" ]; then
        if ! docker image inspect "timequant/engine-${engine}:latest" >/dev/null 2>&1; then
            echo "Image timequant/engine-${engine}:latest not found. Please build it first (e.g. via ./build_all.sh)."
            FAILED_TESTS+=($engine)
            continue
        fi

        docker run --rm \
            --user "$(id -u):$(id -g)" \
            -v "$ENGINE_DIR":/workspace \
            -w /workspace \
            --entrypoint /bin/bash \
            timequant/engine-${engine}:latest \
            -c "./test.sh"

        EXIT_CODE=$?

        if [ $EXIT_CODE -eq 0 ]; then
             echo "Engine $engine passed!"
        else
             echo "Engine $engine failed!"
             FAILED_TESTS+=($engine)
        fi
    else
        echo "No test.sh found for $engine!"
        FAILED_TESTS+=($engine)
    fi
done

if [ ${#FAILED_TESTS[@]} -eq 0 ]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "The following engines failed their tests: ${FAILED_TESTS[@]}"
    exit 1
fi
