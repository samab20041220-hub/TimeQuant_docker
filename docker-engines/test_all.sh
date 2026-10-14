#!/bin/bash

BASE_DIR="$(pwd)/docker-engines/engines"
FAILED_TESTS=()

echo "Testing all TimeQuant engines..."

for engine in $(ls -1 "$BASE_DIR"); do
    echo "====================================="
    echo "Testing engine: $engine"
    echo "====================================="

    # We mount the test directory to /workspace and run test.sh.
    # Because of Docker networking and mounting, we use the absolute path.
    TEST_DIR="$BASE_DIR/$engine/test"

    if [ -f "$BASE_DIR/$engine/test.sh" ]; then
        docker run --rm \
            --user 1000:1000 \
            -v "$TEST_DIR":/workspace \
            -w /workspace \
            --entrypoint /bin/bash \
            timequant/engine-${engine}:latest \
            -c "cd /workspace && bash ../test.sh"

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
