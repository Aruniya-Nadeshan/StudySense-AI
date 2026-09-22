import math

from agent import StudyAgent


class StudyPlanner:
    def __init__(self):
        self.agent = StudyAgent()

    def create_plan(self, student):
        """
        Create a personalized study plan based on topic priorities.

        The total allocated study time will always equal the
        student's available study time.
        """

        ranked_topics = self.agent.rank_topics(student.topics)

        # No topics = no study plan
        if not ranked_topics:
            return []

        # Calculate fuzzy priority for each topic
        priorities = [
            self.agent.calculate_priority(topic)
            for topic in ranked_topics
        ]

        total_priority = sum(priorities)

        # Safety check
        if total_priority == 0:
            return []

        study_plan = []

        # Store fractional remainders so leftover minutes
        # can be distributed fairly.
        remainders = []

        allocated_total = 0

        for topic, priority in zip(ranked_topics, priorities):

            time_share = priority / total_priority

            exact_minutes = (
                student.available_study_minutes * time_share
            )

            # First allocate only whole minutes
            allocated_minutes = math.floor(exact_minutes)

            allocated_total += allocated_minutes

            remainder = exact_minutes - allocated_minutes

            study_plan.append(
                {
                    "topic": topic.name,
                    "priority": priority,
                    "minutes": allocated_minutes
                }
            )

            remainders.append(remainder)

        # Find how many minutes are still unallocated
        remaining_minutes = (
            student.available_study_minutes - allocated_total
        )

        # Give leftover minutes to topics with the
        # largest decimal remainders.
        remainder_order = sorted(
            range(len(remainders)),
            key=lambda index: remainders[index],
            reverse=True
        )

        for i in range(remaining_minutes):
            topic_index = remainder_order[
                i % len(remainder_order)
            ]

            study_plan[topic_index]["minutes"] += 1

        return study_plan