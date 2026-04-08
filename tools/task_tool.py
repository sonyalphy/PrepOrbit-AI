class TaskTool:
    def __init__(self, db):
        self.db = db

    def create_tasks(self, user_id, tasks):
        self.db.save_tasks(user_id, tasks)

    def create_follow_up_tasks(self, user_id, follow_up_tasks):
        tasks = []
        for item in follow_up_tasks:
            tasks.append({
                "title": item,
                "category": "Follow-up",
                "status": "pending",
                "priority": "high"
            })
        self.db.save_tasks(user_id, tasks)