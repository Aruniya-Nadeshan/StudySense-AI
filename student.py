from dataclasses import dataclass, field
from typing import List


@dataclass
class Topic:
    name: str
    mastery: float
    difficulty: int
    days_to_exam: int

    def __post_init__(self):
        if not 0 <= self.mastery <= 100:
            raise ValueError("Mastery must be between 0 and 100.")

        if not 1 <= self.difficulty <= 10:
            raise ValueError("Difficulty must be between 1 and 10.")

        if self.days_to_exam < 0:
            raise ValueError("Days to exam cannot be negative.")


@dataclass
class Student:
    name: str
    available_study_minutes: int
    topics: List[Topic] = field(default_factory=list)

    def add_topic(self, topic: Topic):
        self.topics.append(topic)