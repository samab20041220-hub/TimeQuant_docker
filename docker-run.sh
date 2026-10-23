#!/usr/bin/env bash
# Standalone Docker runner for TimeQuant Simulation Engines
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${DIR}"

CMD="${1:-help}"
ENGINE="${2:-gpaw}"

case "${CMD}" in
  build)
    if [ -z "$2" ]; then
      echo "🔨 Building all engines..."
      cd docker-engines && ./build_all.sh
    else
      echo "🔨 Building engine: $2..."
      cd docker-engines && ./build_all.sh "$2"
    fi
    ;;
  run)
    mkdir -p "${DIR}/workspace"
    echo "🚀 Running engine container: timequant/engine-${ENGINE}:latest in isolation..."
    docker run --rm -it \
      -v "${DIR}/workspace:/workspace" \
      -w /workspace \
      "timequant/engine-${ENGINE}:latest" "${@:3}"
    ;;
  compose)
    echo "🚀 Starting compose profile: ${ENGINE}..."
    docker compose --profile "${ENGINE}" up -d
    ;;
  list)
    echo "📋 Available TimeQuant engines (31):"
    ls -1 "${DIR}/docker-engines/engines"
    ;;
  status)
    docker ps --filter "name=tq-engine-"
    ;;
  help|*)
    echo "TimeQuant Docker Engines Manager"
    echo "Usage:"
    echo "  $0 list                     - List all 31 supported engines"
    echo "  $0 build [engine]           - Build all engines or a specific one (e.g. $0 build gpaw)"
    echo "  $0 run <engine> [args...]   - Run an isolated engine container interactively"
    echo "  $0 compose <profile>        - Start via compose profile (e.g. $0 compose gpaw)"
    echo "  $0 status                   - Check running engine containers"
    ;;
esac

