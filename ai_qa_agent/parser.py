"""Utilities to clean and save generated pytest code."""

from __future__ import annotations

import re
from pathlib import Path

HEADER = """import sys
from pathlib import Path

import numpy as np
import pytest

CODE_DIR = Path(__file__).resolve().parent.parent.parent / "code"
sys.path.insert(0, str(CODE_DIR))
import majorization  # type: ignore[import-not-found]

"""


def clean_generated_code(raw: str) -> str:
    """Remove markdown fences and extra prose from LLM output."""
    # Strip triple-backtick blocks.
    raw = re.sub(r"```python\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    # Strip leading/trailing blank lines.
    return raw.strip()


def normalize_test_code(code: str, function_name: str) -> str:
    """Sanitize generated test code and prepend a known-good import header."""
    code = clean_generated_code(code)

    # Remove any import lines the LLM may have added despite instructions.
    lines = code.splitlines()
    filtered = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            continue
        filtered.append(line)
    code = "\n".join(filtered)

    # Ensure bare function calls are prefixed with majorization.
    # Match the function name when it appears at the start of a line or after
    # an assignment/comma/open-paren, but not when it is already dotted.
    pattern = re.compile(rf"(?<!majorization\.)\b{re.escape(function_name)}\s*\(")
    code = pattern.sub(f"majorization.{function_name}(", code)

    # Remove any stray placeholder function definitions the LLM may have added.
    code = re.sub(
        rf"^def\s+{re.escape(function_name)}\s*\([^)]*\):\s*(\n\s+.+)*",
        "",
        code,
        flags=re.MULTILINE,
    )

    return HEADER + code.strip() + "\n"


def save_test_file(function_name: str, code: str, output_dir: Path) -> Path:
    """Write generated pytest code to a deterministic file path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"test_{function_name}_generated.py"
    normalized = normalize_test_code(code, function_name)
    path.write_text(normalized, encoding="utf-8")
    return path
