from student import Topic


class StudyAgent:
    def calculate_priority(self, topic: Topic) -> float:
        """
        Calculate how important a topic is to study.

        Higher score = higher study priority.
        """

        mastery_need = 100 - topic.mastery
        difficulty_score = topic.difficulty * 10

        if topic.days_to_exam == 0:
            exam_urgency = 100
        else:
            exam_urgency = 100 / topic.days_to_exam

        priority = (
            mastery_need * 0.5
            + difficulty_score * 0.2
            + exam_urgency * 0.3
        )

        return round(priority, 2)

    def rank_topics(self, topics):
        return sorted(
            topics,
            key=self.calculate_priority,
            reverse=True
        )