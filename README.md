# Code Model ResearchOps Dashboard

A portfolio-ready starter project for evaluating AI coding assistants and tracking model outputs from **experiment** to **release candidate**.

This project is designed for roles involving AI/code-model research operations, technical program management, developer tooling, research-to-release workflows, and evaluation infrastructure.

## What it does

- Stores coding evaluation tasks
- Accepts model-generated code submissions
- Runs task-specific unit tests
- Produces pass/fail scores
- Tracks work through a research pipeline:
  - `idea`
  - `experiment`
  - `validated`
  - `release_candidate`
  - `released`
- Provides two reporting views:
  - Researcher view: detailed test output and failures
  - Leadership view: concise release-readiness summary

## Repo structure

```text
code-model-researchops/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── seed.py
│   │   └── evaluation/
│   │       └── runner.py
│   └── tests/
├── frontend/
│   └── src/
├── sample_tasks/
│   ├── fizzbuzz/
│   └── bugfix_cart/
└── .github/workflows/
```

## Quick start

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Demo workflow

1. Start the backend.
2. Seed the sample tasks.
3. Open the frontend.
4. Choose a coding task.
5. Paste a model-generated answer.
6. Run evaluation.
7. Review:
   - score
   - passed tests
   - failed tests
   - release-readiness summary

## Suggested portfolio upgrades

### Weekend version
- Add 3–5 coding tasks
- Improve README screenshots
- Add simple charts
- Add GitHub Actions

### Strong version
- Add model comparison table
- Add OpenAI/Mistral/local model integration
- Add experiment notes
- Add benchmark tags: `bugfix`, `refactor`, `test-generation`, `api-design`
- Add downloadable leadership report

### Excellent version
- Add task difficulty scoring
- Add flaky-test detection
- Add regression tracking across model versions
- Add authentication
- Add historical trend charts
- Deploy frontend and backend

## Resume bullet

Built a full-stack ResearchOps dashboard for evaluating AI coding assistants, using automated test-based scoring, experiment tracking, and executive-ready summaries to simulate the operational path from code-model research to release candidate.
