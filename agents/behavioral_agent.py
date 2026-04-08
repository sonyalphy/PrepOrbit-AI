class BehavioralAgent:
    def generate_tasks(self, timeline_days):
        prompts = [
            "Tell me about yourself",
            "Conflict in a team",
            "Leadership example",
            "Failure and learning",
            "Tight deadline situation",
            "Difficult stakeholder",
            "Why this company?",
            "Biggest achievement",
            "Handling ambiguity",
            "Decision with limited data"
        ]

        tasks = []
        for i in range(1, timeline_days + 1):
            prompt = prompts[(i - 1) % len(prompts)]
            tasks.append({
                "title": f"Practice STAR answer: {prompt}",
                "category": "Behavioral",
                "status": "pending",
                "priority": "medium",
                "day": i
            })

        return tasks

    def generate_ai_tasks(self, timeline_days):
        topics = [
            "LLM basics",
            "Prompt engineering",
            "RAG fundamentals",
            "Vector embeddings",
            "Fine-tuning vs prompting"
        ]

        tasks = []
        for i in range(1, timeline_days + 1):
            topic = topics[(i - 1) % len(topics)]
            tasks.append({
                "title": f"Revise AI concept: {topic}",
                "category": "AI Skills",
                "status": "pending",
                "priority": "medium",
                "day": i
            })

        return tasks