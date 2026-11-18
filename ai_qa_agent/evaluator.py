"""Evaluate the quality of LLM-generated tests against baseline tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_baseline_tests(baseline_dir: Path) -> dict:
    """Run the hand-written baseline tests and return a summary."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(baseline_dir),
        "-q",
        "--no-header",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=baseline_dir.parent)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "passed": result.returncode == 0,
    }


def evaluate_agent_run(report_data: dict) -> dict:
    """Compute high-level metrics from a completed agent run."""
    functions = report_data.get("functions", {})
    total = len(functions)
    if total == 0:
        return {}

    generation_success = sum(
        1 for r in functions.values() if "generation_error" not in r.get("failure_categories", {})
    )
    fully_passing = sum(1 for r in functions.values() if r.get("returncode") == 0)
    total_tests = sum(
        r.get("passed", 0) + r.get("failed", 0) + r.get("error", 0) for r in functions.values()
    )
    total_passed = sum(r.get("passed", 0) for r in functions.values())

    return {
        "functions_tested": total,
        "generation_success_rate": round(generation_success / total, 3),
        "fully_passing_suites": fully_passing,
        "overall_test_pass_rate": round(total_passed / total_tests, 3) if total_tests else 0.0,
        "total_tests_executed": total_tests,
    }


def load_report_json(report_path: Path) -> dict:
    """Parse a Markdown report into a structured dict for evaluation.

    This is a lightweight parser; for production use, consider emitting JSON.
    """
    text = report_path.read_text(encoding="utf-8")
    # Extract function sections heuristically.
    functions = {}
    for line in text.splitlines():
        if line.startswith("- `") and ":" in line:
            name = line.split("`")[1]
            # Heuristic: if line contains 'passed', it's a function result.
            functions[name] = {"raw": line}
    return {"functions": functions}


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    baseline = repo_root / "ai_qa_agent" / "baseline_tests"
    print(json.dumps(run_baseline_tests(baseline), indent=2))
