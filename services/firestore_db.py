import json
import os
from typing import Any, Dict, List


class LocalDB:
    def __init__(self, path: str = "data.json"):
        self.path = path
        if not os.path.exists(self.path):
            self._write({
                "prep_plans": [],
                "tasks": [],
                "calendar_blocks": [],
                "mock_sessions": [],
                "notes": [],
                "workflow_runs": [],
                "agent_logs": []
            })

    def _read(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def save_prep_plan(self, user_id: str, meta: Dict[str, Any], daily_plan: List[Dict[str, Any]]):
        data = self._read()
        data["prep_plans"].append({
            "user_id": user_id,
            "meta": meta,
            "daily_plan": daily_plan
        })
        self._write(data)

    def save_tasks(self, user_id: str, tasks: List[Dict[str, Any]]):
        data = self._read()
        for task in tasks:
            task["user_id"] = user_id
            data["tasks"].append(task)
        self._write(data)

    def save_calendar_blocks(self, user_id: str, blocks: List[Dict[str, Any]]):
        data = self._read()
        for block in blocks:
            block["user_id"] = user_id
            data["calendar_blocks"].append(block)
        self._write(data)

    def save_mock_session(self, user_id: str, input_data: Dict[str, Any], result: Dict[str, Any]):
        data = self._read()
        data["mock_sessions"].append({
            "user_id": user_id,
            "input": input_data,
            "result": result
        })
        self._write(data)

    def save_notes_from_weakness(self, user_id: str, weak_areas: List[str]):
        data = self._read()
        for area in weak_areas:
            data["notes"].append({
                "user_id": user_id,
                "topic": area,
                "content": f"Need to revise {area}",
                "tag": "weak_area"
            })
        self._write(data)

    def save_note(self, note: Dict[str, Any]):
        data = self._read()
        data["notes"].append(note)
        self._write(data)

    def save_replan(self, user_id: str, result: Dict[str, Any]):
        data = self._read()
        data["workflow_runs"].append({
            "user_id": user_id,
            "workflow_type": "replan",
            "result": result
        })
        self._write(data)

    def log_agent(self, user_id: str, action: str, agent_name: str, status: str):
        data = self._read()
        data["agent_logs"].append({
            "user_id": user_id,
            "action": action,
            "agent_name": agent_name,
            "status": status
        })
        self._write(data)

    def _fetch_by_user(self, collection_name: str, user_id: str):
        data = self._read()
        return [item for item in data.get(collection_name, []) if item.get("user_id") == user_id]

    def get_dashboard(self, user_id: str):
        return {
            "prep_plans": self._fetch_by_user("prep_plans", user_id),
            "tasks": self._fetch_by_user("tasks", user_id),
            "calendar_blocks": self._fetch_by_user("calendar_blocks", user_id),
            "notes": self._fetch_by_user("notes", user_id),
            "mock_sessions": self._fetch_by_user("mock_sessions", user_id),
            "workflow_runs": self._fetch_by_user("workflow_runs", user_id),
            "agent_logs": self._fetch_by_user("agent_logs", user_id),
        }


db = LocalDB()