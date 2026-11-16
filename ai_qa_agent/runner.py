"""Run generated pytest tests and collect results programmatically."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

FAILURE_CATEGORIES = {
    "NotImplementedError": "unimplemented_function",
    "AssertionError": "assertion_failure",
    "ImportError": "import_error",
    "ModuleNotFoundError": "import_error",
    "TypeError": "type_error",
    "ValueError": "value_error",
}


def run_pytest(target: Path, num_workers: int = 1) -> dict:
    """Run pytest on `target` (file or directory) and return a summary."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json_path = Path(tmp.name)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(target),
        "-q",
        "--tb=short",
        "--no-header",
        "--json-report",
        "--json-report-file",
        str(json_path),
    ]
    if num_workers > 1:
        cmd.extend(["-n", str(num_workers)])

    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=target.parent)
    elapsed = time.perf_counter() - start

    summary = _parse_json_report(json_path)
    json_path.unlink(missing_ok=True)

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "passed": summary.get("passed", 0),
        "failed": summary.get("failed", 0),
        "error": summary.get("error", 0),
        "elapsed_seconds": round(elapsed, 3),
        "failure_categories": _classify_failures(result.stdout),
    }


def _parse_json_report(json_path: Path) -> dict:
    """Parse pytest-json-report output into a flat summary."""
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    summary = data.get("summary", {})
    return {
        "passed": summary.get("passed", 0),
        "failed": summary.get("failed", 0),
        "error": summary.get("error", 0),
        "skipped": summary.get("skipped", 0),
    }


def _classify_failures(stdout: str) -> dict[str, int]:
    """Count failures by root-cause category from pytest output."""
    categories: dict[str, int] = {}
    for exception, category in FAILURE_CATEGORIES.items():
        count = len(re.findall(rf"\b{re.escape(exception)}\b", stdout))
        if count:
            categories[category] = categories.get(category, 0) + count
    return categories
