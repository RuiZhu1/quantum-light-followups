"""Helper to load code/majorization.py without treating `code` as a package.

The directory name `code` shadows the Python standard library module `code`,
so we load majorization.py directly via importlib to avoid import conflicts.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_majorization():
    """Load `code/majorization.py` as a standalone module."""
    repo_root = Path(__file__).resolve().parent.parent
    module_path = repo_root / "code" / "majorization.py"
    spec = importlib.util.spec_from_file_location("majorization_demo", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["majorization_demo"] = module
    spec.loader.exec_module(module)
    return module
