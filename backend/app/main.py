from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from email_validator import validate_email, EmailNotValidError

from app.database import get_session, init_db
from app.evaluation.runner import make_leadership_summary, run_python_evaluation
from app.models import CodingTask, EvaluationRun, PipelineStatus, Users
from app.schemas import EvaluationResponse, SubmissionRequest, UserResponse

app = FastAPI(title="Code Model ResearchOps API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ],
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

@app.post("/users")
def create_users(
    request: UserResponse,
    session: Session = Depends(get_session),
):
    # Check if email already exists
    check_email = session.get(Users, request.email)
    if check_email:
        return "Email already found in system." 
    
    # Check if email is in correct format
    try:
        # Check and deliverability (DNS) check
        email_info = validate_email(request.email, check_deliverability=True)
        # Get the normalized form of the email (e.g., lowercase domain)
        normalized_email = email_info.normalized
        
    except EmailNotValidError as e:
        # The library provides human-readable error messages
        return(f"Invalid: {str(e)}")

    # Create user object
    user = Users(first_name=request.first, last_name=request.last, email=normalized_email)

    session.add(user)

    return {"message": "User created successfully"}

