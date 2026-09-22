from agent import StudyAgent


class StudyPlanner:
    def __init__(self):
        self.agent = StudyAgent()

    def create_plan(self, student):
        ranked_topics = self.agent.rank_topics(student.topics)

        total_priority = sum(
            self.agent.calculate_priority(topic)
            for topic in ranked_topics
        )

        study_plan = []

        for topic in ranked_topics:
            priority = self.agent.calculate_priority(topic)

            time_share = priority / total_priority

            allocated_minutes = round(
                student.available_study_minutes * time_share
            )

            study_plan.append(
                {
                    "topic": topic.name,
                    "priority": priority,
                    "minutes": allocated_minutes
                }
            )

        return study_plan