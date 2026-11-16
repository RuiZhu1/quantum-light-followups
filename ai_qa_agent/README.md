# AI QA Agent

An industrial-style demo of AI-assisted test generation built on top of the `quantum_light_followups` research skeleton. It is intended for interview preparation and learning, but uses patterns found in real SDET/QA infrastructure work.

## What it does

The agent implements a closed-loop QA workflow:

1. **Ingest** — reads functions from a target Python module.
2. **Generate** — sends signatures and docstrings to an LLM with a structured prompt.
3. **Sanitize** — strips unsafe imports, normalizes call style, and prepends a known-good header.
4. **Execute** — runs the generated `pytest` cases, optionally in parallel.
5. **Report** — produces a Markdown report with pass/fail counts, failure categories, and timing.

## Industrial features

| Feature | Files | Why it matters |
|---|---|---|
| Structured config | `settings.py`, `pyproject.toml` | Env-based, validated, typed |
| Structured logging | `logging_config.py` | JSON logs for production observability |
| LLM retry/backoff | `agent.py` | Resilient to transient API failures |
| Package manifest | `pyproject.toml` | Installable, versioned, tool config |
| Lint / format / type check | `.github/workflows/...`, `pyproject.toml` | Code quality gates |
| Pre-commit hooks | `.pre-commit-config.yaml` | Local quality checks |
| Multi-stage Docker | `Dockerfile` | Lean, non-root, health-checked image |
| Docker Compose | `docker-compose.yml` | Local orchestration of CLI + API |
| Helm chart | `helm/ai-qa-agent/` | Production Kubernetes deployment |
| REST API | `api.py` | Service-oriented interface |
| Cloud deployment example | `terraform/` | AWS ECS Fargate template |
| CI/CD | `.github/workflows/ai_qa_agent.yml` | Lint, test, build, push to GHCR |

## Setup

```bash
cd ai_qa_agent
python -m venv venv
source venv/bin/activate
pip install -e ".[dev,web]"
```

## Configuration

Configuration is loaded from environment variables (prefixed with `AI_QA_`) or an `ai_qa_agent/.env` file.

```bash
cp .env.example .env
# edit .env with your API keys
source .env
```

Key variables:
- `AI_QA_CLIENT` — `placeholder`, `openai`, or `anthropic`
- `AI_QA_OPENAI_API_KEY` / `AI_QA_OPENAI_MODEL`
- `AI_QA_ANTHROPIC_API_KEY` / `AI_QA_ANTHROPIC_MODEL`
- `AI_QA_NUM_WORKERS` — parallel pytest workers
- `AI_QA_LOG_LEVEL` — `DEBUG`, `INFO`, `WARNING`, `ERROR`

## CLI usage

```bash
# From the ai_qa_agent directory
python main.py --client placeholder --num-workers 2

# Or from the repository root
python -m ai_qa_agent.main --client placeholder --num-workers 2

# OpenAI / Zhipu / Anthropic
python main.py --client openai --num-workers 2
```

## REST API usage

Run the service from the **repository root** so the `ai_qa_agent` package is importable:

```bash
# From the repository root
uvicorn ai_qa_agent.api:app --reload

# Health check
curl http://localhost:8000/health

# Generate tests for one function
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"function_name": "lorenz"}'

# Generate tests for all functions
curl -X POST http://localhost:8000/generate-all
```

## Baseline tests

Hand-written tests validate the target functions before trusting generated tests:

```bash
python -m pytest ai_qa_agent/baseline_tests/ -v
```

## Docker

```bash
# Build
docker build -f ai_qa_agent/Dockerfile -t ai-qa-agent:latest .

# Run CLI pipeline
docker run --rm ai-qa-agent:latest

# Run API
docker run --rm -p 8000:8000 ai-qa-agent:latest \
  uvicorn ai_qa_agent.api:app --host 0.0.0.0 --port 8000
```

## Docker Compose

```bash
cd ai_qa_agent
docker-compose up --build
```

## Kubernetes / Helm

```bash
cd ai_qa_agent/helm/ai-qa-agent

# Create the secret for LLM keys
kubectl create secret generic llm-api-keys \
  --from-literal=openai-api-key=your-key

# Install the chart
helm install ai-qa-agent .
```

## CI/CD

The GitHub Actions workflow (`.github/workflows/ai_qa_agent.yml`) runs:

1. `ruff` lint and format checks
2. `mypy` type checking
3. Baseline tests with coverage
4. AI QA agent pipeline (placeholder mode)
5. Docker image build and push to GitHub Container Registry

## Terraform / AWS

An example AWS ECS Fargate deployment is in `terraform/`. It expects:
- A VPC with subnets and security groups
- An ECS task execution role
- An AWS Secrets Manager secret for the OpenAI API key

## Interview narrative

> "I built an AI-assisted test-generation service with industrial SDET patterns. The agent reads a function, asks an LLM for pytest cases, sanitizes and runs them, and reports pass/fail with failure categories. I added structured logging, retry logic, validated configuration, a FastAPI service, multi-stage Docker builds, Helm charts for Kubernetes, GitHub Actions CI/CD with lint/type/test/build/push stages, and a Terraform example for AWS deployment. Running it on my research project generated 30 tests, 12 passed and 18 failed — mostly because the LLM hallucinated expected values, which reinforced why baseline tests and human review are essential in agent-driven QA."

## Security notes

- Never commit API keys. `.env` and Terraform state files are `.gitignore`d.
- The Docker image runs as a non-root user.
- Kubernetes secrets are mounted via the `llm-api-keys` Secret, not plain env vars in the chart.
