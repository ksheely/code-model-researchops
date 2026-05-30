from pydantic import BaseModel


class SubmissionRequest(BaseModel):
    task_id: int
    model_name: str = "manual_submission"
    submitted_code: str


class EvaluationResponse(BaseModel):
    run_id: int
    passed: bool
    score: float
    test_output: str
    leadership_summary: str

class UserResponse(BaseModel):
    first: str
    last: str
    email: str
