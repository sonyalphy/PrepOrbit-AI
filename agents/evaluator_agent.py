class EvaluatorAgent:
    def analyze(self, question_type, prompt, answer_text):
        score = 5
        weak_areas = []
        strengths = []

        text = answer_text.lower()

        if question_type.lower() == "system_design":
            checks = {
                "scalability": ["scalability", "scale", "horizontal"],
                "database design": ["database", "db", "schema"],
                "caching": ["cache", "redis", "memcache"],
                "load balancing": ["load balancer", "lb"],
                "api design": ["api", "endpoint", "rest"],
            }

        elif question_type.lower() == "dsa":
            checks = {
                "time complexity": ["o(", "time complexity", "linear", "log n"],
                "space complexity": ["space complexity", "in-place"],
                "edge cases": ["edge case", "null", "empty", "duplicate"],
                "approach clarity": ["approach", "first", "then", "finally"],
            }

        else:
            checks = {
                "structure": ["situation", "task", "action", "result"],
                "clarity": ["because", "therefore", "impact"],
                "ownership": ["i took", "i led", "i decided"],
            }

        for area, keywords in checks.items():
            if any(keyword in text for keyword in keywords):
                score += 1
                strengths.append(area)
            else:
                weak_areas.append(area)

        score = min(score, 10)

        return {
            "score": score,
            "summary": "Good attempt. Focus on the missing areas to improve the next round.",
            "strengths": strengths,
            "weak_areas": weak_areas,
            "follow_up_tasks": [f"Revise {area}" for area in weak_areas]
        }