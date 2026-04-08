from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

from services.orchestrator import (
    create_prep_plan,
    analyze_answer,
    replan_schedule,
    get_dashboard,
    start_mock_interview_session,
    evaluate_mock_interview_session,
)

app = FastAPI(
    title="PrepOrbit AI",
    description="Multi-agent interview preparation and analysis assistant",
    version="3.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class PrepPlanRequest(BaseModel):
    user_id: str
    target_role: str
    company: str
    timeline_days: int
    focus_areas: List[str]


class AnalyzeRequest(BaseModel):
    user_id: str
    question_type: str
    prompt: str
    answer_text: str


class ReplanRequest(BaseModel):
    user_id: str
    missed_days: int


class MockInterviewStartRequest(BaseModel):
    user_id: str
    interview_type: str


class MockInterviewEvaluateRequest(BaseModel):
    user_id: str
    interview_type: str
    prompt: str
    answer_text: str


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/prep-plan")
def prep_plan(req: PrepPlanRequest):
    try:
        return create_prep_plan(req.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        return analyze_answer(req.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/replan")
def replan(req: ReplanRequest):
    try:
        return replan_schedule(req.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mock-interview/start")
def start_mock_interview(req: MockInterviewStartRequest):
    try:
        return start_mock_interview_session(req.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mock-interview/evaluate")
def evaluate_mock_interview(req: MockInterviewEvaluateRequest):
    try:
        return evaluate_mock_interview_session(req.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{user_id}/dashboard")
def dashboard(user_id: str):
    try:
        return get_dashboard(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))