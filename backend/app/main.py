from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.database import get_session, init_db
from app.evaluation.runner import make_leadership_summary, run_python_evaluation
from app.models import CodingTask, EvaluationRun, PipelineStatus
from app.schemas import EvaluationResponse, SubmissionRequest

app = FastAPI(title="Code Model ResearchOps API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Code Model ResearchOps API is running"}


@app.get("/tasks")
def list_tasks(session: Session = Depends(get_session)):
    return session.exec(select(CodingTask)).all()


@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(CodingTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}/status")
def update_task_status(
    task_id: int,
    status: PipelineStatus,
    session: Session = Depends(get_session),
):
    task = session.get(CodingTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_submission(
    request: SubmissionRequest,
    session: Session = Depends(get_session),
):
    task = session.get(CodingTask, request.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    result = run_python_evaluation(
        submitted_code=request.submitted_code,
        tests_code=task.tests_code,
    )

    summary = make_leadership_summary(
        model_name=request.model_name,
        task_title=task.title,
        passed=result["passed"],
        score=result["score"],
    )

    run = EvaluationRun(
        task_id=task.id,
        model_name=request.model_name,
        submitted_code=request.submitted_code,
        passed=result["passed"],
        score=result["score"],
        test_output=result["test_output"],
        leadership_summary=summary,
    )

    session.add(run)
    session.commit()
    session.refresh(run)

    return EvaluationResponse(
        run_id=run.id,
        passed=run.passed,
        score=run.score,
        test_output=run.test_output,
        leadership_summary=run.leadership_summary,
    )


@app.get("/runs")
def list_runs(session: Session = Depends(get_session)):
    return session.exec(select(EvaluationRun)).all()
