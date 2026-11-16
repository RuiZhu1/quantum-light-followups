"""Generate a concise report from pytest results."""

from __future__ import annotations

from pathlib import Path


def generate_report(
    function_results: dict[str, dict],
    output_path: Path | None = None,
    total_generation_time: float = 0.0,
) -> str:
    """Build a human-readable report from per-function pytest results."""
    lines = ["# AI Test Generation Report", ""]

    total_tests = sum(
        r.get("passed", 0) + r.get("failed", 0) + r.get("error", 0)
        for r in function_results.values()
    )
    total_passed = sum(r.get("passed", 0) for r in function_results.values())
    total_failed = sum(r.get("failed", 0) for r in function_results.values())
    total_errors = sum(r.get("error", 0) for r in function_results.values())
    total_execution_time = sum(r.get("elapsed_seconds", 0.0) for r in function_results.values())

    lines.append("## Summary")
    lines.append(f"- Functions tested: {len(function_results)}")
    lines.append(f"- Generated tests executed: {total_tests}")
    lines.append(f"- Passed: {total_passed} / {total_tests}")
    lines.append(f"- Failed: {total_failed} / {total_tests}")
    lines.append(f"- Errors: {total_errors} / {total_tests}")
    lines.append(f"- LLM generation time: {total_generation_time:.3f}s")
    lines.append(f"- Test execution time: {total_execution_time:.3f}s")
    lines.append("")

    passing = [name for name, r in function_results.items() if r["returncode"] == 0]
    failing = [name for name, r in function_results.items() if r["returncode"] != 0]

    lines.append(f"## Fully passing suites: {len(passing)}")
    if passing:
        for name in passing:
            r = function_results[name]
            lines.append(f"- `{name}`: {r['passed']} passed ({r['elapsed_seconds']}s)")
    else:
        lines.append("- None")
    lines.append("")

    lines.append(f"## Failing/error suites: {len(failing)}")
    if failing:
        for name in failing:
            r = function_results[name]
            lines.append(
                f"- `{name}`: {r.get('passed', 0)} passed, "
                f"{r.get('failed', 0)} failed, {r.get('error', 0)} error "
                f"(gen {r.get('generation_seconds', 0)}s, run {r['elapsed_seconds']}s)"
            )
            if r.get("failure_categories"):
                cats = ", ".join(f"{k}: {v}" for k, v in r["failure_categories"].items())
                lines.append(f"  - Failure categories: {cats}")
            # Include a short failure excerpt for manual inspection.
            excerpt = "\n".join(r["stdout"].splitlines()[:8])
            lines.append("  ```")
            lines.extend(f"  {line}" for line in excerpt.splitlines())
            lines.append("  ```")
            lines.append("")
    else:
        lines.append("- None")
        lines.append("")

    lines.append("## Notes")
    lines.append(
        "Failing tests are expected when the LLM hallucinates incorrect expected values "
        "or when the target function is not yet implemented. Baseline tests remain the "
        "source of truth for implemented functions."
    )

    report = "\n".join(lines)
    if output_path:
        output_path.write_text(report, encoding="utf-8")
    return report
