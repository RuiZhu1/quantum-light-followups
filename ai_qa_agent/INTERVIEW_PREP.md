# Interview Prep: AI QA Agent Demo

Use this doc to prepare for the NVIDIA AI Agent / AI Infra SDET recruiter/hiring manager call.

---

## 1. Two-minute project narrative

> "I recently built a small AI-assisted test-generation prototype on top of a quantum-optics research skeleton I was working on. The agent reads a Python function's signature and docstring, sends it to an LLM, gets back pytest cases, writes them to disk, runs them, and produces a Markdown report with pass/fail summaries and failure excerpts.
>
> I hand-wrote baseline tests first for the functions I implemented — Lorenz curves, majorization checks, Shannon entropy, and binary entropy — to make sure the target code was correct before trusting generated tests. Then I let the agent generate additional tests. Some generated tests passed, but many failed — not because the code was wrong, but because the LLM hallucinated expected values or misunderstood the math. I also deliberately left one function, `renyi`, unimplemented, so the generated tests fail with `NotImplementedError`.
>
> I also built industrial-grade scaffolding around the prototype: a `pyproject.toml` package with typed settings and structured logging, LLM retry/backoff, a FastAPI service, multi-stage Docker builds with a non-root user and health checks, Docker Compose, a Helm chart for Kubernetes with liveness/readiness probes and Secrets management, a GitHub Actions CI/CD pipeline that lints, type-checks, tests, builds, and pushes the image to a container registry, and a Terraform example for AWS ECS Fargate. The main takeaway for me was that LLM-generated tests are useful for expanding coverage quickly, but you cannot trust them blindly. You still need deterministic validation, baseline tests, and human review to separate real code bugs from agent hallucinations. That's exactly the kind of agent-driven QA workflow your team is building."

---

## 2. Likely questions and suggested answers

### Q1: "How do you validate the output of an LLM/agent when there's no single correct answer?"

**Answer:**
> "For test generation, I use a layered approach. First, the generated code must be syntactically valid and runnable — that's an automatic filter. Second, I compare the generated tests against hand-written baseline tests on known-good functions. Third, I run the generated tests and check that failures make sense — for example, `renyi` fails because it's not implemented, not because the test is wrong. Finally, for more open-ended agent outputs, I'd use LLM-as-a-judge with a reference rubric, plus human sampling on a subset."

### Q2: "How would you design an agent to generate test cases automatically?"

**Answer:**
> "I'd structure it as a closed loop: the agent reads the function under test and its docstring, builds a prompt that asks for normal, edge, and invalid cases, receives pytest code, sanitizes it, writes it to a test file, runs it, and reports the result. The prompt should be explicit about imports, assertions, and floating-point tolerances. The agent should also receive feedback — pass/fail signals and coverage metrics — so it can iteratively improve the tests."

### Q3: "What are the risks of AI-generated tests, and how do you mitigate them?"

**Answer:**
> "The biggest risks are hallucinated assertions, tests that pass trivially without covering real behavior, and tests that are syntactically valid but semantically wrong. I mitigate them by: (1) requiring generated tests to exercise the actual function with concrete inputs, (2) running them against baseline tests on known-good implementations, (3) using coverage tools to detect shallow tests, and (4) keeping a human-in-the-loop for reviewing generated tests before they enter the regression suite."

### Q4: "Tell me about a time you debugged a complex system."

**Answer:** *(use the quantum project or the agent pipeline itself)*
> "In the quantum project, I had to debug why `shannon` was emitting NaN warnings. It turned out `np.log(0)` was being evaluated even inside `np.where`, because NumPy evaluates both branches. I fixed it by computing the log only on a masked positive array. The same systematic approach applies to distributed AI systems: isolate the failing component, reproduce with minimal input, check assumptions about data shape and edge cases, then validate the fix with regression tests."

### Q5: "Have you worked with Docker or Kubernetes?"

**Answer:**
> "For this demo I containerized the agent with a Dockerfile and docker-compose, and I wrote a Kubernetes Job manifest so the test-generation pipeline can run as a scheduled job in a cluster. I also set up a GitHub Actions workflow that builds the Docker image and runs the pipeline on every push. It's not production-scale experience, but it gave me hands-on practice with the lifecycle: local development → containerization → CI/CD → orchestration."

### Q6: "How would you design a CI/CD pipeline for AI-generated tests?"

**Answer:**
> "I'd separate the pipeline into stages: first run hand-written baseline tests to ensure the target code is healthy, then run the agent to generate tests, then validate that generated tests are syntactically valid and executable, then run them and compare results against baselines. Failures would be classified — is it a code bug, an agent hallucination, or an infrastructure issue? Reports and artifacts would be uploaded for review. I'd gate the merge on baseline tests passing, while treating generated-test failures as informational at first, until we have enough confidence to auto-accept them."

### Q7: "Why NVIDIA, and why SDET rather than SWE?"

**Answer:**
> "NVIDIA because it's at the center of AI infrastructure and GPU computing — the software you ship directly determines whether researchers and engineers can train and deploy models at scale. SDET rather than SWE because I'm drawn to the quality-engineering side: designing automation, building tools that catch bugs early, and now using AI to rethink how validation is done. I enjoy the combination of coding, debugging, and thinking about how to measure correctness."

---

## 3. Key phrases to weave into the conversation

- "agent-driven QA workflow"
- "test generation, execution, and failure analysis"
- "baseline tests before trusting generated tests"
- "deterministic validation for probabilistic outputs"
- "human-in-the-loop review"
- "root-cause reporting"
- "CI/CD, containerization, and reproducible test environments"
- "parallel test execution and performance benchmarking"

---

## 4. Questions to ask Emily / the hiring manager

1. "What does a typical day look like for an AI Agent SDET on the team?"
2. "What is the biggest quality challenge the team is solving with agents right now?"
3. "How much of the work is building frameworks versus applying existing LLM tools?"
4. "What does success look like in the first 90 days?"
5. "What are the next steps after this call?"

---

## 5. Logistics to confirm on the call

- Time and platform for Thursday
- Which specific opening is the best fit (JR2020478, JR2025044, or JR2027720)
- Your current status and earliest start date
- Whether you need visa sponsorship
- Salary expectations (have a range ready, but only share if asked)
