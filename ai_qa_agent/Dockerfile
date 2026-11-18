# Multi-stage Dockerfile for the AI QA Agent.
# Builds a lean, non-root container suitable for CI/CD and Kubernetes.

# -----------------------------------------------------------------------------
# Build stage: install build dependencies and Python packages
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# Install system build dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a virtual environment.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ai_qa_agent/pyproject.toml /build/pyproject.toml
COPY ai_qa_agent/README.md /build/README.md
COPY ai_qa_agent/__init__.py /build/ai_qa_agent/__init__.py
RUN pip install --no-cache-dir -e ".[web]"

# -----------------------------------------------------------------------------
# Production stage: copy only the venv and application code
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS production

WORKDIR /app

# Create a non-root user for security.
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy virtual environment from builder.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code and the target research module.
COPY ai_qa_agent /app/ai_qa_agent
COPY code /app/code

# Ensure the non-root user owns the working directory.
RUN chown -R appuser:appgroup /app
USER appuser

# Expose the API port.
EXPOSE 8000

# Health check for orchestrators.
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Default: run the CLI pipeline in placeholder mode.
# Override with `docker run ai-qa-agent:latest python -m ai_qa_agent.main --client openai`
CMD ["python", "-m", "ai_qa_agent.main", "--client", "placeholder"]
