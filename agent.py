from student import Topic
from fuzzy_engine import FuzzyStudyEngine


class StudyAgent:
    def __init__(self):
        self.fuzzy_engine = FuzzyStudyEngine()

    def calculate_priority(self, topic: Topic) -> float:
        """
        Calculate study priority using fuzzy reasoning.

        The agent considers:
        - Student mastery
        - Topic difficulty
        - Number of days until the exam

        Higher score = higher study priority.
        """

        return self.fuzzy_engine.calculate_priority(
            mastery=topic.mastery,
            difficulty=topic.difficulty,
            days_to_exam=topic.days_to_exam
        )

    def rank_topics(self, topics):
        """
        Rank topics from highest to lowest study priority.
        """

        return sorted(
            topics,
            key=self.calculate_priority,
            reverse=True
        )