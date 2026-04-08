from agents.planner_agent import PlannerAgent
from agents.dsa_agent import DSAAgent
from agents.sysdesign_agent import SystemDesignAgent
from agents.behavioral_agent import BehavioralAgent
from agents.evaluator_agent import EvaluatorAgent

from tools.task_tool import TaskTool
from tools.calendar_tool import CalendarTool
from tools.notes_tool import NotesTool
from tools.analysis_tool import AnalysisTool

from services.firestore_db import db

planner = PlannerAgent()
dsa = DSAAgent()
sysd = SystemDesignAgent()
beh = BehavioralAgent()
evaluator = EvaluatorAgent()

task_tool = TaskTool(db)
calendar_tool = CalendarTool(db)
notes_tool = NotesTool(db)
analysis_tool = AnalysisTool(db)


def create_prep_plan(data):
    user_id = data["user_id"]
    timeline_days = data["timeline_days"]
    focus_areas = data["focus_areas"]

    daily_plan = planner.generate_plan(timeline_days, focus_areas)
    calendar_blocks = planner.generate_blocks(daily_plan)

    tasks = []
    if "DSA" in focus_areas:
        tasks.extend(dsa.generate_tasks(timeline_days))
    if "System Design" in focus_areas:
        tasks.extend(sysd.generate_tasks(timeline_days))
    if "Behavioral" in focus_areas:
        tasks.extend(beh.generate_tasks(timeline_days))
    if "AI" in focus_areas or "AI Skills" in focus_areas:
        tasks.extend(beh.generate_ai_tasks(timeline_days))

    db.save_prep_plan(user_id, data, daily_plan)

    task_tool.create_tasks(user_id, tasks)
    calendar_tool.create_blocks(user_id, calendar_blocks)
    notes_tool.save_note(
        user_id=user_id,
        topic="prep_plan_summary",
        content=f"Generated a {timeline_days}-day plan for {data['target_role']} at {data['company']}.",
        tag="plan"
    )

    db.log_agent(user_id, "workflow_create_prep_plan", "OrchestratorAgent", "success")

    return {
        "message": "Prep plan created successfully",
        "user_id": user_id,
        "daily_plan": daily_plan,
        "tasks_created": len(tasks),
        "calendar_blocks_created": len(calendar_blocks),
        "agents_used": [
            "OrchestratorAgent",
            "PlannerAgent",
            "DSAAgent",
            "SystemDesignAgent",
            "BehavioralAgent"
        ],
        "tools_used": ["TaskTool", "CalendarTool", "NotesTool"]
    }


def analyze_answer(data):
    user_id = data["user_id"]

    result = evaluator.analyze(
        data["question_type"],
        data["prompt"],
        data["answer_text"]
    )

    analysis_tool.save_analysis(user_id, data, result)
    notes_tool.save_notes_from_weakness(user_id, result["weak_areas"])
    task_tool.create_follow_up_tasks(user_id, result["follow_up_tasks"])

    db.log_agent(user_id, "workflow_analyze_answer", "EvaluatorAgent", "success")

    return {
        "message": "Answer analyzed successfully",
        "user_id": user_id,
        **result,
        "agents_used": ["OrchestratorAgent", "EvaluatorAgent"],
        "tools_used": ["AnalysisTool", "NotesTool", "TaskTool"]
    }


def replan_schedule(data):
    user_id = data["user_id"]
    missed_days = data["missed_days"]

    result = planner.replan_after_missed_days(missed_days)

    db.save_replan(user_id, result)
    notes_tool.save_note(
        user_id=user_id,
        topic="replan_update",
        content=f"Preparation replanned after missing {missed_days} day(s).",
        tag="replan"
    )

    db.log_agent(user_id, "workflow_replan_schedule", "PlannerAgent", "success")

    return {
        "message": "Schedule replanned successfully",
        "user_id": user_id,
        **result,
        "agents_used": ["OrchestratorAgent", "PlannerAgent"],
        "tools_used": ["NotesTool"]
    }


def start_mock_interview_session(data):
    user_id = data["user_id"]
    interview_type = data["interview_type"].lower()

    question_bank = {
        "dsa": [
            "How would you solve Two Sum efficiently?",
            "Explain sliding window with an example.",
            "How would you detect a cycle in a linked list?"
        ],
        "system_design": [
            "Design a URL shortener.",
            "Design a notification system.",
            "Design a ride-booking service like Uber."
        ],
        "behavioral": [
            "Tell me about a time you handled conflict in a team.",
            "Describe a situation where you took ownership.",
            "Tell me about a failure and what you learned."
        ],
        "ai": [
            "What is overfitting in machine learning?",
            "Explain transformers in simple terms.",
            "What is the difference between fine-tuning and prompting?"
        ]
    }

    prompt = question_bank.get(interview_type, ["Tell me about yourself."])[0]

    calendar_tool.create_interview_slot(
        user_id=user_id,
        title=f"Mock Interview - {interview_type.title()}",
        date="2026-04-08",
        start_time="20:00",
        end_time="20:30"
    )

    db.log_agent(user_id, "workflow_mock_interview_start", "MockInterviewAgent", "success")

    return {
        "message": "Mock interview started successfully",
        "user_id": user_id,
        "interview_type": interview_type,
        "prompt": prompt,
        "agents_used": ["OrchestratorAgent", "MockInterviewAgent"],
        "tools_used": ["CalendarTool"]
    }


def evaluate_mock_interview_session(data):
    user_id = data["user_id"]
    interview_type = data["interview_type"]
    prompt = data["prompt"]
    answer_text = data["answer_text"]

    result = evaluator.analyze(interview_type, prompt, answer_text)

    analysis_tool.save_analysis(
        user_id,
        {
            "question_type": interview_type,
            "prompt": prompt,
            "answer_text": answer_text
        },
        result
    )

    notes_tool.save_notes_from_weakness(user_id, result["weak_areas"])
    task_tool.create_follow_up_tasks(user_id, result["follow_up_tasks"])

    db.log_agent(user_id, "workflow_mock_interview_evaluate", "MockInterviewAgent", "success")

    return {
        "message": "Mock interview answer evaluated successfully",
        "user_id": user_id,
        "interview_type": interview_type,
        **result,
        "agents_used": ["OrchestratorAgent", "MockInterviewAgent", "EvaluatorAgent"],
        "tools_used": ["AnalysisTool", "NotesTool", "TaskTool"]
    }


def get_dashboard(user_id):
    dashboard_data = db.get_dashboard(user_id)
    return {
        "message": "Dashboard fetched successfully",
        "user_id": user_id,
        **dashboard_data
    }