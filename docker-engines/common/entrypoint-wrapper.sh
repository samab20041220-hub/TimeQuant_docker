#!/bin/bash
# Generic wrapper: runs the engine command, streams stderr live and keeps a copy
# in /workspace/error.log; propagates the engine's exit code.
echo "[Wrapper] Starting execution of: $@"

"$@" 2> >(tee /workspace/error.log >&2)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "[Wrapper] Execution failed with exit code $EXIT_CODE (stderr saved in /workspace/error.log)" >&2
fi

exit $EXIT_CODE
