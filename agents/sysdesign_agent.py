class SystemDesignAgent:
    def generate_tasks(self, timeline_days):
        topics = [
            "Scalability basics",
            "Load balancing",
            "Caching",
            "Database design",
            "Rate limiting",
            "Message queues",
            "CAP theorem",
            "Sharding & partitioning",
            "Monitoring & observability",
            "API design"
        ]

        tasks = []
        for i in range(1, timeline_days + 1):
            topic = topics[(i - 1) % len(topics)]
            tasks.append({
                "title": f"Revise system design topic: {topic}",
                "category": "System Design",
                "status": "pending",
                "priority": "medium",
                "day": i
            })

        return tasks