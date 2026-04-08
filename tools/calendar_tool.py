class CalendarTool:
    def __init__(self, db):
        self.db = db

    def create_blocks(self, user_id, blocks):
        self.db.save_calendar_blocks(user_id, blocks)

    def create_interview_slot(self, user_id, title, date, start_time, end_time):
        self.db.save_calendar_blocks(user_id, [{
            "title": title,
            "date": date,
            "start_time": start_time,
            "end_time": end_time
        }])