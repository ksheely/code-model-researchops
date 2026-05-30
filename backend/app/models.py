from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


class PipelineStatus(str, Enum):
    idea = "idea"
    experiment = "experiment"
    validated = "validated"
    release_candidate = "release_candidate"
    released = "released"


class CodingTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    slug: str = Field(index=True, unique=True)
    category: str
    difficulty: str
    prompt: str
    starter_code: str
    tests_code: str
    status: PipelineStatus = PipelineStatus.idea


class EvaluationRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="codingtask.id")
    model_name: str
    submitted_code: str
    passed: bool
    score: float
    test_output: str
    leadership_summary: str

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str