from student import Topic
from fuzzy_engine import FuzzyStudyEngine


class StudyAgent:
    def __init__(self):
        self.fuzzy_engine = FuzzyStudyEngine()

    def calculate_priority(self, topic: Topic) -> float:

        performance_trend = topic.get_performance_trend()

        return self.fuzzy_engine.calculate_priority(
            mastery=topic.mastery,
            difficulty=topic.difficulty,
            days_to_exam=topic.days_to_exam,
            performance_trend=performance_trend
        )

    def rank_topics(self, topics):

        return sorted(
            topics,
            key=self.calculate_priority,
            reverse=True
        )