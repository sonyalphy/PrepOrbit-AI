class AnalysisTool:
    def __init__(self, db):
        self.db = db

    def save_analysis(self, user_id, input_data, result):
        self.db.save_mock_session(user_id, input_data, result)