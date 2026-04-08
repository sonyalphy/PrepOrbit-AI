class NotesTool:
    def __init__(self, db):
        self.db = db

    def save_note(self, user_id, topic, content, tag="general"):
        self.db.save_note({
            "user_id": user_id,
            "topic": topic,
            "content": content,
            "tag": tag
        })

    def save_notes_from_weakness(self, user_id, weak_areas):
        self.db.save_notes_from_weakness(user_id, weak_areas)