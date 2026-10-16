#!/usr/bin/env python3
import os
import subprocess
import sys

def run_tests():
    base_dir = os.environ.get("ENGINES_DIR", "/engines")
    if not os.path.exists(base_dir):
        print(f"[TestRunner] Engines directory not found at: {base_dir}")
        sys.exit(1)

    print(f"[TestRunner] Discovering engines in: {base_dir}")
    engines = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    print(f"[TestRunner] Found {len(engines)} engines: {', '.join(engines)}")

    passed, failed = [], []
    for engine in engines:
        test_script = os.path.join(base_dir, engine, "test.sh")
        if not os.path.exists(test_script):
            print(f"[WARN] No test.sh found for {engine}")
            failed.append(engine)
            continue

        print(f"[TestRunner] Running test for {engine}...")
        res = subprocess.run(["bash", "./test.sh"], cwd=os.path.join(base_dir, engine), capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[PASS] {engine}")
            passed.append(engine)
        else:
            print(f"[FAIL] {engine}: {res.stderr}")
            failed.append(engine)

    print("\n" + "=" * 40)
    print(f"Results: {len(passed)} passed, {len(failed)} failed")
    print("=" * 40)
    sys.exit(0 if not failed else 1)

if __name__ == "__main__":
    run_tests()
