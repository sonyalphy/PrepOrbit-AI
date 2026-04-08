class DSAAgent:
    def generate_tasks(self, timeline_days):
        topics = [
            "Arrays & Strings",
            "Hashing",
            "Sliding Window",
            "Stacks & Queues",
            "Linked Lists",
            "Trees",
            "Binary Search",
            "Dynamic Programming",
            "Graphs",
            "Heaps"
        ]

        tasks = []
        for i in range(1, timeline_days + 1):
            topic = topics[(i - 1) % len(topics)]
            tasks.append({
                "title": f"Solve 2 DSA problems on {topic}",
                "category": "DSA",
                "status": "pending",
                "priority": "high",
                "day": i
            })

        return tasks