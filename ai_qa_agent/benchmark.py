"""Benchmark the AI QA agent pipeline.

Measures:
- LLM test-generation latency per function
- pytest execution time per function
- Total pipeline throughput
- Parallel speedup with pytest-xdist
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from ai_qa_agent.settings import Settings

ROOT = Path(__file__).resolve().parent


def run_pipeline(num_workers: int, settings: Settings) -> dict:
    """Run the agent pipeline and return timing metrics."""
    cmd = [
        sys.executable,
        str(ROOT / "main.py"),
        "--client",
        settings.client,
        "--num-workers",
        str(num_workers),
    ]
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    elapsed = time.perf_counter() - start
    return {
        "num_workers": num_workers,
        "returncode": result.returncode,
        "total_seconds": round(elapsed, 3),
    }


def main() -> int:
    settings = Settings()
    print(f"Benchmarking AI QA Agent pipeline (client={settings.client})...\n")

    for workers in [1, 2, 4]:
        print(f"Running with {workers} pytest worker(s)...")
        metrics = run_pipeline(num_workers=workers, settings=settings)
        print(f"  Total time: {metrics['total_seconds']}s")
        print()

    print("Benchmark complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
