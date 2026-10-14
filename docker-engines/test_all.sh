#!/bin/bash

BASE_DIR="$(pwd)/docker-engines/engines"
FAILED_TESTS=()

echo "Testing all TimeQuant engines..."

for engine in $(ls -1 "$BASE_DIR"); do
    echo "====================================="
    echo "Testing engine: $engine"
    echo "====================================="

    # Mount the engine directory (which contains both test.sh and the test/ directory) to /workspace
    ENGINE_DIR="$BASE_DIR/$engine"

    if [ -f "$ENGINE_DIR/test.sh" ]; then
        docker run --rm \
            --user 1000:1000 \
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
