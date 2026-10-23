#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$ROOT_DIR/engines"
DOCKERHUB_NAMESPACE="${DOCKERHUB_NAMESPACE:-timequant}"
BUILD_AND_CLEAN="${BUILD_AND_CLEAN:-0}"

if [ $# -gt 0 ]; then
    ENGINES="$@"
else
    ENGINES="$(ls -1 "$BASE_DIR")"
fi

echo "Pushing TimeQuant engines to namespace '$DOCKERHUB_NAMESPACE': $ENGINES"

for engine in $ENGINES; do
    if [ ! -d "$BASE_DIR/$engine" ]; then
        echo "Error: Engine directory '$BASE_DIR/$engine' does not exist." >&2
        exit 1
    fi

    LOCAL_TAG="timequant/engine-${engine}:latest"
    REMOTE_TAG="${DOCKERHUB_NAMESPACE}/engine-${engine}:latest"

    if [ "$BUILD_AND_CLEAN" = "1" ] || ! docker image inspect "$LOCAL_TAG" >/dev/null 2>&1; then
        echo "Building missing image $LOCAL_TAG..."
        "$ROOT_DIR/build_all.sh" "$engine"
    fi

    if [ "$LOCAL_TAG" != "$REMOTE_TAG" ]; then
        docker tag "$LOCAL_TAG" "$REMOTE_TAG"
    fi

    echo "====================================="
    echo "Pushing: $REMOTE_TAG"
    echo "====================================="
    docker push "$REMOTE_TAG"

    if [ "$BUILD_AND_CLEAN" = "1" ]; then
        echo "Cleaning up local image and build cache to save disk space..."
        docker rmi "$REMOTE_TAG" "$LOCAL_TAG" 2>/dev/null || true
        docker builder prune -f >/dev/null 2>&1 || true
    fi
done

echo "All selected engines pushed successfully!"

