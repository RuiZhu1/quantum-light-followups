"""FastAPI service exposing the AI QA agent pipeline as REST endpoints."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai_qa_agent.agent import generate_tests_for_function, select_target_functions
from ai_qa_agent.logging_config import configure_logging
from ai_qa_agent.parser import clean_generated_code, save_test_file
from ai_qa_agent.runner import run_pytest
from ai_qa_agent.settings import Settings

settings = Settings()
configure_logging(log_level=settings.log_level, json_logs=settings.json_logs)

app = FastAPI(title="AI QA Agent", version="0.1.0")


class GenerateRequest(BaseModel):
    """Request body for test generation."""

    function_name: str
    client: str | None = None


class GenerateResponse(BaseModel):
    """Response body for test generation."""

    function_name: str
    test_code: str
    passed: int
    failed: int
    error: int
    elapsed_seconds: float


@app.get("/health")
def health() -> dict:
    """Health check endpoint for load balancers and k8s probes."""
    return {"status": "healthy", "client": settings.client}


@app.get("/functions")
def list_functions() -> dict:
    """List available target functions in the configured module."""
    functions = select_target_functions(settings.target_module)
    return {"functions": list(functions.keys())}


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest) -> GenerateResponse:
    """Generate and run tests for a single function."""
    functions = select_target_functions(settings.target_module)
    if req.function_name not in functions:
        raise HTTPException(status_code=404, detail=f"Function {req.function_name} not found")

    client = req.client or settings.client
    settings.client = client

    raw_tests = generate_tests_for_function(functions[req.function_name], settings=settings)
    cleaned = clean_generated_code(raw_tests)
    test_path = save_test_file(req.function_name, cleaned, settings.generated_tests_dir)
    result = run_pytest(test_path, num_workers=settings.num_workers)

    return GenerateResponse(
        function_name=req.function_name,
        test_code=cleaned,
        passed=result["passed"],
        failed=result["failed"],
        error=result["error"],
        elapsed_seconds=result["elapsed_seconds"],
    )


@app.post("/generate-all")
def generate_all() -> dict:
    """Generate and run tests for all target functions."""
    functions = select_target_functions(settings.target_module)
    results = []
    for name in functions:
        raw_tests = generate_tests_for_function(functions[name], settings=settings)
        cleaned = clean_generated_code(raw_tests)
        test_path = save_test_file(name, cleaned, settings.generated_tests_dir)
        result = run_pytest(test_path, num_workers=settings.num_workers)
        results.append(
            {
                "function_name": name,
                "passed": result["passed"],
                "failed": result["failed"],
                "error": result["error"],
            }
        )
    return {"results": results}
