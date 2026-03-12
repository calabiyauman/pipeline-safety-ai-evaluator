"""Run local checks equivalent to CI before pushing."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_step(name: str, command: list[str]) -> int:
    print(f"\n==> {name}")
    print("$", " ".join(command))
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"\nFAILED: {name} (exit {result.returncode})")
        return result.returncode
    print(f"PASSED: {name}")
    return 0


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    print(f"Repository: {repo_root}")

    checks = [
        ("flake8", [sys.executable, "-m", "flake8", "src", "tests"]),
        ("pytest", [sys.executable, "-m", "pytest", "tests", "-q"]),
    ]

    for name, command in checks:
        code = run_step(name, command)
        if code != 0:
            return code

    print("\nAll local CI preflight checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
