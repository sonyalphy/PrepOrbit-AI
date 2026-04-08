class PlannerAgent:
    def generate_plan(self, timeline_days, focus_areas):
        plan = []
        for day in range(1, timeline_days + 1):
            topics = []

            if "DSA" in focus_areas:
                topics.append(f"Practice core DSA topic {day}")
            if "System Design" in focus_areas:
                topics.append(f"Revise system design concept {day}")
            if "Behavioral" in focus_areas:
                topics.append(f"Practice STAR story {day}")
            if "AI Skills" in focus_areas or "AI" in focus_areas:
                topics.append(f"Revise AI/ML concept {day}")

            plan.append({
                "day": day,
                "topics": topics
            })

        return plan

    def generate_blocks(self, daily_plan):
        blocks = []
        base_day = 8
        for item in daily_plan:
            blocks.append({
                "title": f"Study Block - Day {item['day']}",
                "date": f"2026-04-{base_day + item['day'] - 1:02d}",
                "start_time": "19:00",
                "end_time": "20:30"
            })
        return blocks

    def replan_after_missed_days(self, missed_days):
        return {
            "message": f"Prep plan updated after missing {missed_days} day(s).",
            "new_focus": [
                "High-priority DSA revision",
                "Core system design practice",
                "Behavioral answer refinement"
            ]
        }