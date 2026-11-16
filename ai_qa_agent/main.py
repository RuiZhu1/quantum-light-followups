"""End-to-end pipeline: generate tests with an LLM agent and run them."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Ensure the repository root is on sys.path so `ai_qa_agent` and `code` packages are importable.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import structlog

try:
    from ai_qa_agent.agent import generate_tests_for_function, select_target_functions
    from ai_qa_agent.logging_config import configure_logging
    from ai_qa_agent.parser import clean_generated_code, save_test_file
    from ai_qa_agent.reporter import generate_report
    from ai_qa_agent.runner import run_pytest
    from ai_qa_agent.settings import Settings
except ModuleNotFoundError:
    # Fallback when running the script directly inside the package directory.
    from agent import (  # type: ignore[import-not-found, no-redef]
        generate_tests_for_function,
        select_target_functions,
    )
    from logging_config import configure_logging  # type: ignore[import-not-found, no-redef]
    from parser import clean_generated_code, save_test_file  # type: ignore[import-not-found, no-redef]
    from reporter import generate_report  # type: ignore[import-not-found, no-redef]
    from runner import run_pytest  # type: ignore[import-not-found, no-redef]
    from settings import Settings  # type: ignore[import-not-found, no-redef]

logger = structlog.get_logger()


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments, allowing env vars to provide defaults."""
    parser = argparse.ArgumentParser(description="Generate pytest tests with an LLM agent.")
    parser.add_argument(
        "--functions",
        nargs="+",
        default=None,
        help="Names of functions to test (default: lorenz, is_majorized, shannon, binary_entropy, renyi)",
    )
    parser.add_argument(
        "--client",
        choices=["openai", "anthropic", "placeholder"],
        default=None,
        help="LLM backend to use",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=None,
        help="Number of parallel pytest workers (requires pytest-xdist)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Path to write the Markdown report",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = Settings()

    # CLI overrides env vars.
    if args.client is not None:
        settings.client = args.client
    if args.num_workers is not None:
        settings.num_workers = args.num_workers
    if args.report is not None:
        settings.report_path = args.report

    configure_logging(log_level=settings.log_level, json_logs=settings.json_logs)
    logger.info(
        "pipeline_started",
        client=settings.client,
        num_workers=settings.num_workers,
        target_module=str(settings.target_module),
    )

    targets = select_target_functions(settings.target_module, args.functions)
    if not targets:
        logger.error("no_target_functions_found")
        return 1

    # Clear previous generated tests to avoid stale results.
    settings.generated_tests_dir.mkdir(parents=True, exist_ok=True)
    for old_file in settings.generated_tests_dir.glob("test_*_generated.py"):
        old_file.unlink()

    function_results: dict[str, dict] = {}
    total_generation_time = 0.0

    for name, source in targets.items():
        logger.info("generating_tests", function=name)
        gen_start = time.perf_counter()
        try:
            raw_tests = generate_tests_for_function(source, settings=settings)
        except Exception as exc:
            logger.error("generation_failed", function=name, error=str(exc))
            function_results[name] = {
                "returncode": 1,
                "stdout": "",
                "stderr": str(exc),
                "passed": 0,
                "failed": 0,
                "error": 1,
                "elapsed_seconds": 0.0,
                "failure_categories": {"generation_error": 1},
                "generation_seconds": 0.0,
            }
            continue
        gen_elapsed = time.perf_counter() - gen_start
        total_generation_time += gen_elapsed

        cleaned = clean_generated_code(raw_tests)
        test_path = save_test_file(name, cleaned, settings.generated_tests_dir)
        logger.info("test_file_saved", function=name, path=str(test_path))

        result = run_pytest(test_path, num_workers=settings.num_workers)
        result["generation_seconds"] = round(gen_elapsed, 3)
        function_results[name] = result
        logger.info(
            "test_run_complete",
            function=name,
            passed=result["passed"],
            failed=result["failed"],
            error=result["error"],
            elapsed=result["elapsed_seconds"],
        )

    report = generate_report(
        function_results,
        output_path=settings.report_path,
        total_generation_time=round(total_generation_time, 3),
    )
    logger.info("report_written", path=str(settings.report_path))
    print(f"\nReport written to: {settings.report_path}")
    print("\n" + "=" * 50)
    print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
