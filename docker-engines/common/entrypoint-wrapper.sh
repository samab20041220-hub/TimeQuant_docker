#!/bin/bash
set -e

# Generic wrapper for capturing errors and logs
echo "[Wrapper] Starting execution of: $@"

# Execute the actual command
"$@" 2> /workspace/error.log
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "[Wrapper] Execution failed with exit code $EXIT_CODE" >&2
  cat /workspace/error.log >&2
fi

exit $EXIT_CODE
