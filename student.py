from dataclasses import dataclass, field
from typing import List


@dataclass
class Topic:
    name: str
    mastery: float
    difficulty: int
    days_to_exam: int

    def __post_init__(self):
        """
        Validate the topic data after the object is created.
        """

        if not 0 <= self.mastery <= 100:
            raise ValueError(
                "Mastery must be between 0 and 100."
            )

        if not 1 <= self.difficulty <= 10:
            raise ValueError(
                "Difficulty must be between 1 and 10."
            )

        if self.days_to_exam < 0:
            raise ValueError(
                "Days to exam cannot be negative."
            )

    def update_mastery(self, quiz_score: float):
        """
        Update the student's mastery of this topic
        using their latest quiz performance.

        Existing mastery contributes 70%.
        New quiz score contributes 30%.
        """

        if not 0 <= quiz_score <= 100:
            raise ValueError(
                "Quiz score must be between 0 and 100."
            )

        updated_mastery = (
            self.mastery * 0.7
            + quiz_score * 0.3
        )

        self.mastery = round(updated_mastery, 2)


@dataclass
class Student:
    name: str
    available_study_minutes: int
    topics: List[Topic] = field(default_factory=list)

    def __post_init__(self):
        """
        Validate student data.
        """

        if self.available_study_minutes < 0:
            raise ValueError(
                "Available study minutes cannot be negative."
            )

    def add_topic(self, topic: Topic):
        """
        Add a new topic to the student's study list.
        """

        self.topics.append(topic)