"""LLM-based test generation agent for scientific Python functions."""

from __future__ import annotations

import ast
from pathlib import Path

import structlog
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from ai_qa_agent.settings import Settings

logger = structlog.get_logger()

PROMPT_TEMPLATE = """You are an expert SDET and Python test engineer.

Your task is to generate pytest unit tests for the following Python function.
The function is part of a scientific computing project and uses NumPy.

Function source:
```python
{source}
```

Requirements for the generated tests:
1. Use pytest.
2. Call the function under test as `majorization.{name}(...)`. Do NOT use any other import or call style.
3. Do NOT write any `import` statements. Do NOT write `import numpy as np`, `import pytest`, `from code...`, or `import majorization`. The test harness will prepend all necessary imports automatically.
4. Cover normal inputs, edge cases, and at least one invalid/unexpected input if applicable.
5. For floating-point comparisons, use `np.allclose` or `pytest.approx` with reasonable tolerances.
6. Tests should be self-contained and runnable.
7. Return ONLY the test functions, without markdown fences or explanation.
8. Do not include a main block, docstrings, or example usage.
"""


def extract_function_sources(module_path: Path) -> dict[str, str]:
    """Extract top-level function names and source snippets from a Python file."""
    source = module_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1
            end = node.end_lineno
            func_source = "\n".join(source.splitlines()[start:end])
            functions[node.name] = func_source
    return functions


def select_target_functions(module_path: Path, names: list[str] | None = None) -> dict[str, str]:
    """Return function sources to test. Defaults to a curated Milestone 1 subset.

    The default list includes `renyi` even though it is not yet implemented, so
    the demo can show failure analysis and root-cause reporting.
    """
    all_functions = extract_function_sources(module_path)
    if names is None:
        names = ["lorenz", "is_majorized", "shannon", "binary_entropy", "renyi"]
    return {name: all_functions[name] for name in names if name in all_functions}


def generate_tests_for_function(func_source: str, settings: Settings) -> str:
    """Call the configured LLM to generate pytest code for one function."""
    first_line = func_source.strip().splitlines()[0]
    name = first_line.replace("def ", "").split("(")[0].strip()
    prompt = PROMPT_TEMPLATE.format(source=func_source, name=name)

    logger.info("generating_tests", function=name, client=settings.client)

    if settings.client == "openai":
        return _call_openai(prompt, settings)
    if settings.client == "anthropic":
        return _call_anthropic(prompt, settings)

    # Fallback for environments without an API key: deterministic placeholder.
    return _placeholder_tests(func_source)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    reraise=True,
)
def _call_openai(prompt: str, settings: Settings) -> str:
    try:
        import openai
    except ImportError as exc:
        raise RuntimeError("openai package is not installed") from exc

    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")

    client_kwargs = {"api_key": settings.openai_api_key}
    if settings.openai_base_url:
        client_kwargs["base_url"] = settings.openai_base_url

    client = openai.OpenAI(**client_kwargs)  # type: ignore[arg-type]
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You generate pytest unit tests for Python functions."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=2048,
    )
    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("OpenAI returned empty content")
    logger.info("openai_response_received", model=settings.openai_model, length=len(content))
    return content


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    reraise=True,
)
def _call_anthropic(prompt: str, settings: Settings) -> str:
    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError("anthropic package is not installed") from exc

    if not settings.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(  # type: ignore[call-overload]
        model=settings.anthropic_model,
        max_tokens=2048,
        temperature=0.2,
        system="You generate pytest unit tests for Python functions.",
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.content[0].text
    if content is None:
        raise RuntimeError("Anthropic returned empty content")
    logger.info("anthropic_response_received", model=settings.anthropic_model, length=len(content))
    return content


def _placeholder_tests(func_source: str) -> str:
    """Generate a minimal placeholder test when no LLM key is available."""
    first_line = func_source.strip().splitlines()[0]
    name = first_line.replace("def ", "").split("(")[0].strip()

    # Tailored smoke inputs so implemented functions pass and NotImplementedError
    # functions fail, making the demo interesting even without an LLM.
    smoke_inputs = {
        "lorenz": "np.array([0.25, 0.5, 0.25])",
        "is_majorized": "np.array([0.25, 0.25, 0.25, 0.25]), np.array([1.0, 0.0, 0.0, 0.0])",
        "shannon": "np.array([0.5, 0.5])",
        "binary_entropy": "0.5",
        "renyi": "np.array([0.5, 0.5]), 2.0",
    }
    args = smoke_inputs.get(name, "")

    # No imports here; parser.py will prepend the standard header.
    return f"""def test_{name}_placeholder():
    # Placeholder smoke test generated without LLM access.
    result = majorization.{name}({args})
    assert result is not None
"""
